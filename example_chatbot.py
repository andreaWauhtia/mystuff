#!/usr/bin/env python3
"""
Example usage of the Coach Assistant Chatbot API

This script demonstrates how to use the chatbot API for various coaching tasks.
"""

from chatbot import ChatbotAPI


def main():
    print("=" * 60)
    print("Coach Assistant Chatbot - Example Usage")
    print("=" * 60)
    print()
    
    # Create a chatbot session
    print("1. Creating chatbot session...")
    api = ChatbotAPI(team_name="USAO U8")
    print(f"   ✓ Session created for team: {api.get_team_name()}")
    print()
    
    # Example 1: Get help
    print("2. Getting help information...")
    response = api.send_message("/help-coach")
    print(response)
    print()
    
    # Example 2: Ask a natural language question
    print("3. Asking about match analysis...")
    response = api.send_message("Can you help me analyze our matches?")
    print(response)
    print()
    
    # Example 3: Analyze a match (if data exists)
    print("4. Analyzing a match...")
    response = api.send_message("/analyze-match 2025-11-01")
    print(response)
    print()
    
    # Example 4: Scout a player
    print("5. Scouting a player...")
    response = api.send_message("/scout-player Nestor")
    print(response)
    print()
    
    # Example 5: Plan a training session
    print("6. Planning a training session...")
    response = api.send_message("/plan-session")
    print(response)
    print()
    
    # Example 6: Review performance
    print("7. Reviewing team performance...")
    response = api.send_message("/review-performance last-3-matches")
    print(response)
    print()
    
    # Show conversation history
    print("8. Conversation history:")
    history = api.get_history()
    print(f"   Total messages: {len(history)}")
    print()
    
    # Export conversation
    print("9. Exporting conversation history...")
    output_file = api.export_history("/tmp/chat_history.json", format='json')
    print(f"   ✓ Exported to: {output_file}")
    print()
    
    # List available commands
    print("10. Available commands:")
    commands = api.list_commands()
    for cmd in commands:
        print(f"   • {cmd}")
    print()
    
    print("=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


def interactive_mode():
    """Run the chatbot in interactive mode."""
    print("=" * 60)
    print("Coach Assistant Chatbot - Interactive Mode")
    print("=" * 60)
    print()
    
    # Get team name
    team_name = input("Enter your team name: ").strip()
    if not team_name:
        team_name = "My Team"
    
    # Create chatbot session
    api = ChatbotAPI(team_name=team_name)
    print(f"\n✓ Session created for team: {team_name}")
    print("Type 'quit' or 'exit' to end the session.")
    print("Type '/help-coach' for available commands.\n")
    
    # Chat loop
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("\nEnding chat session. Goodbye!")
                api.end_session()
                break
            
            # Send message and get response
            response = api.send_message(user_input)
            print(f"\nBot: {response}\n")
        
        except KeyboardInterrupt:
            print("\n\nSession interrupted. Goodbye!")
            api.end_session()
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        interactive_mode()
    else:
        main()
