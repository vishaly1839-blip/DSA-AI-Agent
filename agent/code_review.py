"""
DSA AI Agent - Code Review Module
Review and analyze DSA code
"""

import re
from typing import List, Dict, Optional


class CodeReviewer:
    """
    Code reviewer for DSA problems
    Analyzes code for issues and improvements
    """

    def __init__(self):
        self.reviews = []

    def analyze_code(self, code: str, language: str = "python") -> Dict:
        """Analyze code and return feedback"""
        
        issues = []
        suggestions = []
        complexity = "Unknown"

        if language.lower() == "python":
            issues = self._analyze_python(code)
            complexity = self._estimate_complexity(code)
        elif language.lower() == "cpp" or language.lower() == "c++":
            issues = self._analyze_cpp(code)
            complexity = self._estimate_complexity(code)

        suggestions = self._get_suggestions(issues)

        return {
            "issues": issues,
            "suggestions": suggestions,
            "complexity": complexity
        }

    def _analyze_python(self, code: str) -> List[str]:
        """Analyze Python code"""
        issues = []

        # Check for common issues
        if "for i in range(len(" in code:
            issues.append("Consider enumerate() instead of range(len())")

        if ".append(" in code and "range" in code:
            issues.append("List comprehension might be more efficient")

        if "while True" in code and "break" not in code:
            issues.append("Potential infinite loop - ensure break condition")

        if "== True" in code or "== False" in code:
            issues.append("Use 'if x:' instead of 'if x == True:'")

        if re.search(r"\[\d+\]", code):
            issues.append("Magic number detected - consider constant")

        return issues

    def _analyze_cpp(self, code: str) -> List[str]:
        """Analyze C++ code"""
        issues = []

        if "using namespace std;" in code:
            issues.append("Avoid 'using namespace std;' in production")

        if "new" in code and "delete" not in code:
            issues.append("Memory leak - missing delete")

        if "cin >> " in code:
            issues.append("Consider faster I/O for large input")

        if "=" in code and "==" in code.replace("=", ""): 
            # Simple check for assignment in condition
            pass

        return issues

    def _estimate_complexity(self, code: str) -> str:
        """Estimate time complexity"""
        
        code_lower = code.lower()
        
        # Nested loops
        if code_lower.count("for") >= 2 or code_lower.count("while") >= 2:
            if "for" in code_lower and "for" in code_lower:
                return "O(n²) - Quadratic"
        
        # Binary search pattern
        if "left" in code_lower and "right" in code_lower:
            return "O(log n) - Logarithmic"
        
        # Single loop
        if "for" in code_lower or "while" in code_lower:
            return "O(n) - Linear"
        
        # Hash operations
        if "set(" in code_lower or "dict(" in code_lower:
            return "O(1) - Constant"
        
        return "O(n) - Linear"

    def _get_suggestions(self, issues: List[str]) -> List[str]:
        """Get improvement suggestions"""
        
        suggestions = []
        
        if not issues:
            suggestions.append("Code looks clean!")
            return suggestions

        for issue in issues:
            if "enumerate" in issue:
                suggestions.append("Use enumerate for index access")
            if "comprehension" in issue:
                suggestions.append("List comprehension is more Pythonic")
            if "magic" in issue:
                suggestions.append("Define constants with meaningful names")
            if "infinite" in issue:
                suggestions.append("Verify all paths lead to break/return")

        return suggestions

    def review_linked_list(self, code: str) -> str:
        """Specific review for linked list code"""
        
        issues = []
        
        # Check for null handling
        if "head ==" not in code and "head==" not in code:
            issues.append("Check for null/None head")
        
        # Check memory
        if "next" in code and "prev" not in code:
            issues.append("Consider if you need previous pointer")
        
        return self._format_review("Linked List", issues)

    def review_binary_search(self, code: str) -> str:
        """Specific review for binary search"""
        
        issues = []
        
        # Check for off-by-one
        if "<=" not in code and "<" in code:
            issues.append("Verify <= vs < in condition")
        
        # Check mid calculation
        if "(left + right) / 2" in code:
            issues.append("Use (left + right) // 2 to avoid overflow")
            issues.append("Better: left + (right - left) // 2")
        
        return self._format_review("Binary Search", issues)

    def review_dp(self, code: str) -> str:
        """Specific review for DP"""
        
        issues = []
        
        # Check for tabulation vs memoization
        if "dp" not in code.lower():
            issues.append("Consider using DP array")
        
        # Check for base case
        if code.count("return") > 1 and "if" not in code[:50]:
            issues.append("Check base case handling")
        
        return self._format_review("Dynamic Programming", issues)

    def _format_review(self, topic: str, issues: List[str]) -> str:
        """Format review output"""
        
        if not issues:
            return f"✅ {topic}: Code looks good!"

        result = f"⚠️  {topic} Issues Found:\n"
        for i, issue in enumerate(issues, 1):
            result += f"{i}. {issue}\n"

        return result


class CodeFormatter:
    """Format code for display"""

    @staticmethod
    def format_python(code: str, indent: int = 4) -> str:
        """Format Python code"""
        lines = code.split('\n')
        formatted = []

        for line in lines:
            stripped = line.rstrip()
            formatted.append(stripped)

        return '\n'.join(formatted)

    @staticmethod
    def add_line_numbers(code: str) -> str:
        """Add line numbers"""
        lines = code.split('\n')
        numbered = []

        for i, line in enumerate(lines, 1):
            numbered.append(f"{i:3d} | {line}")

        return '\n'.join(numbered)


__all__ = ['CodeReviewer', 'CodeFormatter']
