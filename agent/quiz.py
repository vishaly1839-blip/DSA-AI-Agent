"""
DSA AI Agent - Quiz System
Interactive knowledge testing
"""

import random
from typing import List, Dict, Optional


class QuizQuestion:
    """Individual quiz question"""
    
    def __init__(
        self,
        question: str,
        options: List[str],
        correct: int,
        explanation: str,
        topic: str,
        difficulty: str = "easy"
    ):
        self.question = question
        self.options = options
        self.correct = correct  # Index of correct answer (0-3)
        self.explanation = explanation
        self.topic = topic
        self.difficulty = difficulty


class Quiz:
    """Quiz system for DSA topics"""
    
    def __init__(self):
        self.questions = self._load_questions()
        self.current_quiz = []
        self.score = 0
        self.total_questions = 0
        
    def _load_questions(self) -> List[QuizQuestion]:
        """Load all quiz questions"""
        questions = []
        
        # Array questions
        questions.extend([
            QuizQuestion(
                "What is the time complexity of accessing an element in an array?",
                ["O(n)", "O(1)", "O(log n)", "O(n²)"],
                1,
                "Arrays provide O(1) random access using index. Element is at arr[index].",
                "array",
                "easy"
            ),
            QuizQuestion(
                "What is the worst-case time complexity of linear search in an array?",
                ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                1,
                "Linear search may need to check all elements, so O(n).",
                "array",
                "easy"
            ),
            QuizQuestion(
                "Which operation is O(1) in an array?",
                ["Search", "Insert at beginning", "Access by index", "Delete at beginning"],
                2,
                "Access by index is O(1) because array stores elements contiguously.",
                "array",
                "easy"
            ),
            QuizQuestion(
                "What is the space complexity of creating a new array of size n?",
                ["O(1)", "O(log n)", "O(n)", "O(n²)"],
                2,
                "New array of size n requires O(n) space.",
                "array",
                "medium"
            ),
        ])
        
        # Linked List questions
        questions.extend([
            QuizQuestion(
                "What is the time complexity to insert at the beginning of a linked list?",
                ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                0,
                "Insert at head is O(1) - just update the head pointer.",
                "linked_list",
                "easy"
            ),
            QuizQuestion(
                "What is the time complexity to access the nth element in a linked list?",
                ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                1,
                "Linked list requires traversal, so O(n).",
                "linked_list",
                "easy"
            ),
            QuizQuestion(
                "Which linked list type allows traversal in both directions?",
                ["Singly", "Doubly", "Circular", "Array"],
                1,
                "Doubly linked list has prev and next pointers.",
                "linked_list",
                "easy"
            ),
            QuizQuestion(
                "What is the space complexity of a linked list with n nodes?",
                ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                1,
                "Each node stores data + pointer, so O(n) space.",
                "linked_list",
                "medium"
            ),
        ])
        
        # Stack questions
        questions.extend([
            QuizQuestion(
                "What is the time complexity of push operation in a stack?",
                ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                0,
                "Push adds to top in O(1) time.",
                "stack",
                "easy"
            ),
            QuizQuestion(
                "Stack follows which principle?",
                ["FIFO", "LIFO", "Random", "Priority"],
                1,
                "Stack is Last In First Out (LIFO).",
                "stack",
                "easy"
            ),
            QuizQuestion(
                "Which data structure uses LIFO?",
                ["Queue", "Stack", "Array", "Hash Table"],
                1,
                "Stack uses Last In First Out principle.",
                "stack",
                "easy"
            ),
        ])
        
        # Queue questions
        questions.extend([
            QuizQuestion(
                "What is the time complexity of enqueue in a queue?",
                ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                0,
                "Enqueue adds to rear in O(1) time.",
                "queue",
                "easy"
            ),
            QuizQuestion(
                "Queue follows which principle?",
                ["FIFO", "LIFO", "Random", "Priority"],
                0,
                "Queue is First In First Out (FIFO).",
                "queue",
                "easy"
            ),
            QuizQuestion(
                "Which algorithm uses queue for traversal?",
                ["DFS", "BFS", "Binary Search", "Quick Sort"],
                1,
                "BFS (Breadth-First Search) uses queue.",
                "queue",
                "medium"
            ),
        ])
        
        # Tree questions
        questions.extend([
            QuizQuestion(
                "What is the time complexity of search in a balanced BST?",
                ["O(1)", "O(n)", "O(log n)", "O(n²)"],
                2,
                "Balanced BST gives O(log n) search due to halving.",
                "tree",
                "easy"
            ),
            QuizQuestion(
                "Inorder traversal of BST produces:",
                ["Pre-sorted", "Post-sorted", "Reverse sorted", "Random"],
                0,
                "Inorder of BST gives sorted sequence.",
                "tree",
                "medium"
            ),
            QuizQuestion(
                "What is the maximum number of nodes at level k in a binary tree?",
                ["k", "2k", "2^k", "k²"],
                2,
                "Level 0 has 1, level 1 has 2, level k has 2^k nodes.",
                "tree",
                "medium"
            ),
            QuizQuestion(
                "DFS traversal uses which data structure?",
                ["Queue", "Stack", "Array", "Heap"],
                1,
                "DFS uses stack (or recursion which uses call stack).",
                "tree",
                "medium"
            ),
        ])
        
        # Graph questions
        questions.extend([
            QuizQuestion(
                "What is the time complexity of BFS/DFS on a graph with V vertices and E edges?",
                ["O(V)", "O(E)", "O(V + E)", "O(V²)"],
                2,
                "BFS/DFS visits each vertex and edge once: O(V+E).",
                "graph",
                "medium"
            ),
            QuizQuestion(
                "Which algorithm finds shortest path in weighted graph?",
                ["BFS", "DFS", "Dijkstra", "Binary Search"],
                2,
                "Dijkstra's algorithm finds shortest path in weighted graph.",
                "graph",
                "medium"
            ),
            QuizQuestion(
                "What is the space complexity of adjacency matrix?",
                ["O(V)", "O(E)", "O(V²)", "O(V + E)"],
                2,
                "Adjacency matrix is VxV, so O(V²).",
                "graph",
                "medium"
            ),
            QuizQuestion(
                "Dijkstra's algorithm doesn't work for:",
                ["Positive weights", "Negative weights", "Zero weights", "All weights"],
                1,
                "Dijkstra fails with negative edge weights.",
                "graph",
                "hard"
            ),
        ])
        
        # Sorting questions
        questions.extend([
            QuizQuestion(
                "What is the average time complexity of Quick Sort?",
                ["O(n)", "O(n log n)", "O(n²)", "O(log n)"],
                1,
                "Quick Sort average is O(n log n).",
                "sorting",
                "easy"
            ),
            QuizQuestion(
                "Which sorting algorithm is stable?",
                ["Quick Sort", "Heap Sort", "Merge Sort", "Selection Sort"],
                2,
                "Merge Sort is stable - equal elements maintain order.",
                "sorting",
                "medium"
            ),
            QuizQuestion(
                "What is the worst-case of Quick Sort?",
                ["O(n)", "O(n log n)", "O(n²)", "O(log n)"],
                2,
                "Quick Sort worst case is O(n²) when array is already sorted.",
                "sorting",
                "medium"
            ),
            QuizQuestion(
                "Which sort works in O(n) with known range?",
                ["Quick Sort", "Merge Sort", "Counting Sort", "Heap Sort"],
                2,
                "Counting sort is O(n+k) where k is range.",
                "sorting",
                "hard"
            ),
        ])
        
        # Dynamic Programming questions
        questions.extend([
            QuizQuestion(
                "DP is used when problems have:",
                ["Unique solution", "Optimal substructure", "No subproblems", "Constant time"],
                1,
                "DP needs optimal substructure and overlapping subproblems.",
                "dp",
                "medium"
            ),
            QuizQuestion(
                "Which is top-down DP approach?",
                ["Tabulation", "Memoization", "Iteration", "Recursion only"],
                1,
                "Memoization is top-down - recursion with cache.",
                "dp",
                "medium"
            ),
            QuizQuestion(
                "Fibonacci using memoization is:",
                ["O(n)", "O(2^n)", "O(n²)", "O(log n)"],
                0,
                "Memoization reduces exponential to O(n).",
                "dp",
                "medium"
            ),
            QuizQuestion(
                "Space optimization in DP reduces:",
                ["Time", "Space", "Both", "Nothing"],
                1,
                "Space optimization reduces space from O(n) to O(1).",
                "dp",
                "hard"
            ),
        ])
        
