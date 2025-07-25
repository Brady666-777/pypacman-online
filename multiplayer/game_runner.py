"""
Multiplayer PyPacman Game Runner

This module integrates the existing PyPacman game with multiplayer functionality
"""

import threading
import time
import json
from typing import Dict, List, Tuple, Any

import pygame

# Import existing game components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.configs import SCREEN_WIDTH, SCREEN_HEIGHT, Colors
from src.game.state_management import GameState
from src.game.event_management import EventHandler
from src.gui.screen_management import ScreenManager
from src.sprites.pacman import Pacman
from src.sprites.ghosts import GhostManager
from src.sounds import SoundManager


class MultiplayerGameRunner:
    def __init__(self, client_instance):
        self.client = client_instance
        self.screen = client_instance.screen
        
        # Game state
        self.game_state = GameState()
        self.multiplayer_players = {}
        self.local_player_id = None
        
        # Game objects
        self.all_sprites = pygame.sprite.Group()
        self.pacman_sprites = pygame.sprite.Group()
        self.ghost_sprites = pygame.sprite.Group()
        
        # Game components
        self.event_handler = EventHandler(self.screen, self.game_state)
        self.gui = ScreenManager(self.screen, self.game_state, self.all_sprites)
        
        # Load game level
        self.load_level()
        
        # Initialize game objects
        self.setup_game_objects()
        
        # Create local player immediately
        self.setup_local_player()
        
        # Sounds
        self.sound_manager = SoundManager()
        self.initialize_sounds()
        
        # Timing
        self.last_update = time.time()
        
    def load_level(self):
        """Load the game level"""
        import json
        try:
            with open('levels/level1.json', 'r') as f:
                level_data = json.load(f)
                self.matrix = level_data['matrix']
                # Calculate grid positioning (like single-player version)
                from src.utils.coord_utils import place_elements_offset
                from src.configs import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE
                
                num_rows = level_data.get('num_rows', 32)
                num_cols = level_data.get('num_cols', 35)
                
                self.start_x, self.start_y = place_elements_offset(
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT,
                    CELL_SIZE[0] * num_cols,
                    CELL_SIZE[0] * num_rows,
                    0.5,
                    0.5,
                )
                
                self.pacman_start_pos = tuple(level_data.get('pacman_start', [17, 16]))
                
                # Extract ghost positions from level data or use defaults
                self.ghost_den = tuple(level_data.get('ghost_den', [14, 15]))
                self.ghost_positions = {
                    'blinky': tuple(level_data.get('ghost_den', [14, 15])),
                    'pinky': (level_data.get('ghost_den', [14, 15])[0], level_data.get('ghost_den', [14, 15])[1] + 1),
                    'inky': (level_data.get('ghost_den', [14, 15])[0] - 1, level_data.get('ghost_den', [14, 15])[1]),
                    'clyde': (level_data.get('ghost_den', [14, 15])[0] + 1, level_data.get('ghost_den', [14, 15])[1])
                }
        except Exception as e:
            print(f"Failed to load level: {e}")
            # Create minimal level with proper grid positioning
            from src.utils.coord_utils import place_elements_offset
            from src.configs import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE
            
            self.matrix = [['wall'] * 35 for _ in range(35)]
            
            num_rows, num_cols = 32, 35
            self.start_x, self.start_y = place_elements_offset(
                SCREEN_WIDTH,
                SCREEN_HEIGHT,
                CELL_SIZE[0] * num_cols,
                CELL_SIZE[0] * num_rows,
                0.5,
                0.5,
            )
            
            self.pacman_start_pos = (17, 16)
            self.ghost_den = (14, 15)
            self.ghost_positions = {'blinky': (14, 15), 'pinky': (14, 16), 'inky': (13, 15), 'clyde': (15, 15)}
    
    def setup_game_objects(self):
        """Initialize game objects"""
        # Create ghost manager with correct parameters
        self.ghost_manager = GhostManager(
            self.screen,
            self.game_state,
            self.matrix,
            self.ghost_den,  # ghost_matrix_pos: single position where ghosts start
            (self.start_x, self.start_y)  # grid_start_pos: grid positioning coordinates
        )
        
        # Add ghosts to sprite groups
        for ghost in self.ghost_manager.ghosts_list:
            self.ghost_sprites.add(ghost)
            self.all_sprites.add(ghost)
    
    def setup_local_player(self):
        """Setup the local player"""
        if self.client.player_id and self.client.player_id not in self.multiplayer_players:
            # Create local player at the default starting position
            pacman = self.create_player_pacman(self.client.player_id, self.pacman_start_pos)
            self.multiplayer_players[self.client.player_id] = pacman
            self.pacman_sprites.add(pacman)
            self.all_sprites.add(pacman)
            print(f"Local player created: {self.client.player_id}")
    
    def initialize_sounds(self):
        """Initialize sound effects"""
        try:
            self.sound_manager.load_sound("dot", "assets/sounds/pacman_chomp.wav", channel=0)
            self.sound_manager.load_sound("death", "assets/sounds/pacman_death.wav", 0.7, 500, 1)
            self.sound_manager.load_sound("eat_ghost", "assets/sounds/pacman_eatghost.wav", 0.6, 100, 2)
            self.sound_manager.set_background_music("assets/sounds/backgroud.mp3")
            self.sound_manager.play_background_music()
        except Exception as e:
            print(f"Sound initialization error: {e}")
    
    def create_player_pacman(self, player_id: str, position: Tuple[int, int]) -> Pacman:
        """Create a Pacman sprite for a player"""
        pacman = Pacman(
            self.screen,
            self.game_state,
            self.matrix,
            position,
            (self.start_x, self.start_y)  # Use the correct grid start position
        )
        
        # Customize appearance for different players
        self.customize_player_appearance(pacman, player_id)
        
        return pacman
    
    def customize_player_appearance(self, pacman: Pacman, player_id: str):
        """Customize pacman appearance for different players"""
        # You could modify colors, add name tags, etc.
        # For now, we'll just store the player ID
        pacman.player_id = player_id
    
    def convert_direction_to_pacman_format(self, direction: str) -> str:
        """Convert full direction words to Pacman's single-letter format"""
        direction_map = {
            "left": "l",
            "right": "r", 
            "up": "u",
            "down": "d"
        }
        return direction_map.get(direction, "r")  # Default to right if unknown
    
    def update_from_server_state(self, server_state: Dict[str, Any]):
        """Update game state from server"""
        players = server_state.get('players', {})
        ghosts = server_state.get('ghosts', {})
        
        # Update player positions
        for player_id, player_data in players.items():
            if player_id not in self.multiplayer_players:
                # Create new player
                position = player_data['position']
                pacman = self.create_player_pacman(player_id, position)
                self.multiplayer_players[player_id] = pacman
                self.pacman_sprites.add(pacman)
                self.all_sprites.add(pacman)
            else:
                # Update existing player
                pacman = self.multiplayer_players[player_id]
                pacman.pacman_pos = player_data['position']
                # Convert direction from server format to Pacman's single-letter format
                server_direction = player_data.get('direction', 'right')
                pacman.move_direction = self.convert_direction_to_pacman_format(server_direction)
                
                # Update score in game state
                if player_id == self.client.player_id:
                    self.game_state.points = player_data.get('score', 0)
        
        # Update ghost positions
        for ghost_name, ghost_data in ghosts.items():
            # Find ghost by name in the ghosts_list
            ghost = None
            for g in self.ghost_manager.ghosts_list:
                if g.name == ghost_name:
                    ghost = g
                    break
                    
            if ghost:
                ghost._ghost_matrix_pos = ghost_data['position']
                ghost._direction = ghost_data.get('direction', 'up')
                ghost.is_scared = ghost_data.get('frightened', False)
                
                # Update ghost image based on state
                if ghost.is_scared:
                    ghost.image = ghost.blue_image
                else:
                    ghost.image = ghost.normal_image
    
    def handle_local_input(self, event):
        """Handle local player input"""
        if event.type == pygame.KEYDOWN:
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
                # Create local player if it doesn't exist yet
                if self.client.player_id and self.client.player_id not in self.multiplayer_players:
                    self.setup_local_player()
                
                # Apply movement locally for immediate feedback
                if self.client.player_id in self.multiplayer_players:
                    pacman = self.multiplayer_players[self.client.player_id]
                    current_pos = pacman.pacman_pos
                    
                    # Update local direction immediately for responsive gameplay
                    pacman_direction = self.convert_direction_to_pacman_format(direction)
                    pacman.move_direction = pacman_direction
                    
                    # Also update the game state direction for consistency
                    self.game_state.direction = pacman_direction
                    
                    # Send to server
                    self.client.send_player_input(direction, current_pos)
                    print(f"Sent input: {direction} at position {current_pos}")
                else:
                    print(f"Player not found: {self.client.player_id}, available players: {list(self.multiplayer_players.keys())}")
    
    def update(self, dt: float):
        """Update game logic"""
        # Update from server state
        if self.client.multiplayer_game_state:
            self.update_from_server_state(self.client.multiplayer_game_state)
        
        # Update sprites (this will update all ghosts and pacman sprites)
        self.all_sprites.update(dt)
    
    def draw(self):
        """Draw game objects"""
        # Clear screen
        self.screen.fill(Colors.BLACK)
        
        # Draw game grid/maze
        self.gui.draw_screens()
        
        # Draw sprites
        self.all_sprites.draw(self.screen)
        
        # Draw UI elements
        self.draw_ui()
    
    def draw_ui(self):
        """Draw game UI elements"""
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Draw scores for all players
        y_offset = 10
        for player_id, player_data in self.client.multiplayer_game_state.get('players', {}).items():
            player_name = player_data.get('name', player_id[:8])
            score = player_data.get('score', 0)
            lives = player_data.get('lives', 3)
            
            color = Colors.WHITE
            if player_id == self.client.player_id:
                color = Colors.YELLOW  # Highlight local player
            
            score_text = font.render(f"{player_name}: {score} (Lives: {lives})", True, color)
            self.screen.blit(score_text, (10, y_offset))
            y_offset += 30
        
        # Draw instructions
        instructions = [
            "Arrow keys: Move",
            "ESC: Leave game"
        ]
        
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, Colors.WHITE)
            self.screen.blit(text, (SCREEN_WIDTH - 200, 10 + i * 25))
        
        # Draw connection status
        status_text = small_font.render(f"Connected to: {self.client.server_ip}:{self.client.server_port}", True, Colors.WHITE)
        self.screen.blit(status_text, (10, SCREEN_HEIGHT - 30))
    
    def run_game_loop(self):
        """Run the main game loop"""
        clock = pygame.time.Clock()
        
        # Ensure local player exists when game starts
        if self.client.player_id and self.client.player_id not in self.multiplayer_players:
            self.setup_local_player()
        
        while self.client.running and self.client.current_menu == "game":
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.client.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.client.leave_game()
                    else:
                        self.handle_local_input(event)
            
            # Update game
            current_time = time.time()
            dt = current_time - self.last_update
            self.last_update = current_time
            
            self.update(dt)
            
            # Draw game
            self.draw()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)
