# 🎓 DSA AI Tutor Agent

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/OpenAI-gpt--3.5-turbo-green?style=for-the-badge" alt="OpenAI">
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
</p>

Your personal **AI-powered DSA (Data Structures and Algorithms) coach** that adapts to your learning style. Built for students preparing for FAANG interviews!

## ✨ Features

- **🤖 AI-Powered Learning** - Smart responses using OpenAI GPT integration
- **📚 Comprehensive DSA Topics** - Arrays, Linked Lists, Trees, Graphs, DP, and more
- **💻 Code Execution** - Run and test your Python solutions
- **🔍 Code Review** - Get AI-powered feedback on your code
- **📝 Quiz System** - Test your knowledge with topic-based quizzes
- **🎯 Progress Tracking** - Track your weak areas and improvement
- **🔐 Debug Mode** - Step-by-step code debugging
- **📊 Visualization** - Visual representations of data structures

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/dsa-ai-tutor.git
cd dsa-ai-tutor

# Install dependencies
pip install -r requirements.txt

# Run the agent
python main.py
```

### With OpenAI API (Optional)

```bash
export OPENAI_API_KEY=your_api_key
python main.py
```

## 📖 Usage

```
You: help
Agent: Available Commands:

TALK ABOUT:
  Type any topic (array, linked list, stack, queue, tree, graph, sorting, dp, heap, trie...)

SPECIAL COMMANDS:
  topics    - List all topics
  progress - Your progress
  review   <code> - Code review
  quiz     - Start a quiz
  run      <code> - Execute code
  visualize - Draw visualization
  practice - Practice problems
  interview - Interview prep
  debug    <code> - Debug code
  exit     - Quit
```

## 🏗️ Architecture

```
dsa-ai-tutor/
├── agent/
│   ├── core.py           # Main agent
│   ├── dsa/
│   │   ├── problems.py   # DSA problems
│   │   └── explainer.py # Topic explanations
│   ├── services/        # Separated services
│   │   ├── ai_service.py
│   │   ├── execution_service.py
│   │   └── user_service.py
│   ├── quiz.py          # Quiz system
│   ├── executor.py     # Code execution
│   ├── memory.py      # Progress tracking
│   ├── visualizer.py # Data structure visualization
│   └── debug.py      # Debug mode
├── main.py
├── app.py             # Streamlit app
├── requirements.txt
└── README.md
```

## 🎯 Topics Covered

### Core Topics
| Topic | Description |
|-------|-------------|
| Arrays/Lists | Contiguous memory, O(1) access |
| Linked Lists | Node-based, O(n) traversal |
| Stack | LIFO, DFS, expression eval |
| Queue | FIFO, BFS, scheduling |
| Trees | BST, AVL, traversals |
| Graphs | BFS/DFS, Dijkstra |
| Sorting | Quick, Merge, Heap sort |
| DP | Memoization, Tabulation |

### Advanced Topics
| Topic | Description |
|-------|-------------|
| Heap | Priority Queue, top-k problems |
| Trie | Prefix Tree, autocomplete |
| Hash Table | O(1) lookups, dictionaries |
| Recursion | Base case, tree recursion |
| Sliding Window | Two pointers, subarrays |
| Two Pointers | Pair finding, sorting |

## 📊 Time Complexity Cheatsheet

```
┌─────────────┬──────────────┬─────────────┐
│ Data Structure│   Access   │  Search   │
├─────────────┼──────────────┼─────────────┤
│ Array       │    O(1)     │   O(n)     │
│ Linked List│    O(n)     │   O(n)     │
│ Hash Table │    O(1)     │   O(1)     │
│ BST        │ O(log n)    │  O(log n)  │
│ Heap      │ O(log n)    │   O(1)     │
└─────────────┴──────────────┴─────────────┘

┌─────────────┬──────────────┬─────────────┐
│  Algorithm  │  Best Case  │ Worst Case │
├─────────────┼──────────────┼─────────────┤
│ Quick Sort │ O(n log n)  │   O(n²)    │
│ Merge Sort │ O(n log n)  │ O(n log n)  │
│ BFS/DFS    │   O(V+E)    │   O(V+E)   │
│ Dijkstra   │ O(E log V)  │ O(E log V) │
└─────────────┴──────────────┴─────────────┘
```

## 🎬 Demo

Run the agent and try these commands:

```
You: array
Agent: 📚 Array/List Basics: ...

You: quiz dp
Agent: 🎯 DP Quiz (5 questions) ...

You: run print([1,2,3])
Agent: ✅ Output: [1, 2, 3]
```

## 🔧 Tech Stack

- **Language**: Python 3.8+
- **AI**: OpenAI GPT-3.5 Turbo
- **UI**: Streamlit (optional)
- **Storage**: JSON files

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

---

<p align="center">Made with ❤️ for FAANG aspirants</p>
