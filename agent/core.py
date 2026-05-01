"""
DSA AI Agent - Core Module v2
Complete agent with all enhancements
"""

import os
from datetime import datetime
from .dsa.problems import DSAProblems
from .dsa.explainer import DSAExplainer
from .ai_integration import AIIntegration
from .code_review import CodeReviewer
from .memory import UserSession, ProgressTracker
from .quiz import QuizManager
from .executor import CodeExecutor, TestRunner, TestCase
from .visualizer import Visualizer
from .debug import CodeDebugger, DebugCommandHandler


class DSAAgent:
    """
    Complete DSA AI Agent with all features:
    - DSA knowledge base
    - Additional topics (Heap, Trie, etc.)
    - AI integration (OpenAI)
    - Code review
    - Progress tracking
    - Quiz system
    - Code execution
    - Visualization
    - Debug mode
    """

    def __init__(self, api_key: str = ""):
        self.model = "gpt-3.5-turbo"
        self.conversation_history = []

        # Initialize all modules
        self.dsa_problems = DSAProblems()
        self.explainer = DSAExplainer()
        self.ai = AIIntegration(api_key)
        self.reviewer = CodeReviewer()
        self.session = UserSession()
        self.tracker = ProgressTracker()
        
        # Phase 5 modules
        self.quiz_manager = QuizManager()
        self.executor = CodeExecutor()
        self.test_runner = TestRunner()
        self.visualizer = Visualizer()
        
        # Debug mode (NEW)
        self.debugger = CodeDebugger()
        self.debug_handler = DebugCommandHandler(self.debugger)
        self.debug_active = False
        
        # Quiz state
        self.quiz_active = False

        print("""
╔═══════════════════════════════════════════╗
║     🎓 DSA AI Tutor Agent v2.0            ║
║     Full Features Enabled!               ║
╚═══════════════════════════════════════════╝
""")

    def chat(self, user_message: str) -> str:
        """Process user message"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })

        response = self._process_message(user_message)

        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })

        return response

    def _process_message(self, message: str) -> str:
        """Process message and route to appropriate handler"""
        msg = message.lower().strip()

        # Check commands
        if msg in ['exit', 'quit', 'bye']:
            return self._get_exit_message()

        if msg == 'help':
            return self._get_help()

        if msg == 'progress' or msg == 'stats':
            return self._get_progress()

        if msg.startswith('review ') or msg.startswith('code '):
            code = message[message.find(' ')+1:]
            return self.review_code(code)

        if msg == 'topics':
            return self._list_topics()

        # Quiz commands
        if msg.startswith('quiz'):
            return self._handle_quiz(message)
        
        # Code execution
        if msg.startswith('run ') or msg.startswith('execute '):
            return self._handle_execute(message)
        
        # Visualize commands
        if msg.startswith('visualize ') or msg.startswith('draw '):
            return self._handle_visualize(message)
        
        # Practice problems
        if msg == 'practice' or msg == 'problems':
            return self._get_practice_problems()
        
        # Interview prep
        if 'interview' in msg:
            return self._handle_interview(message)

        # Debug mode
        if msg.startswith('debug '):
            return self._handle_debug(message)

        # If debug is active, pass commands to debug handler
        if self.debug_active:
            return self.debug_handler.handle(message)

        # Topic routing
        return self._route_topic(msg)

    def _route_topic(self, msg: str) -> str:
        """Route to appropriate topic handler"""

        # Core topics
        if 'complexity' in msg or 'big o' in msg:
            return self._get_complexity()

        if 'array' in msg or 'list' in msg:
            return self._explain_array()

        if 'linked list' in msg:
            return self._explain_linked_list()

        if 'stack' in msg:
            return self._explain_stack()

        if 'queue' in msg:
            return self._explain_queue()

        if 'tree' in msg or 'bst' in msg:
            return self._explain_tree()

        if 'sort' in msg:
            return self._explain_sorting()

        if 'graph' in msg:
            return self._explain_graph()

        if 'dp' in msg or 'dynamic' in msg:
            return self._explain_dp()

        # New topics
        if 'heap' in msg or 'priority' in msg:
            return self.explainer.explain_heap()

        if 'trie' in msg or 'prefix' in msg:
            return self.explainer.explain_trie()

        if 'hash' in msg or 'dictionary' in msg:
            return self.explainer.explain_hash_table()

        if 'recursion' in msg or 'recursive' in msg:
            return self.explainer.explain_recursion()

        if 'sliding window' in msg:
            return self.explainer.explain_sliding_window()

        if 'two pointer' in msg or 'two pointer' in msg:
            return self.explainer.explain_two_pointers()

        return self._default_response(msg)

    def _get_complexity(self) -> str:
        return """📊 Time Complexity Cheatsheet:

