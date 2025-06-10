"""Pyglet-based Tetris game implementation.

This module provides the main game class using Pyglet for improved
performance and visual effects compared to the Pygame version.
"""

import pyglet
from pyglet import gl
from pyglet.window import key
import random
import time
import os
from typing import Optional
from .constants import (
    INITIAL_FALL_TIME, FAST_FALL_TIME, MIN_FALL_TIME, FALL_TIME_DECREASE,
    SCORE_VALUES, LINES_PER_LEVEL, LEVEL_SCORE_BASE,
    LEVEL_SCORE_MULTIPLIER, SPEED_MULTIPLIER, EFFECT_DURATION
)
from .board import Board
from .piece import Piece
from .pyglet_renderer import PygletRenderer
from .pyglet_effects import PygletEffectsManager


class PygletGame:
    """Main Pyglet-based Tetris game class."""
    
    def __init__(self):
        """Initialize the Pyglet game."""
        # Check for display availability
        if os.environ.get('DISPLAY') is None and os.name != 'nt':
            # Try to set a minimal config for headless environments
            try:
                config = pyglet.gl.Config(double_buffer=False)
                print("Warning: No display detected. Attempting headless mode.")
            except:
                print("Error: No display available. Pyglet requires a display to run.")
                print("Please run this on a system with a graphical display.")
                raise
        
        self.board = Board()
        self.renderer = PygletRenderer()
        self.effects_manager = PygletEffectsManager()
        
        # Get the window from renderer
        self.window = self.renderer.get_window()
        
        # Set up event handlers
        self.window.on_key_press = self.on_key_press
        self.window.on_key_release = self.on_key_release
        self.window.on_draw = self.on_draw
        
        # Key state tracking
        self.keys_pressed = set()
        self.key_repeat_timers = {}
        self.key_repeat_delay = 0.15  # Initial delay before repeat
        self.key_repeat_interval = 0.05  # Interval between repeats
        
        # Game timing
        self.last_fall_time = time.time()
        self.last_update_time = time.time()
        
        # Effect timing
        self.line_clear_start_time = 0
        self.pending_line_clear = False
        self.cleared_lines_data = None
        
        # Schedule game update
        pyglet.clock.schedule_interval(self.update, 1/60.0)  # 60 FPS
        
        self.reset_game()
    
    def reset_game(self) -> None:
        """Reset the game to initial state."""
        self.board.clear()
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_time = INITIAL_FALL_TIME / 1000.0  # Convert to seconds
        self.last_fall_time = time.time()
        self.game_over = False
        self.paused = False
        
        # Score-based level progression
        self.next_level_score = LEVEL_SCORE_BASE
        
        # Create first piece
        self.current_piece = Piece()
        self.next_piece = Piece()
        
        # Clear effects
        self.effects_manager.clear_all_effects()
        
        # Reset timing
        self.pending_line_clear = False
        self.cleared_lines_data = None
    
    def on_key_press(self, symbol, modifiers):
        """Handle key press events.
        
        Args:
            symbol: Key symbol
            modifiers: Key modifiers
        """
        if self.game_over:
            if symbol == key.R:
                self.reset_game()
            elif symbol == key.ESCAPE:
                self.window.close()
            return
        
        if symbol == key.ESCAPE:
            self.window.close()
        elif symbol == key.P:
            self.paused = not self.paused
        elif not self.paused and not self.pending_line_clear:
            self.keys_pressed.add(symbol)
            self.key_repeat_timers[symbol] = 0.0
            self._handle_game_input(symbol)
    
    def on_key_release(self, symbol, modifiers):
        """Handle key release events.
        
        Args:
            symbol: Key symbol
            modifiers: Key modifiers
        """
        self.keys_pressed.discard(symbol)
        if symbol in self.key_repeat_timers:
            del self.key_repeat_timers[symbol]
    
    def _handle_game_input(self, symbol):
        """Handle game input.
        
        Args:
            symbol: Key symbol
        """
        if self.current_piece is None:
            return
            
        if symbol == key.LEFT:
            self._move_piece(-1, 0)
        elif symbol == key.RIGHT:
            self._move_piece(1, 0)
        elif symbol == key.DOWN:
            self._move_piece(0, 1)
        elif symbol == key.UP:
            self._rotate_piece()
        elif symbol == key.SPACE:
            self._hard_drop()
    
    def _move_piece(self, dx: int, dy: int) -> bool:
        """Move the current piece.
        
        Args:
            dx: X direction
            dy: Y direction
            
        Returns:
            True if move was successful
        """
        if self.current_piece is None:
            return False
            
        old_x, old_y = self.current_piece.x, self.current_piece.y
        self.current_piece.x += dx
        self.current_piece.y += dy
        
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.x, self.current_piece.y = old_x, old_y
            return False
        
        return True
    
    def _rotate_piece(self) -> bool:
        """Rotate the current piece.
        
        Returns:
            True if rotation was successful
        """
        if self.current_piece is None:
            return False
            
        old_rotation = self.current_piece.rotation
        self.current_piece.rotation = (self.current_piece.rotation + 1) % 4
        
        if not self.board.is_valid_position(self.current_piece):
            self.current_piece.rotation = old_rotation
            return False
        
        return True
    
    def _hard_drop(self) -> None:
        """Drop the piece to the bottom immediately."""
        if self.current_piece is None:
            return
            
        drop_distance = 0
        while self._move_piece(0, 1):
            drop_distance += 1
        
        # Add bonus points for hard drop
        self.score += drop_distance * 2
        
        # Place the piece immediately
        self._place_current_piece()
    
    def _place_current_piece(self) -> None:
        """Place the current piece on the board."""
        if self.current_piece is None:
            return
            
        # Get piece blocks before placing
        piece_blocks = self.current_piece.get_blocks()
        
        # Place piece on board
        self.board.place_piece(self.current_piece)
        
        # Add landing effect
        self.effects_manager.add_piece_land_effect(
            piece_blocks, self.renderer.board_x, self.renderer.board_y
        )
        
        # Check for completed lines
        full_lines = self.board.get_full_lines()
        if full_lines:
            self._start_line_clear_effect(full_lines)
        else:
            self._spawn_next_piece()
    
    def _start_line_clear_effect(self, lines: list) -> None:
        """Start the line clear effect.
        
        Args:
            lines: List of line indices to clear
        """
        self.pending_line_clear = True
        self.line_clear_start_time = time.time()
        self.cleared_lines_data = lines
        
        # Add visual effects
        self.effects_manager.add_line_clear_effect(
            lines, self.renderer.board_x, self.renderer.board_y
        )
        
        # Calculate score
        lines_count = len(lines)
        base_score = SCORE_VALUES.get(lines_count, 0)
        level_multiplier = self.level
        self.score += base_score * level_multiplier
        
        # Update lines cleared
        self.lines_cleared += lines_count
        
        # Check for level up
        if self.score >= self.next_level_score:
            self._level_up()
    
    def _complete_line_clear(self) -> None:
        """Complete the line clearing process."""
        if self.cleared_lines_data:
            self.board.clear_lines(self.cleared_lines_data)
            self.cleared_lines_data = None
        
        self.pending_line_clear = False
        self._spawn_next_piece()
    
    def _level_up(self) -> None:
        """Handle level progression."""
        self.level += 1
        self.next_level_score = int(self.next_level_score * LEVEL_SCORE_MULTIPLIER)
        
        # Increase fall speed
        self.fall_time = max(
            MIN_FALL_TIME / 1000.0,
            self.fall_time / SPEED_MULTIPLIER
        )
        
        # Add level up effect
        center_x = self.renderer.sidebar_x + 150
        center_y = self.window.height // 2
        self.effects_manager.add_level_up_effect(center_x, center_y)
    
    def _spawn_next_piece(self) -> None:
        """Spawn the next piece."""
        self.current_piece = self.next_piece
        self.next_piece = Piece()
        
        # Check if game is over
        if not self.board.is_valid_position(self.current_piece):
            self.game_over = True
    
    def update(self, dt: float) -> None:
        """Update game state.
        
        Args:
            dt: Delta time in seconds
        """
        if self.game_over or self.paused:
            return
        
        current_time = time.time()
        
        # Handle key repeats
        self._handle_key_repeats(dt)
        
        # Update effects
        self.effects_manager.update(dt)
        
        # Handle line clear timing
        if self.pending_line_clear:
            if current_time - self.line_clear_start_time >= EFFECT_DURATION / 1000.0:
                self._complete_line_clear()
            return
        
        # Handle piece falling
        if current_time - self.last_fall_time >= self.fall_time:
            if not self._move_piece(0, 1):
                self._place_current_piece()
            self.last_fall_time = current_time
    
    def _handle_key_repeats(self, dt: float) -> None:
        """Handle key repeat logic.
        
        Args:
            dt: Delta time in seconds
        """
        for key_symbol in list(self.key_repeat_timers.keys()):
            self.key_repeat_timers[key_symbol] += dt
            
            # Check if we should repeat the key
            if (self.key_repeat_timers[key_symbol] >= self.key_repeat_delay and
                key_symbol in [key.LEFT, key.RIGHT, key.DOWN]):
                
                # Reset timer for next repeat
                self.key_repeat_timers[key_symbol] = (
                    self.key_repeat_delay - self.key_repeat_interval
                )
                
                # Handle the repeated input
                self._handle_game_input(key_symbol)
    
    def on_draw(self) -> None:
        """Handle window draw event."""
        self.window.clear()
        
        # Clear previous frame's dynamic content
        self.renderer.game_batch = pyglet.graphics.Batch()
        self.renderer.ui_batch = pyglet.graphics.Batch()
        self.renderer.effects_batch = pyglet.graphics.Batch()
        
        # Draw game elements
        self.renderer.draw_board(self.board)
        
        if not self.pending_line_clear:
            self.renderer.draw_piece(self.current_piece)
            self.renderer.draw_ghost_piece(self.current_piece, self.board)
        
        self.renderer.draw_next_piece(self.next_piece)
        self.renderer.draw_ui(self.score, self.level, self.lines_cleared)
        
        # Draw effects
        self.effects_manager.draw(self.renderer.effects_batch)
        
        # Draw overlays
        if self.game_over:
            self.renderer.draw_game_over()
        elif self.paused:
            self.renderer.draw_pause_screen()
        
        # Render everything
        self.renderer.render()
    
    def run(self) -> None:
        """Start the game loop."""
        print("Starting Pyglet Tetris...")
        print("Controls:")
        print("  Arrow Keys: Move/Rotate")
        print("  Space: Hard Drop")
        print("  P: Pause")
        print("  R: Restart (when game over)")
        print("  ESC: Quit")
        
        try:
            pyglet.app.run()
        except KeyboardInterrupt:
            print("\nGame interrupted by user")
        finally:
            print("Game ended")