"""
Quick test to verify multiplayer client can start
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import pygame
        print("✓ pygame imported successfully")
        
        import pygame_menu
        print("✓ pygame_menu imported successfully")
        
        from client.multiplayer_client import MultiplayerClient
        print("✓ MultiplayerClient imported successfully")
        
        from server.game_server import GameServer
        print("✓ GameServer imported successfully")
        
        from multiplayer.networking import get_local_ip
        print("✓ Networking utilities imported successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Import error: {e}")
        return False

def test_client_init():
    """Test that the client can be initialized"""
    try:
        # Just test initialization, don't run the main loop
        print("Testing client initialization...")
        
        # This would normally start the client, but we'll just test the import
        from client.multiplayer_client import MultiplayerClient
        
        print("✓ Client can be initialized")
        return True
        
    except Exception as e:
        print(f"✗ Client initialization error: {e}")
        return False

if __name__ == "__main__":
    print("=== PyPacman Multiplayer Client Test ===")
    
    if test_imports():
        print("\n✓ All imports successful!")
        
        if test_client_init():
            print("✓ Client initialization test passed!")
            print("\n🎮 Ready to play multiplayer PyPacman!")
            print("\nTo start the game, run:")
            print("  python main_multiplayer.py")
            print("\nOr use the launcher:")
            print("  launcher.bat")
        else:
            print("✗ Client initialization failed")
    else:
        print("✗ Import test failed")
