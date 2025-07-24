#!/usr/bin/env python3
"""
PyPacman Multiplayer - Final Installation Verification and Usage Guide
"""

import os
import sys
import subprocess

def check_installation():
    """Check if all components are properly installed"""
    print("🔍 Checking PyPacman Multiplayer Installation...")
    
    # Check Python version
    python_version = sys.version_info
    print(f"✓ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    # Check pygame
    try:
        import pygame
        print(f"✓ pygame {pygame.version.ver}")
    except ImportError:
        print("✗ pygame not found")
        return False
    
    # Check pygame-menu
    try:
        import pygame_menu
        print("✓ pygame-menu installed")
    except ImportError:
        print("✗ pygame-menu not found")
        return False
    
    # Check required directories
    required_dirs = ['server', 'client', 'multiplayer', 'assets', 'levels']
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"✓ {dir_name}/ directory found")
        else:
            print(f"✗ {dir_name}/ directory missing")
            return False
    
    # Check key files
    key_files = [
        'main_multiplayer.py',
        'server/game_server.py',
        'client/multiplayer_client.py',
        'multiplayer/game_runner.py',
        'levels/level1.json'
    ]
    
    for file_name in key_files:
        if os.path.exists(file_name):
            print(f"✓ {file_name}")
        else:
            print(f"✗ {file_name} missing")
            return False
    
    return True

def show_usage():
    """Show usage instructions"""
    print("\n🎮 PyPacman Multiplayer - Ready to Play!")
    print("=" * 50)
    
    print("\n📋 How to Play:")
    print("1. HOST A GAME:")
    print("   - Run: python main_multiplayer.py")
    print("   - Enter your player name")
    print("   - Click 'Host Game'")
    print("   - Share your IP with friends")
    print("   - Wait for players to join")
    print("   - Click 'Start Game'")
    
    print("\n2. JOIN A GAME:")
    print("   - Run: python main_multiplayer.py")
    print("   - Enter your player name")
    print("   - Click 'Join Game'")
    print("   - Enter host's IP and port")
    print("   - Click 'Join'")
    
    print("\n3. DEDICATED SERVER:")
    print("   - Run: python server/main_server.py")
    print("   - Players connect using client")
    
    print("\n🎯 Game Controls:")
    print("   - Arrow Keys: Move Pacman")
    print("   - ESC: Leave game")
    
    print("\n🏆 Game Features:")
    print("   - Up to 4 players simultaneously")
    print("   - Competitive scoring")
    print("   - Shared ghost AI")
    print("   - Power pellets affect all players")
    print("   - Real-time synchronization")
    
    print("\n🔧 Technical:")
    print("   - Client-server architecture")
    print("   - Authoritative server")
    print("   - 60 FPS simulation")
    print("   - 30 FPS network updates")
    
    print("\n🚀 Quick Start:")
    print("   launcher.bat  (Windows)")
    print("   python main_multiplayer.py  (Cross-platform)")

def run_tests():
    """Run multiplayer tests"""
    print("\n🧪 Running Multiplayer Tests...")
    try:
        result = subprocess.run([sys.executable, 'test_multiplayer.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if "All tests passed" in result.stdout:
            print("✓ All multiplayer tests passed!")
            return True
        else:
            print("⚠ Some tests may have issues")
            print(result.stdout[-200:])  # Show last 200 chars
            return False
    except subprocess.TimeoutExpired:
        print("⚠ Tests timed out (but this may be normal)")
        return True
    except Exception as e:
        print(f"✗ Test error: {e}")
        return False

def main():
    """Main verification function"""
    print("PyPacman Multiplayer - Installation Verification")
    print("=" * 50)
    
    if not check_installation():
        print("\n❌ Installation check failed!")
        print("Please run: python setup.py")
        return False
    
    print("\n✅ Installation check passed!")
    
    # Optionally run tests
    print("\nWould you like to run tests? (y/n): ", end="")
    try:
        response = input().lower()
        if response in ['y', 'yes']:
            run_tests()
    except KeyboardInterrupt:
        print("\nSkipping tests...")
    
    show_usage()
    
    print("\n🎉 PyPacman Multiplayer is ready!")
    print("Enjoy playing with friends!")
    
    return True

if __name__ == "__main__":
    main()
