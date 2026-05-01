"""
DSA AI Agent - Visualizer
Visual diagrams for trees, graphs, arrays
"""

from typing import List, Dict, Optional, Tuple
import random


class TreeNode:
    """Binary tree node"""
    
    def __init__(self, val: int, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Visualizer:
    """Create visual representations of DSA concepts"""
    
    # ANSI colors
    RESET = "\033[0m"
    BOLD = "\033[1m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    PURPLE = "\033[95m"
    
    def __init__(self, use_colors: bool = True):
        self.use_colors = use_colors
        
    def _color(self, text: str, color: str) -> str:
        """Apply color to text"""
        if not self.use_colors:
            return text
        return f"{color}{text}{self.RESET}"
    
    def draw_array(self, arr: List, highlight: List[int] = None) -> str:
        """Draw array visualization"""
        if highlight is None:
            highlight = []
        
        result = "\n📊 Array Visualization:\n"
        result += "Index: "
        
        for i in range(len(arr)):
            idx_str = f"{i:<4}"
            result += self._color(idx_str, self.CYAN)
        
        result += "\n"
        result += "Value:"
        
        for i, val in enumerate(arr):
            if i in highlight:
                val_str = f"{self._color('▶', self.YELLOW)}{val}{self._color('◀', self.YELLOW)}"
            else:
                val_str = str(val)
            result += f" {val_str:<4}"
        
        result += "\n"
        result += f"{self._color('─' * 40, self.PURPLE)}\n"
        
        return result
    
    def draw_linked_list(self, values: List, cycle: bool = False) -> str:
        """Draw linked list"""
        result = "\n🔗 Linked List Visualization:\n"
        
        for i, val in enumerate(values):
            node = f"[{val}|→]"
            node = self._color(node, self.BLUE)
            result += node
            
            if i < len(values) - 1:
                result += "──▶"
            elif cycle:
                result += self._color("──▶", self.RED)
                result += " (cycle back to head)"
            else:
                result += self._color("──▶ NULL", self.RED)
        
        result += "\n"
        return result
    
    def draw_stack(self, items: List, max_display: int = 8) -> str:
        """Draw stack visualization"""
        result = "\n📚 Stack Visualization:\n"
        result += "┌───────┐\n"
        
        display_items = items[-max_display:] if len(items) > max_display else items
        
        for item in reversed(display_items):
            item_str = f"│ {item:<5} │"
            item_str = self._color(item_str, self.BLUE)
            result += item_str + "\n"
        
        if len(items) > max_display:
            result += self._color("│  ...  │\n", self.YELLOW)
        
        result += "└───────┘\n"
        result += self._color("  ↑TOP", self.GREEN)
        
        return result
    
    def draw_queue(self, items: List, max_display: int = 8) -> str:
        """Draw queue visualization"""
        result = "\n📮 Queue Visualization:\n"
        result += self._color("FRONT → ", self.GREEN)
        
        display_items = items[:max_display] if len(items) > max_display else items
        
        for i, item in enumerate(display_items):
            box = f"[{item}]"
            box = self._color(box, self.BLUE)
            result += box
            
            if i < len(display_items) - 1:
                result += "──"
        
        if len(items) > max_display:
            result += self._color(" ...", self.YELLOW)
        
        result += self._color(" ←REAR", self.RED)
        
        # Show extra in queue
        if len(items) > max_display:
            result += f"\n({len(items) - max_display} more items)"
        
        return result
    
    def draw_binary_tree(self, root: TreeNode) -> str:
        """Draw binary tree"""
        result = "\n🌳 Binary Tree Visualization:\n"
        
        if not root:
            return result + "(empty tree)\n"
        
        # Get all levels
        levels = []
        self._get_tree_levels(root, 0, levels)
        
        # Draw each level
        for level_idx, nodes in enumerate(levels):
            # Calculate spacing
            if level_idx == 0:
                spacing = ""
            else:
                num_spaces = 8 // (level_idx + 1)
                spacing = " " * num_spaces
            
            level_str = ""
            
            for i, val in enumerate(nodes):
                if val is not None:
                    node = self._color(f"[{val}]", self.BLUE)
                else:
                    node = " _ "
                
                if i < len(nodes) - 1:
                    level_str += node + spacing
                else:
                    level_str += node
            
            result += level_str + "\n"
            
            # Draw connectors for next level
            if level_idx < len(levels) - 1:
                next_level = levels[level_idx + 1]
                conn_str = ""
                for i in range(len(next_level)):
                    if next_level[i] is not None:
                        if i % 2 == 0:
                            conn_str += self._color("┌──", self.PURPLE)
                        else:
                            conn_str += self._color("┴──", self.PURPLE)
                    else:
                        conn_str += "    "
                result += conn_str + "\n"
        
        # Legend
        result += f"""
{self._color('─' * 30, self.PURPLE)}
Legend: Level order (top-to-bottom)
"""
        
        return result
    
    def _get_tree_levels(self, node: TreeNode, level: int, levels: List) -> None:
        """Get all levels of tree"""
        if level >= len(levels):
            levels.append([])
        
        if node is None:
            if level == 0:
                levels[level].append(None)
            return
        
        levels[level].append(node.val)
        
        self._get_tree_levels(node.left, level + 1, levels)
        self._get_tree_levels(node.right, level + 1, levels)
        
        # Fill empty spots
        if level < len(levels) - 1:
            while len(levels[level + 1]) < len(levels[level]) * 2:
                levels[level + 1].append(None)
    
    def draw_bst_operations(self, values: List[int], operation: str) -> str:
        """Draw BST operations step by step"""
        result = f"\n🌳 BST {operation.upper()} Operation:\n"
        result += self._color("═" * 40, self.PURPLE) + "\n"
        
        tree = None
        
        for i, val in enumerate(values):
            if operation.lower() == "insert":
                result += f"\nStep {i+1}: Insert {val}\n"
                tree = self._insert_bst(tree, val)
                result += self.draw_binary_tree(tree)
                
        return result
    
    def _insert_bst(self, node: TreeNode, val: int) -> TreeNode:
        """Insert into BST"""
        if node is None:
            return TreeNode(val)
        
        if val < node.val:
            node.left = self._insert_bst(node.left, val)
        else:
            node.right = self._insert_bst(node.right, val)
        
        return node
    
    def draw_graph(self, adj_list: Dict[int, List[int]]) -> str:
        """Draw graph (text-based)"""
        result = "\n🕸️ Graph Visualization:\n"
        result += self._color("═" * 30, self.PURPLE) + "\n"
        
        for node, neighbors in adj_list.items():
            neighbors_str = ", ".join(str(n) for n in neighbors)
            line = f"  {self._color(str(node), self.BLUE)} ──▶ [{neighbors_str}]"
            result += line + "\n"
        
        result += f"""
{self._color('─' * 30, self.PURPLE)}
Adjacency List Representation
"""
        
        return result
    
    def draw_bfs(self, adj_list: Dict[int, List[int]], start: int = 0) -> str:
        """Draw BFS traversal steps"""
        result = "\n🔍 BFS Traversal:\n"
        result += self._color("═" * 40, self.PURPLE) + "\n"
        
        visited = set()
        queue = [start]
        steps = []
        
        while queue:
            node = queue.pop(0)
            
            if node in visited:
                continue
            
            visited.add(node)
            steps.append(node)
            
            for neighbor in adj_list.get(node, []):
                if neighbor not in visited:
                    queue.append(neighbor)
        
        # Format steps
        for i, node in enumerate(steps):
            result += f"Step {i+1}: Visit {self._color(str(node), self.BLUE)}\n"
        
        result += f"\n{self._color('Order: ', self.CYAN)}{steps}\n"
        
        return result
    
    def draw_dfs(self, adj_list: Dict[int, List[int]], start: int = 0) -> str:
        """Draw DFS traversal steps"""
        result = "\n🔍 DFS Traversal:\n"
        result += self._color("═" * 40, self.PURPLE) + "\n"
        
        visited = set()
        stack = [start]
        steps = []
        
        while stack:
            node = stack.pop()
            
            if node in visited:
                continue
            
            visited.add(node)
            steps.append(node)
            
            for neighbor in adj_list.get(node, []):
                if neighbor not in visited:
                    stack.append(neighbor)
        
        # Format steps
        for i, node in enumerate(steps):
            result += f"Step {i+1}: Visit {self._color(str(node), self.BLUE)}\n"
        
        result += f"\n{self._color('Order: ', self.CYAN)}{steps}\n"
        
        return result
    
    def draw_sorting_animation(self, arr: List[int], name: str = "Bubble") -> str:
        """Show sorting animation frames"""
        result = f"\n📊 {name} Sort Animation:\n"
        result += self._color("═" * 40, self.PURPLE) + "\n"
        
        # Create copy for animation
        arr_copy = arr.copy()
        
        if name.lower() == "bubble":
            n = len(arr_copy)
            for i in range(n):
                for j in range(0, n - i - 1):
                    frame = f"Compare [{arr_copy[j]},{arr_copy[j+1]}]: "
                    frame += str(arr_copy)
                    frame = self._color(frame, self.CYAN)
                    result += frame + "\n"
                    
                    if arr_copy[j] > arr_copy[j + 1]:
                        arr_copy[j], arr_copy[j + 1] = arr_copy[j + 1], arr_copy[j]
                        result += self._color("  → Swap!\n", self.YELLOW)
        
        result += f"\n{self._color('Final: ', self.GREEN)}{arr_copy}\n"
        
        return result
    
    def draw_sliding_window(self, arr: List[int], k: int) -> str:
        """Draw sliding window technique"""
        result = f"\n🪟 Sliding Window (k={k}):\n"
        result += self._color("═" * 40, self.PURPLE) + "\n"
        
        n = len(arr)
        
        for i in range(n - k + 1):
            window = arr[i:i+k]
            window_str = self._color(str(window), self.BLUE)
            max_val = max(window)
            max_str = self._color(str(max_val), self.YELLOW)
            
            result += f"Window [{i}..{i+k-1}]: {window_str}\n"
            result += f"  Current max: {max_str}\n"
            result += "---\n"
        
        return result
    
    def draw_two_pointers(self, arr: List[int], target: int) -> str:
        """Draw two pointers technique"""
        target_str = self._color(str(target), self.YELLOW)
        result = f"\n👆 Two Pointers (target={target_str}):\n"
        result += self._color("═" * 40, self.PURPLE) + "\n"
        
        left = 0
        right = len(arr) - 1
        step = 0
        
        while left < right:
            step += 1
            
            current_sum = arr[left] + arr[right]
            left_val = self._color(str(arr[left]), self.BLUE)
            right_val = self._color(str(arr[right]), self.RED)
            
            result += f"\nStep {step}:\n"
            result += f"  Left={left_val}, Right={right_val}\n"
            result += f"  Sum: {current_sum}\n"
            
            if current_sum == target:
                result += self._color("  ✅ Found!\n", self.GREEN)
                break
            elif current_sum < target:
                result += f"  Sum too small → move left\n"
                left += 1
            else:
                result += f"  Sum too large → move right\n"
                right -= 1
        
        if left >= right:
            result += self._color("\n❌ No pair found\n", self.RED)
        
        return result
    
    def create_sample_tree(self) -> TreeNode:
        """Create a sample binary tree"""
        #        5
        #       / \
        #      3   8
        #     / \   \
        #    1   4   9
        
        root = TreeNode(5)
        root.left = TreeNode(3, TreeNode(1), TreeNode(4))
        root.right = TreeNode(8, None, TreeNode(9))
        
        return root
    
    def create_sample_graph(self) -> Dict[int, List[int]]:
        """Create sample graph"""
        return {
            0: [1, 2],
            1: [2, 3],
            2: [3],
            3: [4],
            4: [0]
        }


def demo():
    """Demo visualization"""
    v = Visualizer()
    
    # Array demo
    print(v.draw_array([1, 2, 3, 4, 5], highlight=[2]))
    
    # Stack demo
    print(v.draw_stack([1, 2, 3, 4]))
    
    # Queue demo
    print(v.draw_queue([1, 2, 3, 4, 5]))
    
    # Tree demo
    tree = v.create_sample_tree()
    print(v.draw_binary_tree(tree))
    
    # Graph demo
    graph = v.create_sample_graph()
    print(v.draw_graph(graph))
    print(v.draw_bfs(graph, 0))
    print(v.draw_dfs(graph, 0))
    
    # Sorting
    print(v.draw_sorting_animation([5, 2, 8, 1, 9], "Bubble"))
    
    # Sliding window
    print(v.draw_sliding_window([1, 2, 3, 4, 5, 6, 7], 3))


__all__ = ['Visualizer', 'TreeNode']
