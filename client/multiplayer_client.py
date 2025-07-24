"""
PyPacman Multiplayer Client

This module handles the client-side game interface for multiplayer PyPacman
"""

import json
import socket
import threading
import time
from collections import deque
from typing import Dict, Any, Optional

import pygame
import pygame_menu

# Import existing game components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.configs import SCREEN_WIDTH, SCREEN_HEIGHT, Colors
from src.gui.screen_management import ScreenManager
from src.game.state_management import GameState
from src.sounds import SoundManager


class MultiplayerClient:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("PyPacman Multiplayer")
        
        # Network settings
        self.server_socket: Optional[socket.socket] = None
        self.server_ip = "127.0.0.1"  # Default to localhost
        self.server_port = 55000  # Default server port
        self.player_id: Optional[str] = None
        self.player_name = ""
        
        # Game state
        self.game_state = GameState()
        self.multiplayer_game_state = {}
        self.game_state_buffer = deque(maxlen=100)
        self.buffer_lock = threading.Lock()
        self.running = True
        self.connected = False
        self.listening_thread = None
        
        # Game objects
        self.all_sprites = pygame.sprite.Group()
        self.gui = ScreenManager(self.screen, self.game_state, self.all_sprites)
        self.game_runner = None
        
        # Menu system
        self.current_menu = "main"
        self.setup_menus()
        
        # Sounds
        self.sound_manager = SoundManager()
        self.initialize_sounds()
        
        # Network timing
        self.last_packet_sent = 0
        self.packet_send_rate = 1000 / 20  # 20 packets per second
        
    def setup_menus(self):
        """Setup the game menus"""
        # Main menu
        self.main_menu = pygame_menu.Menu('PyPacman Multiplayer', SCREEN_WIDTH, SCREEN_HEIGHT,
                                         theme=pygame_menu.themes.THEME_BLUE)
        
        self.name_input = self.main_menu.add.text_input('Player Name: ', default='Player')
        self.main_menu.add.button('Host Game', self.host_game)
        self.main_menu.add.button('Join Game', self.show_join_menu)
        self.main_menu.add.button('Quit', self.quit_game)
        
        # Join game menu
        self.join_menu = pygame_menu.Menu('Join Game', SCREEN_WIDTH, SCREEN_HEIGHT,
                                         theme=pygame_menu.themes.THEME_BLUE)
        
        self.ip_input = self.join_menu.add.text_input('Server IP: ', default='127.0.0.1')
        self.port_input = self.join_menu.add.text_input('Port: ', default='55000')
        self.join_menu.add.button('Join', self.join_game)
        self.join_menu.add.button('Join Local (127.0.0.1)', self.join_localhost)
        self.join_menu.add.button('Join Network (192.168.0.167)', self.join_network)
        self.join_menu.add.button('Back', self.show_main_menu)
        
        # Lobby menu
        self.lobby_menu = pygame_menu.Menu('Game Lobby', SCREEN_WIDTH, SCREEN_HEIGHT,
                                          theme=pygame_menu.themes.THEME_GREEN)
        
        self.lobby_info = self.lobby_menu.add.label('Waiting for players...')
        self.lobby_menu.add.button('Start Game', self.start_game)
        self.lobby_menu.add.button('Leave', self.leave_game)
    
    def initialize_sounds(self):
        """Initialize sound effects"""
        try:
            self.sound_manager.load_sound("dot", "assets/sounds/pacman_chomp.wav", channel=0)
            self.sound_manager.load_sound("death", "assets/sounds/pacman_death.wav", 0.7, 500, 1)
            self.sound_manager.load_sound("eat_ghost", "assets/sounds/pacman_eatghost.wav", 0.6, 100, 2)
            self.sound_manager.set_background_music("assets/sounds/backgroud.mp3")
        except Exception as e:
            print(f"Sound initialization error: {e}")
    
    def host_game(self):
        """Host a new game"""
        self.player_name = self.name_input.get_value()
        if not self.player_name:
            return
        
        # Start local server
        self.start_local_server()
        
        # Connect to local server
        self.server_ip = "127.0.0.1"
        if self.connect_to_server():
            self.current_menu = "lobby"
    
    def start_local_server(self):
        """Start a local game server"""
        try:
            from server.game_server import GameServer
            self.local_server = GameServer(max_players=4)
            self.server_thread = threading.Thread(target=self.local_server.start_server, daemon=True)
            self.server_thread.start()
            
            # Wait for server to start
            time.sleep(1)
            self.server_port = self.local_server.get_port()
            
        except Exception as e:
            print(f"Failed to start local server: {e}")
    
    def show_join_menu(self):
        """Show the join game menu"""
        self.current_menu = "join"
    
    def show_main_menu(self):
        """Show the main menu"""
        self.current_menu = "main"
    
    def join_game(self):
        """Join an existing game"""
        self.player_name = self.name_input.get_value()
        self.server_ip = self.ip_input.get_value()
        
        try:
            self.server_port = int(self.port_input.get_value())
        except ValueError:
            print("Invalid port number")
            return
        
        if self.connect_to_server():
            self.current_menu = "lobby"
    
    def join_localhost(self):
        """Quick join to localhost server"""
        self.player_name = self.name_input.get_value()
        self.server_ip = "127.0.0.1"
        self.server_port = 55000
        
        # Update inputs to show what we're connecting to
        self.ip_input.set_value("127.0.0.1")
        self.port_input.set_value("55000")
        
        if self.connect_to_server():
            self.current_menu = "lobby"
    
    def join_network(self):
        """Quick join to network server"""
        self.player_name = self.name_input.get_value()
        self.server_ip = "192.168.0.167"
        self.server_port = 55000
        
        # Update inputs to show what we're connecting to
        self.ip_input.set_value("192.168.0.167")
        self.port_input.set_value("55000")
        
        if self.connect_to_server():
            self.current_menu = "lobby"
    
    def connect_to_server(self) -> bool:
        """Connect to the game server"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect((self.server_ip, self.server_port))
            
            # Send join request
            join_message = json.dumps({
                "action": "join",
                "player_name": self.player_name
            })
            self.server_socket.send(join_message.encode('utf-8'))
            
            # Wait for response
            response = self.server_socket.recv(2048).decode('utf-8')
            join_response = json.loads(response)
            
            if join_response.get("action") == "join_success":
                self.player_id = join_response.get("player_id")
                self.multiplayer_game_state = join_response.get("game_state", {})
                self.connected = True
                
                # Start listening for game updates
                self.listening_thread = threading.Thread(target=self.listen_for_updates, daemon=True)
                self.listening_thread.start()
                
                print(f"Connected to server as {self.player_name}")
                return True
            else:
                print(f"Failed to join: {join_response.get('message', 'Unknown error')}")
                return False
                
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def listen_for_updates(self):
        """Listen for game state updates from server"""
        while self.running and self.connected:
            try:
                data = self.server_socket.recv(2048).decode('utf-8')
                if not data:
                    break
                
                # Handle multiple messages
                messages = data.split('\n')
                for message in messages:
                    if message.strip():
                        try:
                            update = json.loads(message)
                            
                            with self.buffer_lock:
                                self.game_state_buffer.append(update)
                                
                        except json.JSONDecodeError:
                            continue
                            
            except Exception as e:
                print(f"Listen error: {e}")
                break
        
        self.connected = False
    
    def process_game_updates(self):
        """Process pending game state updates"""
        with self.buffer_lock:
            while self.game_state_buffer:
                update = self.game_state_buffer.popleft()
                action = update.get('action')
                
                if action == 'game_state_update':
                    self.multiplayer_game_state = update.get('game_state', {})
                    self.update_local_game_state()
    
    def update_local_game_state(self):
        """Update local game state from multiplayer state"""
        if not self.multiplayer_game_state:
            return
        
        # Update player positions and scores
        players = self.multiplayer_game_state.get('players', {})
        
        # Update lobby info
        if self.current_menu == "lobby":
            player_count = len(players)
            status = self.multiplayer_game_state.get('game_status', 'waiting')
            self.lobby_info.set_title(f"Players: {player_count}/4 - Status: {status}")
        
        # Update game state for playing
        elif self.current_menu == "game":
            # Update player positions, scores, etc.
            pass
    
    def start_game(self):
        """Request to start the game"""
        if not self.connected:
            return
        
        start_message = json.dumps({
            "action": "start_game",
            "player_id": self.player_id
        })
        
        try:
            self.server_socket.send(start_message.encode('utf-8'))
            
            # Initialize game runner
            from multiplayer.game_runner import MultiplayerGameRunner
            self.game_runner = MultiplayerGameRunner(self)
            self.current_menu = "game"
            
        except Exception as e:
            print(f"Failed to start game: {e}")
    
    def leave_game(self):
        """Leave the current game"""
        if self.connected:
            disconnect_message = json.dumps({
                "action": "disconnect",
                "player_id": self.player_id
            })
            
            try:
                self.server_socket.send(disconnect_message.encode('utf-8'))
            except:
                pass
            
            self.disconnect()
        
        self.current_menu = "main"
    
    def disconnect(self):
        """Disconnect from server"""
        self.connected = False
        if self.server_socket:
            self.server_socket.close()
            self.server_socket = None
        self.player_id = None
    
    def send_player_input(self, direction: str, position: tuple):
        """Send player input to server"""
        if not self.connected:
            return
        
        current_time = time.time() * 1000
        if current_time - self.last_packet_sent < self.packet_send_rate:
            return
        
        message = json.dumps({
            "action": "move",
            "player_id": self.player_id,
            "direction": direction,
            "position": position
        })
        
        try:
            self.server_socket.send(message.encode('utf-8'))
            self.last_packet_sent = current_time
        except Exception as e:
            print(f"Failed to send input: {e}")
    
    def handle_input(self, event):
        """Handle keyboard input"""
        if event.type == pygame.KEYDOWN:
            if self.current_menu == "game":
                # Handle game input
                direction = None
                if event.key == pygame.K_UP:
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                elif event.key == pygame.K_LEFT:
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
                
                if direction:
                    # Get current position (would need to be tracked)
                    position = (0, 0)  # Placeholder
                    self.send_player_input(direction, position)
    
    def quit_game(self):
        """Quit the game"""
        self.running = False
        self.disconnect()
    
    def run(self):
        """Main game loop"""
        clock = pygame.time.Clock()
        
        while self.running:
            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.quit_game()
                else:
                    self.handle_input(event)
            
            # Process game updates
            self.process_game_updates()
            
            # Clear screen
            self.screen.fill(Colors.BLACK)
            
            # Draw current menu/game
            if self.current_menu == "main":
                self.main_menu.update(events)
                self.main_menu.draw(self.screen)
            elif self.current_menu == "join":
                self.join_menu.update(events)
                self.join_menu.draw(self.screen)
            elif self.current_menu == "lobby":
                self.lobby_menu.update(events)
                self.lobby_menu.draw(self.screen)
            elif self.current_menu == "game":
                # Use game runner for game loop
                if self.game_runner:
                    try:
                        self.game_runner.run_game_loop()
                        return  # Exit main loop when game ends
                    except Exception as e:
                        print(f"Game runner error: {e}")
                        self.current_menu = "main"  # Return to main menu on error
                else:
                    # Fallback if game runner not initialized
                    self.current_menu = "main"
            
            # Update display
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()


if __name__ == "__main__":
    client = MultiplayerClient()
    client.run()
