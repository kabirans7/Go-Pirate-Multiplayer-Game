# GoPirate - Final Project (CSAS 2124)

## Overview

GoPirate is a multiplayer, turn-based battle game with integrated player chat and a smart chatbot assistant. Players choose unique characters, take turns battling, and can chat with each other and the bot during the game. The game uses object-oriented programming, design patterns, SQLite database storage, and a full GUI made with Tkinter.

## Features

- Character selection screen with unique stats  
- Turn-based battle with attack, defend, and special move actions  
- Player-to-player chat during battle  
- Chatbot helper that responds to game-related questions  
- Escalation to a simulated live agent if the chatbot cannot answer  
- SQLite database saves all game sessions, chat logs, bot responses, and unknown queries  
- GUI updates player stats, logs, and chat messages live  

## How to Run

Navigate to the project folder `final_pirate`:

For MacOS / Linux:  
cd final_pirate  
python3 -m main.server_gui_main   (Start server)  
python3 -m main.client_gui_main   (Start client 1)  
python3 -m main.client_gui_main   (Start client 2)  
python3 -m main.client_gui_main   (Start client 3)  

For Windows:  
cd final_pirate  
py -m main.server_gui_main  
py -m main.client_gui_main  
py -m main.client_gui_main  
py -m main.client_gui_main  

The server must be running before clients connect. All three clients must join to start a game.

## File Structure

- battle/: Battle system files  
- chatbot/: Chatbot logic and backend files  
- main/: Server, client, and database manager  
- data/: SQLite game database (empty folder required for initial use if .db file is not generated yet)
- test files in root: pytest files for chatbot, database, and battle system  

## Dependencies

- Python (Run on 3.13) 
- Tkinter (comes with Python)  
- pytest (for testing)

## Testing

Run tests from inside wd `final_pirate/`:  
pytest

Tests include:  
- Battle tests: Attack reduces HP; defend reduces damage  
- Chatbot tests: Responds correctly to known game questions; escalates unrecognized ones to human simulation; stable and deterministic behavior  
- Database tests: Inserts and retrieves player chats, bot logs, and unknown queries into a temporary database  

All tests pass.

## Design Patterns Used

- Creational: Factory (CharacterFactory), Singleton (DatabaseManager)  
- Structural: Adapter (chatbot integration), Facade (server-client communication)  
- Behavioral: Strategy (battle action handling), Observer (bot escalation to human), Command (chat commands)  

## Notes

- We used a fixed response for human escalation to improve test stability.  
- The system is modular and easily expandable for future features.  