# Hash Table questions
        questions.extend([
            QuizQuestion(
                "What is average time complexity of hash table lookup?",
                ["O(n)", "O(1)", "O(log n)", "O(n²)"],
                1,
                "Hash table gives O(1) average lookup.",
                "hash",
                "easy"
            ),
            QuizQuestion(
                "What handles collisions in hash tables?",
                ["Array", "Linked List", "Chaining/Probing", "Tree"],
                2,
                "Chaining (linked list at bucket) or open addressing.",
                "hash",
                "medium"
            ),
            QuizQuestion(
                "Load factor in hash table is:",
                ["n/k", "k/n", "n*k", "n+k"],
                0,
                "Load factor = n/k where k is number of buckets.",
                "hash",
                "medium"
            ),
            QuizQuestion(
                "What is the best way to handle hash collisions?",
                ["Use larger array", "Chaining", "Rehash everything", "Use linear search"],
                1,
                "Chaining (linked list at each bucket) handles collisions efficiently.",
                "hash",
                "medium"
            ),
            QuizQuestion(
                "When should you resize a hash table?",
                ["Every 100 inserts", "When load factor > 0.75", "Never", "When empty"],
                1,
                "Resize when load factor exceeds 0.75 to maintain O(1) operations.",
                "hash",
                "hard"
            ),
        ])
        
        # Heap questions
        questions.extend([
            QuizQuestion(
                "Heap is a:",
                ["Binary tree", "Binary search tree", "Complete binary tree", "AVL tree"],
                2,
                "Heap is a complete binary tree with heap property.",
                "heap",
                "medium"
            ),
            QuizQuestion(
                "Root of max-heap contains:",
                ["Minimum", "Maximum", "Average", "Random"],
                1,
                "Max-heap root is maximum element.",
                "heap",
                "easy"
            ),
            QuizQuestion(
                "What is time complexity of heap insert?",
                ["O(1)", "O(n)", "O(log n)", "O(n log n)"],
                2,
                "Heap insert is O(log n) for heapify up.",
                "heap",
                "medium"
            ),
        ])
        
        return questions
    
    def get_quiz_by_topic(self, topic: str, count: int = 5) -> List[QuizQuestion]:
        """Get quiz questions for a topic"""
        topic_questions = [q for q in self.questions if q.topic.lower() == topic.lower()]
        
        if not topic_questions:
            return self.get_random_quiz(count)
        
        return random.sample(topic_questions, min(count, len(topic_questions)))
    
    def get_random_quiz(self, count: int = 5) -> List[QuizQuestion]:
        """Get random quiz questions"""
        return random.sample(self.questions, min(count, len(self.questions)))
    
    def check_answer(self, question: QuizQuestion, answer: int) -> bool:
        """Check if answer is correct"""
        return answer == question.correct
    
    def format_question(self, q: QuizQuestion, index: int) -> str:
        """Format question for display"""
        options_text = ""
        for i, option in enumerate(q.options):
            options_text += f"  {i+1}. {option}\n"
        
        return f"""
📌 Question {index}: {q.question}

{options_text}
Difficulty: {q.difficulty.upper()} | Topic: {q.topic}
"""
    
    def start_quiz(self, topic: str = "random", count: int = 5) -> Dict:
        """Start a new quiz"""
        if topic.lower() == "random":
            self.current_quiz = self.get_random_quiz(count)
        else:
            self.current_quiz = self.get_quiz_by_topic(topic, count)
        
        self.score = 0
        self.total_questions = len(self.current_quiz)
        
        return {
            "status": "started",
            "topic": topic,
            "count": self.total_questions,
            "questions": self.current_quiz
        }
    
    def submit_answer(self, question_index: int, answer: int) -> Dict:
        """Submit answer for a question"""
        if question_index >= len(self.current_quiz):
            return {"error": "Invalid question index"}
        
        question = self.current_quiz[question_index]
        correct = self.check_answer(question, answer)
        
        if correct:
            self.score += 1
        
        return {
            "correct": correct,
            "correct_answer": question.correct,
            "explanation": question.explanation,
            "score": self.score,
            "total": self.total_questions
        }


