#!/usr/bin/env python3
"""
Coach Assistant Chatbot - Core Implementation

This chatbot provides a conversational interface for football team coaching support.
It integrates with the coach_assistant.chatmode.md specification and supports
slash commands for match analysis, player scouting, and training evaluation.
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json


class CoachChatbot:
    """
    Main chatbot class implementing the Coach Assistant functionality.
    
    This class provides:
    - Conversational interface for coaching support
    - Slash command processing
    - Integration with data sources in .memory-bank/
    - Command routing to specialized handlers
    """
    
    def __init__(self, team_name: Optional[str] = None, memory_bank_path: Optional[str] = None):
        """
        Initialize the Coach Assistant Chatbot.
        
        Args:
            team_name: Name of the team to personalize interactions
            memory_bank_path: Path to .memory-bank directory (defaults to repository root)
        """
        self.team_name = team_name
        self.memory_bank_path = Path(memory_bank_path or ".memory-bank")
        self.conversation_history: List[Dict[str, str]] = []
        self.commands = {
            '/analyze-match': self._handle_analyze_match,
            '/scout-player': self._handle_scout_player,
            '/analyze-training': self._handle_analyze_training,
            '/plan-session': self._handle_plan_session,
            '/review-performance': self._handle_review_performance,
            '/help-coach': self._handle_help,
        }
        
        # If team name not provided, ask for it
        if not self.team_name:
            self._greeting_message = (
                "Welcome to Coach Assistant! 🏆\n\n"
                "To personalize your experience, please provide your team name.\n"
                "You can do this by calling set_team_name() or by including it in your messages."
            )
    
    def set_team_name(self, team_name: str) -> str:
        """Set the team name for personalized interactions."""
        self.team_name = team_name
        return f"Team set to: {team_name}. How can I assist you today?"
    
    def chat(self, message: str) -> str:
        """
        Process a chat message and return a response.
        
        Args:
            message: User message (can be a slash command or natural language)
        
        Returns:
            Bot response as a string
        """
        # Store message in conversation history
        self._add_to_history("user", message)
        
        # Check if team name is set
        if not self.team_name:
            # Try to extract team name from message
            team_match = re.search(r'(?:team|équipe|club)(?:\s+name)?(?:\s+is)?[:\s]+([A-Z][A-Za-z0-9\s\.]+)', message, re.IGNORECASE)
            if team_match:
                self.team_name = team_match.group(1).strip()
                response = f"Perfect! Team '{self.team_name}' registered. How can I help you today?"
            else:
                response = self._greeting_message
            self._add_to_history("assistant", response)
            return response
        
        # Check if message is a slash command
        if message.strip().startswith('/'):
            response = self._process_command(message.strip())
        else:
            response = self._process_natural_language(message)
        
        self._add_to_history("assistant", response)
        return response
    
    def _process_command(self, command_text: str) -> str:
        """
        Process a slash command.
        
        Args:
            command_text: Command string starting with /
        
        Returns:
            Command execution result
        """
        # Parse command and arguments
        parts = command_text.split(maxsplit=1)
        command = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Find and execute command handler
        if command in self.commands:
            handler = self.commands[command]
            return handler(args)
        else:
            return (
                f"❌ Unknown command: {command}\n\n"
                f"Available commands:\n"
                f"  /analyze-match [matchday]\n"
                f"  /scout-player [player_name]\n"
                f"  /analyze-training [date]\n"
                f"  /plan-session\n"
                f"  /review-performance [period]\n"
                f"  /help-coach\n\n"
                f"Type /help-coach for detailed help."
            )
    
    def _process_natural_language(self, message: str) -> str:
        """
        Process natural language input and provide contextual assistance.
        
        Args:
            message: Natural language message
        
        Returns:
            Contextual response
        """
        message_lower = message.lower()
        
        # Match analysis keywords
        if any(kw in message_lower for kw in ['match', 'game', 'competition', 'analyse', 'analyze']):
            return (
                f"I can help you analyze matches for {self.team_name}! 📊\n\n"
                f"Use `/analyze-match [matchday]` to get a detailed match analysis.\n"
                f"Example: `/analyze-match 2025-11-07`\n\n"
                f"I'll process timeline data, calculate metrics, and generate insights."
            )
        
        # Player scouting keywords
        elif any(kw in message_lower for kw in ['player', 'scout', 'evaluation', 'joueur']):
            return (
                f"I can help you scout players from {self.team_name}! 🔍\n\n"
                f"Use `/scout-player [player_name]` to evaluate a player's performance.\n"
                f"Example: `/scout-player Nestor`\n\n"
                f"I'll analyze data from roster, training, and competition records."
            )
        
        # Training keywords
        elif any(kw in message_lower for kw in ['training', 'session', 'entraînement', 'practice']):
            return (
                f"I can help with training sessions for {self.team_name}! 🏃\n\n"
                f"Available commands:\n"
                f"  • `/analyze-training [date]` - Analyze a past training session\n"
                f"  • `/plan-session` - Plan an upcoming training session\n\n"
                f"What would you like to do?"
            )
        
        # Performance review keywords
        elif any(kw in message_lower for kw in ['performance', 'review', 'progress', 'stats']):
            return (
                f"I can review {self.team_name}'s performance! 📈\n\n"
                f"Use `/review-performance [period]` to get performance insights.\n"
                f"Examples:\n"
                f"  • `/review-performance last-3-matches`\n"
                f"  • `/review-performance last-month`\n"
                f"  • `/review-performance season`"
            )
        
        # Help keywords
        elif any(kw in message_lower for kw in ['help', 'aide', 'command', 'what can you do']):
            return self._handle_help("")
        
        # Default response
        else:
            return (
                f"I'm here to assist {self.team_name} with coaching insights! 🏆\n\n"
                f"I can help you with:\n"
                f"  • Match analysis and statistics\n"
                f"  • Player scouting and evaluation\n"
                f"  • Training session planning and review\n"
                f"  • Team performance tracking\n\n"
                f"Type `/help-coach` to see all available commands, or just ask me what you need!"
            )
    
    def _handle_analyze_match(self, args: str) -> str:
        """
        Handle /analyze-match command.
        
        Args:
            args: Match day identifier (e.g., "2025-11-07")
        
        Returns:
            Match analysis result
        """
        if not args:
            return (
                "❌ Please specify a matchday.\n\n"
                "Usage: /analyze-match [matchday]\n"
                "Example: /analyze-match 2025-11-07"
            )
        
        matchday = args.strip()
        
        # Check if match data exists
        match_data_path = self.memory_bank_path / "competitions" / "analysis" / matchday
        
        if match_data_path.exists():
            # Try to load and summarize existing analysis
            json_file = match_data_path / f"{matchday}.json"
            md_file = match_data_path / f"{matchday}.md"
            
            if json_file.exists():
                try:
                    with open(json_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    our_team = data.get('our_team', self.team_name)
                    opponent = data.get('opponent_team', 'opponent')
                    score1 = data.get('score1', 0)
                    score2 = data.get('score2', 0)
                    
                    # Count goals
                    us_goals = sum(1 for e in data.get('events', []) 
                                  if e.get('team') == 'us' and e.get('classification') == 'goal')
                    opp_goals = sum(1 for e in data.get('events', []) 
                                   if e.get('team') == 'opponent' and e.get('classification') == 'goal')
                    
                    # Count shots
                    us_shots = sum(1 for e in data.get('events', []) 
                                  if e.get('team') == 'us' and e.get('classification') == 'shoot')
                    
                    return (
                        f"📊 **Match Analysis: {matchday}**\n\n"
                        f"**{our_team}** vs **{opponent}**\n"
                        f"Score: {score1} - {score2}\n\n"
                        f"🎯 **Key Stats:**\n"
                        f"  • Goals scored: {us_goals}\n"
                        f"  • Goals conceded: {opp_goals}\n"
                        f"  • Shots attempted: {us_shots}\n"
                        f"  • Total events: {len(data.get('events', []))}\n\n"
                        f"✅ Detailed report available at: {md_file.name}\n"
                        f"📁 Data location: {match_data_path}"
                    )
                except Exception as e:
                    return f"⚠️ Error reading match data: {str(e)}"
            
            return (
                f"✅ Match data found for {matchday}\n"
                f"📁 Location: {match_data_path}\n\n"
                f"Use the parse_timeline.py tool to process the match data."
            )
        else:
            return (
                f"❌ No match data found for {matchday}\n\n"
                f"Expected location: {match_data_path}\n\n"
                f"To add match data:\n"
                f"1. Prepare timeline data in JSON format\n"
                f"2. Run: `python tools/parse_timeline.py --input <file> --matchday {matchday}`\n"
                f"3. Then use /analyze-match again"
            )
    
    def _handle_scout_player(self, args: str) -> str:
        """
        Handle /scout-player command.
        
        Args:
            args: Player name
        
        Returns:
            Player scouting report
        """
        if not args:
            return (
                "❌ Please specify a player name.\n\n"
                "Usage: /scout-player [player_name]\n"
                "Example: /scout-player Nestor"
            )
        
        player_name = args.strip()
        
        # Search for player in match data
        competitions_path = self.memory_bank_path / "competitions" / "analysis"
        
        if not competitions_path.exists():
            return (
                f"❌ No competition data available.\n\n"
                f"Expected path: {competitions_path}"
            )
        
        player_events = []
        matches_played = []
        
        # Scan all match data for player
        for match_dir in competitions_path.iterdir():
            if match_dir.is_dir():
                json_file = match_dir / f"{match_dir.name}.json"
                if json_file.exists():
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        
                        # Find player events
                        for event in data.get('events', []):
                            if event.get('player') and player_name.lower() in event.get('player', '').lower():
                                player_events.append({
                                    'matchday': match_dir.name,
                                    'event': event
                                })
                                if match_dir.name not in matches_played:
                                    matches_played.append(match_dir.name)
                    except:
                        pass
        
        if not player_events:
            return (
                f"❌ No data found for player '{player_name}' in {self.team_name}\n\n"
                f"Searched in: {competitions_path}\n"
                f"Make sure:\n"
                f"  • Player name is spelled correctly\n"
                f"  • Match data has been processed\n"
                f"  • Player participated in analyzed matches"
            )
        
        # Calculate statistics
        goals = sum(1 for pe in player_events if pe['event'].get('classification') == 'goal')
        shots = sum(1 for pe in player_events if pe['event'].get('classification') == 'shoot')
        
        return (
            f"🔍 **Player Scout Report: {player_name}**\n\n"
            f"Team: {self.team_name}\n"
            f"Matches analyzed: {len(matches_played)}\n\n"
            f"📊 **Performance Stats:**\n"
            f"  • Total goals: {goals}\n"
            f"  • Total shots: {shots}\n"
            f"  • Total events: {len(player_events)}\n"
            f"  • Conversion rate: {(goals / (goals + shots) * 100) if (goals + shots) > 0 else 0:.1f}%\n\n"
            f"📅 **Matches played:**\n"
            + '\n'.join(f"  • {match}" for match in sorted(matches_played)) +
            f"\n\n✅ Player shows activity across {len(matches_played)} match(es)"
        )
    
    def _handle_analyze_training(self, args: str) -> str:
        """
        Handle /analyze-training command.
        
        Args:
            args: Training date
        
        Returns:
            Training analysis result
        """
        if not args:
            return (
                "❌ Please specify a training date.\n\n"
                "Usage: /analyze-training [date]\n"
                "Example: /analyze-training 2025-11-10"
            )
        
        training_date = args.strip()
        training_path = self.memory_bank_path / "trainings" / "report" / f"{training_date}.md"
        
        if training_path.exists():
            return (
                f"✅ Training report found for {training_date}\n"
                f"📁 Location: {training_path}\n\n"
                f"To view the full report, open: {training_path}"
            )
        else:
            return (
                f"❌ No training report found for {training_date}\n\n"
                f"Expected location: {training_path}\n\n"
                f"Training reports should be placed in: {self.memory_bank_path / 'trainings' / 'report'}/"
            )
    
    def _handle_plan_session(self, args: str) -> str:
        """
        Handle /plan-session command.
        
        Returns:
            Interactive planning guidance
        """
        return (
            f"📋 **Training Session Planning for {self.team_name}**\n\n"
            f"Let's plan your next training session!\n\n"
            f"Consider these aspects:\n"
            f"  1. **Warm-up** (10-15 min)\n"
            f"     • Light jogging, dynamic stretching\n"
            f"     • Ball control exercises\n\n"
            f"  2. **Technical Skills** (20-25 min)\n"
            f"     • Passing drills\n"
            f"     • Shooting practice\n"
            f"     • Dribbling exercises\n\n"
            f"  3. **Tactical Training** (15-20 min)\n"
            f"     • Positioning drills\n"
            f"     • Team formations\n"
            f"     • Set pieces\n\n"
            f"  4. **Small-sided Games** (15-20 min)\n"
            f"     • 4v4 or 5v5 matches\n"
            f"     • Apply learned techniques\n\n"
            f"  5. **Cool Down** (10 min)\n"
            f"     • Light jogging\n"
            f"     • Static stretching\n\n"
            f"💡 **Tip**: Focus on areas that need improvement based on recent match analysis.\n"
            f"Use `/review-performance` to identify weak points."
        )
    
    def _handle_review_performance(self, args: str) -> str:
        """
        Handle /review-performance command.
        
        Args:
            args: Period specification (e.g., "last-3-matches", "last-month")
        
        Returns:
            Performance review
        """
        if not args:
            return (
                "❌ Please specify a review period.\n\n"
                "Usage: /review-performance [period]\n"
                "Examples:\n"
                "  • /review-performance last-3-matches\n"
                "  • /review-performance last-month\n"
                "  • /review-performance season"
            )
        
        period = args.strip().lower()
        
        # Load all available match data
        competitions_path = self.memory_bank_path / "competitions" / "analysis"
        
        if not competitions_path.exists():
            return (
                f"❌ No competition data available.\n\n"
                f"Expected path: {competitions_path}"
            )
        
        matches = []
        for match_dir in sorted(competitions_path.iterdir(), reverse=True):
            if match_dir.is_dir():
                json_file = match_dir / f"{match_dir.name}.json"
                if json_file.exists():
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            matches.append({
                                'matchday': match_dir.name,
                                'data': json.load(f)
                            })
                    except:
                        pass
        
        if not matches:
            return (
                f"❌ No match data available for performance review.\n\n"
                f"Process some matches first using `/analyze-match [matchday]`"
            )
        
        # Filter matches based on period
        if 'last' in period and 'match' in period:
            # Extract number from period (e.g., "last-3-matches" -> 3)
            match_count = re.search(r'(\d+)', period)
            if match_count:
                num_matches = int(match_count.group(1))
                matches = matches[:num_matches]
        
        # Calculate aggregate statistics
        total_goals = 0
        total_conceded = 0
        total_shots = 0
        wins = 0
        losses = 0
        draws = 0
        
        for match in matches:
            data = match['data']
            
            us_goals = sum(1 for e in data.get('events', []) 
                          if e.get('team') == 'us' and e.get('classification') == 'goal')
            opp_goals = sum(1 for e in data.get('events', []) 
                           if e.get('team') == 'opponent' and e.get('classification') == 'goal')
            us_shots = sum(1 for e in data.get('events', []) 
                          if e.get('team') == 'us' and e.get('classification') == 'shoot')
            
            total_goals += us_goals
            total_conceded += opp_goals
            total_shots += us_shots
            
            if us_goals > opp_goals:
                wins += 1
            elif us_goals < opp_goals:
                losses += 1
            else:
                draws += 1
        
        efficiency = (total_goals / (total_goals + total_shots) * 100) if (total_goals + total_shots) > 0 else 0
        
        return (
            f"📈 **Performance Review: {period.replace('-', ' ').title()}**\n\n"
            f"Team: {self.team_name}\n"
            f"Matches analyzed: {len(matches)}\n\n"
            f"🏆 **Match Record:**\n"
            f"  • Wins: {wins}\n"
            f"  • Draws: {draws}\n"
            f"  • Losses: {losses}\n"
            f"  • Win rate: {(wins / len(matches) * 100) if matches else 0:.1f}%\n\n"
            f"⚽ **Offensive Stats:**\n"
            f"  • Total goals: {total_goals}\n"
            f"  • Goals per match: {(total_goals / len(matches)):.1f}\n"
            f"  • Total shots: {total_shots}\n"
            f"  • Shot efficiency: {efficiency:.1f}%\n\n"
            f"🛡️ **Defensive Stats:**\n"
            f"  • Goals conceded: {total_conceded}\n"
            f"  • Conceded per match: {(total_conceded / len(matches)):.1f}\n"
            f"  • Goal difference: {total_goals - total_conceded:+d}\n\n"
            f"💡 **Insights:**\n" +
            (f"  • Strong offensive performance! Averaging {(total_goals / len(matches)):.1f} goals per match.\n" if total_goals / len(matches) > 5 else "") +
            (f"  • Excellent shot efficiency at {efficiency:.1f}%.\n" if efficiency > 60 else "") +
            (f"  • Defense needs attention. Conceding {(total_conceded / len(matches)):.1f} goals per match.\n" if total_conceded / len(matches) > 3 else "") +
            (f"  • Great form! Winning {(wins / len(matches) * 100):.0f}% of matches.\n" if wins / len(matches) > 0.6 else "")
        )
    
    def _handle_help(self, args: str) -> str:
        """
        Handle /help-coach command.
        
        Returns:
            Detailed help information
        """
        return (
            f"🏆 **Coach Assistant - Help Guide**\n\n"
            f"Team: {self.team_name or '(not set)'}\n\n"
            f"**Available Commands:**\n\n"
            f"1. **/analyze-match [matchday]**\n"
            f"   Analyze a specific match with detailed statistics.\n"
            f"   Example: `/analyze-match 2025-11-07`\n\n"
            f"2. **/scout-player [player_name]**\n"
            f"   Evaluate individual player performance across matches.\n"
            f"   Example: `/scout-player Nestor`\n\n"
            f"3. **/analyze-training [date]**\n"
            f"   Review a past training session.\n"
            f"   Example: `/analyze-training 2025-11-10`\n\n"
            f"4. **/plan-session**\n"
            f"   Get guidance for planning an upcoming training session.\n\n"
            f"5. **/review-performance [period]**\n"
            f"   Review team performance over a specified period.\n"
            f"   Examples:\n"
            f"   • `/review-performance last-3-matches`\n"
            f"   • `/review-performance last-month`\n"
            f"   • `/review-performance season`\n\n"
            f"6. **/help-coach**\n"
            f"   Display this help guide.\n\n"
            f"**Natural Language Support:**\n"
            f"You can also just chat naturally! I'll understand questions like:\n"
            f"  • \"How did we perform in the last match?\"\n"
            f"  • \"Tell me about Nestor's performance\"\n"
            f"  • \"What should we focus on in training?\"\n\n"
            f"**Data Sources:**\n"
            f"  • Match data: `.memory-bank/competitions/analysis/`\n"
            f"  • Training reports: `.memory-bank/trainings/report/`\n"
            f"  • Player roster: `.memory-bank/roster/`\n\n"
            f"For more information, see: `.github/chatmodes/coach_assistant.chatmode.md`"
        )
    
    def _add_to_history(self, role: str, content: str):
        """Add a message to conversation history."""
        self.conversation_history.append({
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        })
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get the full conversation history."""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """Clear the conversation history."""
        self.conversation_history.clear()
