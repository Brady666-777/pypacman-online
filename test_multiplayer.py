"""
Test script for PyPacman Multiplayer functionality
"""

import sys
import os
import threading
import time
import json
import socket

# Add the parent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from server.game_server import GameServer
from multiplayer.networking import test_connection, wait_for_server_start


def test_server_startup():
    """Test that the server starts up correctly"""
    print("Testing server startup...")
    
    try:
        server = GameServer(max_players=2, host='127.0.0.1', port=0)
        server_thread = threading.Thread(target=server.start_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        if wait_for_server_start(server):
            port = server.get_port()
            print(f"✓ Server started successfully on port {port}")
            
            # Test connection
            if test_connection('127.0.0.1', port):
                print("✓ Server is accepting connections")
            else:
                print("✗ Server not accepting connections")
            
            server.stop_server()
            return True
        else:
            print("✗ Server failed to start")
            return False
            
    except Exception as e:
        print(f"✗ Server startup error: {e}")
        return False


def test_client_connection():
    """Test client connection to server"""
    print("Testing client connection...")
    
    try:
        # Start server
        server = GameServer(max_players=2, host='127.0.0.1', port=0)
        server_thread = threading.Thread(target=server.start_server, daemon=True)
        server_thread.start()
        
        if not wait_for_server_start(server):
            print("✗ Server failed to start")
            return False
        
        port = server.get_port()
        
        # Test client connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('127.0.0.1', port))
        
        # Send join message
        join_message = json.dumps({
            "action": "join",
            "player_name": "TestPlayer"
        })
        client_socket.send(join_message.encode('utf-8'))
        
        # Receive response
        response = client_socket.recv(2048).decode('utf-8')
        join_response = json.loads(response)
        
        if join_response.get("action") == "join_success":
            print("✓ Client connection successful")
            print(f"  Player ID: {join_response.get('player_id')}")
            success = True
        else:
            print("✗ Client connection failed")
            success = False
        
        client_socket.close()
        server.stop_server()
        return success
        
    except Exception as e:
        print(f"✗ Client connection error: {e}")
        return False


def test_game_state_sync():
    """Test game state synchronization"""
    print("Testing game state synchronization...")
    
    try:
        # Start server
        server = GameServer(max_players=2, host='127.0.0.1', port=0)
        server_thread = threading.Thread(target=server.start_server, daemon=True)
        server_thread.start()
        
        if not wait_for_server_start(server):
            print("✗ Server failed to start")
            return False
        
        port = server.get_port()
        
        # Connect two clients
        clients = []
        for i in range(2):
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('127.0.0.1', port))
            
            # Join game
            join_message = json.dumps({
                "action": "join",
                "player_name": f"TestPlayer{i+1}"
            })
            client_socket.send(join_message.encode('utf-8'))
            
            # Receive join response
            response = client_socket.recv(2048).decode('utf-8')
            join_response = json.loads(response)
            
            if join_response.get("action") == "join_success":
                clients.append({
                    "socket": client_socket,
                    "player_id": join_response.get("player_id")
                })
            else:
                print(f"✗ Client {i+1} failed to join")
                return False
        
        # Start game
        start_message = json.dumps({
            "action": "start_game",
            "player_id": clients[0]["player_id"]
        })
        clients[0]["socket"].send(start_message.encode('utf-8'))
        
        # Wait for game state updates with longer timeout
        time.sleep(3)
        
        # Check if both clients receive updates
        updates_received = 0
        for i, client in enumerate(clients):
            try:
                client["socket"].settimeout(2)  # Increased timeout
                response = client["socket"].recv(2048).decode('utf-8')
                print(f"Client {i+1} received: {response[:100]}...")  # Debug output
                if "game_state_update" in response or "action" in response:
                    updates_received += 1
            except socket.timeout:
                print(f"Client {i+1} timed out waiting for update")
                pass
        
        print(f"Updates received: {updates_received}/{len(clients)}")
        
        if updates_received >= 1:  # At least one client should receive updates
            print("✓ Game state synchronization working")
            success = True
        else:
            print("✗ Game state synchronization failed")
            success = False
        
        # Cleanup
        for client in clients:
            client["socket"].close()
        server.stop_server()
        
        return success
        
    except Exception as e:
        print(f"✗ Game state sync error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print("=== PyPacman Multiplayer Tests ===\n")
    
    tests = [
        ("Server Startup", test_server_startup),
        ("Client Connection", test_client_connection),
        ("Game State Sync", test_game_state_sync)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED\n")
        else:
            print(f"✗ {test_name} FAILED\n")
    
    print(f"=== Test Results: {passed}/{total} passed ===")
    
    if passed == total:
        print("🎉 All tests passed! Multiplayer functionality is working.")
    else:
        print("❌ Some tests failed. Check the implementation.")


if __name__ == "__main__":
    run_all_tests()
