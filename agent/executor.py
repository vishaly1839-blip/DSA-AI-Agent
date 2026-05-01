"""
DSA AI Agent - Code Executor
Safe Python code execution with test validation
"""

import io
import sys
import traceback
import re
import time
from typing import Dict, List, Optional, Any


class TestCase:
    """Test case for code validation"""
    
    def __init__(
        self,
        input_data: str = "",
        expected_output: str = "",
        description: str = ""
    ):
        self.input_data = input_data
        self.expected_output = expected_output.strip()
        self.description = description


class ExecutionResult:
    """Code execution result"""
    
    def __init__(
        self,
        success: bool,
        output: str = "",
        error: str = "",
        execution_time: float = 0.0
    ):
        self.success = success
        self.output = output
        self.error = error
        self.execution_time = execution_time


class CodeExecutor:
    """Execute Python code safely"""
    
    def __init__(self, timeout: int = 5, memory_limit: int = 50):
        self.timeout = timeout
        self.memory_limit = memory_limit  # MB
        self.sandbox_globals = {
            "__name__": "__main__",
            "__doc__": None,
            "__builtins__": __builtins__,
        }
    
    def execute(self, code: str, input_data: str = "") -> ExecutionResult:
        """Execute Python code"""
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        
        start_time = time.time()
        
        try:
            # Create a restricted environment
            exec_globals = self.sandbox_globals.copy()
            exec_globals["__builtins__"] = {
                'print': print,
                'len': len,
                'range': range,
                'int': int,
                'float': float,
                'str': str,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'bool': bool,
                'abs': abs,
                'min': min,
                'max': max,
                'sum': sum,
                'sorted': sorted,
                'reversed': reversed,
                'enumerate': enumerate,
                'zip': zip,
                'map': map,
                'filter': filter,
                'input': lambda: input_data.strip() if input_data else "",
                'open': None,  # Disabled for safety
                'exec': None,
                'eval': None,
                '__import__': None,
            }
            
            # Execute code
            exec(code, exec_globals)
            
            execution_time = time.time() - start_time
            
            output = stdout_capture.getvalue()
            
            return ExecutionResult(
                success=True,
                output=output.strip(),
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            error_msg = f"{type(e).__name__}: {str(e)}"
            
            return ExecutionResult(
                success=False,
                output=stdout_capture.getvalue().strip(),
                error=error_msg,
                execution_time=execution_time
            )
        
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    def run_function(
        self,
        code: str,
        function_name: str,
        args: List[Any]
    ) -> ExecutionResult:
        """Run a specific function with args"""
        stdout_capture = io.StringIO()
        stderr_capture = io.StringIO()
        
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = stdout_capture
        sys.stderr = stderr_capture
        
        start_time = time.time()
        
        try:
            exec_globals = self.sandbox_globals.copy()
            exec_globals["__builtins__"] = {
                'print': print,
                'len': len,
                'range': range,
                'int': int,
                'float': float,
                'str': str,
                'list': list,
                'dict': dict,
                'set': set,
                'tuple': tuple,
                'bool': bool,
                'abs': abs,
                'min': min,
                'max': max,
                'sum': sum,
                'sorted': sorted,
            }
            
            exec(code, exec_globals)
            
            # Get function and call it
            func = exec_globals.get(function_name)
            if not func:
                return ExecutionResult(
                    success=False,
                    error=f"Function '{function_name}' not found"
                )
            
            result = func(*args)
            
            execution_time = time.time() - start_time
            
            output = stdout_capture.getvalue()
            if result is not None:
                output += str(result)
            
            return ExecutionResult(
                success=True,
                output=output.strip(),
                execution_time=execution_time
            )
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            return ExecutionResult(
                success=False,
                error=f"{type(e).__name__}: {str(e)}"
            )
        
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr


class TestRunner:
    """Run test cases against code"""
    
    def __init__(self):
        self.executor = CodeExecutor()
    
    def run_tests(
        self,
        code: str,
        test_cases: List[TestCase]
    ) -> Dict:
        """Run all test cases"""
        results = []
        passed = 0
        
        for i, test in enumerate(test_cases):
            result = self.executor.execute(code, test.input_data)
            
            if result.success:
                actual = result.output.strip()
                expected = test.expected_output.strip()
                
                # Compare outputs (flexible match)
                passed_test = self._compare_output(actual, expected)
                
                results.append({
                    "test_num": i + 1,
                    "description": test.description,
                    "input": test.input_data,
                    "expected": expected,
                    "actual": actual,
                    "passed": passed_test,
                    "error": None if passed_test else "Output mismatch"
                })
                
                if passed_test:
                    passed += 1
            else:
                results.append({
                    "test_num": i + 1,
                    "description": test.description,
                    "input": test.input_data,
                    "expected": test.expected_output,
                    "actual": None,
                    "passed": False,
                    "error": result.error
                })
        
        total = len(test_cases)
        score = f"{passed}/{total}"
        percentage = (passed / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "passed": passed,
            "score": score,
            "percentage": percentage,
            "results": results
        }
    
    def _compare_output(self, actual: str, expected: str) -> bool:
        """Compare actual vs expected output"""
        # Exact match
        if actual == expected:
            return True
        
        # Normalize and compare
        actual_norm = self._normalize_output(actual)
        expected_norm = self._normalize_output(expected)
        
        if actual_norm == expected_norm:
            return True
        
        # Check if expected is contained in actual
        if expected_norm in actual_norm:
            return True
        
        # Handle list/tuple outputs
        try:
            actual_list = eval(f"[{actual}]")
            expected_list = eval(f"[{expected}]")
            
            if actual_list == expected_list:
                return True
        except:
            pass
        
        return False
    
    def _normalize_output(self, output: str) -> str:
        """Normalize output for comparison"""
        # Remove whitespace
        output = output.strip()
        # Replace multiple spaces with single
        output = re.sub(r'\s+', ' ', output)
        # Remove trailing commas
        output = output.rstrip(', ')
        return output
    
    def run_function_tests(
        self,
        code: str,
        function_name: str,
        test_cases: List[Dict]
    ) -> Dict:
        """Run tests for a function"""
        results = []
        passed = 0
        
        for i, test in enumerate(test_cases):
            args = test.get("args", [])
            expected = test.get("expected", "")
            
            result = self.executor.run_function(code, function_name, args)
            
            if result.success:
                actual = result.output.strip()
                
                passed_test = self._compare_output(actual, str(expected))
                
                results.append({
                    "test_num": i + 1,
                    "args": args,
                    "expected": expected,
                    "actual": actual,
                    "passed": passed_test
                })
                
                if passed_test:
                    passed += 1
            else:
                results.append({
                    "test_num": i + 1,
                    "args": args,
                    "expected": expected,
                    "actual": None,
                    "passed": False,
                    "error": result.error
                })
        
        total = len(test_cases)
        score = f"{passed}/{total}"
        percentage = (passed / total * 100) if total > 0 else 0
        
        return {
            "total": total,
            "passed": passed,
            "score": score,
            "percentage": percentage,
            "results": results
        }


class SolutionValidator:
    """Validate common DSA solutions"""
    
    @staticmethod
    def validate_two_sum(user_code: str) -> Dict:
        """Validate Two Sum solution"""
        executor = CodeExecutor()
        
        test_cases = [
            TestCase(
                input_data="[2,7,11,15]\n9",
                expected_output="0 1",
                description="Basic case"
            ),
            TestCase(
                input_data="[3,2,4]\n6",
                expected_output="1 2",
                description="Different indices"
            ),
        ]
        
        runner = TestRunner()
        return runner.run_tests(user_code, test_cases)
    
    @staticmethod
    def validate_reverse_linked_list(user_code: str) -> Dict:
        """Validate reverse linked list"""
        # This would need more complex validation
        return {"status": "complex", "message": "Manual review required"}
    
    @staticmethod
    def validate_binary_search(user_code: str) -> Dict:
        """Validate binary search"""
        test_cases = [
            TestCase(
                input_data="[1,2,3,4,5]\n3",
                expected_output="2",
                description="Element found"
            ),
            TestCase(
                input_data="[1,2,3,4,5]\n6",
                expected_output="-1",
                description="Element not found"
            ),
        ]
        
        runner = TestRunner()
        return runner.run_tests(user_code, test_cases)


def format_test_results(results: Dict) -> str:
    """Format test results for display"""
    total = results["total"]
    passed = results["passed"]
    percentage = results["percentage"]
    
    emoji = "✅" if percentage == 100 else "⚠️" if percentage >= 50 else "❌"
    
    output = f"""
{emoji} Test Results: {passed}/{total} ({percentage:.0f}%)
---
"""
    
    for result in results["results"]:
        passed_emoji = "✅" if result["passed"] else "❌"
        
        output += f"""
Test {result['test_num']}: {passed_emoji}
Description: {result.get('description', 'N/A')}
"""
        
        if result.get("error"):
            output += f"Error: {result['error']}\n"
        else:
            output += f"Expected: {result.get('expected', 'N/A')}\n"
            output += f"Actual: {result.get('actual', 'N/A')}\n"
        
        output += "---\n"
    
    return output


__all__ = [
    'CodeExecutor', 
    'TestRunner', 
    'TestCase', 
    'ExecutionResult',
    'SolutionValidator',
    'format_test_results'
]
