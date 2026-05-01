"""
DSA AI Agent - Memory / Progress Tracking Module
Track user learning progress and weak areas
"""

import json
from datetime import datetime
from typing import Dict, List, Optional


class UserSession:
    """Track user session and progress"""

    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        self.topics_covered = []
        self.problems_attempted = []
        self.weak_areas = []
        self.strengths = []
        self.session_start = datetime.now()
        self.conversation_count = 0

    def add_topic(self, topic: str):
        """Record topic covered"""
        if topic not in self.topics_covered:
            self.topics_covered.append(topic)
        self.conversation_count += 1

    def add_problem(self, problem: str, attempted: bool = True):
        """Record problem attempt"""
        self.problems_attempted.append({
            "problem": problem,
            "attempted": attempted,
            "timestamp": datetime.now().isoformat()
        })

    def get_stats(self) -> Dict:
        """Get session statistics"""
        return {
            "user_id": self.user_id,
            "topics_covered": len(self.topics_covered),
            "problems_attempted": len(self.problems_attempted),
            "conversation_count": self.conversation_count,
            "weak_areas": self.weak_areas,
            "strengths": self.strengths
        }

    def save(self, filepath: str = ""):
        """Save session to file"""
        if not filepath:
            filepath = f"session_{self.user_id}.json"

        data = {
            "user_id": self.user_id,
            "topics_covered": self.topics_covered,
            "problems_attempted": self.problems_attempted,
            "weak_areas": self.weak_areas,
            "strengths": self.strengths,
            "session_start": self.session_start.isoformat()
        }

        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)

    def load(self, filepath: str = ""):
        """Load session from file"""
        if not filepath:
            filepath = f"session_{self.user_id}.json"

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
                self.user_id = data.get("user_id", "default")
                self.topics_covered = data.get("topics_covered", [])
                self.problems_attempted = data.get("problems_attempted", [])
                self.weak_areas = data.get("weak_areas", [])
                self.strengths = data.get("strengths", [])
        except FileNotFoundError:
            pass


class ProgressTracker:
    """Track overall learning progress"""

    def __init__(self):
        self.sessions: List[UserSession] = []
        self.difficulty_level = "Beginner"

    def add_session(self, session: UserSession):
        """Add new session"""
        self.sessions.append(session)

    def analyze_weak_areas(self) -> List[str]:
        """Analyze weak areas across sessions"""
        topic_count = {}

        for session in self.sessions:
            for topic in session.topics_covered:
                topic_count[topic] = topic_count.get(topic, 0) + 1

        # Topics covered less frequently are weak areas
        sorted_topics = sorted(topic_count.items(), key=lambda x: x[1])
        return [t[0] for t in sorted_topics[:3]]

    def get_recommendations(self) -> List[str]:
        """Get practice recommendations"""
        weak = self.analyze_weak_areas()

        recommendations = []
        if "dp" in weak or "dynamic" in weak:
            recommendations.append("Practice more DP problems - start with easy like Climbing Stairs")
        if "graph" in weak:
            recommendations.append("Practice BFS/DFS - start with Number of Islands")
        if "tree" in weak:
            recommendations.append("Practice tree traversals - start with Maximum Depth")

        if not recommendations:
            recommendations.append("Great progress! Try medium/hard problems")

        return recommendations

    def get_progress_report(self) -> str:
        """Generate progress report"""
        total_convos = sum(s.conversation_count for s in self.sessions)
        total_problems = len(self.problems_attempted) + sum(
            len(s.problems_attempted) for s in self.sessions
        )

        weak = self.analyze_weak_areas()

        report = f"""
📊 Progress Report:

Sessions: {len(self.sessions)}
Conversations: {total_convos}
Problems Attempted: {total_problems}

🎯 Focus Areas (need practice):
"""
        for area in weak:
            report += f"- {area}\n"

        recommendations = self.get_recommendations()
        report += "\n💡 Recommendations:\n"
        for rec in recommendations:
            report += f"- {rec}\n"

        return report


class TopicTracker:
    """Track specific topic progress"""

    def __init__(self, topic: str):
        self.topic = topic
        self.concepts = []
        self.problems_solved = []
        self.difficulty_score = 0

    def mark_concept_learned(self, concept: str):
        """Mark concept as learned"""
        if concept not in self.concepts:
            self.concepts.append(concept)
            self.difficulty_score += 1

    def mark_problem_solved(self, problem: str, difficulty: str):
        """Mark problem as solved"""
        self.problems_solved.append({
            "problem": problem,
            "difficulty": difficulty,
            "timestamp": datetime.now().isoformat()
        })

        # Update difficulty score
        diff_scores = {"Easy": 1, "Medium": 2, "Hard": 3}
        self.difficulty_score += diff_scores.get(difficulty, 1)

    def get_level(self) -> str:
        """Get current mastery level"""
        if self.difficulty_score < 5:
            return "Beginner"
        elif self.difficulty_score < 15:
            return "Intermediate"
        else:
            return "Advanced"


def print_progress_bar(current: int, total: int, level: str = ""):
    """Print progress bar"""
    percentage = current / total if total > 0 else 0
    filled = int(percentage * 20)
    bar = "█" * filled + "░" * (20 - filled)

    print(f"\r[{bar}] {int(percentage * 100)}% {level}", end="")


__all__ = ['UserSession', 'ProgressTracker', 'TopicTracker', 'print_progress_bar']
