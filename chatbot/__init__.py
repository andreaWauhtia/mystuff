"""
Coach Assistant Chatbot Package

This package provides a Python API for the Coach Assistant chatbot,
implementing the specifications from .github/chatmodes/coach_assistant.chatmode.md
"""

from .coach_chatbot import CoachChatbot
from .chatbot_api import ChatbotAPI

__version__ = "1.0.0"
__all__ = ["CoachChatbot", "ChatbotAPI"]
