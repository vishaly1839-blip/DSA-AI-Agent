"""
DSA AI Agent - DSA Module
Contains DSA problems, explanations, and code solutions
"""

from typing import Dict, List, Optional


class DSAProblem:
    """Represents a DSA problem"""
    
    def __init__(self, name: str, difficulty: str, topic: str):
        self.name = name
        self.difficulty = difficulty
        self.topic = topic
        self.solutions = {}
        self.hints = []
        self.explanation = ""
    
    def add_solution(self, language: str, code: str, complexity: str):
        """Add a solution in a specific language"""
        self.solutions[language] = {
            "code": code,
            "complexity": complexity
        }
    
    def add_hint(self, hint: str):
        """Add a hint"""
        self.hints.append(hint)


class DSAProblems:
    """Database of DSA problems"""
    
    def __init__(self):
        self.problems = self._init_problems()
    
    def _init_problems(self) -> Dict[str, DSAProblem]:
        """Initialize problem database"""
        problems = {}
        
        # Two Sum
        p = DSAProblem("Two Sum", "Easy", "Array")
        p.explanation = """Two Sum Problem:
        
GOAL: Find two numbers in array that add up to target.

APPROACH 1 (Brute Force):
- Check all pairs
- Time: O(n²), Space: O(1)

APPROACH 2 (Hash Map):
- Store Complement = target - num
- Check if complement exists
- Time: O(n), Space: O(n)"""
        p.add_solution("python", """def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

# Example
nums = [2, 7, 11, 15]
target = 9
print(two_sum(nums, target))  # Output: [0, 1]""", "Time: O(n), Space: O(n)")
        p.add_solution("cpp", """vector<int> twoSum(vector<int>& nums, int target) {
    unordered_map<int, int> mp;
    for(int i = 0; i < nums.size(); i++) {
        int complement = target - nums[i];
        if(mp.count(complement))
            return {mp[complement], i};
        mp[nums[i]] = i;
    }
    return {};
}""", "Time: O(n), Space: O(n)")
        p.hints = [
            "Think: What number do we need to find?",
            "Use a hash map to store seen numbers",
            "For each number, check if target - number exists"
        ]
        problems["two sum"] = p
        
        # Reverse Linked List
        p = DSAProblem("Reverse Linked List", "Easy", "Linked List")
        p.explanation = """Reverse Linked List:

ITERATIVE APPROACH:
1. Initialize prev = None, curr = head
2. While curr exists:
   - Save next = curr.next
   - Reverse: curr.next = prev
   - Move: prev = curr, curr = next
3. Return prev

Time: O(n), Space: O(1)"""
        p.add_solution("python", """class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverse_list(head):
    prev = None
    curr = head
    
    while curr:
        next_temp = curr.next
        curr.next = prev
        prev = curr
        curr = next_temp
    
    return prev

# Create list: 1 -> 2 -> 3 -> None
head = ListNode(1, ListNode(2, ListNode(3)))
new_head = reverse_list(head)
# Now: 3 -> 2 -> 1 -> None""", "Time: O(n), Space: O(1)")
        p.hints = [
            "Use three pointers: prev, curr, next",
            "Always save next before changing curr.next",
            "Think of it as reversing direction step by step"
        ]
        problems["reverse linked list"] = p
        
        # Valid Parentheses
        p = DSAProblem("Valid Parentheses", "Easy", "Stack")
        p.explanation = """Valid Parentheses:

RULE: Each opening bracket must have matching closing bracket.

ALGORITHM:
1. Use a stack
2. For each character:
   - If opening bracket: push to stack
   - If closing bracket: check stack top matches
3. At end, stack should be empty

EDGE CASES:
- Empty string → valid
- Single closing bracket → invalid
- Unmatched opening → invalid at end"""
        p.add_solution("python", """def is_valid(s):
    stack = []
    mapping = {')': '(', ']': '[', '}': '{'}
    
    for char in s:
        if char in mapping:
            # Closing bracket
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            # Opening bracket
            stack.append(char)
    
    return len(stack) == 0

# Examples
print(is_valid("()"))      # True
print(is_valid("()[]{}"))  # True
print(is_valid("(]"))      # False""", "Time: O(n), Space: O(n)")
        p.add_solution("cpp", """bool isValid(string s) {
    stack<char> st;
    unordered_map<char, char> mp = {
        {')', '('}, {']', '['}, {'}', '{'}
    };
    
    for(char c : s) {
        if(mp.count(c)) {
            if(st.empty() || st.top() != mp[c])
                return false;
            st.pop();
        } else {
            st.push(c);
        }
    }
    return st.empty();
}""", "Time: O(n), Space: O(n)")
        p.hints = [
            "Use a stack to track opening brackets",
            "Closing brackets must match most recent opening",
            "Stack should be empty at the end"
        ]
        problems["valid parentheses"] = p
        
        # Maximum Subarray (Kadane's Algorithm)
        p = DSAProblem("Maximum Subarray", "Medium", "DP/Array")
        p.explanation = """Maximum Subarray (Kadane's Algorithm):

PROBLEM: Find contiguous subarray with largest sum.

KADANE'S ALGORITHM:
- At each position, decide: start new subarray or extend?
- max_ending_here = max(nums[i], max_ending_here + nums[i])
- max_so_far = max(max_so_far, max_ending_here)

KEY INSIGHT:
- If current sum becomes negative, restart"""
        p.add_solution("python", """def max_subarray(nums):
    max_sum = nums[0]
    current_sum = nums[0]
    
    for i in range(1, len(nums)):
        # Either extend previous or start new
        current_sum = max(nums[i], current_sum + nums[i])
        max_sum = max(max_sum, current_sum)
    
    return max_sum

# Example
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
print(max_subarray(nums))  # Output: 6
# Subarray: [4, -1, 2, 1]""", "Time: O(n), Space: O(1)")
        p.hints = [
            "Think: Should we include current element?",
            "If sum becomes negative, start fresh",
            "Track maximum sum seen so far"
        ]
        problems["max subarray"] = p
        
        # Climbing Stairs
        p = DSAProblem("Climbing Stairs", "Easy", "DP")
        p.explanation = """Climbing Stairs:

PROBLEM: Reach nth stair. Can take 1 or 2 steps at a time.

RECURRENCE:
- ways(n) = ways(n-1) + ways(n-2)
- Base cases: ways(1)=1, ways(2)=2

This is Fibonacci!

APPROACHES:
1. Recursion (memoization) - O(n) space
2. Iterative - O(1) space
3. Formula"""
        p.add_solution("python", """def climb_stairs(n):
    if n <= 2:
        return n
    
    prev1, prev2 = 2, 1
    
    for _ in range(3, n + 1):
        current = prev1 + prev2
        prev2 = prev1
        prev1 = current
    
    return prev1

# Examples
print(climb_stairs(2))  # 2 (1+1, 2)
print(climb_stairs(3))  # 3 (1+1+1, 1+2, 2+1)
print(climb_stairs(4))  # 5""", "Time: O(n), Space: O(1)")
        p.hints = [
            "How many ways to reach step 1? 1",
            "How many ways to reach step 2? 2",
            "For step n: ways(n-1) + ways(n-2)"
        ]
        problems["climbing stairs"] = p
        
        # Merge Intervals
        p = DSAProblem("Merge Intervals", "Medium", "Array")
        p.explanation = """Merge Intervals:

PROBLEM: Merge overlapping intervals.

ALGORITHM:
1. Sort intervals by start time
2. Merge first interval with result
3. For each interval:
   - If overlaps with last: merge
   - Else: add new interval

COMPLEXITY: O(n log n) for sorting"""
        p.add_solution("python", """def merge(intervals):
    if not intervals:
        return []
    
    # Sort by start time
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    
    for start, end in intervals[1:]:
        # Check if overlaps with last interval
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    
    return merged

# Example
intervals = [[1,3],[2,6],[8,10],[15,18]]
print(merge(intervals))
# Output: [[1,6],[8,10],[15,18]]""", "Time: O(n log n), Space: O(1)")
        p.hints = [
            "Sort intervals first",
            "Check if current overlaps with previous",
            "Merge by taking max of end times"
        ]
        problems["merge intervals"] = p
        
        # Binary Search
        p = DSAProblem("Binary Search", "Easy", "Searching")
        p.explanation = """Binary Search:

PROBLEM: Find target in sorted array.

APPROACH:
1. Set left = 0, right = n-1
2. While left <= right:
   - mid = (left + right) // 2
   - If arr[mid] == target: return mid
   - If target < arr[mid]: right = mid - 1
   - Else: left = min + 1

KEY: Use <= in condition"""
        p.add_solution("python", """def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1  # Not found

# Example
arr = [1, 3, 5, 7, 9, 11, 13, 15]
print(binary_search(arr, 7))   # 3
print(binary_search(arr, 6))   # -1""", "Time: O(log n), Space: O(1)")
        p.hints = [
            "Array must be sorted",
            "Use left <= right in while condition",
            "Update boundaries to exclude searched area"
        ]
        problems["binary search"] = p
        
        # Quick Sort
        p = DSAProblem("Quick Sort", "Medium", "Sorting")
        p.explanation = """Quick Sort:

DIVIDE AND CONQUER:
1. Choose pivot element
2. Partition: elements < pivot left, > pivot right
3. Recursively sort subarrays

AVERAGE: O(n log n)
WORST: O(n²) (already sorted)"""
        p.add_solution("python", """def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)

# Example
arr = [3, 6, 8, 10, 1, 2, 1]
print(quick_sort(arr))
# Output: [1, 1, 2, 3, 6, 8, 10]""", "Time: O(n log n) avg, Space: O(n)")
        p.hints = [
            "Choose a pivot element",
            "Partition around the pivot",
            "Recursively sort left and right"
        ]
        problems["quick sort"] = p
        
        # BFS
        p = DSAProblem("BFS", "Medium", "Graph")
        p.explanation = """Breadth-First Search:

LEVEL-ORDER TRAVERSAL:
1. Use queue
2. Enqueue starting node
3. While queue not empty:
   - Dequeue, process
   - Enqueue all unvisited neighbors

USES:
- Shortest path (unweighted)
- Level order traversal"""
        p.add_solution("python", """from collections import deque

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return result

# Example graph (adjacency list)
graph = {
    'A': ['B', 'C'],
    'B': ['A', 'D', 'E'],
    'C': ['A', 'F'],
    'D': ['B'],
    'E': ['B', 'F'],
    'F': ['C', 'E']
}

print(bfs(graph, 'A'))
# Output: ['A', 'B', 'C', 'D', 'E', 'F']""", "Time: O(V+E), Space: O(V)")
        p.hints = [
            "Use a queue for BFS",
            "Mark visited to avoid cycles",
            "Process all neighbors at current level"
        ]
        problems["bfs"] = p
        
        return problems
    
    def get_problem(self, name: str) -> Optional[DSAProblem]:
        """Get problem by name"""
        name_lower = name.lower()
        for key, problem in self.problems.items():
            if name_lower in key or key in name_lower:
                return problem
        return None
    
    def list_by_topic(self, topic: str) -> List[DSAProblem]:
        """List problems by topic"""
        return [p for p in self.problems.values() 
                if p.topic.lower() == topic.lower()]


__all__ = ['DSAProblems', 'DSAProblem']
