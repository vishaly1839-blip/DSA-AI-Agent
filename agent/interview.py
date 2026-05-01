"""
DSA AI Agent - Interview Prep Module
FAANG practice mode
"""

import random
from typing import List, Dict, Optional


class InterviewProblem:
    """Interview problem with metadata"""
    
    def __init__(
        self,
        id: int,
        name: str,
        difficulty: str,
        topics: List[str],
        companies: List[str],
        description: str
    ):
        self.id = id
        self.name = name
        self.difficulty = difficulty
        self.topics = topics
        self.companies = companies
        self.description = description


class InterviewPrep:
    """FAANG Interview Preparation"""
    
    def __init__(self):
        self.problems = self._load_problems()
        self.bookmarked = []
    
    def _load_problems(self) -> List[InterviewProblem]:
        """Load FAANG problems"""
        problems = []
        
        # Google problems
        problems.extend([
            InterviewProblem(
                15, "3Sum", "medium", 
                ["array", "two-pointer", "sorting"], 
                ["google", "amazon", "meta"],
                "Find all unique triplets that sum to 0"
            ),
            InterviewProblem(
                11, "Container With Most Water", "medium",
                ["array", "two-pointer", "greedy"],
                ["google", "amazon"],
                "Find container holding most water"
            ),
            InterviewProblem(
                56, "Merge Intervals", "medium",
                ["array", "sorting", "interval"],
                ["google", "meta", "apple"],
                "Merge overlapping intervals"
            ),
            InterviewProblem(
                297, "Serialize/Deserialize", "hard",
                ["tree", "design", "bfs", "dfs"],
                ["google", "amazon", "meta"],
                "Serialize and deserialize binary tree"
            ),
        ])
        
        # Meta problems
        problems.extend([
            InterviewProblem(
                1, "Two Sum", "easy",
                ["array", "hash"],
                ["meta", "amazon", "apple"],
                "Find two numbers that sum to target"
            ),
            InterviewProblem(
                146, "LRU Cache", "medium",
                ["hash", "design", "linked-list"],
                ["meta", "amazon", "apple", "google"],
                "Implement LRU cache"
            ),
            InterviewProblem(
                91, "Decode Ways", "medium",
                ["string", "dp"],
                ["meta", "amazon"],
                "Decode ways for encoded message"
            ),
        ])
        
        # Amazon problems
        problems.extend([
            InterviewProblem(
                206, "Reverse Linked List", "easy",
                ["linked-list", "recursion"],
                ["amazon", "apple", "meta"],
                "Reverse linked list iteratively"
            ),
            InterviewProblem(
                102, "Binary Tree Level Order", "medium",
                ["tree", "bfs", "queue"],
                ["amazon", "apple", "meta"],
                "Level order traversal of tree"
            ),
            InterviewProblem(
                98, "Validate BST", "medium",
                ["tree", "bst", "dfs"],
                ["amazon", "meta", "apple"],
                "Check if valid binary search tree"
            ),
            InterviewProblem(
                543, "Diameter of Binary Tree", "easy",
                ["tree", "dfs"],
                ["amazon", "meta"],
                "Find diameter of binary tree"
            ),
        ])
        
        # Apple problems
        problems.extend([
            InterviewProblem(
                5, "Longest Palindrome", "medium",
                ["string", "dp", "two-pointer"],
                ["apple", "amazon"],
                "Find longest palindromic substring"
            ),
            InterviewProblem(
                23, "Merge K Sorted Lists", "hard",
                ["linked-list", "heap", "merge"],
                ["apple", "amazon", "meta"],
                "Merge k sorted linked lists"
            ),
        ])
        
        # General FAANG
        problems.extend([
            InterviewProblem(
                76, "Minimum Window Substring", "hard",
                ["string", "sliding-window", "hash"],
                ["google", "meta", "amazon"],
                "Find minimum window substring"
            ),
            InterviewProblem(
                322, "Coin Change", "medium",
                ["dp", "array"],
                ["amazon", "apple", "meta"],
                "Minimum coins to make amount"
            ),
            InterviewProblem(
                10, "Regex Matching", "hard",
                ["string", "dp"],
                ["meta", "google", "apple"],
                "Regular expression matching"
            ),
            InterviewProblem(
                49, "Group Anagrams", "medium",
                ["string", "hash", "sorting"],
                ["meta", "amazon", "apple"],
                "Group anagrams together"
            ),
        ])
        
        return problems
    
    def get_by_company(self, company: str) -> List[InterviewProblem]:
        """Get problems by company"""
        company = company.lower()
        return [p for p in self.problems if company in [c.lower() for c in p.companies]]
    
    def get_by_difficulty(self, difficulty: str) -> List[InterviewProblem]:
        """Get problems by difficulty"""
        return [p for p in self.problems if p.difficulty == difficulty]
    
    def get_by_topic(self, topic: str) -> List[InterviewProblem]:
        """Get problems by topic"""
        topic = topic.lower()
        return [p for p in self.problems if topic in p.topics]
    
    def get_random(self, count: int = 3, difficulty: str = None) -> List[InterviewProblem]:
        """Get random problems"""
        problems = self.problems
        if difficulty:
            problems = self.get_by_difficulty(difficulty)
        return random.sample(problems, min(count, len(problems)))
    
    def format_problem(self, p: InterviewProblem) -> str:
        """Format problem for display"""
        companies = ", ".join(p.companies)
        topics = ", ".join(p.topics)
        return f"""
Problem {p.id}: {p.name}
Difficulty: {p.difficulty.upper()}
Companies: {companies}
Topics: {topics}
Description: {p.description}
"""
    
    def format_problems(self, problems: List[InterviewProblem]) -> str:
        """Format multiple problems"""
        result = "📝 Interview Problems:\n\n"
        for p in problems:
            result += self.format_problem(p)
            result += "---\n"
        return result


class InterviewSession:
    """Manage interview practice"""
    
    def __init__(self):
        self.prep = InterviewPrep()
        self.current_problems = []
        self.current_index = 0
    
    def start_easy(self, count: int = 3) -> str:
        """Start easy session"""
        self.current_problems = self.prep.get_random(count, "easy")
        return self._format_session("Easy")
    
    def start_medium(self, count: int = 3) -> str:
        """Start medium session"""
        self.current_problems = self.prep.get_random(count, "medium")
        return self._format_session("Medium")
    
    def start_hard(self, count: int = 3) -> str:
        """Start hard session"""
        self.current_problems = self.prep.get_random(count, "hard")
        return self._format_session("Hard")
    
    def start_company(self, company: str, count: int = 3) -> str:
        """Start by company"""
        problems = self.prep.get_by_company(company)
        self.current_problems = random.sample(problems, min(count, len(problems)))
        return self._format_session(company.title())
    
    def start_topic(self, topic: str, count: int = 3) -> str:
        """Start by topic"""
        problems = self.prep.get_by_topic(topic)
        self.current_problems = random.sample(problems, min(count, len(problems)))
        return self._format_session(topic.title())
    
    def _format_session(self, session_type: str) -> str:
        """Format session start"""
        return f"""
🎯 {session_type} Interview Prep - Started!

Problems: {len(self.current_problems)}

{self.prep.format_problems(self.current_problems)}

Type 'hint' for hints, or 'answer' for solution.
"""
    
    def next_problem(self) -> str:
        """Get next problem"""
        if self.current_index < len(self.current_problems) - 1:
            self.current_index += 1
            p = self.current_problems[self.current_index]
            return self.prep.format_problem(p)
        return "No more problems! Start new session."


__all__ = ['InterviewPrep', 'InterviewSession', 'InterviewProblem']
