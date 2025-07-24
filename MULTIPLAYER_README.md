# PyPacman Multiplayer

A multiplayer version of the classic Pacman game built with Python and Pygame.

## Quick Start

### Using the Launcher (Easiest)
1. Double-click `launcher.bat`
2. Choose your option:
   - **Option 1**: Start Multiplayer Client (Host or Join games)
   - **Option 2**: Start Dedicated Server
   - **Option 3**: Run Original Single Player Game
   - **Option 4**: Local Test (Host and Join on same computer)

### Manual Start

#### Start Multiplayer Client
```bash
python main_multiplayer.py
```

#### Start Dedicated Server
```bash
python server/main_server.py
```

#### Run Single Player
```bash
python main.py
```

## How to Play Multiplayer

### Hosting a Game
1. Start the multiplayer client
2. Enter your player name
3. Click "Host Game" - this will start a local server and connect you to it

### Joining a Game
1. Start the multiplayer client
2. Enter your player name
3. Click "Join Game"
4. Enter the server IP and port:
   - **Local/Same Computer**: `127.0.0.1:55000`
   - **Network**: Ask the host for their IP address and use port `55000`

### Dedicated Server
If you want to run a dedicated server:
1. Start the server with `python server/main_server.py`
2. Players can connect to your IP address on port 55000
3. Make sure to configure your firewall to allow port 55000

## Network Configuration

### For Local Testing
- Server IP: `127.0.0.1` or `localhost`
- Port: `55000`

### For Network Play
- Host needs to share their IP address (run `ipconfig` to find it)
- Port: `55000` (default)
- **Important**: Configure Windows Firewall to allow port 55000

## Requirements

- Python 3.7+
- pygame
- pygame-menu

Install requirements:
```bash
pip install pygame pygame-menu
```

## Project Structure

```
PyPacman/
├── launcher.bat              # Easy launcher for all game modes
├── main.py                   # Single player game
├── main_multiplayer.py       # Multiplayer client entry point
├── client/                   # Multiplayer client code
│   └── multiplayer_client.py
├── server/                   # Multiplayer server code
│   ├── main_server.py        # Server entry point
│   ├── game_server.py        # Server logic
│   └── game_simulator.py     # Game simulation
├── multiplayer/              # Shared multiplayer components
├── src/                      # Original game source code
├── assets/                   # Game assets (images, sounds)
└── levels/                   # Game levels and configurations
```

## Troubleshooting

### Cannot Connect to Server
1. Make sure the server is running
2. Check the IP address and port
3. Verify Windows Firewall settings
4. Try local test first (Option 4 in launcher)

### Performance Issues
- Multiplayer works best on local networks
- For internet play, stable connection required
- Maximum 4 players recommended

## Controls

- **Arrow Keys**: Move Pacman
- **ESC**: Return to menu (in-game)

Enjoy playing PyPacman Multiplayer!
