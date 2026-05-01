"""
DSA AI Agent - Chat Interface
Enhanced chat interface with better UX
"""

import os
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)


class ChatInterface:
    """
    Enhanced chat interface with colors and better UX
    """
    
    def __init__(self, agent):
        self.agent = agent
        self.session_start = datetime.now()
        self.message_count = 0
        
        # Chat colors
        self.USER_COLOR = Fore.CYAN
        self.AGENT_COLOR = Fore.GREEN
        self.ERROR_COLOR = Fore.RED
        self.INFO_COLOR = Fore.YELLOW
    
    def print_banner(self):
        """Print welcome banner"""
        print(f"""
{Fore.MAGENTA}╔═══════════════════════════════════════════════════╗
║     🎓 DSA AI Tutor Agent v1.0                   ║
║     Your Personal DSA Learning Assistant        ║
╚═══════════════════════════════════════════════════╝{Style.RESET_ALL}
""")
    
    def print_help(self):
        """Print help menu"""
        print(f"""
{self.INFO_COLOR}📚 Available Commands:{Style.RESET_ALL}

  {self.USER_COLOR}explain <topic>{Style.RESET_ALL}  - Detailed explanation
  {self.USER_COLOR}code <problem>{Style.RESET_ALL}   - Generate code solution
  {self.USER_COLOR}hint <problem>{Style.RESET_ALL}   - Get hints
  {self.USER_COLOR}complexity{Style.RESET_ALL}     - Complexity cheatsheet
  {self.USER_COLOR}practice{Style.RESET_ALL}       - Practice recommendations
  {self.USER_COLOR}problems{Style.RESET_ALL}       - List common problems
  {self.USER_COLOR}help{Style.RESET_ALL}          - Show this help

{self.INFO_COLOR}Topics you can ask about:{Style.RESET_ALL}
  array, linked list, stack, queue
  tree, bst, graph, heap
  sorting, searching, dp, dynamic
  hash table, trie
""")
    
    def chat_loop(self):
        """Main chat loop"""
        self.print_banner()
        print(f"{self.INFO_COLOR}Type 'help' for commands or 'exit' to quit{Style.RESET_ALL}\n")
        
        while True:
            try:
                # Get user input
                user_input = input(f"{self.USER_COLOR}You ► {Style.RESET_ALL}").strip()
                
                if not user_input:
                    continue
                
                self.message_count += 1
                
                # Process commands
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print(f"\n{self.AGENT_COLOR}👋 Goodbye! Happy coding! 🚀{Style.RESET_ALL}")
                    print(f"{self.INFO_COLOR}Messages exchanged: {self.message_count}{Style.RESET_ALL}")
                    break
                
                if user_input.lower() == 'help':
                    self.print_help()
                    continue
                
                if user_input.lower() == 'problems':
                    self._show_problems()
                    continue
                
                if user_input.lower() == 'practice':
                    self._show_practice()
                    continue
                
                # Get response from agent
                response = self.agent.chat(user_input)
                print(f"\n{self.AGENT_COLOR}Agent ► {Style.RESET_ALL}{response}\n")
                
            except KeyboardInterrupt:
                print(f"\n\n{self.AGENT_COLOR}👋 Goodbye! Happy coding! 🚀{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{self.ERROR_COLOR}❌ Error: {e}{Style.RESET_ALL}")
    
    def _show_problems(self):
        """Show common DSA problems"""
        print(f"""
{self.INFO_COLOR}📝 Common DSA Problems by Topic:{Style.RESET_ALL}

{Fore.CYAN}ARRAYS:{Style.RESET_ALL}
  • Two Sum
  • Maximum Subarray (Kadane's Algorithm)
  • Rotate Array
  • Merge Intervals
  • Product of Array Except Self

{Fore.CYAN}LINKED LISTS:{Style.RESET_ALL}
  • Reverse Linked List
  • Detect Cycle
  • Merge Two Sorted Lists
  • Add Two Numbers
  • Linked List Cycle II

{Fore.CYAN}STACK:{Style.RESET_ALL}
  • Valid Parentheses
  • Evaluate Reverse Polish Notation
  • Decode String
  • Daily Temperatures
  • Largest Rectangle in Histogram

{Fore.CYAN}DYNAMIC PROGRAMMING:{Style.RESET_ALL}
  • Climbing Stairs
  • House Robber
  • Longest Increasing Subsequence
  • Coin Change
  • Edit Distance
  • Partition Equal Subset Sum

{Fore.CYAN}GRAPHS:{Style.RESET_ALL}
  • Number of Islands
  • Clone Graph
  • Course Schedule
  • Word Ladder
  • Network Delay Time
""")
    
    def _show_practice(self):
        """Show practice recommendations"""
        print(f"""
{self.INFO_COLOR}🎯 Practice Recommendations:{Style.RESET_ALL}

{Fore.CYAN}BEGINNER:{Style.RESET_ALL}
  1. Two Sum (Easy)
  2. Valid Parentheses (Easy)
  3. Reverse Linked List (Easy)
  4. Maximum Subarray (Medium)

{Fore.CYAN}INTERMEDIATE:{Style.RESET_ALL}
  1. 3Sum (Medium)
  2. Merge Intervals (Medium)
  3. Clone Graph (Medium)
  4. Longest Increasing Subsequence (Medium)
  5. House Robber II (Medium)

{Fore.CYAN}ADVANCED:{Style.RESET_ALL}
  1. Merge K Sorted Lists (Hard)
  2. Word Ladder II (Hard)
  3. Edit Distance (Hard)
  4. Trapping Rain Water (Hard)

{Fore.CYAN}TIPS:{Style.RESET_ALL}
  • Start with Easy problems
  • Master arrays and linked lists first
  • Then move to trees and graphs
  • Finally tackle DP problems
  • Practice daily - consistency is key!
""")


class ColoredOutput:
    """Colored output utility"""
    
    @staticmethod
    def success(msg):
        return f"{Fore.GREEN}✓ {msg}{Style.RESET_ALL}"
    
    @staticmethod
    def error(msg):
        return f"{Fore.RED}✗ {msg}{Style.RESET_ALL}"
    
    @staticmethod
    def info(msg):
        return f"{Fore.CYAN}ℹ {msg}{Style.RESET_ALL}"
    
    @staticmethod
    def warning(msg):
        return f"{Fore.YELLOW}⚠ {msg}{Style.RESET_ALL}"


__all__ = ['ChatInterface', 'ColoredOutput']
