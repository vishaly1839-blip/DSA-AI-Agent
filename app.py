"""
DSA AI Tutor Agent - Streamlit Web UI
Run: streamlit run app.py
"""

import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta
from agent.core import DSAAgent
from agent.code_review import CodeReviewer


def init_session():
    """Initialize session state"""
    if 'agent' not in st.session_state:
        st.session_state.agent = DSAAgent()
    if 'reviewer' not in st.session_state:
        st.session_state.reviewer = CodeReviewer()
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'progress' not in st.session_state:
        st.session_state.progress = {
            'topics': [],
            'problems_solved': 0,
            'quizzes_taken': 0,
            'streak': 0,
            'badges': [],
            'reviews': {},
            'ratings': {}
        }


def show_certificate(topic: str) -> str:
    """Generate certificate HTML"""
    cert_id = random.randint(1000, 9999)
    html = f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px; border-radius: 15px; text-align: center; color: white; margin: 10px 0;">
        <h2>🏆 Certificate of Completion</h2>
        <p>This certifies that you have completed</p>
        <h3>{topic}</h3>
        <p>Certificate ID: #{cert_id}</p>
        <p>Date: {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
    """
    return html


def load_driver_sheet():
    """Load driver sheet"""
    try:
        return pd.read_csv("driver_sheet.csv")
    except:
        # Create default
        return pd.DataFrame({
            'Date': [],
            'Topic': [],
            'Problem': [],
            'Status': [],
            'Difficulty': [],
            'Solution': [],
            'Notes': []
        })


def save_driver_sheet(df):
    """Save driver sheet"""
    df.to_csv("driver_sheet.csv", index=False)


def add_problem_to_sheet(problem, topic, difficulty, solution, notes):
    """Add new problem to driver sheet"""
    df = load_driver_sheet()
    new_row = pd.DataFrame({
        'Date': [datetime.now().strftime('%Y-%m-%d')],
        'Topic': [topic],
        'Problem': [problem],
        'Status': ['In Progress'],
        'Difficulty': [difficulty],
        'Solution': [solution],
        'Notes': [notes]
    })
    df = pd.concat([df, new_row], ignore_index=True)
    save_driver_sheet(df)
    return df


def main():
    st.set_page_config(page_title="DSA AI Tutor", page_icon="🎓", layout="wide")
    init_session()
    
    # Dark mode
    dark_mode = st.toggle("🌙 Dark Mode", value=False)
    if dark_mode:
        st.markdown("""<style>.stApp{background-color:#1e1e1e;color:#fff}</style>""", unsafe_allow_html=True)
    
    st.markdown("""<h1 style='text-align:center;color:#4CAF50;'>🎓 DSA AI Tutor Agent</h1>""", unsafe_allow_html=True)
    
    # Progress dashboard
    st.header("📊 Your Progress")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Topics", len(st.session_state.progress['topics']))
    with col2:
        st.metric("Solved", st.session_state.progress['problems_solved'])
    with col3:
        st.metric("Quizzes", st.session_state.progress['quizzes_taken'])
    with col4:
        st.metric("🔥 Streak", st.session_state.progress['streak'])
    
    if st.session_state.progress['badges']:
        st.write("🏅 Badges:", ", ".join(st.session_state.progress['badges']))
    
    # Spaced Repetition
    st.header("📅 Spaced Repetition")
    review_items = []
    today = datetime.now().date()
    for topic, next_review in st.session_state.progress['reviews'].items():
        review_date = datetime.strptime(next_review, '%Y-%m-%d').date()
        if review_date <= today:
            review_items.append(topic)
    
    if review_items:
        st.warning(f"📚 Topics to review: {', '.join(review_items)}")
    else:
        st.success("✅ All caught up!")
    
    # Voice Input (placeholder)
    if st.checkbox("🎤 Voice Input"):
        st.warning("🎤 Voice coming soon!")
    
    # Sidebar
    with st.sidebar:
        st.header("📚 Topics")
        topics = st.multiselect(
            "Select topics:",
            ["array", "linked list", "stack", "queue", "tree", "graph", "sorting", "dp", "heap", "trie"],
            default=st.session_state.progress['topics']
        )
        
        if st.button("🔄 Reset Chat"):
            st.session_state.messages = []
            st.rerun()
        
        # Add Problem Form
        st.header("➕ Add New Problem")
        with st.form("add_problem"):
            problem_name = st.text_input("Problem Name", placeholder="Two Sum")
            topic_select = st.selectbox("Topic", ["array", "linked list", "stack", "queue", "tree", "graph", "sorting", "dp", "heap", "trie"])
            difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
            solution_code = st.text_area("Solution Code", height=100, placeholder="def twoSum(nums, target):\n    pass")
            notes = st.text_input("Notes", placeholder="Hint or approach")
            
            submit = st.form_submit_button("💾 Add to Sheet")
            if submit and problem_name:
                df = add_problem_to_sheet(problem_name, topic_select, difficulty, solution_code, notes)
                st.success(f"✅ Added: {problem_name}")
                st.session_state.progress['problems_solved'] += 1
        
        # Driver Sheet
        st.header("📋 Driver Sheet")
        try:
            df = load_driver_sheet()
            st.dataframe(df, use_container_width=True)
        except:
            st.warning("driver_sheet.csv not found")
        
        if st.button("📥 Export Session"):
            import json
            st.download_button(
                label="Download JSON",
                data=json.dumps({"messages": st.session_state.messages}),
                file_name="dsa_session.json",
                mime="application/json"
            )
        
        if st.button("🏆 Get Certificate") and topics:
            topic = random.choice(topics)
            st.markdown(show_certificate(topic), unsafe_allow_html=True)
            if topic not in st.session_state.progress['badges']:
                st.session_state.progress['badges'].append(topic)
    
    # Mode selection
    mode = st.radio("Mode", ["Chat", "Editor", "Code Review", "Visualize"], horizontal=True)
    
    if mode == "Chat":
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
        
        if prompt := st.chat_input("Ask about DSA..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            response = st.session_state.agent.chat(prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            for topic in topics:
                if topic not in st.session_state.progress['topics']:
                    st.session_state.progress['topics'].append(topic)
                    st.session_state.progress['reviews'][topic] = (
                        (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
                    )
            st.rerun()
    
    elif mode == "Editor":
        st.subheader("💻 Code Editor")
        editor_code = st.text_area("Write code:", height=300, placeholder="def solution():\n    pass")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("▶️ Run Code") and editor_code:
                result = st.session_state.agent.executor.execute(editor_code)
                if result.success:
                    st.success(f"Output: {result.output}")
                else:
                    st.error(f"Error: {result.error}")
        
        with col2:
            if st.button("🔍 Analyze") and editor_code:
                st.json(st.session_state.reviewer.analyze_code(editor_code, "python"))
    
    elif mode == "Code Review":
        st.subheader("🔍 Code Review")
        code = st.text_area("Paste code:", height=200)
        difficulty = st.slider("Rate Difficulty", 1, 5, 3)
        
        if st.button("Analyze Code") and code:
            result = st.session_state.reviewer.analyze_code(code, "python")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Complexity", result['complexity'])
            with col2:
                st.metric("Issues", len(result['issues']))
            
            if result['issues']:
                for issue in result['issues']:
                    st.markdown(f"- {issue}")
            else:
                st.success("✅ No issues!")
            
            st.session_state.progress['problems_solved'] += 1
            st.session_state.progress['ratings'][f"p_{st.session_state.progress['problems_solved']}"] = difficulty
    
    else:  # Visualize
        st.header("🎬 Animated Visualizations")
        viz_type = st.selectbox("Type", ["Sorting", "Tree", "Graph", "Sliding Window"])
        
        if viz_type == "Sorting":
            arr = st.text_input("Array", "5,2,8,1,9,3")
            arr = [int(x) for x in arr.split(",")]
            if st.button("▶️ Animate"):
                st.text("🔄 Bubble Sort Steps:")
                arr_copy = arr.copy()
                for i in range(len(arr_copy)):
                    for j in range(len(arr_copy) - i - 1):
                        st.markdown(f"Compare [{arr_copy[j]},{arr_copy[j+1]}]: {arr_copy}")
                        if arr_copy[j] > arr_copy[j+1]:
                            arr_copy[j], arr_copy[j+1] = arr_copy[j+1], arr_copy[j]
                            st.markdown(f"➡️ Swap! `{arr_copy}`")
                st.success(f"✅ Final: {arr_copy}")
        
        elif viz_type == "Tree":
            values = st.text_input("Values", "5,3,8,1,4,9")
            values = [int(x) for x in values.split(",")]
            if st.button("▶️ Animate"):
                anim = st.session_state.agent.visualizer
                tree = None
                for val in values:
                    tree = anim._insert_bst(tree, val)
                    st.text(anim.draw_binary_tree(tree))
                st.success("✅ Done!")
        
        elif viz_type == "Graph":
            edges = st.text_input("Edges", "0-1,1-2,2-3")
            adj = {}
            for e in edges.split(","):
                a, b = map(int, e.split("-"))
                adj.setdefault(a, []).append(b)
                adj.setdefault(b, []).append(a)
            trav = st.selectbox("Type", ["BFS", "DFS"])
            if st.button("▶️ Animate"):
                anim = st.session_state.agent.visualizer
                st.text(anim.draw_bfs(adj, 0) if trav == "BFS" else anim.draw_dfs(adj, 0))
        
        else:
            arr = st.text_input("Array", "1,2,3,4,5,6,7")
            arr = [int(x) for x in arr.split(",")]
            k = st.slider("k", 2, len(arr), 3)
            if st.button("▶️ Animate"):
                st.text(st.session_state.agent.visualizer.draw_sliding_window(arr, k))


if __name__ == "__main__":
    main()
