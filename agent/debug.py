"""
DSA AI Agent - Debug Module
Interactive code debugger with step-by-step execution
"""

import sys
import traceback
import ast
import io
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field


@dataclass
class Breakpoint:
    """Code breakpoint"""
    line: int
    enabled: bool = True


@dataclass 
class DebugFrame:
    """Debug stack frame"""
    name: str
    locals: Dict[str, Any] = field(default_factory=dict)
    globals: Dict[str, Any] = field(default_factory=dict)


class DebugResult:
    """Debug execution result"""
    
    def __init__(
        self,
        success: bool,
        current_line: int = 0,
        output: str = "",
        variables: Dict[str, Any] = None,
        error: str = "",
        finished: bool = False
    ):
        self.success = success
        self.current_line = current_line
        self.output = output
        self.variables = variables or {}
        self.error = error
        self.finished = finished


class CodeDebugger:
    """Interactive code debugger"""
    
    def __init__(self):
        self.code = ""
        self.lines = []
        self.current_line = 0
        self.variables = {}
        self.breakpoints = []
        self.finished = False
        self.output = []
        
    def start_debug(self, code: str) -> str:
        """Start debugging session"""
        self.code = code
        self.lines = code.split('\n')
        self.current_line = 0
        self.variables = {}
        self.finished = False
        self.output = []
        
        # Show first line
        return self._format_status()
    
    def step(self) -> DebugResult:
        """Execute next line"""
        if self.finished:
            return DebugResult(success=True, finished=True)
        
        if self.current_line >= len(self.lines):
            self.finished = True
            return DebugResult(success=True, finished=True, variables=self.variables)
        
        # Get current line
        line = self.lines[self.current_line].strip()
        
        if not line or line.startswith('#'):
            self.current_line += 1
            return self._execute_line(line)
        
        # Execute line
        return self._execute_line(line)
    
    def _execute_line(self, line: str) -> DebugResult:
        """Execute a single line"""
        if not line:
            self.current_line += 1
            return DebugResult(
                success=True,
                current_line=self.current_line,
                variables=self.variables.copy()
            )
        
        # Capture output
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        
        try:
            # Execute in context
            exec(line, {}, self.variables)
            
            # Get output
            line_output = sys.stdout.getvalue()
            sys.stdout = old_stdout
            
            if line_output:
                self.output.append(line_output)
            
            self.current_line += 1
            
            return DebugResult(
                success=True,
                current_line=self.current_line,
                output=line_output,
                variables=self.variables.copy()
            )
            
        except Exception as e:
            sys.stdout = old_stdout
            error_msg = f"Error at line {self.current_line + 1}: {type(e).__name__}: {str(e)}"
            
            return DebugResult(
                success=False,
                current_line=self.current_line,
                error=error_msg,
                variables=self.variables.copy()
            )
    
    def run_to_end(self) -> DebugResult:
        """Run to completion"""
        while not self.finished and self.current_line < len(self.lines):
            result = self.step()
            if not result.success:
                return result
                
        return DebugResult(
            success=True,
            finished=True,
            variables=self.variables.copy()
        )
    
    def _format_status(self) -> str:
        """Format debug status"""
        if self.current_line >= len(self.lines):
            return f"""✅ Debug complete!

Variables: {self.variables}"""
        
        line_num = self.current_line + 1
        line = self.lines[self.current_line]
        
        return f"""🔍 Debugging... Line {line_num}:

→ {line}

Variables: {self.variables}

Commands: step, run, vars, quit"""
    
    def get_variables(self) -> Dict[str, Any]:
        """Get current variables"""
        return self.variables.copy()


class DebugCommandHandler:
    """Handle debug commands"""
    
    def __init__(self, debugger: CodeDebugger):
        self.debugger = debugger
    
    def handle(self, message: str) -> str:
        """Handle debug command"""
        msg = message.lower().strip()
        
        if msg in ['quit', 'exit', 'q']:
            self.debugger.finished = True
            return "👋 Exited debug mode."
        
        if msg in ['step', 'n', 'next']:
            result = self.debugger.step()
            return self._format_result(result)
        
        if msg in ['run', 'r']:
            result = self.debugger.run_to_end()
            return self._format_result(result)
        
        if msg in ['vars', 'variables']:
            vars_str = "\n".join(f"  {k}: {v}" for k, v in self.debugger.variables.items())
            return f"""📦 Variables:
{vars_str or '  (none)'}"""
        
        # Unknown command
        return "Unknown command. Try: step, run, vars, quit"
    
    def _format_result(self, result: DebugResult) -> str:
        """Format debug result"""
        if result.finished:
            return f"""✅ Debug complete!

Variables:
{self._format_vars(result.variables)}"""
        
        if not result.success:
            return f"❌ {result.error}"
        
        return self._format_status(result)
    
    def _format_status(self, result: DebugResult) -> str:
        """Format status"""
        if self.debugger.current_line >= len(self.debugger.lines):
            return f"""✅ Finished!

Variables: {result.variables}"""
        
        line_num = self.debugger.current_line + 1
        line = self.debugger.lines[self.debugger.current_line]
        
        output = f"→ Line {line_num}: {line}\n\n"
        output += "Variables:\n" + self._format_vars(result.variables)
        
        return output
    
    def _format_vars(self, variables: Dict) -> str:
        """Format variables"""
        if not variables:
            return "  (none)"
        return "\n".join(f"  {k}: {v}" for k, v in variables.items())


__all__ = ['CodeDebugger', 'DebugCommandHandler', 'DebugResult', 'Breakpoint']
