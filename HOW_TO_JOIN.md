# How to Join a PyPacman Multiplayer Game

## Quick Start Guide

### Step 1: Start the Server

First, someone needs to run the game server. You have three options:

**Option 1 - Easy startup (Recommended):**
```bash
python start_server.py
```

**Option 2 - Using main server:**
```bash
python server/main_server.py
```

**Option 3 - Direct server:**
```bash
python server/game_server.py
```

The server will start on `localhost:55000` by default.

### Step 2: Start the Client

Run the multiplayer client:

```bash
# In the PyPacman directory
python client/multiplayer_client.py
```

### Step 3: Join the Game

1. **Enter your name** in the "Player Name" field
2. **Click "Join Game"**
3. **Enter server details**:
   - Server IP: `127.0.0.1` (for local games) or the host's IP address
   - Port: `55000` (default port)
4. **Click "Join"**

### Step 4: Wait in Lobby

- You'll enter the game lobby
- Wait for other players to join
- The host can start the game when ready

### Step 5: Play the Game

- Use **Arrow keys** to move your Pacman
- Press **ESC** to leave the game

## Game Controls

| Key  | Action      |
| ---- | ----------- |
| ↑↓←→ | Move Pacman |
| ESC  | Leave game  |

## Game Features

The multiplayer PyPacman game allows multiple players to compete in the classic Pacman experience:

- Multiple players can play simultaneously
- Each player controls their own Pacman
- Compete for high scores by collecting dots and eating ghosts
- Real-time multiplayer synchronization

## Network Setup

### For Local Games (Same Computer)

- Server IP: `127.0.0.1` or `localhost`
- Port: `55000`

### For Network Games (Different Computers)

- Server IP: The IP address of the computer running the server
- Port: `55000` (or whatever port the server is using)
- Make sure the server's firewall allows connections on this port

## Troubleshooting

### ❌ "Connection refused" Error (WinError 10061)

This means no server is running on the specified port. To fix:

1. **Make sure the server is actually running**:
   ```bash
   python start_server.py
   ```
   You should see: "PyPacman Server started on 0.0.0.0:55000"

2. **Check if the server started successfully**:
   - Look for error messages in the server terminal
   - Make sure port 55000 isn't being used by another program

3. **Verify the port**:
   - Server should show it's running on port 55000
   - Client should connect to port 55000

### Cannot Connect to Server

1. **Verify server is running** and shows "Server started on 0.0.0.0:55000"
2. **Check the IP address and port number** in the client
3. **For local games**: Use `127.0.0.1` and port `55000`
4. **For network games**: Use the server computer's IP address
5. **Check firewall settings** - port 55000 must be allowed

### Game Not Starting

1. Make sure at least 2 players are in the lobby
2. Wait for the host to start the game
3. Check that all players are connected

### Lag or Disconnection

1. Check network connection
2. Try reducing the number of players
3. Restart the client and reconnect

## Example Session

```bash
# Terminal 1: Start server
python start_server.py

# Terminal 2: Start client 1
python client/multiplayer_client.py

# Terminal 3: Start client 2
python client/multiplayer_client.py
```

Each client will show a menu where you can enter your name and join the game!