┌─────────────┬──────────────┬─────────────┐
│ Data Structure│   Access   │  Search   │
├─────────────┼──────────────┼─────────────┤
│ Array       │    O(1)     │   O(n)     │
│ Linked List│    O(n)     │   O(n)     │
│ Hash Table │    O(1)     │   O(1)     │
│ BST        │ O(log n)    │  O(log n)  │
│ Heap      │ O(log n)    │   O(1)     │
│ Trie      │   O(m)      │   O(m)     │
└─────────────┴──────────────┴─────────────┘

┌─────────────┬──────────────┬─────────────┐
│  Algorithm  │  Best Case  │ Worst Case │
├─────────────┼──────────────┼─────────────┤
│ Quick Sort │ O(n log n)  │   O(n²)    │
│ Merge Sort │ O(n log n)  │ O(n log n)  │
│ BFS/DFS    │   O(V+E)    │   O(V+E)   │
│ Dijkstra   │ O(E log V)  │ O(E log V) │
└─────────────┴──────────────┴─────────────┘

💡 Pro Tips:
• O(1) = Constant • O(log n) = Logarithmic
• O(n) = Linear • O(n log n) = Linearithmic"""

    def _explain_array(self) -> str:
        return """📚 Array/List Basics:

WHAT: Contiguous memory storage

OPERATIONS:
• Access: O(1) • Search: O(n)
• Insert: O(n) • Delete: O(n)

PYTHON:
```python
arr = [1, 2, 3, 4, 5]
arr.append(6)
arr.pop()
```

PROBLEMS: Two Sum, Max Subarray, Merge Intervals"""

    def _explain_linked_list(self) -> str:
        return """🔗 Linked List:

TYPES: Singly, Doubly, Circular

OPERATIONS:
• Access: O(n) • Insert: O(1)
• Delete: O(1) • Search: O(n)

PYTHON:
```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
```

PROBLEMS: Reverse, Detect Cycle, Merge"""

    def _explain_stack(self) -> str:
        return """📚 Stack (LIFO):

OPERATIONS:
• push: O(1) • pop: O(1)
• peek: O(1)

USE: DFS, undo/redo, expression eval

PROBLEMS: Valid Parentheses, Decode String"""

    def _explain_queue(self) -> str:
        return """📚 Queue (FIFO):

OPERATIONS:
• enqueue: O(1) • dequeue: O(1)

USE: BFS, scheduling

PROBLEMS: Number of Islands (BFS)"""

    def _explain_tree(self) -> str:
        return """🌳 Tree & BST:

TYPES: Binary Tree, BST, AVL, Trie

OPERATIONS (BST):
• Search: O(log n)
• Insert: O(log n)
• Delete: O(log n)

TRAVERSALS: Inorder, Preorder, Postorder, Level"""

    def _explain_sorting(self) -> str:
        return """📊 Sorting Algorithms:

┌────────────┬──────────┬──────────┐
│ Algorithm  │  Best    │  Worst   │
├────────────┼──────────┼──────────┤
│ Quick     │O(n log n)│  O(n²)   │
│ Merge    │O(n log n)│O(n log n)│
│ Heap     │O(n log n)│O(n log n)│
│ Insertion │   O(n)   │  O(n²)   │
└────────────┴──────────┴──────────┘

BEST: Quick/Merge Sort (general)"""

    def _explain_graph(self) -> str:
        return """🕸️ Graph Basics:

REPRESENTATIONS:
• Adjacency Matrix: O(1) edge check
• Adjacency List: O(V+E) space

TRAVERSALS:
• BFS: Shortest path (unweighted)
• DFS: Path finding, cycles

ALGORITHMS:
• Dijkstra, Bellman-Ford, Floyd"""

    def _explain_dp(self) -> str:
        return """⚡ Dynamic Programming:

WHEN:
• Optimal Substructure
• Overlapping Subproblems

APPROACHES:
1. Top-Down: Recursion + Memoization
2. Bottom-Up: Tabulation

PROBLEMS:
• Climbing Stairs
• House Robber
• Longest Increasing Subsequence
• Coin Change"""

    def _list_topics(self) -> str:
        return """📚 Available Topics:

CORE TOPICS:
• complexity - Time complexity
• array - Arrays & Lists
• linked list - Linked Lists
• stack - Stack
• queue - Queue
• tree - Trees & BST
• graph - Graphs
• sorting - Sorting
• dp - Dynamic Programming

NEW (v2):
• heap - Heap / Priority Queue
• trie - Trie / Prefix Tree
• hash - Hash Table
• recursion - Recursion
• sliding window - Sliding Window
• two pointers - Two Pointers"""

    def _get_help(self) -> str:
        return """📚 Available Commands:

TALK ABOUT:
Type any topic above!

