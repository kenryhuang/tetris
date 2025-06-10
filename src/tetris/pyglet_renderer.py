"""Pyglet-based renderer for the Tetris game.

This module provides a modern, OpenGL-accelerated renderer using Pyglet
for better visual effects and performance compared to Pygame.
"""

import pyglet
from pyglet import shapes, text
from pyglet.gl import *
from typing import Optional, Tuple, List
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GAME_WIDTH, GAME_HEIGHT,
    CELL_SIZE, BORDER_WIDTH, SIDEBAR_WIDTH, PREVIEW_SIZE,
    COLORS, BOARD_WIDTH, BOARD_HEIGHT, PIECE_COLORS
)
from .board import Board
from .piece import Piece


class PygletRenderer:
    """Handles all game rendering using Pyglet with OpenGL acceleration."""
    
    def __init__(self):
        """Initialize the Pyglet renderer."""
        # Create window with OpenGL context
        self.window = pyglet.window.Window(
            width=WINDOW_WIDTH, 
            height=WINDOW_HEIGHT,
            caption="Tetris - Pyglet Edition",
            resizable=False
        )
        
        # Enable alpha blending for transparency effects
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Create batches for efficient rendering
        self.background_batch = pyglet.graphics.Batch()
        self.game_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()
        self.effects_batch = pyglet.graphics.Batch()
        
        # Calculate positions
        self.board_x = BORDER_WIDTH
        self.board_y = BORDER_WIDTH
        self.sidebar_x = GAME_WIDTH + BORDER_WIDTH * 2
        
        # Create background elements
        self._create_background()
        
        # Font for UI text
        self.font_large = pyglet.font.load('Arial', 24)
        self.font_medium = pyglet.font.load('Arial', 16)
        self.font_small = pyglet.font.load('Arial', 12)
        
        # Store shapes for reuse
        self.board_cells = []
        self.ui_elements = []
        
    def _create_background(self):
        """Create static background elements."""
        # Main background
        self.background = shapes.Rectangle(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
            color=COLORS['BACKGROUND'],
            batch=self.background_batch
        )
        
        # Game area border
        border_color = COLORS['BORDER']
        
        # Top border
        shapes.Rectangle(
            0, GAME_HEIGHT + BORDER_WIDTH, 
            GAME_WIDTH + BORDER_WIDTH * 2, BORDER_WIDTH,
            color=border_color, batch=self.background_batch
        )
        
        # Bottom border
        shapes.Rectangle(
            0, 0, GAME_WIDTH + BORDER_WIDTH * 2, BORDER_WIDTH,
            color=border_color, batch=self.background_batch
        )
        
        # Left border
        shapes.Rectangle(
            0, 0, BORDER_WIDTH, GAME_HEIGHT + BORDER_WIDTH * 2,
            color=border_color, batch=self.background_batch
        )
        
        # Right border
        shapes.Rectangle(
            GAME_WIDTH + BORDER_WIDTH, 0, 
            BORDER_WIDTH, GAME_HEIGHT + BORDER_WIDTH * 2,
            color=border_color, batch=self.background_batch
        )
        
        # Sidebar background
        shapes.Rectangle(
            self.sidebar_x, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT,
            color=COLORS['SIDEBAR'], batch=self.background_batch
        )
    
    def draw_cell(self, x: int, y: int, color: Tuple[int, int, int], 
                  offset_x: int = 0, offset_y: int = 0, 
                  size: int = CELL_SIZE, batch=None) -> shapes.Rectangle:
        """Draw a single cell with modern flat design.
        
        Args:
            x: Grid x coordinate
            y: Grid y coordinate  
            color: RGB color tuple
            offset_x: X offset for drawing position
            offset_y: Y offset for drawing position
            size: Size of the cell
            batch: Pyglet batch for efficient rendering
            
        Returns:
            The created rectangle shape
        """
        if batch is None:
            batch = self.game_batch
            
        pixel_x = offset_x + x * size
        # Flip Y coordinate for Pyglet (origin at bottom-left)
        pixel_y = WINDOW_HEIGHT - (offset_y + (y + 1) * size)
        
        # Main cell rectangle
        cell_rect = shapes.Rectangle(
            pixel_x + 1, pixel_y + 1, size - 2, size - 2,
            color=color, batch=batch
        )
        
        # Add subtle border for depth
        border_color = tuple(max(0, c - 30) for c in color)
        border_rect = shapes.Rectangle(
            pixel_x, pixel_y, size, size,
            color=border_color, batch=batch
        )
        
        return cell_rect
    
    def draw_board(self, board: Board) -> None:
        """Draw the game board.
        
        Args:
            board: The game board to draw
        """
        # Clear previous board cells
        self.board_cells.clear()
        
        for y in range(board.height):
            for x in range(board.width):
                if board.grid[y][x] is not None:
                    self.draw_cell(
                        x, y, board.grid[y][x],
                        self.board_x, self.board_y,
                        batch=self.game_batch
                    )
    
    def draw_piece(self, piece: Optional[Piece]) -> None:
        """Draw the current falling piece.
        
        Args:
            piece: The piece to draw, or None
        """
        if piece is None:
            return
            
        for x, y in piece.get_blocks():
            if y >= 0:  # Only draw visible blocks
                self.draw_cell(
                    x, y, piece.color,
                    self.board_x, self.board_y,
                    batch=self.game_batch
                )
    
    def draw_ghost_piece(self, piece: Optional[Piece], board: Board) -> None:
        """Draw a ghost (preview) of where the piece will land.
        
        Args:
            piece: The current piece
            board: The game board
        """
        if piece is None:
            return
            
        # Create a copy and drop it to the bottom
        ghost_piece = Piece(piece.type, piece.x, piece.y)
        ghost_piece.rotation = piece.rotation
        
        while board.is_valid_position(ghost_piece):
            ghost_piece.y += 1
        ghost_piece.y -= 1
        
        # Draw with transparency
        ghost_color = (*piece.color[:3], 80)  # Add alpha
        
        for x, y in ghost_piece.get_blocks():
            if y >= 0:
                pixel_x = self.board_x + x * CELL_SIZE
                pixel_y = WINDOW_HEIGHT - (self.board_y + (y + 1) * CELL_SIZE)
                
                # Draw semi-transparent ghost piece
                shapes.Rectangle(
                    pixel_x + 2, pixel_y + 2, 
                    CELL_SIZE - 4, CELL_SIZE - 4,
                    color=ghost_color, batch=self.game_batch
                )
    
    def draw_next_piece(self, piece: Optional[Piece]) -> None:
        """Draw the next piece preview.
        
        Args:
            piece: The next piece to draw
        """
        if piece is None:
            return
            
        # Preview area position
        preview_x = self.sidebar_x + 20
        preview_y = WINDOW_HEIGHT - 150
        
        # Draw preview background
        shapes.Rectangle(
            preview_x - 10, preview_y - 10,
            PREVIEW_SIZE * 4 + 20, PREVIEW_SIZE * 4 + 20,
            color=COLORS['WHITE'], batch=self.ui_batch
        )
        
        # Center the piece in preview area
        blocks = piece.get_blocks()
        if blocks:
            min_x = min(x for x, y in blocks)
            max_x = max(x for x, y in blocks)
            min_y = min(y for x, y in blocks)
            max_y = max(y for x, y in blocks)
            
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            
            offset_x = preview_x + (4 - width) * PREVIEW_SIZE // 2 - min_x * PREVIEW_SIZE
            offset_y = preview_y + (4 - height) * PREVIEW_SIZE // 2 - min_y * PREVIEW_SIZE
            
            for x, y in blocks:
                pixel_x = offset_x + x * PREVIEW_SIZE
                pixel_y = WINDOW_HEIGHT - (offset_y + (y + 1) * PREVIEW_SIZE)
                
                shapes.Rectangle(
                    pixel_x, pixel_y, PREVIEW_SIZE, PREVIEW_SIZE,
                    color=piece.color, batch=self.ui_batch
                )
    
    def draw_ui(self, score: int, level: int, lines: int) -> None:
        """Draw the user interface elements.
        
        Args:
            score: Current score
            level: Current level
            lines: Lines cleared
        """
        # Clear previous UI elements
        self.ui_elements.clear()
        
        # UI text positions
        text_x = self.sidebar_x + 20
        
        # Score
        score_label = text.Label(
            'SCORE', font_name='Arial', font_size=16,
            x=text_x, y=WINDOW_HEIGHT - 250,
            color=(*COLORS['TEXT'], 255), batch=self.ui_batch
        )
        score_value = text.Label(
            str(score), font_name='Arial', font_size=20,
            x=text_x, y=WINDOW_HEIGHT - 275,
            color=(*COLORS['ACCENT'], 255), batch=self.ui_batch
        )
        
        # Level
        level_label = text.Label(
            'LEVEL', font_name='Arial', font_size=16,
            x=text_x, y=WINDOW_HEIGHT - 320,
            color=(*COLORS['TEXT'], 255), batch=self.ui_batch
        )
        level_value = text.Label(
            str(level), font_name='Arial', font_size=20,
            x=text_x, y=WINDOW_HEIGHT - 345,
            color=(*COLORS['ACCENT'], 255), batch=self.ui_batch
        )
        
        # Lines
        lines_label = text.Label(
            'LINES', font_name='Arial', font_size=16,
            x=text_x, y=WINDOW_HEIGHT - 390,
            color=(*COLORS['TEXT'], 255), batch=self.ui_batch
        )
        lines_value = text.Label(
            str(lines), font_name='Arial', font_size=20,
            x=text_x, y=WINDOW_HEIGHT - 415,
            color=(*COLORS['ACCENT'], 255), batch=self.ui_batch
        )
        
        # Next piece label
        next_label = text.Label(
            'NEXT', font_name='Arial', font_size=16,
            x=text_x, y=WINDOW_HEIGHT - 100,
            color=(*COLORS['TEXT'], 255), batch=self.ui_batch
        )
    
    def draw_game_over(self) -> None:
        """Draw game over screen."""
        # Semi-transparent overlay
        overlay = shapes.Rectangle(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
            color=(0, 0, 0, 180), batch=self.ui_batch
        )
        
        # Game over text
        game_over_text = text.Label(
            'GAME OVER', font_name='Arial', font_size=36,
            x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2 + 50,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255), batch=self.ui_batch
        )
        
        restart_text = text.Label(
            'Press R to restart or ESC to quit', 
            font_name='Arial', font_size=16,
            x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2 - 20,
            anchor_x='center', anchor_y='center',
            color=(200, 200, 200, 255), batch=self.ui_batch
        )
    
    def draw_pause_screen(self) -> None:
        """Draw pause screen."""
        # Semi-transparent overlay
        overlay = shapes.Rectangle(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
            color=(0, 0, 0, 120), batch=self.ui_batch
        )
        
        # Pause text
        pause_text = text.Label(
            'PAUSED', font_name='Arial', font_size=36,
            x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2 + 20,
            anchor_x='center', anchor_y='center',
            color=(255, 255, 255, 255), batch=self.ui_batch
        )
        
        continue_text = text.Label(
            'Press P to continue', 
            font_name='Arial', font_size=16,
            x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2 - 20,
            anchor_x='center', anchor_y='center',
            color=(200, 200, 200, 255), batch=self.ui_batch
        )
    
    def clear_batches(self) -> None:
        """Clear all rendering batches for the next frame."""
        # Note: In Pyglet, we typically don't need to manually clear batches
        # as they are redrawn each frame. However, for dynamic content,
        # we might need to recreate certain elements.
        pass
    
    def render(self) -> None:
        """Render all batches to the screen."""
        self.window.clear()
        
        # Draw in order: background, game, effects, UI
        self.background_batch.draw()
        self.game_batch.draw()
        self.effects_batch.draw()
        self.ui_batch.draw()
    
    def get_window(self) -> pyglet.window.Window:
        """Get the Pyglet window instance.
        
        Returns:
            The Pyglet window
        """
        return self.window