"""
Striver A2Z DSA Sheet - SQLite Database
Manages problems and user progress using SQLite
"""

import sqlite3
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class StriverDatabase:
    """SQLite database manager for Striver A2Z Sheet"""
    
    def __init__(self, db_path: str = "striver_sheet.db"):
        self.db_path = db_path
        self.init_database()
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get SQLite connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """Initialize database with tables"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Problems table - stores all Striver A2Z problems
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS problems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                problem_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                topic TEXT NOT NULL,
                subtopic TEXT,
                difficulty TEXT NOT NULL,
                url TEXT,
                video_url TEXT,
                tutorial_url TEXT,
                is_premium INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # User progress table - tracks each user's solved problems
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                problem_id TEXT NOT NULL,
                status TEXT DEFAULT 'not_solved',
                solved_at TEXT,
                attempts INTEGER DEFAULT 0,
                time_spent INTEGER DEFAULT 0,
                notes TEXT,
                UNIQUE(user_id, problem_id),
                FOREIGN KEY (problem_id) REFERENCES problems(problem_id)
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_problems_topic ON problems(topic)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_problems_difficulty ON problems(difficulty)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_progress_user ON user_progress(user_id)
        """)
        
        conn.commit()
        conn.close()
    
    def add_problem(self, problem_id: str, name: str, topic: str, 
                  difficulty: str, subtopic: str = "", 
                  url: str = "", video_url: str = "") -> bool:
        """Add a single problem to the database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO problems 
                (problem_id, name, topic, subtopic, difficulty, url, video_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (problem_id, name, topic, subtopic, difficulty, url, video_url))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def add_problems_batch(self, problems: List[Dict]) -> int:
        """Add multiple problems in batch"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        count = 0
        for p in problems:
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO problems 
                    (problem_id, name, topic, subtopic, difficulty, url, video_url)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    p.get('problem_id', ''),
                    p.get('name', ''),
                    p.get('topic', ''),
                    p.get('subtopic', ''),
                    p.get('difficulty', 'Easy'),
                    p.get('url', ''),
                    p.get('video_url', '')
                ))
                count += 1
            except sqlite3.IntegrityError:
                continue
        
        conn.commit()
        conn.close()
        return count
    
    def get_all_problems(self) -> List[Dict]:
        """Get all problems"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT problem_id, name, topic, subtopic, difficulty, url, video_url
            FROM problems
            ORDER BY topic, difficulty, name
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_problems_by_topic(self, topic: str) -> List[Dict]:
        """Get problems filtered by topic"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT problem_id, name, topic, subtopic, difficulty, url, video_url
            FROM problems
            WHERE topic = ?
            ORDER BY difficulty, name
        """, (topic,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_problems_by_difficulty(self, difficulty: str) -> List[Dict]:
        """Get problems filtered by difficulty"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT problem_id, name, topic, subtopic, difficulty, url, video_url
            FROM problems
            WHERE difficulty = ?
            ORDER BY topic, name
        """, (difficulty,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_problem_by_id(self, problem_id: str) -> Optional[Dict]:
        """Get a single problem by ID"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT problem_id, name, topic, subtopic, difficulty, url, video_url
            FROM problems
            WHERE problem_id = ?
        """, (problem_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    # User Progress Methods
    def update_user_progress(self, user_id: str, problem_id: str, 
                          status: str = "solved", notes: str = "") -> bool:
        """Update user's progress for a problem"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        solved_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S') if status == "solved" else None
        
        cursor.execute("""
            INSERT INTO user_progress (user_id, problem_id, status, solved_at, attempts, notes)
            VALUES (?, ?, ?, ?, 1, ?)
            ON CONFLICT(user_id, problem_id) DO UPDATE SET
                status = excluded.status,
                solved_at = excluded.solved_at,
                attempts = attempts + 1,
                notes = excluded.notes
        """, (user_id, problem_id, status, solved_at, notes))
        
        conn.commit()
        conn.close()
        return True
    
    def get_user_progress(self, user_id: str) -> Dict:
        """Get all progress for a user"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get solved problems
        cursor.execute("""
            SELECT problem_id, status, solved_at, attempts, notes
            FROM user_progress
            WHERE user_id = ?
        """, (user_id,))
        
        progress_rows = cursor.fetchall()
        
        # Get all problems to calculate stats
        cursor.execute("SELECT problem_id, topic, difficulty FROM problems")
        all_problems = cursor.fetchall()
        
        conn.close()
        
        # Build progress mapping
        progress_map = {row['problem_id']: dict(row) for row in progress_rows}
        
        # Calculate statistics
        stats = {
            'total_problems': len(all_problems),
            'solved_count': 0,
            'not_solved_count': 0,
            'topics': {}
        }
        
        # Count by topic
        topics_dict = {}
        for p in all_problems:
            topic = p['topic']
            if topic not in topics_dict:
                topics_dict[topic] = {'total': 0, 'solved': 0}
            topics_dict[topic]['total'] += 1
            
            if p['problem_id'] in progress_map:
                if progress_map[p['problem_id']]['status'] == 'solved':
                    topics_dict[topic]['solved'] += 1
        
        stats['topics'] = topics_dict
        stats['solved_count'] = sum(t['solved'] for t in topics_dict.values())
        stats['not_solved_count'] = stats['total_problems'] - stats['solved_count']
        
        return {
            'user_id': user_id,
            'progress': progress_map,
            'stats': stats
        }
    
    def get_topic_progress(self, user_id: str, topic: str) -> Dict:
        """Get progress for a specific topic"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Get problems for this topic
        cursor.execute("""
            SELECT problem_id FROM problems WHERE topic = ?
        """, (topic,))
        
        topic_problems = [row['problem_id'] for row in cursor.fetchall()]
        
        # Get user progress for these problems
        placeholders = ','.join(['?' for _ in topic_problems])
        if placeholders:
            cursor.execute(f"""
                SELECT problem_id, status FROM user_progress
                WHERE user_id = ? AND problem_id IN ({placeholders})
            """, (user_id, *topic_problems))
        else:
            cursor.execute("""
                SELECT problem_id, status FROM user_progress
                WHERE user_id = ? AND 1=0
            """, (user_id,))
        
        solved = sum(1 for row in cursor.fetchall() if row['status'] == 'solved')
        
        conn.close()
        
        return {
            'topic': topic,
            'total': len(topic_problems),
            'solved': solved,
            'remaining': len(topic_problems) - solved
        }
    
    def get_all_topics(self) -> List[str]:
        """Get all unique topics"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT DISTINCT topic FROM problems ORDER BY topic")
        topics = [row['topic'] for row in cursor.fetchall()]
        
        conn.close()
        return topics
    
    def get_problem_count(self) -> int:
        """Get total problem count"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM problems")
        count = cursor.fetchone()['count']
        
        conn.close()
        return count


# Singleton instance
_db_instance: Optional[StriverDatabase] = None


def get_striver_db(db_path: str = "striver_sheet.db") -> StriverDatabase:
    """Get singleton database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = StriverDatabase(db_path)
    return _db_instance


__all__ = ['StriverDatabase', 'get_striver_db']
