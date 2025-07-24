# PyPacman Multiplayer - Quick Start Guide

## ✅ Installation Complete!

Pygame has been successfully installed (version 2.6.1) and all tests are passing!

## 🚀 How to Play

### Option 1: Use the Launcher (Recommended)

```bash
launcher.bat
```

This will show you a menu with options to:

1. Start Multiplayer Client (Host/Join Game)
2. Start Dedicated Server
3. Run Original Single Player Game
4. Test Multiplayer Functionality

### Option 2: Direct Commands

**Start Multiplayer Client:**

```bash
C:/Users/Brady/AppData/Local/Microsoft/WindowsApps/python3.11.exe main_multiplayer.py
```

**Start Dedicated Server:**

```bash
C:/Users/Brady/AppData/Local/Microsoft/WindowsApps/python3.11.exe server/main_server.py
```

**Test Multiplayer:**

```bash
C:/Users/Brady/AppData/Local/Microsoft/WindowsApps/python3.11.exe test_multiplayer.py
```

## 🎮 Game Instructions

1. **Host a Game:**

   - Run the multiplayer client
   - Enter your player name
   - Click "Host Game"
   - Share your IP address with friends
   - Wait for players to join
   - Click "Start Game"

2. **Join a Game:**

   - Run the multiplayer client
   - Enter your player name
   - Click "Join Game"
   - Enter the host's IP address and port
   - Click "Join"

3. **Controls:**
   - Arrow keys to move your Pacman
   - ESC to leave the game

## 🔧 Technical Details

- **Max Players:** 4
- **Default Port:** 55000
- **Network:** LAN/Local network
- **Game Features:**
  - Multiple Pacman players
  - Shared ghosts
  - Individual scoring
  - Power pellets affect all players

## ✨ What's New

This multiplayer version transforms the original PyPacman into a competitive multiplayer experience where:

- Up to 4 players can play simultaneously
- All players share the same maze and ghosts
- Each player has their own score and lives
- Power pellets affect ghosts for all players
- Real-time synchronization across all clients

## 🎯 Next Steps

You're ready to play! Try hosting a game and see how the multiplayer experience works. The implementation follows the air-hockey multiplayer pattern with:

- Client-server architecture
- Real-time game state synchronization
- Authoritative server for game logic
- Smooth multiplayer experience

Have fun playing multiplayer PyPacman! 🎮
