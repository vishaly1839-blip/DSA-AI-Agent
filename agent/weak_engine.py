"""
DSA AI Agent - Weakness Engine
Tracks user mistakes and identifies weak areas
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


class MistakeRecord:
    """Record of user mistake"""
    
    def __init__(
        self,
        topic: str,
        problem: str = "",
        error_type: str = "",
        description: str = "",
        timestamp: str = ""
    ):
        self.topic = topic
        self.problem = problem
        self.error_type = error_type
        self.description = description
        self.timestamp = timestamp or datetime.now().isoformat()
        self.count = 1
    
    def to_dict(self) -> Dict:
        return {
            "topic": self.topic,
            "problem": self.problem,
            "error_type": self.error_type,
            "description": self.description,
            "timestamp": self.timestamp,
            "count": self.count
        }


class TopicStats:
    """Statistics for a topic"""
    
    def __init__(self, topic: str):
        self.topic = topic
        self.attempts = 0
        self.correct = 0
        self.wrong = 0
        self.time_spent = 0.0  # seconds
        self.mistakes = []
    
    @property
    def accuracy(self) -> float:
        if self.attempts == 0:
            return 0.0
        return (self.correct / self.attempts) * 100
    
    def to_dict(self) -> Dict:
        return {
            "topic": self.topic,
            "attempts": self.attempts,
            "correct": self.correct,
            "wrong": self.wrong,
            "accuracy": self.accuracy,
            "time_spent": self.time_spent,
            "mistakes": self.mistakes
        }


class WeaknessEngine:
    """
    Weakness Engine - Track mistakes and detect weak topics
    Helps identify areas that need more practice
    """

    def __init__(self, user_id: str = "default", storage_path: str = "data/"):
        self.user_id = user_id
        self.storage_path = storage_path
        self.topic_stats: Dict[str, TopicStats] = {}
        self.mistake_history: List[MistakeRecord] = []
        self.weak_topics: List[str] = []
        self.pattern_count: Dict[str, int] = defaultdict(int)
        
        # Create storage directory
        os.makedirs(storage_path, exist_ok=True)
        
        # Load existing data
        self._load_data()

    def record_attempt(
        self,
        topic: str,
        correct: bool,
        time_spent: float = 0.0,
        problem: str = ""
    ):
        """Record a problem attempt"""
        if topic not in self.topic_stats:
            self.topic_stats[topic] = TopicStats(topic)
        
        stats = self.topic_stats[topic]
        stats.attempts += 1
        stats.time_spent += time_spent
        
        if correct:
            stats.correct += 1
        else:
            stats.wrong += 1
            # Record mistake for wrong answers
            self._record_mistake(topic, problem)
        
        # Recalculate weak topics
        self._update_weak_topics()
        
        # Save data
        self._save_data()

    def _record_mistake(self, topic: str, problem: str = ""):
        """Record a mistake"""
        # Determine error type based on topic
        error_type = self._classify_error(topic, problem)
        
        mistake = MistakeRecord(
            topic=topic,
            problem=problem,
            error_type=error_type,
            description=f"Mistake in {topic}"
        )
        
        self.mistake_history.append(mistake)
        
        # Update pattern count
        self.pattern_count[error_type] += 1

    def _classify_error(self, topic: str, problem: str) -> str:
        """Classify the type of error based on topic"""
        error_patterns = {
            "array": "index_out_of_bound",
            "linked_list": "null_pointer",
            "tree": "traversal_error",
            "graph": "cycle_detection",
            "dp": "state_transition",
            "heap": "heap_property",
            "string": "off_by_one",
            "sorting": "boundary_condition",
            "sliding_window": "window_size",
            "two_pointers": "pointer_sync"
        }
        
        topic_lower = topic.lower()
        for key, error in error_patterns.items():
            if key in topic_lower:
                return error
        
        return "logic_error"

    def _update_weak_topics(self):
        """Update the list of weak topics"""
        weak_list = []
        
        for topic, stats in self.topic_stats.items():
            if stats.attempts >= 3:  # Minimum 3 attempts to judge
                if stats.accuracy < 70:  # Below 70% is weak
                    weak_list.append((topic, stats.accuracy))
        
        # Sort by accuracy (lowest first)
        weak_list.sort(key=lambda x: x[1])
        self.weak_topics = [t[0] for t in weak_list]

    def get_weak_topics(self, limit: int = 3) -> List[str]:
        """Get the weakest topics"""
        return self.weak_topics[:limit]

    def get_strong_topics(self, limit: int = 3) -> List[str]:
        """Get the strongest topics"""
        strong = []
        
        for topic, stats in self.topic_stats.items():
            if stats.attempts >= 3 and stats.accuracy >= 80:
                strong.append((topic, stats.accuracy))
        
        strong.sort(key=lambda x: x[1], reverse=True)
        return [t[0] for t in strong[:limit]]

    def get_topic_accuracy(self, topic: str) -> float:
        """Get accuracy for a specific topic"""
        if topic in self.topic_stats:
            return self.topic_stats[topic].accuracy
        return 0.0

    def get_practice_recommendation(self) -> str:
        """Get AI-powered practice recommendation"""
        weak = self.get_weak_topics(3)
        
        if not weak:
            if not self.topic_stats:
                return "Start with easy problems in any topic!"
            return "Great job! Try medium/hard problems now."
        
        recommendations = {
            "array": "Practice Two Sum, Maximum Subarray - focus on index handling",
            "linked list": "Practice Reverse Linked List - check null pointers",
            "tree": "Practice tree traversals - inorder, preorder, postorder",
            "graph": "Practice BFS/DFS - Number of Islands is good start",
            "dp": "Start with Climbing Stairs, then House Robber",
            "heap": "Practice Kth Largest, median problems",
            "sorting": "Practice Merge Intervals - check boundary conditions",
            "sliding window": "Practice Maximum Average Subarray",
            "string": "Practice two pointer string problems",
        }
        
        msg = "🎯 Focus Areas (weak topics):\n\n"
        for i, topic in enumerate(weak, 1):
            msg += f"{i}. {topic.title()}"
            if topic in recommendations:
                msg += f"\n   → {recommendations[topic]}"
            msg += "\n"
        
        return msg

    def force_practice(self, topic: Optional[str] = None) -> str:
        """Force practice on weak topic"""
        target = topic or (self.get_weak_topics(1) or ["array"])[0]
        
        return f"""⚠️ Practice Mode: {target.title()}

