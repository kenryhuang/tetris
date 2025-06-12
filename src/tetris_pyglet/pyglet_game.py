"""Main game logic for Pyglet Tetris implementation.

This module contains the main game class that coordinates all
components and handles game state, input, and timing.
"""

import pyglet
from pyglet.window import key
import random
import time
from typing import Optional
from .constants import (
    INITIAL_FALL_TIME, FAST_FALL_TIME, MIN_FALL_TIME, FALL_TIME_DECREASE,
    SCORE_VALUES, LINES_PER_LEVEL, LEVEL_SCORE_BASE,
    LEVEL_SCORE_MULTIPLIER, SPEED_MULTIPLIER, EFFECT_DURATION,
    KEY_MAPPINGS, ALT_KEY_MAPPINGS, TARGET_FPS
)
from .board import Board
from .piece import Piece
from .renderer import PygletRenderer
from .effects import PygletEffectsManager


class PygletTetrisGame:
    """Main Pyglet-based Tetris game class."""
    
    def __init__(self, window: pyglet.window.Window = None):
        """Initialize the Pyglet game.
        
        Args:
            window: Existing pyglet window to use. If None, renderer creates a new one.
        """
        # Core components
        self.board = Board()
        self.renderer = PygletRenderer(window)
        self.effects_manager = PygletEffectsManager()
        
        # Get the window from renderer
        self.window = self.renderer.get_window()
        
        # Game state
        self.reset_game()
        
        # Input handling
        self.keys_pressed = set()
        self.key_repeat_timers = {}
        self.key_repeat_delay = 0.12  # Reasonable initial delay to prevent double triggers
        self.key_repeat_interval = 0.04  # Balanced repeat interval for smooth but controlled movement
        
        # Timing
        self.last_fall_time = 0.0
        self.last_update_time = time.time()
        
        # Effect timing
        self.line_clear_start_time = 0.0
        self.pending_line_clear = False
        self.cleared_lines_data = None
        
        # Animation states
        self.game_over_animation_time = 0.0
        self.piece_lock_animation_time = 0.0
        
    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board.clear()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = INITIAL_FALL_TIME
        self.game_over = False
        self.paused = False
        
        # Game timing
        self.game_start_time = time.time()
        
        # Score-based level progression
        self.next_level_score = LEVEL_SCORE_BASE
        
        # Create first piece and next piece
        self.current_piece = self._create_new_piece()
        self.next_piece = self._create_new_piece()
        self.ghost_piece = None
        self._update_ghost_piece()
        
        # Clear effects
        self.effects_manager.clear_all_effects()
        
        # Reset animation states
        self.game_over_animation_time = 0.0
        self.piece_lock_animation_time = 0.0
        self.pending_line_clear = False
        
    def _create_new_piece(self) -> Piece:
        """Create a new random piece.
        
        Returns:
            New Piece instance
        """
        piece_type = Piece.get_random_type()
        return Piece(piece_type, x=4, y=0)
    
    def _update_ghost_piece(self) -> None:
        """Update the ghost piece position."""
        if self.current_piece:
            self.ghost_piece = self.current_piece.copy()
            
            # Move ghost piece down until it can't move further
            while self.board.is_valid_position(self.ghost_piece):
                self.ghost_piece.y += 1
            self.ghost_piece.y -= 1  # Move back to last valid position
    
    def _spawn_next_piece(self) -> bool:
        """Spawn the next piece.
        
        Returns:
            True if piece was spawned successfully, False if game over
        """
        self.current_piece = self.next_piece
        self.next_piece = self._create_new_piece()
        
        # Check if the new piece can be placed
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
            return False
        
        self._update_ghost_piece()
        return True
    
    def _move_piece(self, dx: int, dy: int) -> bool:
        """Try to move the current piece.
        
        Args:
            dx: Horizontal movement
            dy: Vertical movement
            
        Returns:
            True if piece was moved successfully
        """
        if not self.current_piece or self.game_over or self.paused:
            return False
        
        # Create a copy to test the move
        test_piece = self.current_piece.copy()
        test_piece.move(dx, dy)
        
        if self.board.is_valid_position(test_piece):
            self.current_piece.move(dx, dy)
            self._update_ghost_piece()
            
            # Reset fall timer on horizontal movement
            if dx != 0:
                self.current_piece.reset_lock_delay()
            
            return True
        
        return False
    
    def _rotate_piece(self, clockwise: bool = True) -> bool:
        """Try to rotate the current piece.
        
        Args:
            clockwise: Rotation direction
            
        Returns:
            True if piece was rotated successfully
        """
        if not self.current_piece or self.game_over or self.paused:
            return False
        
        # Try simple rotation first
        if self.current_piece.can_rotate(self.board, clockwise):
            self.current_piece.rotate(clockwise)
            self._update_ghost_piece()
            return True
        
        # Try wall kick
        if self.current_piece.try_wall_kick(self.board, clockwise):
            self._update_ghost_piece()
            return True
        
        return False
    
    def _hard_drop(self) -> None:
        """Drop the piece to the bottom immediately."""
        if not self.current_piece or self.game_over or self.paused:
            return
        
        # Drop to bottom without scoring
        while self._auto_fall():
            pass
        
        # Lock the piece immediately
        self._lock_piece()
    
    def _soft_drop(self) -> bool:
        """Move piece down one line (soft drop).
        
        Returns:
            True if piece moved down
        """
        return self._move_piece(0, 1)
    
    def _auto_fall(self) -> bool:
        """Move piece down one line automatically (no scoring).
        
        Returns:
            True if piece moved down
        """
        return self._move_piece(0, 1)
    
    def _lock_piece(self) -> None:
        """Lock the current piece to the board."""
        if not self.current_piece:
            return
        
        # Place piece on board
        self.board.place_piece(self.current_piece)
        
        # Add explosion effects for each block
        for x, y in self.current_piece.get_blocks():
            # Effects removed - only using line_effects now
            pass
        
        # Check for line clears
        full_lines = self.board.get_full_lines()
        if full_lines:
            self._start_line_clear(full_lines)
        else:
            # Spawn next piece immediately if no lines to clear
            self._spawn_next_piece()
        
        # Start piece lock animation
        self.piece_lock_animation_time = 0.0
    
    def _start_line_clear(self, lines: list) -> None:
        """Start the line clearing process.
        
        Args:
            lines: List of line indices to clear
        """
        self.pending_line_clear = True
        self.cleared_lines_data = lines
        self.line_clear_start_time = time.time()

        # Start board animation
        self.board.start_line_clear_animation(lines)
        
        # Add line clear effects
        for line_y in lines:
            self.effects_manager.add_line_clear_effect(line_y)
            
            # Explosion effects removed - only using line_effects now

    def _complete_line_clear(self) -> None:
        """Complete the line clearing process."""
        if not self.pending_line_clear or not self.cleared_lines_data:
            return
        
        lines_cleared = len(self.cleared_lines_data)
        
        # Clear the lines from the board
        self.board.clear_lines(self.cleared_lines_data)
        
        # Update statistics
        self.lines_cleared += lines_cleared
        
        # Calculate score
        line_score = SCORE_VALUES.get(lines_cleared, 0)
        self.score += line_score
        
        # Check for level up (score-based)
        if self.score >= self.next_level_score:
            self._level_up()
        
        # Reset line clear state
        self.pending_line_clear = False
        self.cleared_lines_data = None
        
        # Clear locked blocks animation
        self.board.clear_locked_blocks()
        
        # Spawn next piece
        self._spawn_next_piece()
    
    def _level_up(self) -> None:
        """Handle level progression."""
        self.level += 1
        
        # Increase fall speed
        self.fall_time = max(MIN_FALL_TIME, self.fall_time * SPEED_MULTIPLIER)
        
        # Calculate next level score requirement
        self.next_level_score = int(self.next_level_score * LEVEL_SCORE_MULTIPLIER)
        
        # Celebration effects removed - only using line_effects now
    
    def _handle_input(self, dt: float) -> None:
        """Handle continuous input with key repeat.
        
        Args:
            dt: Delta time in seconds
        """
        if self.game_over or self.paused:
            return
        
        # Update key repeat timers
        for key_code in list(self.key_repeat_timers.keys()):
            if key_code in self.keys_pressed:
                self.key_repeat_timers[key_code] += dt
            else:
                del self.key_repeat_timers[key_code]
        
        # Handle movement keys with repeat
        movement_keys = {
            KEY_MAPPINGS['LEFT']: (-1, 0),
            KEY_MAPPINGS['RIGHT']: (1, 0),
            KEY_MAPPINGS['DOWN']: (0, 1),
            ALT_KEY_MAPPINGS.get('LEFT', key.A): (-1, 0),
            ALT_KEY_MAPPINGS.get('RIGHT', key.D): (1, 0),
            ALT_KEY_MAPPINGS.get('DOWN', key.S): (0, 1),
        }
        
        for key_code, (dx, dy) in movement_keys.items():
            if key_code in self.keys_pressed:
                timer = self.key_repeat_timers.get(key_code, 0)
                
                # Fixed trigger logic for reliable key response
                should_trigger = False
                
                if timer <= dt:  # First press detection (within first frame)
                    should_trigger = True
                elif timer >= self.key_repeat_delay:
                    # After initial delay, trigger at regular intervals
                    time_since_delay = timer - self.key_repeat_delay
                    # Check if we've reached a repeat interval
                    if time_since_delay % self.key_repeat_interval <= dt:
                        should_trigger = True
                
                if should_trigger:
                    if dy == 1:  # Down key - soft drop
                        self._soft_drop()
                    else:  # Left/Right movement
                        self._move_piece(dx, dy)
    
    def update(self, dt: float) -> None:
        """Update game state.
        
        Args:
            dt: Delta time in seconds
        """
        current_time = time.time()
        
        # Handle input
        self._handle_input(dt)
        
        # Update effects
        self.effects_manager.update(dt)
        
        # Update renderer animation
        self.renderer.update_animation(dt)
        
        # Update current piece animations
        if self.current_piece:
            self.current_piece.update_visual_position(dt)
            self.current_piece.update_rotation_animation(dt)
            self.current_piece.update_effects(dt)
        
        # Update board animations
        if self.pending_line_clear:
            if self.board.update_line_clear_animation(dt):
                # Animation complete, finish line clear
                self._complete_line_clear()
        
        # Handle piece falling
        if not self.game_over and not self.paused and not self.pending_line_clear:
            if self.current_piece:
                # Check if piece should fall
                if current_time - self.last_fall_time >= self.fall_time:
                    if not self._auto_fall():
                        # Piece can't move down, start lock delay
                        self.current_piece.is_falling = False
                    else:
                        # Piece moved down successfully
                        self.current_piece.is_falling = True
                        self.current_piece.reset_lock_delay()
                    
                    self.last_fall_time = current_time
                
                # Always update lock delay when piece is not falling
                if not self.current_piece.is_falling:
                    if self.current_piece.update_lock_delay(dt):
                        self._lock_piece()
        
        # Update animation timers
        if self.game_over:
            self.game_over_animation_time += dt
        
        if self.piece_lock_animation_time >= 0:
            self.piece_lock_animation_time += dt
            if self.piece_lock_animation_time >= 0.2:  # Reset after animation
                self.piece_lock_animation_time = -1
    
    def draw(self) -> None:
        """Draw the game."""
        # Clear screen
        self.renderer.clear()
        
        # Draw board
        self.renderer.draw_board(self.board)
        
        # Draw ghost piece
        if self.ghost_piece and not self.pending_line_clear:
            self.renderer.draw_piece(self.ghost_piece, ghost=True)
        
        # Draw current piece
        if self.current_piece and not self.pending_line_clear:
            self.renderer.draw_piece(self.current_piece)
        
        # Calculate game time
        game_time = int(time.time() - self.game_start_time) if hasattr(self, 'game_start_time') else 0
        
        # Draw UI
        self.renderer.draw_ui(self.score, self.level, self.lines_cleared, self.next_piece, 
                             self.current_piece, game_time)
        
        # Draw effects
        self.effects_manager.draw(self.renderer.effect_batch, self.renderer.effect_group)
        
        # Draw game over screen
        if self.game_over:
            self.renderer.draw_game_over(self.score)
        
        # Draw pause screen
        if self.paused and not self.game_over:
            self.renderer.draw_pause_screen()
        
        # Render all batches
        self.renderer.draw()
    
    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handle key press events.
        
        Args:
            symbol: Key symbol
            modifiers: Key modifiers
        """
        self.keys_pressed.add(symbol)
        
        # Initialize key repeat timer
        if symbol not in self.key_repeat_timers:
            self.key_repeat_timers[symbol] = 0.0
        
        # Handle single-press actions
        if symbol == KEY_MAPPINGS['ROTATE_CW'] or symbol == ALT_KEY_MAPPINGS.get('ROTATE_CW', key.W):
            self._rotate_piece(True)
        elif symbol == KEY_MAPPINGS.get('ROTATE_CCW', key.Z):
            self._rotate_piece(False)
        elif symbol == KEY_MAPPINGS['DROP'] or symbol == ALT_KEY_MAPPINGS.get('DROP', key.ENTER):
            self._hard_drop()
        elif symbol == KEY_MAPPINGS['PAUSE']:
            if not self.game_over:
                self.paused = not self.paused
        elif symbol == KEY_MAPPINGS['RESTART']:
            self.reset_game()
        elif symbol == KEY_MAPPINGS['QUIT']:
            self.window.close()
    
    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Handle key release events.
        
        Args:
            symbol: Key symbol
            modifiers: Key modifiers
        """
        self.keys_pressed.discard(symbol)
    
    def get_window(self) -> pyglet.window.Window:
        """Get the game window.
        
        Returns:
            The pyglet window instance
        """
        return self.window
