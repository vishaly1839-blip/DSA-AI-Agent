"""
DSA AI Agent - Roadmap Module
Skill assessment and personalized learning path (Striver-based)
"""

from typing import Dict, List, Optional
from .quiz import SKILL_ASSESSMENT_QUESTIONS


# Striver's SDE Sheet roadmap
STIVER_ROADMAP = {
    "Beginner": {
        "description": "Welcome! Let's build your foundation.",
        "duration": "2-3 weeks",
        "focus": "Basic data structures and easy problems",
        "topics": [
            {"topic": "Arrays", "problems": 15, "weight": 1},
            {"topic": "Strings", "problems": 10, "weight": 1},
            {"topic": "Linked Lists", "problems": 15, "weight": 1},
            {"topic": "Stacks/Queues", "problems": 10, "weight": 1},
        ],
        "target": "Solve 50+ easy problems",
        "resources": "Striver's SDE Sheet - Arrays & Strings parts"
    },
    "Intermediate": {
        "description": "Great progress! Time to level up.",
        "duration": "4-6 weeks",
        "focus": "Advanced structures and algorithms",
        "topics": [
            {"topic": "Trees", "problems": 20, "weight": 2},
            {"topic": "Graphs", "problems": 20, "weight": 2},
            {"topic": "Dynamic Programming", "problems": 30, "weight": 3},
            {"topic": "Sorting & Searching", "problems": 15, "weight": 2},
        ],
        "target": "Solve 100+ medium problems",
        "resources": "Striver's SDE Sheet - Graphs & DP parts"
    },
    "Advanced": {
        "description": "Almost there! FAANG prep mode.",
        "duration": "3-4 weeks",
        "focus": "Hard problems and optimization",
        "topics": [
            {"topic": "DP (Hard)", "problems": 25, "weight": 3},
            {"topic": "Graphs (Hard)", "problems": 15, "weight": 3},
            {"topic": "Trees (Hard)", "problems": 15, "weight": 3},
            {"topic": "Advanced Topics", "problems": 20, "weight": 3},
        ],
        "target": "Solve 50+ hard problems",
        "resources": "Striver's SDE Sheet - HARD section"
    }
}


class SkillAssessor:
    """
    Skill assessment to determine user level
    """

    def __init__(self):
        self.questions = SKILL_ASSESSMENT_QUESTIONS
        self.score = 0
        self.total = len(self.questions)

    def get_question(self, index: int) -> Optional[Dict]:
        """Get question by index"""
        if index >= len(self.questions):
            return None
        
        q = self.questions[index]
        return {
            "question": q.question,
            "options": q.options,
            "topic": q.topic,
            "difficulty": q.difficulty
        }

    def check_answer(self, index: int, answer: int) -> Dict:
        """Check answer and return result"""
        if index >= len(self.questions):
            return {"error": "Invalid question index"}
        
        q = self.questions[index]
        correct = (answer == q.correct)
        
        if correct:
            self.score += 1
        
        return {
            "correct": correct,
            "correct_answer": q.correct,
            "explanation": q.explanation
        }

    def assess_level(self) -> str:
        """Assess user level based on score"""
        percentage = (self.score / self.total) * 100
        
        if percentage >= 80:
            return "Advanced"
        elif percentage >= 60:
            return "Intermediate"
        else:
            return "Beginner"

    def get_assessment_result(self) -> str:
        """Get assessment result message"""
        percentage = (self.score / self.total) * 100
        level = self.assess_level()
        
        return {
            "score": self.score,
            "total": self.total,
            "percentage": percentage,
            "level": level
        }


