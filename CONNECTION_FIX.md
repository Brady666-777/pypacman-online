# 🎮 PyPacman Multiplayer - Connection Fix Guide

## ❌ Problem: "Connection refused" Error (WinError 10061)

You're getting this error because **no server is running** on port 55000.

## ✅ Solution: Start the Server First!

### Step 1: Start the Server
Before anyone can join, someone must start the server:

```bash
# In the PyPacman directory, run:
python start_server.py
```

You should see output like:
```
🎮 PyPacman Multiplayer Server
========================================
Starting server on port 55000...
Players can connect using:
  IP: 127.0.0.1 (local)
  Port: 55000

Press Ctrl+C to stop the server
========================================
PyPacman Server started on 0.0.0.0:55000
```

### Step 2: Test the Connection
Once the server is running, test it:

```bash
python test_connection.py
```

This should show: "✅ SUCCESS: Server is running and accepting connections!"

### Step 3: Now Clients Can Join
With the server running, clients can connect:

```bash
python client/multiplayer_client.py
```

Use these connection details:
- **IP**: `127.0.0.1` (for local network)
- **Port**: `55000`

## 🌐 For Network Games (Different Computers)

If you want to play across different computers on the same network:

### On the Server Computer:
1. **Start the server**: `python start_server.py`
2. **Find the computer's IP address**:
   - Windows: `ipconfig` (look for IPv4 Address)
   - Mac/Linux: `ifconfig` or `ip addr`
3. **Share the IP address** with other players

### On Client Computers:
1. **Start the client**: `python client/multiplayer_client.py`
2. **Use the server's IP address** instead of 127.0.0.1
3. **Use port 55000**

## 🔧 Troubleshooting Checklist

- [ ] Server is running (you see "PyPacman Server started on 0.0.0.0:55000")
- [ ] Using correct IP address (127.0.0.1 for local, server's IP for network)
- [ ] Using correct port (55000)
- [ ] Firewall allows connections on port 55000
- [ ] No other program is using port 55000

## 🚀 Quick Test

Run this to verify everything works:

```bash
# Terminal 1: Start server
python start_server.py

# Terminal 2: Test connection
python test_connection.py

# Terminal 3: Start client
python client/multiplayer_client.py
```

The server **must be running first** before anyone can connect!
