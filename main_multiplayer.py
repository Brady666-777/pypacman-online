"""
Main entry point for PyPacman Multiplayer Client
"""

import sys
import os

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from client.multiplayer_client import MultiplayerClient


def main():
    """Main function to start the multiplayer client"""
    print("Starting PyPacman Multiplayer Client...")
    
    try:
        client = MultiplayerClient()
        client.run()
    except KeyboardInterrupt:
        print("\nShutting down client...")
    except Exception as e:
        print(f"Client error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Client stopped.")


if __name__ == "__main__":
    main()
