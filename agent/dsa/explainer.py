"""
DSA AI Agent - Additional Topics Explainer
Heap, Trie, Recursion, Sliding Window, Hash Table
"""

class DSAExplainer:
    """Additional DSA topic explanations"""

    @staticmethod
    def explain_heap() -> str:
        return """📚 Heap / Priority Queue:

WHAT IS A HEAP?
A binary tree that satisfies the heap property:
- Max Heap: Parent >= Children
- Min Heap: Parent <= Children

COMPLEXITY:
• Insert: O(log n)
• Delete Max/Min: O(log n)
• Get Max/Min: O(1)

PYTHON (min-heap):
```python
import heapq

# Create min-heap
heap = []
heapq.heappush(heap, 5)
heapq.heappush(heap, 3)
heapq.heappush(heap, 7)

heapq.heappop(heap)  # Returns 3 (min)
```

USE CASES:
• Priority Queue
• Top K elements
• Median finder
• Dijkstra's algorithm

🎯 PROBLEMS:
1. Kth Largest Element
2. Top K Frequent Elements
3. Median of Data Stream
4. Merge K Sorted Lists"""

    @staticmethod
    def explain_hash_table() -> str:
        return """📚 Hash Table:

WHAT IS A HASH TABLE?
Key-value store using hash function.
Maps keys to array indices.

COMPLEXITY (Average):
• Insert: O(1)
• Delete: O(1)
• Search: O(1)

COMPLEXITY (Worst):
• Insert: O(n)
• Delete: O(n)
• Search: O(n)

HASH COLLISIONS:
1. Chaining (linked list at each bucket)
2. Open Addressing (linear/quadratic probing)

PYTHON:
```python
# Dictionary
d = {}
d['key'] = 'value'
print(d['key'])  # 'value'

# Set
s = {1, 2, 3}
s.add(4)
```

🎯 PROBLEMS:
1. Two Sum
2. Valid Anagram
3. First Unique Character
4. Subarray Sum Equals K"""

    @staticmethod
    def explain_trie() -> str:
        return """📚 Trie (Prefix Tree):

WHAT IS A TRIE?
Tree where each node represents a character.
Used for string operations.

COMPLEXITY:
• Insert: O(m) where m = word length
• Search: O(m)
• Prefix search: O(m)

PYTHON:
```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end
```

USE CASES:
• Auto-complete
• Spell checker
• IP routing
• Dictionary

🎯 PROBLEMS:
1. Implement Trie
2. Word Search
3. Prefix Tree"""

    @staticmethod
    def explain_recursion() -> str:
        return """📚 Recursion:

WHAT IS RECURSION?
Function that calls itself to solve smaller subproblems.

KEY COMPONENTS:
1. Base Case - Stop condition
2. Recursive Case - Call itself

PATTERNS:
• Linear Recursion
• Binary Recursion  
• Tail Recursion
• Tree Recursion

EXAMPLE - Factorial:
```python
def factorial(n):
    # Base Case
    if n <= 1:
        return 1
    # Recursive Case
    return n * factorial(n - 1)

print(factorial(5))  # 120
```

EXAMPLE - Fibonacci:
```python
def fib(n):
    if n <= 1:
        return n
    return fib(n-1) + fib(n-2)
```

WARNING: Exponential time without memoization!

MEMOIZATION:
```python
def fibMemo(n, memo={}):
    if n in memo:
        return memo[n]
    if n <= 1:
        return n
    memo[n] = fibMemo(n-1, memo) + fibMemo(n-2, memo)
    return memo[n]
```

🎯 PROBLEMS:
1. Fibonacci Number
2. Reverse String
3. Power
4. Permutations"""

    @staticmethod
    def explain_sliding_window() -> str:
        return """📚 Sliding Window:

WHAT IS IT?
Technique to process subarrays in O(n)
Two pointers: left, right

TYPES:
1. Fixed Window Size
2. Dynamic Window Size

FIXED WINDOW:
```python
def fixed_window(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i-k]
        max_sum = max(max_sum, window_sum)
    
    return max_sum
```

DYNAMIC WINDOW:
```python
def dynamic_window(arr, target):
    left = 0
    current_sum = 0
    
    for right in range(len(arr)):
        current_sum += arr[right]
        
        while current_sum > target:
            current_sum -= arr[left]
            left += 1
        
        if current_sum == target:
            return [left, right]
    
    return [-1, -1]
```

🎯 PROBLEMS:
1. Maximum Sum Subarray
2. minimum Size Subarray Sum
3. Longest Substring Without Repeating
4. Fruit Into Baskets"""

    @staticmethod
    def explain_two_pointers() -> str:
        return """📚 Two Pointers:

WHAT IS IT?
Two pointers moving in same/different directions.

TYPES:
1. Opposite Direction (start, end)
2. Same Direction (fast, slow)

TWO SUM (Sorted):
```python
def two_sum(arr, target):
    left, right = 0, len(arr) - 1
    
    while left < right:
        current = arr[left] + arr[right]
        if current == target:
            return [left, right]
        elif current < target:
            left += 1
        else:
            right -= 1
```

LINKED LIST CYCLE:
```python
def hasCycle(head):
    slow = fast = head
    
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        
        if slow == fast:
            return True
    
    return False
```

REMOVE DUPLICATES:
```python
def remove_duplicates(arr):
    if not arr:
        return 0
    
    left = 1
    for right in range(1, len(arr)):
        if arr[right] != arr[right-1]:
            arr[left] = arr[right]
            left += 1
    
    return left
```

🎯 PROBLEMS:
1. Valid Palindrome
2. 3Sum
3. Container With Most Water
4. Remove Duplicates"""


__all__ = ['DSAExplainer']
