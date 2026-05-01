"""
DSA AI Tutor Agent - Main Entry Point
A conversational AI agent for learning Data Structures and Algorithms
"""

from agent.core import DSAAgent

def main():
    print("=" * 50)
    print("🎓 DSA AI Tutor Agent")
    print("=" * 50)
    print("Your personal DSA learning assistant!\n")
    print("Type 'exit' to quit, 'help' for commands\n")
    
    # Initialize the agent
    agent = DSAAgent()
    
    # Start conversation loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\n👋 Goodbye! Happy coding! 🚀")
                break
                
            if user_input.lower() == 'help':
                print("""
📚 Available Commands:
- explain <problem>  : Explain a DSA problem
- code <problem>    : Generate code solution
- hint <problem>   : Get hints
- complexity      : Show complexity cheatsheet
- practice        : Get practice recommendations
- help           : Show this help
                """)
                continue
            
            # Get response from agent
            response = agent.chat(user_input)
            print(f"\nAgent: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye! Happy coding! 🚀")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