class RoadmapPlanner:
    """
    Personalized roadmap based on Striver's SDE Sheet
    """

    def __init__(self, level: str = "Beginner"):
        self.level = level
        self.roadmap = STIVER_ROADMAP.get(level, STIVER_ROADMAP["Beginner"])

    def get_roadmap(self) -> str:
        """Get formatted roadmap"""
        rd = self.roadmap
        
        msg = f"""
📚 Your Personalized Roadmap: {self.level}
{'='*40}

📖 Description: {rd['description']}
⏱️  Duration: {rd['duration']}
🎯 Focus: {rd['focus']}
🏆 Target: {rd['target']}

📚 Topics to Cover:
"""
        
        for i, topic in enumerate(rd["topics"], 1):
            msg += f"""
{i}. {topic['topic']}
   - Problems: {topic['problems']}
   - Difficulty: {'⭐' * topic['weight']}
"""
        
        msg += f"""
📖 Resources: {rd['resources']}

💡 Tips:
• Practice 2-3 problems daily
• Start with easy, move to medium/hard
• Review concepts before problems
• Track your progress!

Let's start! Type 'topics' to begin learning.
"""
        
        return msg

    def get_next_topic(self, completed: List[str]) -> Optional[str]:
        """Get next topic to study"""
        topics = self.roadmap["topics"]
        
        for topic in topics:
            if topic["topic"] not in completed:
                return topic["topic"]
        
        return None

    def get_topic_recommendations(self, weak_topics: List[str]) -> str:
        """Get recommendations based on weak areas"""
        topics = self.roadmap["topics"]
        
        msg = """
🎯 Recommended Practice (based on weak areas):
"""
        
        for topic in topics:
            if topic["topic"] in weak_topics:
                msg += f"""
• {topic['topic']}: {topic['problems']} problems
  Priority: HIGH
"""
            else:
                msg += f"""
• {topic['topic']}: {topic['problems']} problems
  Priority: Normal
"""
        
        return msg


class AssessmentFlow:
    """Skill assessment flow"""

    def __init__(self):
        self.assessor = SkillAssessor()
        self.current_question = 0
        self.active = False

    def start(self) -> str:
        """Start skill assessment"""
        self.assessor = SkillAssessor()
        self.current_question = 0
        self.active = True
        
        return self._get_question_text()

    def _get_question_text(self) -> str:
        """Get current question text"""
        q = self.assessor.get_question(self.current_question)
        
        if not q:
            return self._end_assessment()
        
        options = ""
        for i, opt in enumerate(q["options"], 1):
            options += f"  {i}. {opt}\n"
        
        return f"""
🎯 Skill Assessment (Question {self.current_question + 1}/{self.assessor.total})

{q['question']}

{options}
Topic: {q['topic']} | Difficulty: {q['difficulty'].upper()}
---

Type answer number (1-4)
"""

    def submit_answer(self, answer: int) -> str:
        """Submit answer"""
        if not self.active:
            return "No assessment active. Type 'assess' to start."
        
        result = self.assessor.check_answer(self.current_question, answer)
        
        if result["correct"]:
            feedback = "✅ Correct!"
        else:
            feedback = f"❌ Wrong! Answer: {result['correct_answer'] + 1}"
        
        feedback += f"\n📝 {result['explanation']}"
        
        self.current_question += 1
        
        if self.current_question >= self.assessor.total:
            return feedback + "\n\n" + self._end_assessment()
        
        return feedback + "\n\n" + self._get_question_text()

    def _end_assessment(self) -> str:
        """End assessment and show results"""
        self.active = False
        result = self.assessor.get_assessment_result()
        
        level = result["level"]
        roadmap = RoadmapPlanner(level)
        
        emoji = "🏆" if level == "Advanced" else "🎉" if level == "Intermediate" else "🌱"
        
        msg = f"""
{emoji} Assessment Complete!

Score: {result['score']}/{result['total']} ({result['percentage']:.0f}%)
Detected Level: {level}

{roadmap.get_roadmap()}
"""
        
        return msg


__all__ = ['SkillAssessor', 'RoadmapPlanner', 'AssessmentFlow', 'STIVER_ROADMAP']
