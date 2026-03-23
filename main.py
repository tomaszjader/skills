import uuid
import os
import logging
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from core.agent import get_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Rich console
console = Console()

# Load environment variables
load_dotenv()

def run_conversation(agent, user_input: str, config: dict):
    """Handle a single interaction with the agent."""
    return agent.invoke(
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

def main():
    """Main function to run the SQL Assistant."""
    # Check for API key
    if not os.getenv("OPENAI_API_KEY"):
        console.print("[yellow]Warning: OPENAI_API_KEY not found in environment. Please set it in .env file.[/yellow]")
    
    # Initialize the agent
    try:
        agent = get_agent()
    except Exception as e:
        logger.critical(f"Failed to initialize agent: {e}")
        console.print(f"[bold red]Critical Error:[/bold red] Could not initialize the AI agent. Check your configuration and API keys.")
        return

    # Configuration for this conversation thread
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    console.print(Panel.fit(
        "Welcome to the [bold blue]SQL Assistant (Refactored)[/bold blue]!\n"
        "I can help you analyze sales and inventory data using specialized skills.\n"
        "Type [bold red]'exit'[/bold red] to quit.",
        title="System",
        border_style="green"
    ))
    
    while True:
        try:
            user_input = console.input("\n[bold green]You:[/bold green] ")
            if user_input.lower() in ["exit", "quit", "q"]:
                console.print("[blue]Goodbye![/blue]")
                break
            
            if not user_input.strip():
                continue
                
            # Ask for a SQL query
            with console.status("[bold blue]Agent is processing...[/bold blue]"):
                result = run_conversation(agent, user_input, config)
            
            # Print the conversation
            for message in result["messages"]:
                # We only print Assistant or Tool messages to avoid re-printing the user input
                if message.type == "ai":
                    if message.content:
                        console.print(Panel(Markdown(message.content), title="Assistant", border_style="blue"))
                elif message.type == "tool":
                    # Tool output is often long, we show a snippet
                    content_snippet = message.content[:150].replace('\n', ' ')
                    console.print(f"[dim]Tool ({message.name}): {content_snippet}...[/dim]")
                    
        except KeyboardInterrupt:
            console.print("\n[blue]Goodbye![/blue]")
            break
        except Exception as e:
            logger.error(f"Error during agent interaction: {e}", exc_info=True)
            console.print(f"[bold red]Interactions Error:[/bold red] {e}")

if __name__ == "__main__":
    main()