You've been struggling with this topic.
Let's practice together!

Try these problems:
- Easy first, then Medium
- Don't move on until you get 3 correct in a row
- I'll track your progress

Type 'quiz {target}' or 'practice {target}' to start!
"""

    def analyze_patterns(self) -> str:
        """Analyze mistake patterns"""
        if not self.pattern_count:
            return "No mistakes recorded yet. Great progress!"
        
        # Find most common error types
        sorted_errors = sorted(
            self.pattern_count.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        msg = "🔍 Mistake Patterns:\n\n"
        for error_type, count in sorted_errors[:5]:
            msg += f"- {error_type.replace('_', ' ').title()}: {count}x\n"
        
        # Get suggestions based on patterns
        msg += "\n💡 Suggestions:\n"
        
        if sorted_errors:
            top_error = sorted_errors[0][0]
            suggestions = {
                "index_out_of_bound": "Always check array bounds before accessing!",
                "null_pointer": "Check for None/null before using pointers!",
                "traversal_error": "Practice all 3 tree traversals!",
                "cycle_detection": "Use visited set in BFS/DFS!",
                "state_transition": "Define base case and transition clearly!",
                "heap_property": "Remember parent >= children in max heap!",
                "off_by_one": "Use examples to verify boundaries!",
                "boundary_condition": "Test edge cases: empty, single element!",
                "window_size": "Start with window=1 and grow!",
                "pointer_sync": "Ensure pointers move correctly!"
            }
            
            if top_error in suggestions:
                msg += f"- {suggestions[top_error]}\n"
        
        return msg

    def get_stats_report(self) -> str:
        """Get comprehensive stats report"""
        total_attempts = sum(s.attempts for s in self.topic_stats.values())
        total_correct = sum(s.correct for s in self.topic_stats.values())
        
        overall_accuracy = 0.0
        if total_attempts > 0:
            overall_accuracy = (total_correct / total_attempts) * 100
        
        msg = f"""
📊 Weakness Analysis Report
{'='*35}

Overall: {total_correct}/{total_attempts} ({overall_accuracy:.1f}%)

🎯 Weak Topics (need practice):
"""
        for topic in self.get_weak_topics(3):
            acc = self.get_topic_accuracy(topic)
            msg += f"- {topic.title()}: {acc:.1f}%\n"
        
        msg += "\n💪 Strong Topics:"
        for topic in self.get_strong_topics(3):
            acc = self.get_topic_accuracy(topic)
            msg += f"- {topic.title()}: {acc:.1f}%\n"
        
        msg += f"\n{self.get_practice_recommendation()}"
        
        return msg

    def _save_data(self):
        """Save weakness data to file"""
        data = {
            "user_id": self.user_id,
            "topic_stats": {
                topic: stats.to_dict() 
                for topic, stats in self.topic_stats.items()
            },
            "mistake_history": [m.to_dict() for m in self.mistake_history],
            "weak_topics": self.weak_topics,
            "pattern_count": dict(self.pattern_count)
        }
        
        filepath = os.path.join(self.storage_path, f"weakness_{self.user_id}.json")
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def _load_data(self):
        """Load weakness data from file"""
        filepath = os.path.join(self.storage_path, f"weakness_{self.user_id}.json")
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Load topic stats
            topic_data = data.get("topic_stats", {})
            for topic, stats_dict in topic_data.items():
                stats = TopicStats(topic)
                stats.attempts = stats_dict.get("attempts", 0)
                stats.correct = stats_dict.get("correct", 0)
                stats.wrong = stats_dict.get("wrong", 0)
                stats.time_spent = stats_dict.get("time_spent", 0.0)
                stats.mistakes = stats_dict.get("mistakes", [])
                self.topic_stats[topic] = stats
            
            # Load mistake history
            mistake_data = data.get("mistake_history", [])
            for m_dict in mistake_data:
                mistake = MistakeRecord(
                    topic=m_dict.get("topic", ""),
                    problem=m_dict.get("problem", ""),
                    error_type=m_dict.get("error_type", ""),
                    description=m_dict.get("description", ""),
                    timestamp=m_dict.get("timestamp", "")
                )
                mistake.count = m_dict.get("count", 1)
                self.mistake_history.append(mistake)
            
            # Load weak topics
            self.weak_topics = data.get("weak_topics", [])
            
            # Load pattern count
            self.pattern_count = defaultdict(int)
            self.pattern_count.update(data.get("pattern_count", {}))
            
        except FileNotFoundError:
            pass


__all__ = ['WeaknessEngine', 'MistakeRecord', 'TopicStats']
