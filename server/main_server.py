"""
Standalone PyPacman Multiplayer Server
"""

import sys
import os
import argparse

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from server.game_server import GameServer


def main():
    """Main function to start the server"""
    parser = argparse.ArgumentParser(description='PyPacman Multiplayer Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host address to bind to')
    parser.add_argument('--port', type=int, default=55000, help='Port to bind to')
    parser.add_argument('--max-players', type=int, default=4, help='Maximum number of players')
    
    args = parser.parse_args()
    
    print(f"Starting PyPacman Multiplayer Server...")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Max Players: {args.max_players}")
    
    try:
        server = GameServer(
            max_players=args.max_players,
            host=args.host,
            port=args.port
        )
        server.start_server()
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Server error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("Server stopped.")


if __name__ == "__main__":
    main()
