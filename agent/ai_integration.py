"""
DSA AI Agent - AI Integration Module
OpenAI API integration for smarter responses
"""

import os
from typing import Optional, List, Dict

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIIntegration:
    """
    AI Integration for OpenAI API
    Makes DSA agent smarter with LLM
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
        self.available = False
        
        if self.api_key and OPENAI_AVAILABLE:
            openai.api_key = self.api_key
            self.available = True
            print("✅ AI Integration enabled!")
        else:
            print("⚠️  AI not available. Set OPENAI_API_KEY")

    def get_response(
        self, 
        messages: List[Dict[str, str]], 
        model: str = "gpt-3.5-turbo",
        max_tokens: int = 500
    ) -> Optional[str]:
        """
        Get AI response for user message
        """
        if not self.available:
            return None

        try:
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ AI Error: {e}")
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


def setup_ai(api_key: str = "") -> AIIntegration:
    """Setup AI integration"""
    return AIIntegration(api_key)


__all__ = ['AIIntegration', 'setup_ai']
