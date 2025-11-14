# Coach Assistant Chatbot - API Documentation

## Overview

The Coach Assistant Chatbot is a Python-based conversational interface for football team coaching support. It implements the specifications from `.github/chatmodes/coach_assistant.chatmode.md` and provides both slash commands and natural language interaction.

## Features

- 🏆 **Team-specific coaching assistance**
- 📊 **Match analysis with detailed statistics**
- 🔍 **Player scouting and performance evaluation**
- 🏃 **Training session planning and review**
- 📈 **Performance tracking over time**
- 💬 **Natural language understanding**
- 📝 **Conversation history management**

## Installation

No additional dependencies required beyond the base project requirements:

```bash
pip install -r requirements.txt
```

## Quick Start

### Basic Usage

```python
from chatbot import ChatbotAPI

# Create a chatbot session
api = ChatbotAPI(team_name="USAO U8")

# Send a message
response = api.send_message("Hello!")
print(response)

# Use a slash command
response = api.send_message("/help-coach")
print(response)
```

### Interactive Mode

Run the chatbot in interactive mode:

```bash
python example_chatbot.py --interactive
```

### Example Script

Run the example script to see all features:

```bash
python example_chatbot.py
```

## API Reference

### ChatbotAPI Class

#### Constructor

```python
api = ChatbotAPI(team_name=None, memory_bank_path=None)
```

**Parameters:**
- `team_name` (str, optional): Name of the team for personalized interactions
- `memory_bank_path` (str, optional): Path to `.memory-bank` directory (defaults to repository root)

#### Methods

##### `send_message(message: str) -> str`

Send a message to the chatbot and get a response.

```python
response = api.send_message("How did we perform?")
```

##### `set_team_name(team_name: str) -> str`

Set or update the team name.

```python
confirmation = api.set_team_name("USAO U8")
```

##### `get_team_name() -> Optional[str]`

Get the current team name.

```python
team = api.get_team_name()
```

##### `get_history() -> List[Dict[str, str]]`

Get the full conversation history.

```python
history = api.get_history()
for msg in history:
    print(f"{msg['role']}: {msg['content']}")
```

##### `clear_history()`

Clear the conversation history.

```python
api.clear_history()
```

##### `export_history(output_path: str, format: str = 'json') -> str`

Export conversation history to a file.

```python
# Export as JSON
file_path = api.export_history("chat_history.json", format='json')

# Export as text
file_path = api.export_history("chat_history.txt", format='txt')
```

##### `list_commands() -> List[str]`

Get a list of available slash commands.

```python
commands = api.list_commands()
print(commands)  # ['/analyze-match', '/scout-player', ...]
```

##### `get_command_help(command: str) -> str`

Get help information for a specific command.

```python
help_text = api.get_command_help('/analyze-match')
print(help_text)
```

##### `end_session()`

End the current chat session.

```python
api.end_session()
```

##### `is_active() -> bool`

Check if the session is active.

```python
if api.is_active():
    response = api.send_message("Hello")
```

## Available Commands

### 1. `/analyze-match [matchday]`

Analyze a specific match with detailed statistics.

**Usage:**
```python
response = api.send_message("/analyze-match 2025-11-07")
```

**Data Requirements:**
- Match data must be processed and stored in `.memory-bank/competitions/analysis/[matchday]/`
- Use `tools/parse_timeline.py` to process raw match data

### 2. `/scout-player [player_name]`

Evaluate individual player performance across matches.

**Usage:**
```python
response = api.send_message("/scout-player Nestor")
```

**Output:**
- Goals scored
- Shots attempted
- Conversion rate
- Matches played

### 3. `/analyze-training [date]`

Review a past training session.

**Usage:**
```python
response = api.send_message("/analyze-training 2025-11-10")
```

**Data Requirements:**
- Training reports should be in `.memory-bank/trainings/report/[date].md`

### 4. `/plan-session`

Get guidance for planning an upcoming training session.

**Usage:**
```python
response = api.send_message("/plan-session")
```

**Output:**
- Warm-up exercises
- Technical skills drills
- Tactical training
- Small-sided games
- Cool down routines

### 5. `/review-performance [period]`

Review team performance over a specified period.

**Usage:**
```python
# Last 3 matches
response = api.send_message("/review-performance last-3-matches")

# Last month
response = api.send_message("/review-performance last-month")

# Full season
response = api.send_message("/review-performance season")
```

