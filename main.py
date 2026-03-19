import uuid
import os
from dotenv import load_dotenv
from core.agent import get_agent

# Load environment variables
load_dotenv()

def main():
    """Main function to run the SQL Assistant."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY not found in environment. Please set it in .env file.")
        # return # Proceed anyway to see error or if user set it differently
    
    # Initialize the agent
    agent = get_agent()
    
    # Configuration for this conversation thread
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    print("Welcome to the SQL Assistant!")
    print("Type 'exit' to quit.")
    print("-" * 30)
    
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ["exit", "quit", "q"]:
            break
            
        # Ask for a SQL query
        result = agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": user_input,
                    }
                ]
            },
            config
        )
        
        # Print the conversation
        for message in result["messages"]:
            # We only print Assistant or Tool messages to avoid re-printing the user input
            if message.type in ["ai", "tool"]:
                if hasattr(message, 'pretty_print'):
                    message.pretty_print()
                else:
                    print(f"{message.type.upper()}: {message.content}")

if __name__ == "__main__":
    main()
