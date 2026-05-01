"""
DSA AI Agent - User Service
User management, profiles, and authentication
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional


class UserProfile:
    """User profile data"""
    
    def __init__(
        self,
        user_id: str,
        username: str = "",
        email: str = "",
        level: str = "Beginner"
    ):
        self.user_id = user_id
        self.username = username or user_id
        self.email = email
        self.level = level  # Beginner, Intermediate, Advanced
        self.topics_covered = []
        self.problems_solved = []
        self.quiz_scores = []
        self.created_at = datetime.now().isoformat()
        self.last_active = datetime.now().isoformat()
        self.streak_days = 0
    
    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "level": self.level,
            "topics_covered": self.topics_covered,
            "problems_solved": self.problems_solved,
            "quiz_scores": self.quiz_scores,
            "created_at": self.created_at,
            "last_active": self.last_active,
            "streak_days": self.streak_days
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProfile':
        profile = cls(
            user_id=data.get("user_id", ""),
            username=data.get("username", ""),
            email=data.get("email", ""),
            level=data.get("level", "Beginner")
        )
        profile.topics_covered = data.get("topics_covered", [])
        profile.problems_solved = data.get("problems_solved", [])
        profile.quiz_scores = data.get("quiz_scores", [])
        profile.created_at = data.get("created_at", datetime.now().isoformat())
        profile.last_active = data.get("last_active", datetime.now().isoformat())
        profile.streak_days = data.get("streak_days", 0)
        return profile


class UserService:
    """
    User Service for user management
    Handles profiles, auth, and session tracking
    """

    def __init__(self, storage_path: str = "data/"):
        self.storage_path = storage_path
        self.current_user = None
        self.users: Dict[str, UserProfile] = {}
        
        # Create storage directory if needed
        os.makedirs(storage_path, exist_ok=True)

    def create_user(
        self,
        user_id: str,
        username: str = "",
        email: str = ""
    ) -> UserProfile:
        """Create new user"""
        profile = UserProfile(user_id, username, email)
        self.users[user_id] = profile
        self._save_user(profile)
        return profile

    def get_user(self, user_id: str) -> Optional[UserProfile]:
        """Get user by ID"""
        if user_id in self.users:
            return self.users[user_id]
        
        # Try loading from file
        profile = self._load_user(user_id)
        if profile:
            self.users[user_id] = profile
        return profile

    def login(self, user_id: str) -> bool:
        """Login user"""
        profile = self.get_user(user_id)
        if profile:
            self.current_user = profile
            profile.last_active = datetime.now().isoformat()
            self._save_user(profile)
            return True
        return False

    def logout(self):
        """Logout current user"""
        if self.current_user:
            self._save_user(self.current_user)
            self.current_user = None

    def update_level(self, level: str):
        """Update user skill level"""
        if self.current_user:
            self.current_user.level = level
            self._save_user(self.current_user)

    def add_topic(self, topic: str):
        """Record topic covered"""
        if self.current_user and topic not in self.current_user.topics_covered:
            self.current_user.topics_covered.append(topic)
            self._save_user(self.current_user)

    def add_problem_solved(self, problem: str, difficulty: str):
        """Record problem solved"""
        if self.current_user:
            self.current_user.problems_solved.append({
                "problem": problem,
                "difficulty": difficulty,
                "timestamp": datetime.now().isoformat()
            })
            self._save_user(self.current_user)

    def add_quiz_score(self, topic: str, score: int, total: int):
        """Record quiz score"""
        if self.current_user:
            self.current_user.quiz_scores.append({
                "topic": topic,
                "score": score,
                "total": total,
                "timestamp": datetime.now().isoformat()
            })
            self._save_user(self.current_user)

    def get_stats(self) -> Dict:
        """Get current user stats"""
        if not self.current_user:
            return {}
        
        return {
            "user_id": self.current_user.user_id,
            "username": self.current_user.username,
            "level": self.current_user.level,
            "topics_count": len(self.current_user.topics_covered),
            "problems_solved": len(self.current_user.problems_solved),
            "quizzes_taken": len(self.current_user.quiz_scores),
            "streak_days": self.current_user.streak_days
        }

    def get_progress_report(self) -> str:
        """Get progress report"""
        if not self.current_user:
            return "No user logged in"
        
        stats = self.get_stats()
        
        report = f"""
📊 Progress Report for {stats['username']}:

Level: {stats['level']}
Topics Learned: {stats['topics_count']}
Problems Solved: {stats['problems_solved']}
Quizzes Taken: {stats['quizzes_taken']}
Streak Days: {stats['streak_days']}
"""
        return report

    def _save_user(self, profile: UserProfile):
        """Save user to file"""
        filepath = os.path.join(self.storage_path, f"{profile.user_id}.json")
        with open(filepath, 'w') as f:
            json.dump(profile.to_dict(), f, indent=2)

    def _load_user(self, user_id: str) -> Optional[UserProfile]:
        """Load user from file"""
        filepath = os.path.join(self.storage_path, f"{user_id}.json")
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                return UserProfile.from_dict(data)
        except FileNotFoundError:
            return None


__all__ = ['UserService', 'UserProfile']