**Output:**
- Match record (wins, draws, losses)
- Offensive statistics
- Defensive statistics
- Performance insights

### 6. `/help-coach`

Display detailed help and available commands.

**Usage:**
```python
response = api.send_message("/help-coach")
```

## Natural Language Support

The chatbot understands natural language queries and will guide you to the appropriate command:

```python
# These all work:
api.send_message("Can you analyze our last match?")
api.send_message("Tell me about Nestor's performance")
api.send_message("What should we work on in training?")
api.send_message("How are we doing this season?")
```

## Data Structure

The chatbot expects data in the following structure:

```
.memory-bank/
├── competitions/
│   └── analysis/
│       └── [matchday]/
│           ├── [matchday].json       # Match data
│           ├── [matchday].md         # Match report
│           └── parsed_by_side.csv    # Parsed events
├── trainings/
│   └── report/
│       └── [date].md                 # Training reports
└── roster/
    └── [player files]                # Player information
```

## Examples

### Example 1: Complete Match Analysis Workflow

```python
from chatbot import ChatbotAPI

# Initialize
api = ChatbotAPI(team_name="USAO U8")

# Greet
print(api.send_message("Hello!"))

# Analyze a specific match
print(api.send_message("/analyze-match 2025-11-01"))

# Scout top player
print(api.send_message("/scout-player Nestor"))

# Review recent performance
print(api.send_message("/review-performance last-3-matches"))

# Export conversation
api.export_history("match_analysis_session.json")
```

### Example 2: Training Planning

```python
from chatbot import ChatbotAPI

api = ChatbotAPI(team_name="My Team")

# Get training plan
plan = api.send_message("/plan-session")
print(plan)

# Ask for specific advice
advice = api.send_message("What drills should we focus on for shooting?")
print(advice)
```

### Example 3: Player Evaluation

```python
from chatbot import ChatbotAPI

api = ChatbotAPI(team_name="USAO U8")

# Scout multiple players
players = ["Nestor", "Maxence", "Lilou"]
for player in players:
    report = api.send_message(f"/scout-player {player}")
    print(f"\n{report}\n")
    print("-" * 60)
```

## Error Handling

The API provides clear error messages:

```python
from chatbot import ChatbotAPI

api = ChatbotAPI(team_name="My Team")

# Missing matchday
response = api.send_message("/analyze-match")
# Returns: "❌ Please specify a matchday..."

# Invalid command
response = api.send_message("/unknown-command")
# Returns: "❌ Unknown command: /unknown-command..."

# No data available
response = api.send_message("/analyze-match 2099-01-01")
# Returns: "❌ No match data found for 2099-01-01..."
```

## Integration with Existing Tools

The chatbot integrates with existing repository tools:

### Parse Timeline Tool

```bash
# Process match data
python tools/parse_timeline.py --input timeline.json --matchday 2025-11-07

# Then analyze in chatbot
python -c "
from chatbot import ChatbotAPI
api = ChatbotAPI(team_name='USAO U8')
print(api.send_message('/analyze-match 2025-11-07'))
"
```

## Conversation History

Access and export conversation history:

```python
api = ChatbotAPI(team_name="My Team")

# Chat
api.send_message("Hello")
api.send_message("/help-coach")

# Get history
history = api.get_history()
print(f"Total messages: {len(history)}")

# Export
api.export_history("session.json", format='json')
api.export_history("session.txt", format='txt')
```

## Advanced Usage

### Custom Memory Bank Path

```python
api = ChatbotAPI(
    team_name="My Team",
    memory_bank_path="/custom/path/to/.memory-bank"
)
```

### Session Management

```python
api = ChatbotAPI(team_name="My Team")

# Check if active
if api.is_active():
    response = api.send_message("Hello")

# End session
api.end_session()

# This will raise RuntimeError
# api.send_message("Hello")  # Error!
```

## Testing

Test the chatbot with the example script:

```bash
# Run all examples
python example_chatbot.py

# Interactive mode
python example_chatbot.py --interactive
```

## Contributing

To extend the chatbot:

1. Add new command handlers in `chatbot/coach_chatbot.py`
2. Register commands in the `commands` dictionary
3. Update documentation
4. Add examples to `example_chatbot.py`

## Support

For issues or questions:
- Check the chatmode specification: `.github/chatmodes/coach_assistant.chatmode.md`
- Review example usage: `example_chatbot.py`
- See this documentation: `chatbot/README.md`

## License

Part of the mystuff repository.
