# PyPacman Multiplayer

A real-time multiplayer version of the classic Pac-Man game built with Python and Pygame.

## Features

- **Real-time Multiplayer**: Up to 4 players can play simultaneously
- **Client-Server Architecture**: Authoritative server for cheat prevention
- **Synchronized Game State**: All players see the same game state
- **Networked Physics**: Collision detection and game logic run on the server
- **Player Lobbies**: Wait for players and start games together
- **Host or Join**: Players can host their own games or join existing ones

## Game Features

- Multiple Pac-Man players in the same maze
- Shared ghosts that chase all players
- Competitive scoring system
- Power pellets affect all ghosts for all players
- Lives system for each player
- Real-time position synchronization

## Installation

1. Install Python 3.7 or higher
2. Install required dependencies:
   ```bash
   pip install -r requirements_multiplayer.txt
   ```

## Quick Start

### Option 1: Host a Game (Recommended)

1. Run the multiplayer client:
   ```bash
   python main_multiplayer.py
   ```
2. Enter your player name
3. Click "Host Game"
4. Share your IP address with other players
5. Wait for players to join, then click "Start Game"

### Option 2: Join a Game

1. Run the multiplayer client:
   ```bash
   python main_multiplayer.py
   ```
2. Enter your player name
3. Click "Join Game"
4. Enter the host's IP address and port
5. Click "Join"

### Option 3: Dedicated Server

1. Start a dedicated server:
   ```bash
   python server/main_server.py --host 0.0.0.0 --port 55000
   ```
2. Players can join using the client

## Controls

- **Arrow Keys**: Move your Pac-Man
- **ESC**: Leave game (return to lobby)

## Network Architecture

The game uses a client-server architecture inspired by the air-hockey example:

### Server (`server/`)

- `game_server.py`: Main server handling client connections
- `game_simulator.py`: Server-side game logic and physics
- `main_server.py`: Standalone server launcher

### Client (`client/`)

- `multiplayer_client.py`: Main client interface with menus
- Game networking and server communication

### Shared (`multiplayer/`)

- `game_runner.py`: Client-side game rendering and input handling
- `networking.py`: Networking utilities

## Server Features

- **Authoritative Simulation**: All game logic runs on the server
- **Player Management**: Handle joins, disconnects, and player states
- **Ghost AI**: Centralized ghost behavior and pathfinding
- **Collision Detection**: Server-side collision detection
- **Score Management**: Track and synchronize player scores
- **Game State Broadcasting**: Send updates to all clients

## Client Features

- **Menu System**: Host/join lobbies with player management
- **Real-time Rendering**: Smooth interpolation of game objects
- **Input Handling**: Send player inputs to server
- **Game State Synchronization**: Receive and apply server updates
- **UI Elements**: Player scores, lives, and connection status

## Technical Implementation

Based on the air-hockey multiplayer example, the game implements:

1. **Socket-based Communication**: TCP sockets for reliable message delivery
2. **JSON Message Protocol**: Structured communication between client and server
3. **Game State Updates**: Regular broadcasts of complete game state
4. **Action Queue System**: Server processes player actions in order
5. **Threaded Architecture**: Separate threads for network I/O and game logic

## Message Types

### Client → Server

- `join`: Join the game with player name
- `move`: Send player movement input
- `start_game`: Request to start the game
- `disconnect`: Leave the game

### Server → Client

- `join_success`: Confirm successful join with player ID
- `game_state_update`: Complete game state update
- `error`: Error messages

## Configuration

### Server Configuration

- `max_players`: Maximum number of players (default: 4)
- `host`: Server bind address (default: 0.0.0.0)
- `port`: Server port (default: 55000)

### Game Configuration

- Simulation rate: 60 FPS
- Network update rate: 30 FPS
- Player input rate: 20 FPS

## Differences from Original PyPacman

1. **Multiple Players**: Support for 2-4 simultaneous Pac-Man players
2. **Networked Architecture**: Client-server instead of local-only
3. **Shared Game State**: All players interact with the same ghosts and maze
4. **Competitive Scoring**: Individual player scores and lives
5. **Real-time Synchronization**: Smooth multiplayer experience

## Known Limitations

1. **LAN Only**: Currently designed for local network play
2. **No Spectators**: Only players can connect
3. **Fixed Maze**: Single level (level1.json)
4. **No Reconnection**: Players must restart if disconnected

## Future Enhancements

- [ ] Multiple maze levels
- [ ] Spectator mode
- [ ] Internet play support
- [ ] Player reconnection
- [ ] Tournament mode
- [ ] Customizable game rules
- [ ] Voice chat integration
- [ ] Leaderboards

## Troubleshooting

### Connection Issues

- Check firewall settings
- Ensure all players are on the same network
- Verify IP address and port are correct
- Try different port numbers if blocked

### Performance Issues

- Reduce network update rate
- Check network latency
- Ensure adequate bandwidth

### Game Sync Issues

- Restart server if game state becomes corrupted
- Check for packet loss
- Verify all clients have same game version

## Development

To modify the game:

1. **Server Logic**: Edit `server/game_simulator.py`
2. **Client Interface**: Edit `client/multiplayer_client.py`
3. **Game Rendering**: Edit `multiplayer/game_runner.py`
4. **Network Protocol**: Edit message handling in both client and server

The codebase maintains compatibility with the original PyPacman while adding multiplayer capabilities through the networking layer.
