# 🌐 PyPacman Network Connection Setup

## ✅ **Configuration Complete!**

Your client is now configured to connect to the server at:
- **Server IP**: `192.168.0.167`
- **Port**: `7885`

## 🎮 **How to Connect**

### Option 1: Quick Connect (Recommended)
```bash
python connect_7885.py
```

### Option 2: Regular Client
```bash
python client/multiplayer_client.py
```
- The connection details are pre-filled
- Just click "Join Game"

### Option 3: Manual Entry
If you need to change the settings:
- Server IP: `192.168.0.167`
- Port: `7885`

## 🔍 **Connection Test**

Test the connection first:
```bash
python test_connection.py
```

This will verify if the server is reachable from your computer.

## 🛡️ **Firewall Settings**

Make sure the server computer (192.168.0.167) allows connections on port **7885**:

### Windows Firewall:
1. Open Windows Defender Firewall
2. Click "Allow an app or feature through Windows Defender Firewall"
3. Add Python and allow it through both Private and Public networks
4. Or create a specific rule for port 7885

### Alternative: Quick test
Try disabling the firewall temporarily to test if that's the issue.

## 📊 **Server Information**
- **Server Computer IP**: 192.168.0.167
- **Server Port**: 7885
- **Network**: Same local network (192.168.0.x)
- **Gateway**: 192.168.0.1

## 🚀 **Quick Start**

1. **Server computer** runs: The server is already running ✅
2. **Your computer** runs: `python client/multiplayer_client.py`
3. **Connect** and play!

## 🔧 **Troubleshooting**

If connection fails:
1. **Ping test**: `ping 192.168.0.167`
2. **Port test**: `telnet 192.168.0.167 7885`
3. **Firewall**: Check Windows Firewall on server
4. **Network**: Ensure both computers are on same Wi-Fi/network

Everything is configured and ready to connect! 🎉
