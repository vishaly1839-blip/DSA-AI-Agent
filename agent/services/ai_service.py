"""
DSA AI Agent - AI Service
OpenAI API integration for smarter responses
"""

import os
from typing import Optional, List, Dict

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIService:
    """
    AI Service for OpenAI API integration
    Provides smarter DSA responses with LLM
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.available = False
        self.model = "gpt-3.5-turbo"
        
        if self.api_key and OPENAI_AVAILABLE:
            openai.api_key = self.api_key
            self.available = True
            print("✅ AI Service enabled!")
        else:
            print("⚠️  AI not available. Set OPENAI_API_KEY")

    def get_response(
        self, 
        messages: List[Dict[str, str]], 
        model: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.7
    ) -> Optional[str]:
        """
        Get AI response for user message
        """
        if not self.available:
            return None

        try:
            model = model or self.model
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ AI Service Error: {e}")
            return None

    def enhance_dsa_response(
        self, 
        user_message: str, 
        context: str
    ) -> str:
        """
        Enhance DSA response with AI
        """
        if not self.available:
            return context

        system_prompt = """You are a DSA (Data Structures and Algorithms) tutor.
Explain concepts simply, provide code examples, and give hints.
Be encouraging and thorough."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {user_message}"}
        ]

        return self.get_response(messages) or context

    def explain_problem(
        self,
        problem_name: str,
        difficulty: str,
        hints_only: bool = False
    ) -> str:
        """
        AI-powered problem explanation
        """
        if not self.available:
            return f"Problem: {problem_name} (Difficulty: {difficulty})"

        system_prompt = f"""You are a DSA tutor. Explain the problem '{problem_name}'.
Difficulty: {difficulty}
Provide:
1. Problem understanding
2. Approach/hints {'(hints only)' if hints_only else ''}
3. Time complexity
4. Space complexity
5. Key insights

Be encouraging and clear."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Explain {problem_name}"}
        ]

        return self.get_response(messages, max_tokens=800) or f"Problem: {problem_name}"

    def review_code(
        self,
        code: str,
        problem: str = ""
    ) -> str:
        """
        AI-powered code review
        """
        if not self.available:
            return "AI not available. Code review disabled."

        system_prompt = """You are a code reviewer. Review the DSA code provided.
Check for:
1. Correctness
2. Edge cases
3. Time/Space complexity
4. Code quality
5. Improvements

Provide constructive feedback."""

        user_content = f"Problem: {problem}\n\nCode:\n```{code}\n```"
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

        return self.get_response(messages, max_tokens=600) or "Code review unavailable"

    def generate_followup(
        self,
        topic: str,
        user_level: str,
        weak_areas: List[str]
    ) -> str:
        """
        Generate follow-up questions based on weak areas
        """
        if not self.available:
            return ""

        weak_str = ", ".join(weak_areas) if weak_areas else "None identified"
        
        system_prompt = f"""You are a DSA tutor. The user is at {user_level} level.
Weak areas: {weak_str}

Generate 2-3 follow-up questions to test understanding of '{topic}'.
Focus on the weak areas.
Questions should be thought-provoking but not too hard."""

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Generate follow-up for {topic}"}
        ]

        return self.get_response(messages, max_tokens=300) or ""


def setup_ai_service(api_key: str = "") -> AIService:
    """Setup AI service"""
    return AIService(api_key)


__all__ = ['AIService', 'setup_ai_service']