class QuizManager:
    """Manage quiz sessions"""
    
    def __init__(self):
        self.quiz = Quiz()
        self.active_quiz = None
        self.current_question_index = 0
        
    def start(self, topic: str = "random", count: int = 5) -> str:
        """Start a new quiz session"""
        self.active_quiz = self.quiz.start_quiz(topic, count)
        self.current_question_index = 0
        
        return self._get_start_message()
    
    def _get_start_message(self) -> str:
        """Get start message"""
        topic = self.active_quiz["topic"]
        count = self.active_quiz["count"]
        
        return f"""
🎯 Quiz Started!

Topic: {topic}
Questions: {count}

Type the number of your answer (1-4) for each question.
Type 'skip' to skip current question.
Type 'quit' to end quiz.

---
"""
    
    def answer(self, user_input: str) -> str:
        """Process user answer"""
        if not self.active_quiz:
            return "No active quiz. Type 'quiz' to start one!"
        
        # Handle special commands
        if user_input.lower() == "quit":
            return self._end_quiz()
        
        if user_input.lower() == "skip":
            return self._next_question()
        
        # Try to parse answer
        try:
            answer = int(user_input) - 1
            if answer < 0 or answer > 3:
                return "Invalid answer. Choose 1-4:"
        except ValueError:
            return "Please enter a number 1-4:"
        
        # Submit answer
        result = self.quiz.submit_answer(self.current_question_index, answer)
        
        if result["correct"]:
            feedback = "✅ Correct!"
        else:
            feedback = f"❌ Wrong! Correct answer: {result['correct_answer'] + 1}"
        
        feedback += f"\n📝 {result['explanation']}"
        
        # Move to next or end
        self.current_question_index += 1
        
        if self.current_question_index >= self.total_questions:
            return feedback + "\n" + self._end_quiz()
        
        return feedback + "\n\n" + self._next_question()
    
    def _next_question(self) -> str:
        """Get next question"""
        q = self.active_quiz["questions"][self.current_question_index]
        return self.quiz.format_question(q, self.current_question_index + 1)
    
    def _end_quiz(self) -> str:
        """End quiz and show results"""
        score = self.quiz.score
        total = self.quiz.total_questions
        percentage = (score / total * 100) if total > 0 else 0
        
        emoji = "🏆" if percentage >= 80 else "🎉" if percentage >= 60 else "💪"
        
        result = f"""
{emoji} Quiz Complete!

Score: {score}/{total} ({percentage:.0f}%)

"""
        
        if percentage >= 80:
            result += "Excellent! Keep it up! 🚀"
        elif percentage >= 60:
            result += "Good job! More practice will help!"
        else:
            result += "Keep learning! You'll get better!"
        
        self.active_quiz = None
        return result