SPECIAL COMMANDS:
• topics - List all topics
• progress - Your progress
• review <code> - Code review
• quiz - Start a quiz
• run <code> - Execute code
• visualize <type> - Draw visualization
• practice - Practice problems
• interview - Interview prep
• debug <code> - Debug code
• exit - Quit

ENHANCED (v2):
✅ All new topics added
✅ Code review feature  
✅ Quiz system
✅ Code execution
✅ Visualization
✅ Progress tracking
✅ Debug mode
��� AI integration ready"""

    def _get_progress(self) -> str:
        stats = self.session.get_stats()
        return f"""📊 Your Progress:

Topics Explored: {stats['topics_covered']}
Problems Attempted: {stats['problems_attempted']}
Conversations: {stats['conversation_count']}

Keep learning! 🎯"""

    def _get_exit_message(self) -> str:
        stats = self.session.get_stats()
        return f"""👋 Goodbye!

📊 Session Summary:
Topics explored: {stats['topics_covered']}
Problems: {stats['problems_attempted']}

Happy Coding! 🚀"""

    def _default_response(self, message: str) -> str:
        return f"""I understand you're asking about: "{message}"

Try these topics:
• array, linked list, stack, queue
• tree, graph, sorting, dp
• heap, trie, hash, recursion
• sliding window, two pointers
• complexity

Or type 'help' for more options!"""

    def review_code(self, code: str) -> str:
        """Review user code"""
        result = self.reviewer.analyze_code(code)
        return f"""🔍 Code Review:

Issues: {', '.join(result['issues']) if result['issues'] else 'None'}
Complexity: {result['complexity']}
Suggestions: {', '.join(result['suggestions']) if result['suggestions'] else 'Good!'}"""

    # Phase 5 handlers
    def _handle_quiz(self, message: str) -> str:
        """Handle quiz commands"""
        parts = message.split()
        if len(parts) == 1:
            return self.quiz_manager.start("random", 5)
        
        topic = parts[1] if len(parts) > 1 else "random"
        return self.quiz_manager.start(topic, 5)

    def _handle_execute(self, message: str) -> str:
        """Execute Python code"""
        code = message[message.find(' ')+1:] if ' ' in message else ""
        if not code:
            return "Please provide code to run. Usage: run <code>"
        
        result = self.executor.execute(code)
        if result.success:
            return f"✅ Output:\n{result.output}"
        else:
            return f"❌ Error: {result.error}"

    def _handle_visualize(self, message: str) -> str:
        """Handle visualization commands"""
        msg = message.lower()
        
        if 'array' in msg:
            return self.visualizer.draw_array([1, 2, 3, 4, 5])
        elif 'tree' in msg:
            tree = self.visualizer.create_sample_tree()
            return self.visualizer.draw_binary_tree(tree)
        elif 'graph' in msg:
            graph = self.visualizer.create_sample_graph()
            return self.visualizer.draw_graph(graph)
        elif 'stack' in msg:
            return self.visualizer.draw_stack([1, 2, 3])
        elif 'queue' in msg:
            return self.visualizer.draw_queue([1, 2, 3])
        else:
            return "Try: visualize array, tree, graph, stack, or queue"

    def _get_practice_problems(self) -> str:
        """Get practice problems"""
        return """📝 Practice Problems:

EASY:
• Two Sum
• Valid Parentheses
• Reverse Linked List
• Merge Two Sorted Lists

MEDIUM:
• 3Sum
• Largest Rectangle in Histogram
• Binary Tree Level Order
• Clone Graph

HARD:
• Merge K Sorted Lists
• Word Search II
• Shortest Path in Grid with Obstacles

Type 'explain <problem>' for approach!"""

    def _handle_interview(self, message: str) -> str:
        """Handle interview prep"""
        return """🎯 Interview Prep:

FAANG Problems:

arrays:
• 15. 3Sum (Medium)
• 11. Container With Most Water (Medium)

strings:
• 49. Group Anagrams (Medium)
• 76. Minimum Window Substring (Hard)

trees:
• 102. Binary Tree Level Order (Medium)
• 297. Serialize/Deserialize (Hard)

DP:
• 322. Coin Change (Medium)
• 10. Regular Expression (Hard)

Practice with: 'quiz' or 'explain <problem>'"""

    def _handle_debug(self, message: str) -> str:
        """Handle debug mode"""
        parts = message.split(' ', 1)
        
        if len(parts) == 1:
            return """🔍 Debug Mode Commands:

• debug <code> - Start debugging
• step / n - Next line
• run - Run to end
• vars - Show variables
• quit - Exit debug

Example: debug x = 5\\nprint(x)"""
        
        code = parts[1]
        
        # Start new debug session
        self.debugger = CodeDebugger()
        self.debug_handler = DebugCommandHandler(self.debugger)
        self.debug_active = True
        
        return self.debugger.start_debug(code)


__all__ = ['DSAAgent']
