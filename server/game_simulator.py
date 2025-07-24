"""
PyPacman Game Simulator

This module handles the server-side game logic including:
- Player movement validation
- Ghost AI behavior
- Collision detection
- Score calculation
- Game state management
"""

import json
import math
import random
import time
from typing import Dict, List, Tuple, Any

# Import the existing game components
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.configs import CELL_SIZE, PACMAN_SPEED, DOT_POINT, POWER_POINT, GHOST_POINT
from src.utils.coord_utils import get_coords_from_idx, get_idx_from_coords


class GameSimulator:
    def __init__(self):
        self.game_matrix = None
        self.collectibles = {}
        self.ghosts = {}
        self.players = {}
        self.game_running = False
        self.level = 1
        self.spawn_positions = [
            (13, 26),  # Default spawn position
            (13, 8),   # Second player spawn
            (26, 13),  # Third player spawn  
            (8, 13)    # Fourth player spawn
        ]
        
        # Load game level
        self.load_level()
        
        # Initialize ghosts
        self.initialize_ghosts()
        
        # Ghost AI states
        self.ghost_mode = "scatter"  # scatter, chase, frightened
        self.ghost_mode_timer = 0
        self.ghost_mode_duration = 7000  # 7 seconds
        self.frightened_timer = 0
        self.frightened_duration = 10000  # 10 seconds
        
    def load_level(self):
        """Load the game level from JSON file"""
        try:
            with open('levels/level1.json', 'r') as f:
                level_data = json.load(f)
                self.game_matrix = level_data['matrix']
                self.start_pos = (level_data.get('cell_width', 20), level_data.get('cell_height', 20))
                self.pacman_pos = tuple(level_data.get('pacman_start', [17, 16]))
                
                # Extract ghost positions from level data or use defaults
                self.ghost_positions = {
                    'blinky': tuple(level_data.get('ghost_den', [14, 15])),
                    'pinky': (level_data.get('ghost_den', [14, 15])[0], level_data.get('ghost_den', [14, 15])[1] + 1),
                    'inky': (level_data.get('ghost_den', [14, 15])[0] - 1, level_data.get('ghost_den', [14, 15])[1]),
                    'clyde': (level_data.get('ghost_den', [14, 15])[0] + 1, level_data.get('ghost_den', [14, 15])[1])
                }
                
                # Initialize collectibles
                self.initialize_collectibles()
                
        except FileNotFoundError:
            print("Level file not found, creating default level")
            self.create_default_level()
    
    def create_default_level(self):
        """Create a simple default level if level file is missing"""
        # This would create a basic maze - simplified for demonstration
        self.game_matrix = [
            ['wall'] * 35,
            ['wall'] + ['dot'] * 33 + ['wall'],
            # ... more rows would be defined here
        ]
        self.start_pos = (50, 50)
        self.pacman_pos = (13, 26)
        self.ghost_positions = {
            'blinky': (13, 13),
            'pinky': (13, 14),
            'inky': (12, 13),
            'clyde': (14, 13)
        }
        self.initialize_collectibles()
    
    def initialize_collectibles(self):
        """Initialize collectible items (dots and power pellets)"""
        self.collectibles = {}
        for row in range(len(self.game_matrix)):
            for col in range(len(self.game_matrix[0])):
                if self.game_matrix[row][col] == 'dot':
                    self.collectibles[f"{row},{col}"] = {
                        "type": "dot",
                        "points": DOT_POINT,
                        "collected": False
                    }
                elif self.game_matrix[row][col] == 'power':
                    self.collectibles[f"{row},{col}"] = {
                        "type": "power",
                        "points": POWER_POINT,
                        "collected": False
                    }
    
    def initialize_ghosts(self):
        """Initialize ghost entities"""
        ghost_names = ['blinky', 'pinky', 'inky', 'clyde']
        for i, name in enumerate(ghost_names):
            if hasattr(self, 'ghost_positions') and name in self.ghost_positions:
                pos = self.ghost_positions[name]
            else:
                pos = (13 + i, 13)  # Default positions
            
            self.ghosts[name] = {
                "position": pos,
                "direction": "up",
                "mode": "scatter",
                "target": None,
                "frightened": False,
                "eaten": False,
                "speed": 1.0
            }
    
    def get_spawn_position(self, player_count: int) -> Tuple[int, int]:
        """Get spawn position for a new player"""
        if player_count < len(self.spawn_positions):
            return self.spawn_positions[player_count]
        return self.spawn_positions[0]  # Default position
    
    def start_game(self):
        """Start the game simulation"""
        self.game_running = True
        self.ghost_mode_timer = 0
        print("Game simulation started")
    
    def stop_game(self):
        """Stop the game simulation"""
        self.game_running = False
        print("Game simulation stopped")
    
    def simulate(self, actions: List[Dict[str, Any]], delta_time: float) -> Dict[str, Any]:
        """Main simulation step"""
        if not self.game_running:
            return self.get_game_state()
        
        # Process player actions
        for action in actions:
            self.process_action(action)
        
        # Update game timers
        self.update_ghost_modes(delta_time)
        
        # Update ghosts
        self.update_ghosts(delta_time)
        
        # Check collisions
        self.check_collisions()
        
        # Check win conditions
        self.check_win_conditions()
        
        return self.get_game_state()
    
    def process_action(self, action: Dict[str, Any]):
        """Process a single player action"""
        action_type = action.get('type')
        
        if action_type == 'move':
            self.handle_player_move(action)
    
    def handle_player_move(self, action: Dict[str, Any]):
        """Handle player movement"""
        player_id = action.get('player_id')
        direction = action.get('direction')
        position = action.get('position')
        
        if player_id not in self.players:
            return
        
        # Validate movement
        if self.is_valid_move(position, direction):
            self.players[player_id]['position'] = position
            self.players[player_id]['direction'] = direction
            
            # Check for collectible pickup
            self.check_collectible_pickup(player_id, position)
    
    
    def is_valid_move(self, position: Tuple[int, int], direction: str) -> bool:
        """Check if a move is valid (not into walls)"""
        row, col = position
        
        # Check bounds
        if row < 0 or row >= len(self.game_matrix) or col < 0 or col >= len(self.game_matrix[0]):
            return False
        
        # Check for walls
        if self.game_matrix[row][col] == 'wall':
            return False
        
        return True
    
    def check_collectible_pickup(self, player_id: str, position: Tuple[int, int]):
        """Check if player picked up a collectible"""
        row, col = position
        collectible_key = f"{row},{col}"
        
        if collectible_key in self.collectibles and not self.collectibles[collectible_key]['collected']:
            collectible = self.collectibles[collectible_key]
            collectible['collected'] = True
            
            # Award points
            if player_id in self.players:
                self.players[player_id]['score'] += collectible['points']
            
            # Handle power pellet
            if collectible['type'] == 'power':
                self.players[player_id]['powered'] = True
                self.players[player_id]['power_time'] = time.time() * 1000
                self.set_ghosts_frightened()
    
    def set_ghosts_frightened(self):
        """Set all ghosts to frightened mode"""
        for ghost in self.ghosts.values():
            ghost['frightened'] = True
            ghost['mode'] = 'frightened'
        
        self.frightened_timer = 0
        self.ghost_mode = 'frightened'
    
    def update_ghost_modes(self, delta_time: float):
        """Update ghost AI modes (scatter/chase/frightened)"""
        if self.ghost_mode == 'frightened':
            self.frightened_timer += delta_time
            if self.frightened_timer >= self.frightened_duration:
                self.ghost_mode = 'scatter'
                self.frightened_timer = 0
                for ghost in self.ghosts.values():
                    ghost['frightened'] = False
                    ghost['mode'] = 'scatter'
        else:
            self.ghost_mode_timer += delta_time
            if self.ghost_mode_timer >= self.ghost_mode_duration:
                self.ghost_mode = 'chase' if self.ghost_mode == 'scatter' else 'scatter'
                self.ghost_mode_timer = 0
                for ghost in self.ghosts.values():
                    ghost['mode'] = self.ghost_mode
    
    def update_ghosts(self, delta_time: float):
        """Update ghost positions and AI"""
        for ghost_name, ghost in self.ghosts.items():
            if not ghost['eaten'] and not ghost.get('frozen', False):
                self.update_ghost_ai(ghost_name, ghost)
                self.move_ghost(ghost)
    
    def update_ghost_ai(self, ghost_name: str, ghost: Dict[str, Any]):
        """Update individual ghost AI behavior"""
        if ghost['mode'] == 'frightened':
            # Random movement when frightened
            directions = ['up', 'down', 'left', 'right']
            ghost['direction'] = random.choice(directions)
        elif ghost['mode'] == 'scatter':
            # Move to scatter corners
            scatter_targets = {
                'blinky': (0, 34),
                'pinky': (0, 0),
                'inky': (34, 34),
                'clyde': (34, 0)
            }
            ghost['target'] = scatter_targets.get(ghost_name, (0, 0))
            self.move_ghost_to_target(ghost)
        elif ghost['mode'] == 'chase':
            # Chase nearest player
            nearest_player = self.find_nearest_player(ghost['position'])
            if nearest_player:
                ghost['target'] = nearest_player['position']
                self.move_ghost_to_target(ghost)
    
    def move_ghost_to_target(self, ghost: Dict[str, Any]):
        """Move ghost towards its target"""
        if not ghost['target']:
            return
        
        ghost_pos = ghost['position']
        target_pos = ghost['target']
        
        # Simple pathfinding - move towards target
        row_diff = target_pos[0] - ghost_pos[0]
        col_diff = target_pos[1] - ghost_pos[1]
        
        if abs(row_diff) > abs(col_diff):
            ghost['direction'] = 'down' if row_diff > 0 else 'up'
        else:
            ghost['direction'] = 'right' if col_diff > 0 else 'left'
    
    def move_ghost(self, ghost: Dict[str, Any]):
        """Move ghost in its current direction"""
        row, col = ghost['position']
        direction = ghost['direction']
        
        # Calculate new position
        new_row, new_col = row, col
        if direction == 'up':
            new_row -= 1
        elif direction == 'down':
            new_row += 1
        elif direction == 'left':
            new_col -= 1
        elif direction == 'right':
            new_col += 1
        
        # Check if move is valid
        if self.is_valid_move((new_row, new_col), direction):
            ghost['position'] = (new_row, new_col)
    
    def find_nearest_player(self, ghost_pos: Tuple[int, int]) -> Dict[str, Any]:
        """Find the nearest player to a ghost"""
        nearest_player = None
        min_distance = float('inf')
        
        for player in self.players.values():
            player_pos = player['position']
            distance = math.sqrt((ghost_pos[0] - player_pos[0])**2 + (ghost_pos[1] - player_pos[1])**2)
            if distance < min_distance:
                min_distance = distance
                nearest_player = player
        
        return nearest_player
    
    def check_collisions(self):
        """Check for collisions between players and ghosts"""
        for player_id, player in self.players.items():
            player_pos = player['position']
            
            for ghost_name, ghost in self.ghosts.items():
                ghost_pos = ghost['position']
                
                # Check if player and ghost are on the same tile
                if player_pos == ghost_pos:
                    if ghost['frightened'] and not ghost['eaten']:
                        # Player eats ghost
                        ghost['eaten'] = True
                        ghost['frightened'] = False
                        player['score'] += GHOST_POINT
                        print(f"Player {player_id} ate ghost {ghost_name}")
                    elif not player['powered'] and not player.get('shield', False):
                        # Ghost catches player (only if player doesn't have shield)
                        player['lives'] -= 1
                        print(f"Player {player_id} caught by ghost {ghost_name}")
                        
                        # Reset player position
                        player['position'] = self.get_spawn_position(0)
                        
                        if player['lives'] <= 0:
                            print(f"Player {player_id} is out of lives!")
    
    def check_win_conditions(self):
        """Check if the game should end"""
        # Check if all collectibles are collected
        uncollected = [c for c in self.collectibles.values() if not c['collected']]
        if not uncollected:
            print("All collectibles collected! Level complete!")
            self.game_running = False
        
        # Check if all players are out of lives
        living_players = [p for p in self.players.values() if p['lives'] > 0]
        if not living_players:
            print("All players out of lives! Game over!")
            self.game_running = False
    
    def get_game_state(self) -> Dict[str, Any]:
        """Get current game state"""
        return {
            "players": {pid: {
                "position": p['position'],
                "direction": p['direction'],
                "score": p['score'],
                "lives": p['lives'],
                "powered": p['powered'],
                "speed_boost": p.get('speed_boost', False),
                "shield": p.get('shield', False)
            } for pid, p in self.players.items()},
            "ghosts": {name: {
                "position": g['position'],
                "direction": g['direction'],
                "mode": g['mode'],
                "frightened": g['frightened'],
                "eaten": g['eaten']
            } for name, g in self.ghosts.items()},
            "collectibles": self.collectibles,
            "game_status": "playing" if self.game_running else "stopped",
            "level": self.level
        }
