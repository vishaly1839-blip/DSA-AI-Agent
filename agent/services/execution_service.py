"""
DSA AI Agent - Execution Service
Safe Python code execution with test validation
"""

import io
import sys
import re
import time
from typing import Dict, List, Optional, Any


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


class ExecutionService:
    """
    Execution Service for safe Python code execution
    Provides code running and test validation
    """

    def __init__(self, timeout: int = 5, memory_limit: int = 50):
        self.timeout = timeout
        self.memory_limit = memory_limit  # MB
        self.sandbox_globals = {
            "__name__": "__main__",
            "__doc__": None,
            "__builtins__": __builtins__
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
                'open': None,
                'exec': None,
                'eval': None,
                '__import__': None,
            }
            
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
        
        old_stdout = sys.stdout
        sys.stdout = stdout_capture
        
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
            return ExecutionResult(
                success=False,
                error=f"{type(e).__name__}: {str(e)}"
            )
        
        finally:
            sys.stdout = old_stdout

    def run_tests(
        self,
        code: str,
        test_cases: List[TestCase]
    ) -> Dict:
        """Run all test cases"""
        results = []
        passed = 0
        
        for i, test in enumerate(test_cases):
            result = self.execute(code, test.input_data)
            
            if result.success:
                actual = result.output.strip()
                expected = test.expected_output.strip()
                
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
        if actual == expected:
            return True
        
        actual_norm = self._normalize_output(actual)
        expected_norm = self._normalize_output(expected)
        
        if actual_norm == expected_norm:
            return True
        
        if expected_norm in actual_norm:
            return True
        
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
        output = output.strip()
        output = re.sub(r'\s+', ' ', output)
        output = output.rstrip(', ')
        return output


__all__ = [
    'ExecutionService', 
    'TestCase', 
    'ExecutionResult'
]
