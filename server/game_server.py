"""
PyPacman Multiplayer Game Server

This server handles the game logic for multiplayer PyPacman, including:
- Managing multiple Pacman players
- Ghost AI simulation
- Collision detection
- Score tracking
- Game state synchronization
"""

import json
import socket
import threading
import time
import uuid
from collections import deque
from _thread import start_new_thread, allocate_lock
from typing import Dict, List, Tuple, Any

from server.game_simulator import GameSimulator


class GameServer:
    def __init__(self, max_players: int = 4, host: str = "0.0.0.0", port: int = 0):
        self.host = host
        self.port = port
        self.max_players = max_players
        self.server_socket = None
        self.active_clients = 0
        self.running = False
        
        # Player management
        self.players: Dict[str, Dict[str, Any]] = {}
        self.player_positions: Dict[str, Tuple[int, int]] = {}
        self.lock = allocate_lock()
        
        # Game state
        self.game_state = {
            "players": {},
            "ghosts": {},
            "collectibles": {},
            "scores": {},
            "game_status": "waiting",  # waiting, playing, game_over
            "level": 1
        }
        
        # Game simulation
        self.simulator = GameSimulator()
        self.sim_delta = 1000 / 60  # 60 FPS simulation
        self.broadcast_delta = 1000 / 30  # 30 FPS broadcast
        self.last_sim = -float('inf')
        self.last_broadcast = -float('inf')
        self.action_queue = []
        
        # Start simulation thread
        start_new_thread(self.game_loop, ())
        
    def game_loop(self):
        """Main game simulation loop"""
        while self.running:
            current_time = time.time() * 1000
            
            # Simulate game logic
            sim_delta = current_time - self.last_sim
            if sim_delta > self.sim_delta:
                with self.lock:
                    self.game_state = self.simulator.simulate(self.action_queue, sim_delta)
                    self.action_queue = []
                    self.last_sim = current_time
            
            # Broadcast game state to clients
            broadcast_delta = current_time - self.last_broadcast
            if broadcast_delta > self.broadcast_delta:
                with self.lock:
                    self.broadcast_game_state()
                    self.last_broadcast = current_time
            
            time.sleep(0.001)  # Small sleep to prevent excessive CPU usage
    
    def start_server(self):
        """Start the game server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.running = True
            self.server_socket.listen(self.max_players)
            
            print(f"PyPacman Server started on {self.host}:{self.get_port()}")
            
            while self.running:
                try:
                    client_socket, client_addr = self.server_socket.accept()
                    print(f"New connection from {client_addr}")
                    start_new_thread(self.handle_client, (client_socket, client_addr))
                except Exception as e:
                    if self.running:
                        print(f"Error accepting connection: {e}")
                    break
                    
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop_server()
    
    def handle_client(self, client_socket: socket.socket, client_addr: tuple):
        """Handle individual client connections"""
        player_id = None
        
        try:
            while self.running:
                data = client_socket.recv(2048).decode('utf-8')
                if not data:
                    break
                
                try:
                    message = json.loads(data)
                    action = message.get('action')
                    
                    if action == 'join':
                        player_id = self.handle_player_join(client_socket, message)
                    elif action == 'disconnect':
                        player_id = message.get('player_id')
                        break
                    elif action == 'move':
                        self.handle_player_move(message)
                    elif action == 'start_game':
                        self.handle_start_game(message)
                    
                except json.JSONDecodeError:
                    print(f"Invalid JSON from {client_addr}")
                    
        except Exception as e:
            print(f"Client handler error: {e}")
        finally:
            if player_id:
                self.handle_player_disconnect(player_id)
            client_socket.close()
            self.active_clients -= 1
    
    def handle_player_join(self, client_socket: socket.socket, message: dict) -> str:
        """Handle a new player joining the game"""
        player_id = str(uuid.uuid4())
        player_name = message.get('player_name', f'Player_{player_id[:8]}')
        
        with self.lock:
            if len(self.players) >= self.max_players:
                error_msg = json.dumps({"action": "error", "message": "Game is full"})
                client_socket.send(error_msg.encode('utf-8'))
                return None
            
            # Add player to game
            self.players[player_id] = {
                "name": player_name,
                "socket": client_socket,
                "score": 0,
                "lives": 3,
                "position": self.simulator.get_spawn_position(len(self.players)),
                "direction": "right",
                "powered": False,
                "power_time": 0
            }
            
            # Add player to simulator
            spawn_pos = self.simulator.get_spawn_position(len(self.players) - 1)
            self.simulator.players[player_id] = {
                "position": spawn_pos,
                "direction": "right",
                "score": 0,
                "lives": 3,
                "powered": False,
                "power_time": 0
            }
            
            # Update game state
            self.game_state["players"][player_id] = {
                "name": player_name,
                "score": 0,
                "lives": 3,
                "position": spawn_pos,
                "direction": "right",
                "powered": False
            }
            
            # Send join confirmation
            response = json.dumps({
                "action": "join_success",
                "player_id": player_id,
                "game_state": self.game_state
            })
            client_socket.send(response.encode('utf-8'))
            
            print(f"Player {player_name} ({player_id}) joined the game")
            
            # Start game if we have enough players
            if len(self.players) >= 2 and self.game_state["game_status"] == "waiting":
                self.game_state["game_status"] = "ready"
        
        self.active_clients += 1
        return player_id
    
    def handle_player_move(self, message: dict):
        """Handle player movement updates"""
        player_id = message.get('player_id')
        direction = message.get('direction')
        position = message.get('position')
        
        if player_id not in self.players:
            return
        
        with self.lock:
            self.action_queue.append({
                "type": "move",
                "player_id": player_id,
                "direction": direction,
                "position": position
            })
    
    def handle_start_game(self, message: dict):
        """Handle game start request"""
        player_id = message.get('player_id')
        
        if player_id not in self.players:
            return
        
        with self.lock:
            if self.game_state["game_status"] == "ready" or len(self.players) >= 2:
                self.game_state["game_status"] = "playing"
                self.simulator.start_game()
                print("Game started!")
                
                # Force an immediate broadcast
                self.broadcast_game_state()
    
    def handle_player_disconnect(self, player_id: str):
        """Handle player disconnection"""
        with self.lock:
            if player_id in self.players:
                player_name = self.players[player_id]["name"]
                del self.players[player_id]
                del self.game_state["players"][player_id]
                print(f"Player {player_name} disconnected")
                
                # Stop game if not enough players
                if len(self.players) < 2 and self.game_state["game_status"] == "playing":
                    self.game_state["game_status"] = "waiting"
                    self.simulator.stop_game()
    
    def broadcast_game_state(self):
        """Broadcast current game state to all connected clients"""
        try:
            message = json.dumps({
                "action": "game_state_update",
                "game_state": self.game_state
            })
            
            disconnected_players = []
            for player_id, player_info in self.players.items():
                try:
                    player_info["socket"].send(message.encode('utf-8'))
                except:
                    disconnected_players.append(player_id)
            
            # Remove disconnected players
            for player_id in disconnected_players:
                self.handle_player_disconnect(player_id)
                
        except Exception as e:
            print(f"Broadcast error: {e}")
    
    def get_port(self) -> int:
        """Get the port the server is listening on"""
        if self.server_socket:
            return self.server_socket.getsockname()[1]
        return None
    
    def stop_server(self):
        """Stop the game server"""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        print("Server stopped")


if __name__ == "__main__":
    server = GameServer(max_players=4)
    try:
        server.start_server()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        server.stop_server()
