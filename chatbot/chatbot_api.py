#!/usr/bin/env python3
"""
Coach Assistant Chatbot API

This module provides a Python API wrapper for the Coach Assistant chatbot.
It exposes a simple interface for creating chat sessions, sending messages,
and managing conversations programmatically.
"""

from typing import Dict, List, Optional
from pathlib import Path
import json
from .coach_chatbot import CoachChatbot


class ChatbotAPI:
    """
    Python API wrapper for the Coach Assistant Chatbot.
    
    This class provides a simple, programmatic interface to the chatbot
    with session management and conversation persistence.
    
    Example:
        ```python
        from chatbot import ChatbotAPI
        
        # Create API instance
        api = ChatbotAPI(team_name="USAO U8")
        
        # Start a conversation
        response = api.send_message("Hello!")
        print(response)
        
        # Use slash commands
        response = api.send_message("/analyze-match 2025-11-07")
        print(response)
        
        # Get conversation history
        history = api.get_history()
        ```
    """
    
    def __init__(self, team_name: Optional[str] = None, memory_bank_path: Optional[str] = None):
        """
        Initialize the Chatbot API.
        
        Args:
            team_name: Name of the team (can be set later with set_team_name)
            memory_bank_path: Path to .memory-bank directory
        """
        self.chatbot = CoachChatbot(team_name=team_name, memory_bank_path=memory_bank_path)
        self._session_active = True
    
    def send_message(self, message: str) -> str:
        """
        Send a message to the chatbot and get a response.
        
        Args:
            message: User message (natural language or slash command)
        
        Returns:
            Chatbot response as a string
        
        Raises:
            RuntimeError: If the session is not active
        """
        if not self._session_active:
            raise RuntimeError("Chat session is not active. Create a new ChatbotAPI instance.")
        
        return self.chatbot.chat(message)
    
    def set_team_name(self, team_name: str) -> str:
        """
        Set or update the team name.
        
        Args:
            team_name: Name of the team
        
        Returns:
            Confirmation message
        """
        return self.chatbot.set_team_name(team_name)
    
    def get_team_name(self) -> Optional[str]:
        """
        Get the current team name.
        
        Returns:
            Team name or None if not set
        """
        return self.chatbot.team_name
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get the full conversation history.
        
        Returns:
            List of message dictionaries with 'role', 'content', and 'timestamp'
        """
        return self.chatbot.get_conversation_history()
    
    def clear_history(self):
        """Clear the conversation history."""
        self.chatbot.clear_history()
    
    def end_session(self):
        """End the current chat session."""
        self._session_active = False
    
    def is_active(self) -> bool:
        """Check if the session is active."""
        return self._session_active
    
    def export_history(self, output_path: str, format: str = 'json') -> str:
        """
        Export conversation history to a file.
        
        Args:
            output_path: Path to save the history
            format: Export format ('json' or 'txt')
        
        Returns:
            Path to the exported file
        
        Raises:
            ValueError: If format is not supported
        """
        history = self.get_history()
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        if format == 'json':
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'team': self.chatbot.team_name,
                    'history': history
                }, f, indent=2, ensure_ascii=False)
        
        elif format == 'txt':
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Coach Assistant Chat History\n")
                f.write(f"Team: {self.chatbot.team_name or '(not set)'}\n")
                f.write(f"{'='*60}\n\n")
                
                for msg in history:
                    role = msg['role'].upper()
                    timestamp = msg.get('timestamp', 'N/A')
                    content = msg['content']
                    f.write(f"[{timestamp}] {role}:\n{content}\n\n")
        
        else:
            raise ValueError(f"Unsupported format: {format}. Use 'json' or 'txt'.")
        
        return str(output_file)
    
    def list_commands(self) -> List[str]:
        """
        Get a list of available slash commands.
        
        Returns:
            List of command strings
        """
        return list(self.chatbot.commands.keys())
    
    def get_command_help(self, command: str) -> str:
        """
        Get help information for a specific command.
        
        Args:
            command: Command name (with or without leading slash)
        
        Returns:
            Help text for the command
        """
        if not command.startswith('/'):
            command = '/' + command
        
        command = command.lower()
        
        if command == '/analyze-match':
            return (
                "Command: /analyze-match [matchday]\n"
                "Description: Analyze a specific match with detailed statistics.\n"
                "Arguments:\n"
                "  matchday - Date identifier for the match (e.g., '2025-11-07')\n"
                "Example: /analyze-match 2025-11-07"
            )
        elif command == '/scout-player':
            return (
                "Command: /scout-player [player_name]\n"
                "Description: Evaluate individual player performance across matches.\n"
                "Arguments:\n"
                "  player_name - Name of the player to scout\n"
                "Example: /scout-player Nestor"
            )
        elif command == '/analyze-training':
            return (
                "Command: /analyze-training [date]\n"
                "Description: Review a past training session.\n"
                "Arguments:\n"
                "  date - Date of the training session (e.g., '2025-11-10')\n"
                "Example: /analyze-training 2025-11-10"
            )
        elif command == '/plan-session':
            return (
                "Command: /plan-session\n"
                "Description: Get guidance for planning an upcoming training session.\n"
                "Arguments: None\n"
                "Example: /plan-session"
            )
        elif command == '/review-performance':
            return (
                "Command: /review-performance [period]\n"
                "Description: Review team performance over a specified period.\n"
                "Arguments:\n"
                "  period - Time period to review (e.g., 'last-3-matches', 'last-month', 'season')\n"
                "Examples:\n"
                "  /review-performance last-3-matches\n"
                "  /review-performance last-month\n"
                "  /review-performance season"
            )
        elif command == '/help-coach':
            return (
                "Command: /help-coach\n"
                "Description: Display detailed help and available commands.\n"
                "Arguments: None\n"
                "Example: /help-coach"
            )
        else:
            return f"Unknown command: {command}"


def create_chat_session(team_name: Optional[str] = None, memory_bank_path: Optional[str] = None) -> ChatbotAPI:
    """
    Convenience function to create a new chat session.
    
    Args:
        team_name: Name of the team
        memory_bank_path: Path to .memory-bank directory
    
    Returns:
        New ChatbotAPI instance
    """
    return ChatbotAPI(team_name=team_name, memory_bank_path=memory_bank_path)