SKILL_ASSESSMENT_QUESTIONS = [
    # Question 1
    QuizQuestion(
        "What is the time complexity of binary search?",
        ["O(n)", "O(log n)", "O(n log n)", "O(n²)"],
        1,
        "Binary search halves the search space each time, so O(log n).",
        "array", "easy"
    ),
    # Question 2
    QuizQuestion(
        "Which data structure uses LIFO principle?",
        ["Queue", "Stack", "Array", "Hash Table"],
        1,
        "Stack is Last In First Out (LIFO).",
        "stack", "easy"
    ),
    # Question 3
    QuizQuestion(
        "What is the worst-case of Quick Sort?",
        ["O(n)", "O(n log n)", "O(n²)", "O(log n)"],
        2,
        "Quick Sort worst case is O(n²) when array is already sorted.",
        "sorting", "medium"
    ),
    # Question 4
    QuizQuestion(
        "DP requires which two properties?",
        ["Random access, Iteration", "Optimal substructure, Overlapping subproblems", "Recursion only, Loop", "Array, Hash"],
        1,
        "DP needs optimal substructure and overlapping subproblems.",
        "dp", "medium"
    ),
    # Question 5
    QuizQuestion(
        "DFS on a graph uses which data structure?",
        ["Queue", "Stack", "Array", "Heap"],
        1,
        "DFS uses stack (or recursion which uses call stack).",
        "graph", "medium"
    ),
]


__all__ = ['Quiz', 'QuizManager', 'QuizQuestion', 'SKILL_ASSESSMENT_QUESTIONS']
