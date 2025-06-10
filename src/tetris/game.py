"""Main game logic for Tetris."""

import pygame
import time
from typing import Optional
from .constants import (
    INITIAL_FALL_TIME, FAST_FALL_TIME, MIN_FALL_TIME, FALL_TIME_DECREASE,
    SCORE_VALUES, LINES_PER_LEVEL, KEY_MAPPINGS, LEVEL_SCORE_BASE,
    LEVEL_SCORE_MULTIPLIER, SPEED_MULTIPLIER, EFFECT_DURATION
)
from .board import Board
from .piece import Piece
from .renderer import GameRenderer
from .effects import EffectsManager


class Game:
    """Main game class that manages the Tetris game state and logic."""
    
    def __init__(self):
        """Initialize the game."""
        self.board = Board()
        self.renderer = GameRenderer()
        self.effects_manager = EffectsManager()
        
        # Key repeat settings
        self.key_repeat_delay = 150  # Initial delay in ms before repeat starts
        self.key_repeat_interval = 50  # Interval between repeats in ms
        self.key_states = {}  # Track key press states and timing
        
        # Effect timing
        self.line_clear_start_time = 0
        self.pending_line_clear = False
        self.cleared_lines_data = None
        
        self.reset_game()
    
    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board.clear()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = INITIAL_FALL_TIME
        self.last_fall_time = time.time() * 1000
        self.game_over = False
        self.paused = False
        
        # Score-based level progression
        self.next_level_score = LEVEL_SCORE_BASE  # Score needed for next level
        
        # Generate first pieces
        self.current_piece = Piece()
        self.next_piece = Piece()
        
        # Move current piece to valid starting position
        while not self.board.is_valid_position(self.current_piece):
            self.current_piece = self.current_piece.move(0, -1)
    
    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle input events.
        
        Args:
            event: Pygame event
            
        Returns:
            True if game should continue, False if should quit
        """
        if event.type == pygame.QUIT:
            return False
        
        current_time = time.time() * 1000
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            
            if self.game_over:
                if event.key == pygame.K_r:
                    self.reset_game()
                return True
            
            if event.key == pygame.K_p:
                self.paused = not self.paused
                return True
            
            if self.paused:
                return True
            
            # Track key press for repeatable actions
            repeatable_keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_DOWN, pygame.K_UP]
            if event.key in repeatable_keys:
                self.key_states[event.key] = {
                    'pressed': True,
                    'last_action_time': current_time,
                    'initial_press': True
                }
            
            # Handle game controls
            if event.key == pygame.K_LEFT:
                self.move_piece(-1, 0)
            elif event.key == pygame.K_RIGHT:
                self.move_piece(1, 0)
            elif event.key == pygame.K_DOWN:
                self.soft_drop()
            elif event.key == pygame.K_UP:
                self.rotate_piece()
            elif event.key == pygame.K_SPACE:
                self.hard_drop()
        
        elif event.type == pygame.KEYUP:
            # Remove key from tracking when released
            if event.key in self.key_states:
                del self.key_states[event.key]
        
        return True
    
    def handle_key_repeat(self) -> None:
        """Handle key repeat for held keys."""
        if self.game_over or self.paused:
            return
        
        current_time = time.time() * 1000
        
        for key, state in list(self.key_states.items()):
            if not state['pressed']:
                continue
            
            # Calculate delay based on whether this is initial press or repeat
            delay = self.key_repeat_delay if state['initial_press'] else self.key_repeat_interval
            
            # Check if enough time has passed for next action
            if current_time - state['last_action_time'] >= delay:
                # Perform the action
                if key == pygame.K_LEFT:
                    self.move_piece(-1, 0)
                elif key == pygame.K_RIGHT:
                    self.move_piece(1, 0)
                elif key == pygame.K_DOWN:
                    self.soft_drop()
                elif key == pygame.K_UP:
                    self.rotate_piece()
                
                # Update timing
                state['last_action_time'] = current_time
                state['initial_press'] = False
    
    def move_piece(self, dx: int, dy: int) -> bool:
        """Try to move the current piece.
        
        Args:
            dx: Horizontal movement
            dy: Vertical movement
            
        Returns:
            True if move was successful, False otherwise
        """
        if self.game_over or self.paused:
            return False
        
        new_piece = self.current_piece.move(dx, dy)
        if self.board.is_valid_position(new_piece):
            self.current_piece = new_piece
            return True
        return False
    
    def rotate_piece(self) -> bool:
        """Try to rotate the current piece.
        
        Returns:
            True if rotation was successful, False otherwise
        """
        if self.game_over or self.paused:
            return False
        
        rotated_piece = self.current_piece.rotate()
        
        # Try basic rotation
        if self.board.is_valid_position(rotated_piece):
            self.current_piece = rotated_piece
            return True
        
        # Try wall kicks (simple implementation)
        for dx in [-1, 1, -2, 2]:
            kicked_piece = rotated_piece.move(dx, 0)
            if self.board.is_valid_position(kicked_piece):
                self.current_piece = kicked_piece
                return True
        
        return False
    
    def soft_drop(self) -> bool:
        """Move piece down faster.
        
        Returns:
            True if piece moved down, False if it landed
        """
        return self.move_piece(0, 1)
    
    def hard_drop(self) -> None:
        """Drop piece to the bottom immediately."""
        if self.game_over or self.paused:
            return
        
        while self.move_piece(0, 1):
            pass
        self.lock_piece()
    
    def lock_piece(self) -> None:
        """Lock the current piece in place and spawn a new one."""
        if self.game_over:
            return
        
        # Place the piece on the board
        self.board.place_piece(self.current_piece)
        
        # Check for completed lines
        full_lines = self.board.get_full_lines()
        if full_lines:
            # Create explosion effects for each block in the full lines
            for line_y in full_lines:
                for x in range(self.board.width):
                    if self.board.grid[line_y][x] is not None:
                        # Add explosion effect at each block position
                        self.effects_manager.add_explosion_effect(x, line_y)
            
            # Clear lines immediately
            lines_cleared = self.board.clear_lines(full_lines)
            self.add_score(lines_cleared)
            self.lines_cleared += lines_cleared
            
            # Spawn new piece immediately
            self.spawn_new_piece()
        else:
            # No lines to clear, spawn new piece immediately
            self.spawn_new_piece()
    
    def spawn_new_piece(self) -> None:
        """Spawn a new piece."""
        self.current_piece = self.next_piece
        self.next_piece = Piece()
        
        # Check if new piece can be placed
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
    
    def add_score(self, lines_cleared: int) -> None:
        """Add score based on lines cleared.
        
        Args:
            lines_cleared: Number of lines cleared
        """
        if lines_cleared in SCORE_VALUES:
            self.score += SCORE_VALUES[lines_cleared] * self.level
            # Check for level up after scoring
            self.update_level()
    
    def update_level(self) -> None:
        """Update level based on score."""
        # Check if player has reached the score threshold for next level
        while self.score >= self.next_level_score:
            self.level += 1
            
            # Calculate next level score requirement
            # Level 1: 200, Level 2: 200+300=500, Level 3: 500+450=950, etc.
            level_increment = int(LEVEL_SCORE_BASE * (LEVEL_SCORE_MULTIPLIER ** (self.level - 1)))
            self.next_level_score += level_increment
            
            # Increase fall speed by 20% each level
            self.fall_time = max(MIN_FALL_TIME, 
                               int(self.fall_time / SPEED_MULTIPLIER))
    
    def update(self) -> None:
        """Update game state."""
        if self.game_over or self.paused:
            return
        
        current_time = time.time() * 1000
        
        # Update effects (convert milliseconds to seconds for arcade)
        delta_time = (current_time - self.last_fall_time) / 1000.0
        self.effects_manager.update(delta_time)
        
        # Handle automatic falling
        if current_time - self.last_fall_time >= self.fall_time:
            if not self.move_piece(0, 1):
                self.lock_piece()
            self.last_fall_time = current_time
    
    def render(self, screen) -> None:
        """Render the game."""
        self.renderer.draw_game(screen, self.board, self.current_piece, 
                               self.score, self.level, self.lines_cleared, 
                               self.next_piece, self.game_over, self.paused)
        
        # Render effects on top using pygame
        self.effects_manager.draw(screen)
    
    def run(self) -> None:
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if not self.handle_input(event):
                    running = False
                    break
            
            # Handle key repeat for held keys
            self.handle_key_repeat()
            
            # Update game state
            self.update()
            
            # Render
            self.render(self.renderer.screen)
            self.renderer.update_display()
            
            # Control frame rate
            clock.tick(60)
        
        self.renderer.quit()
    
    def get_state(self) -> dict:
        """Get current game state for testing.
        
        Returns:
            Dictionary containing game state
        """
        return {
            'score': self.score,
            'level': self.level,
            'lines_cleared': self.lines_cleared,
            'game_over': self.game_over,
            'paused': self.paused,
            'current_piece_type': self.current_piece.type if self.current_piece else None,
            'next_piece_type': self.next_piece.type if self.next_piece else None,
        }