"""Renderer module for Pyglet Tetris implementation.

This module contains the PygletRenderer class that handles all
graphics rendering using pyglet's OpenGL capabilities.
"""

import pyglet
from pyglet import gl, shapes, text
import math
from typing import Optional, Tuple, List
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GAME_WIDTH, GAME_HEIGHT,
    CELL_SIZE, BORDER_WIDTH, SIDEBAR_WIDTH, PREVIEW_SIZE,
    COLORS, BOARD_WIDTH, BOARD_HEIGHT, GLOW_INTENSITY,
    SHADOW_OFFSET, BORDER_RADIUS, GRID_ALPHA
)
from .board import Board
from .piece import Piece


class PygletRenderer:
    """Handles all game rendering using Pyglet and OpenGL."""
    
    def __init__(self, window: pyglet.window.Window = None):
        """Initialize the renderer.
        
        Args:
            window: Existing pyglet window to use. If None, creates a new one.
        """
        # Use provided window or create new one
        if window is None:
            self.window = pyglet.window.Window(
                width=WINDOW_WIDTH,
                height=WINDOW_HEIGHT,
                caption="Tetris - Pyglet Edition",
                resizable=False,
                vsync=True
            )
        else:
            self.window = window
        
        # Enable blending for transparency
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        # Calculate positions
        self.board_x = BORDER_WIDTH
        self.board_y = BORDER_WIDTH
        self.sidebar_x = GAME_WIDTH + BORDER_WIDTH * 2
        
        # Create batch for efficient rendering
        self.main_batch = pyglet.graphics.Batch()
        self.ui_batch = pyglet.graphics.Batch()
        self.effect_batch = pyglet.graphics.Batch()
        
        # Create groups for layered rendering
        self.background_group = pyglet.graphics.Group(order=0)
        self.board_group = pyglet.graphics.Group(order=1)
        self.piece_group = pyglet.graphics.Group(order=2)
        self.effect_group = pyglet.graphics.Group(order=3)
        self.ui_group = pyglet.graphics.Group(order=4)
        
        # Initialize fonts
        self.font_large = pyglet.font.load('Arial', 24)
        self.font_medium = pyglet.font.load('Arial', 16)
        self.font_small = pyglet.font.load('Arial', 12)
        
        # Keep references to dynamic shapes to prevent garbage collection
        self.dynamic_shapes = []
        
        # Create static UI elements
        self._create_static_elements()
        
        # Animation time for effects
        self.animation_time = 0.0
        
    def get_window(self) -> pyglet.window.Window:
        """Get the pyglet window instance.
        
        Returns:
            The pyglet window
        """
        return self.window
    
    def _create_static_elements(self) -> None:
        """Create static UI elements that don't change."""
        # Background
        self.background = shapes.Rectangle(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
            color=COLORS['BACKGROUND'][:3],
            batch=self.main_batch,
            group=self.background_group
        )
        
        # Game board background
        self.board_bg = shapes.Rectangle(
            self.board_x, self.board_y, GAME_WIDTH, GAME_HEIGHT,
            color=COLORS['WHITE'][:3],
            batch=self.main_batch,
            group=self.background_group
        )
        
        # Board border
        self.board_border = shapes.Rectangle(
            self.board_x - 2, self.board_y - 2, 
            GAME_WIDTH + 4, GAME_HEIGHT + 4,
            color=COLORS['BORDER'][:3],
            batch=self.main_batch,
            group=self.background_group
        )
        
        # Sidebar background
        self.sidebar_bg = shapes.Rectangle(
            self.sidebar_x, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT,
            color=COLORS['SIDEBAR'][:3],
            batch=self.main_batch,
            group=self.background_group
        )
    
    def _draw_cell(self, x: float, y: float, color: Tuple[int, int, int, int], 
                   size: float = CELL_SIZE, glow: float = 0.0, 
                   batch: pyglet.graphics.Batch = None,
                   group: pyglet.graphics.Group = None) -> List:
        """Draw a single cell with modern flat design and optional glow.
        
        Args:
            x: X position in pixels
            y: Y position in pixels
            color: RGBA color tuple
            size: Size of the cell
            glow: Glow intensity (0.0 to 1.0)
            batch: Pyglet batch for rendering
            group: Pyglet group for layering
            
        Returns:
            List of created shapes
        """
        if batch is None:
            batch = self.main_batch
        if group is None:
            group = self.piece_group
            
        shapes_list = []
        
        # Determine alpha and main color first
        if len(color) > 3:
            main_color = color[:3]
            alpha = color[3]
        else:
            main_color = color[:3]
            alpha = 255
        
        # Draw glow effect if needed
        if glow > 0.0:
            glow_size = size + glow * 10
            glow_alpha = int(glow * 50) / 255.0
            glow_color = tuple(int(c * glow_alpha) for c in color[:3])
            glow_rect = shapes.Rectangle(
                x - (glow_size - size) / 2,
                y - (glow_size - size) / 2,
                glow_size, glow_size,
                color=glow_color,
                batch=batch,
                group=group
            )
            shapes_list.append(glow_rect)
        
        # Border (light gray)
        border_color = (200, 200, 200)  # Light gray border
        border_rect = shapes.Rectangle(
            x, y, size, size,
            color=border_color,
            batch=batch,
            group=group
        )
        # Apply alpha transparency for ghost pieces
        if alpha < 255:
            border_rect.opacity = alpha
        shapes_list.append(border_rect)
            
        main_rect = shapes.Rectangle(
            x + 2, y + 2, size - 4, size - 4,
            color=main_color,
            batch=batch,
            group=group
        )
        # Apply alpha transparency for ghost pieces
        if alpha < 255:
            main_rect.opacity = alpha
        shapes_list.append(main_rect)
        
        # Inner highlight for depth
        highlight_alpha = 0.3
        highlight_color = tuple(int(min(255, c + 40)) for c in main_color)
        highlight_rect = shapes.Rectangle(
            x + 2, y + size - 3, size - 4, 1,
            color=highlight_color,
            batch=batch,
            group=group
        )
        # Apply alpha transparency for ghost pieces
        if alpha < 255:
            highlight_rect.opacity = alpha
        shapes_list.append(highlight_rect)
        
        # Left highlight
        left_highlight = shapes.Rectangle(
            x + 2, y + 2, 1, size - 4,
            color=highlight_color,
            batch=batch,
            group=group
        )
        # Apply alpha transparency for ghost pieces
        if alpha < 255:
            left_highlight.opacity = alpha
        shapes_list.append(left_highlight)
        
        # Save references to prevent garbage collection
        self.dynamic_shapes.extend(shapes_list)
        return shapes_list
    
    def _draw_grid(self) -> None:
        """Draw subtle grid lines."""
        # Use a darker color for better contrast
        grid_color = (100, 100, 100, int(255 * GRID_ALPHA))
        
        # Vertical lines
        for x in range(1, BOARD_WIDTH):
            line_x = self.board_x + x * CELL_SIZE
            line = shapes.Line(
                line_x, self.board_y,
                line_x, self.board_y + GAME_HEIGHT,
                color=grid_color[:3],
                batch=self.main_batch,
                group=self.board_group
            )
            line.opacity = grid_color[3]
        
        # Horizontal lines
        for y in range(1, BOARD_HEIGHT):
            line_y = self.board_y + y * CELL_SIZE
            line = shapes.Line(
                self.board_x, line_y,
                self.board_x + GAME_WIDTH, line_y,
                color=grid_color[:3],
                batch=self.main_batch,
                group=self.board_group
            )
            line.opacity = grid_color[3]
    
    def draw_board(self, board: Board) -> None:
        """Draw the game board.
        
        Args:
            board: The game board to draw
        """
        self._ensure_static_elements_created()
        self.dynamic_shapes.clear()
        
        # Draw all board blocks
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                color = board.get_block_at(x, y)
                if color is not None:
                    self._draw_board_block(board, x, y, color)
    
    def _ensure_static_elements_created(self) -> None:
        """Ensure static elements are created only once."""
        if not hasattr(self, '_static_elements_created'):
            self._create_static_elements()
            self._draw_grid()
            self._static_elements_created = True
    
    def _draw_board_block(self, board: Board, x: int, y: int, color: Tuple[int, int, int, int]) -> None:
        """Draw a single block on the board with appropriate effects.
        
        Args:
            board: The game board
            x: Block x coordinate
            y: Block y coordinate
            color: Block color
        """
        pixel_x, pixel_y = self._get_board_pixel_position(x, y)
        
        if board.is_line_clearing(y):
            self._draw_line_clearing_block(pixel_x, pixel_y, color, board.get_line_clear_progress(y))
        else:
            self._draw_normal_block(board, pixel_x, pixel_y, color, x, y)
    
    def _get_board_pixel_position(self, x: int, y: int) -> Tuple[int, int]:
        """Get pixel position for board coordinates.
        
        Args:
            x: Board x coordinate
            y: Board y coordinate
            
        Returns:
            Tuple of (pixel_x, pixel_y)
        """
        pixel_x = self.board_x + x * CELL_SIZE
        pixel_y = self.board_y + (BOARD_HEIGHT - 1 - y) * CELL_SIZE
        return pixel_x, pixel_y
    
    def _draw_line_clearing_block(self, pixel_x: int, pixel_y: int, color: Tuple[int, int, int, int], progress: float) -> None:
        """Draw a block with line clearing animation.
        
        Args:
            pixel_x: Pixel x position
            pixel_y: Pixel y position
            color: Block color
            progress: Animation progress (0.0 to 1.0)
        """
        # Fade out and scale effect
        alpha = int(255 * (1.0 - progress))
        scale = 1.0 - progress * 0.3
        size = CELL_SIZE * scale
        offset = (CELL_SIZE - size) / 2
        
        color_with_alpha = (*color[:3], alpha)
        glow = 0.0 * (1.0 - progress)  # Reduce glow during clearing
        
        self._draw_cell(
            pixel_x + offset, pixel_y + offset,
            color_with_alpha, size, glow
        )
    
    def _draw_normal_block(self, board: Board, pixel_x: int, pixel_y: int, color: Tuple[int, int, int, int], x: int, y: int) -> None:
        """Draw a normal block with optional flash effect.
        
        Args:
            board: The game board
            pixel_x: Pixel x position
            pixel_y: Pixel y position
            color: Block color
            x: Board x coordinate
            y: Board y coordinate
        """
        glow = 0.0
        
        if board.is_block_locked(x, y):
            # Apply flash effect to locked blocks
            alpha_modifier = self._calculate_flash_alpha()
            if alpha_modifier < 1.0:
                flash_color = self._apply_alpha_modifier(color, alpha_modifier)
                self._draw_cell(pixel_x, pixel_y, flash_color, glow=0)
                return
        
        self._draw_cell(pixel_x, pixel_y, color, glow=glow)
    
    def _apply_alpha_modifier(self, color: Tuple[int, int, int, int], alpha_modifier: float) -> Tuple[int, int, int, int]:
        """Apply alpha modifier to a color.
        
        Args:
            color: Original color
            alpha_modifier: Alpha multiplier (0.0 to 1.0)
            
        Returns:
            Color with modified alpha
        """
        original_alpha = color[3] if len(color) > 3 else 255
        return (*color[:3], int(original_alpha * alpha_modifier))
    
    def draw_piece(self, piece: Piece, ghost: bool = False) -> None:
        """Draw a tetris piece.
        
        Args:
            piece: The piece to draw
            ghost: Whether to draw as ghost piece
        """
        blocks = piece.get_visual_blocks() if not ghost else piece.get_blocks()
        
        for block_x, block_y in blocks:
            if block_y >= 0:  # Don't draw blocks above the board
                pixel_x, pixel_y = self._get_board_pixel_position(block_x, block_y)
                
                if ghost:
                    self._draw_ghost_block(pixel_x, pixel_y, piece.color)
                else:
                    self._draw_regular_piece_block(pixel_x, pixel_y, piece)
    
    def _draw_ghost_block(self, pixel_x: int, pixel_y: int, color: Tuple[int, int, int, int]) -> None:
        """Draw a ghost piece block.
        
        Args:
            pixel_x: Pixel x position
            pixel_y: Pixel y position
            color: Original piece color
        """
        # Ghost piece - more transparent for better distinction
        ghost_color = (*color[:3], 40)
        self._draw_cell(pixel_x, pixel_y, ghost_color)
    
    def _draw_regular_piece_block(self, pixel_x: int, pixel_y: int, piece: Piece) -> None:
        """Draw a regular piece block with effects.
        
        Args:
            pixel_x: Pixel x position
            pixel_y: Pixel y position
            piece: The piece being drawn
        """
        glow = piece.glow_intensity * GLOW_INTENSITY
        scale = piece.scale
        
        if scale != 1.0:
            self._draw_scaled_block(pixel_x, pixel_y, piece.color, scale, glow)
        else:
            self._draw_cell(pixel_x, pixel_y, piece.color, glow=glow)
    
    def _draw_scaled_block(self, pixel_x: int, pixel_y: int, color: Tuple[int, int, int, int], scale: float, glow: float) -> None:
        """Draw a block with scaling effect.
        
        Args:
            pixel_x: Pixel x position
            pixel_y: Pixel y position
            color: Block color
            scale: Scale factor
            glow: Glow intensity
        """
        size = CELL_SIZE * scale
        offset = (CELL_SIZE - size) / 2
        self._draw_cell(
            pixel_x + offset, pixel_y + offset,
            color, size, glow
        )
    
    def draw_preview_piece(self, piece: Piece, x: int, y: int) -> None:
        """Draw a preview piece in the sidebar.
        
        Args:
            piece: The piece to preview
            x: X position in the sidebar
            y: Y position in the sidebar
        """
        shape = piece.get_shape()
        preview_cell_size = CELL_SIZE / 2
        
        for row in range(4):
            for col in range(4):
                if shape[row][col]:
                    pixel_x, pixel_y = self._get_preview_pixel_position(x, y, col, row, preview_cell_size)
                    self._draw_preview_cell(pixel_x, pixel_y, piece.color, preview_cell_size)
    
    def _get_preview_pixel_position(self, base_x: int, base_y: int, col: int, row: int, cell_size: float) -> Tuple[int, int]:
        """Get pixel position for preview piece cell.
        
        Args:
            base_x: Base x position
            base_y: Base y position
            col: Column in piece shape
            row: Row in piece shape
            cell_size: Size of preview cell
            
        Returns:
            Tuple of (pixel_x, pixel_y)
        """
        pixel_x = base_x + col * cell_size
        pixel_y = base_y + (2 - row) * cell_size
        return pixel_x, pixel_y
    
    def _draw_preview_cell(self, pixel_x: int, pixel_y: int, color: Tuple[int, int, int, int], size: float) -> None:
        """Draw a single preview cell.
        
        Args:
            pixel_x: Pixel x position
            pixel_y: Pixel y position
            color: Cell color
            size: Cell size
        """
        self._draw_cell(
            pixel_x, pixel_y, color,
            size, batch=self.ui_batch,
            group=self.ui_group
        )
    
    def draw_text(self, text_str: str, x: int, y: int, 
                  font_size: str = 'medium', color: Tuple[int, int, int] = None,
                  anchor_x: str = 'left', anchor_y: str = 'bottom') -> text.Label:
        """Draw text on the screen.
        
        Args:
            text_str: Text to draw
            x: X position
            y: Y position
            font_size: Font size ('large', 'medium', 'small')
            color: Text color
            anchor_x: Horizontal anchor
            anchor_y: Vertical anchor
            
        Returns:
            Created text label
        """
        if color is None:
            color = COLORS['TEXT'][:3]
        
        font_map = {
            'large': self.font_large,
            'medium': self.font_medium,
            'small': self.font_small
        }
        
        font = font_map.get(font_size, self.font_medium)
        
        label = text.Label(
            text_str,
            font_name=font.name,
            font_size=font.size,
            x=x, y=y,
            anchor_x=anchor_x,
            anchor_y=anchor_y,
            color=(*color, 255),
            batch=self.ui_batch,
            group=self.ui_group
        )
        
        # Add to tracking list for cleanup
        if not hasattr(self, '_ui_labels'):
            self._ui_labels = []
        self._ui_labels.append(label)
        
        return label
    
    def draw_ui(self, score: int, level: int, lines: int, next_piece: Optional[Piece] = None,
                current_piece: Optional[Piece] = None, game_time: Optional[int] = None) -> None:
        """Draw the user interface elements.
        
        Args:
            score: Current score
            level: Current level
            lines: Lines cleared
            next_piece: Next piece to display in preview
            current_piece: Current falling piece
            game_time: Game time in seconds
        """
        self._clear_ui_labels()
        
        sidebar_x = self.sidebar_x + 20
        current_y = WINDOW_HEIGHT - 50
        
        # Draw UI sections in order
        current_y = self._draw_next_piece_section(next_piece, sidebar_x, current_y)
        current_y = self._draw_score_section(score, sidebar_x, current_y)
        current_y = self._draw_level_section(level, sidebar_x, current_y)
        current_y = self._draw_lines_section(lines, level, sidebar_x, current_y)
        current_y = self._draw_current_piece_section(current_piece, sidebar_x, current_y)
        current_y = self._draw_time_section(game_time, sidebar_x, current_y)
        current_y = self._draw_controls_section(sidebar_x, current_y)
    
    def _clear_ui_labels(self) -> None:
        """Clear previous UI labels."""
        for label in getattr(self, '_ui_labels', []):
            label.delete()
        self._ui_labels = []
    
    def _draw_next_piece_section(self, next_piece: Optional[Piece], sidebar_x: int, current_y: int) -> int:
        """Draw the next piece preview section.
        
        Args:
            next_piece: Next piece to display
            sidebar_x: Sidebar x position
            current_y: Current y position
            
        Returns:
            Updated y position
        """
        if next_piece:
            self.draw_text("NEXT", sidebar_x, current_y, 'medium', COLORS['TEXT'][:3])
            current_y -= 40
            preview_x = sidebar_x + 10
            preview_y = current_y - 60
            self.draw_preview_piece(next_piece, preview_x, preview_y)
            current_y -= 120
        return current_y
    
    def _draw_score_section(self, score: int, sidebar_x: int, current_y: int) -> int:
        """Draw the score section.
        
        Args:
            score: Current score
            sidebar_x: Sidebar x position
            current_y: Current y position
            
        Returns:
            Updated y position
        """
        self.draw_text("SCORE", sidebar_x, current_y, 'medium', COLORS['TEXT'][:3])
        current_y -= 30
        self.draw_text(f"{score:,}", sidebar_x, current_y, 'large', COLORS['ACCENT'][:3])
        current_y -= 60
        return current_y
    
    def _draw_level_section(self, level: int, sidebar_x: int, current_y: int) -> int:
        """Draw the level section.
        
        Args:
            level: Current level
            sidebar_x: Sidebar x position
            current_y: Current y position
            
        Returns:
            Updated y position
        """
        self.draw_text("LEVEL", sidebar_x, current_y, 'medium', COLORS['TEXT'][:3])
        current_y -= 30
        self.draw_text(str(level), sidebar_x, current_y, 'large', COLORS['ACCENT'][:3])
        current_y -= 60
        return current_y
    
    def _draw_lines_section(self, lines: int, level: int, sidebar_x: int, current_y: int) -> int:
        """Draw the lines section with next level progress.
        
        Args:
            lines: Lines cleared
            level: Current level
            sidebar_x: Sidebar x position
            current_y: Current y position
            
        Returns:
            Updated y position
        """
        self.draw_text("LINES", sidebar_x, current_y, 'medium', COLORS['TEXT'][:3])
        current_y -= 30
        self.draw_text(str(lines), sidebar_x, current_y, 'large', COLORS['ACCENT'][:3])
        current_y -= 50
        
        # Next level progress
        lines_to_next_level = (level * 10) - lines
        if lines_to_next_level > 0:
            self.draw_text(f"Next Level: {lines_to_next_level} lines", sidebar_x, current_y, 'small', COLORS['TEXT'][:3])
        current_y -= 30
        return current_y
    
    def _draw_current_piece_section(self, current_piece: Optional[Piece], sidebar_x: int, current_y: int) -> int:
        """Draw the current piece section.
        
        Args:
            current_piece: Current falling piece
            sidebar_x: Sidebar x position
            current_y: Current y position
            
        Returns:
            Updated y position
        """
        if current_piece:
            self.draw_text("CURRENT", sidebar_x, current_y, 'medium', COLORS['TEXT'][:3])
            current_y -= 25
            self.draw_text(f"Type: {current_piece.type}", sidebar_x, current_y, 'small', COLORS['ACCENT'][:3])
            current_y -= 40
        return current_y
    
    def _draw_time_section(self, game_time: Optional[int], sidebar_x: int, current_y: int) -> int:
        """Draw the game time section.
        
        Args:
            game_time: Game time in seconds
            sidebar_x: Sidebar x position
            current_y: Current y position
            
        Returns:
            Updated y position
        """
        if game_time is not None:
            self.draw_text("TIME", sidebar_x, current_y, 'medium', COLORS['TEXT'][:3])
            current_y -= 25
            time_str = self._format_time(game_time)
            self.draw_text(time_str, sidebar_x, current_y, 'small', COLORS['ACCENT'][:3])
            current_y -= 40
        return current_y
    
    def _draw_controls_section(self, sidebar_x: int, current_y: int) -> int:
        """Draw the controls section.
        
        Args:
            sidebar_x: Sidebar x position
            current_y: Current y position
            
        Returns:
            Updated y position
        """
        self.draw_text("CONTROLS", sidebar_x, current_y, 'medium', COLORS['TEXT'][:3])
        current_y -= 25
        
        controls = [
            "← → Move",
            "↓ Soft Drop",
            "↑ Rotate",
            "Space Hard Drop",
            "P Pause",
            "R Restart"
        ]
        
        for control in controls:
            self.draw_text(control, sidebar_x, current_y, 'small', COLORS['GRAY'][:3])
            current_y -= 20
        
        return current_y
    
    def _format_time(self, game_time: int) -> str:
        """Format game time as MM:SS.
        
        Args:
            game_time: Game time in seconds
            
        Returns:
            Formatted time string
        """
        minutes = game_time // 60
        seconds = game_time % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def draw_game_over(self, final_score: int) -> None:
        """Draw game over screen.
        
        Args:
            final_score: Final score to display
        """
        self._draw_overlay(180)
        self._draw_game_over_text(final_score)
    
    def draw_pause_screen(self) -> None:
        """Draw pause screen overlay."""
        self._draw_overlay(120)
        self._draw_pause_text()
    
    def _draw_overlay(self, opacity: int) -> None:
        """Draw semi-transparent overlay.
        
        Args:
            opacity: Overlay opacity (0-255)
        """
        overlay = shapes.Rectangle(
            0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
            color=(0, 0, 0),
            batch=self.effect_batch,
            group=self.effect_group
        )
        overlay.opacity = opacity
    
    def _draw_game_over_text(self, final_score: int) -> None:
        """Draw game over text elements.
        
        Args:
            final_score: Final score to display
        """
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        self.draw_text(
            "GAME OVER", center_x, center_y + 50,
            'large', COLORS['RED'][:3],
            anchor_x='center', anchor_y='center'
        )
        
        self.draw_text(
            f"Final Score: {final_score:,}", center_x, center_y,
            'medium', COLORS['TEXT'][:3],
            anchor_x='center', anchor_y='center'
        )
        
        self.draw_text(
            "Press R to restart or ESC to quit", center_x, center_y - 50,
            'small', COLORS['GRAY'][:3],
            anchor_x='center', anchor_y='center'
        )
    
    def _draw_pause_text(self) -> None:
        """Draw pause screen text elements."""
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2
        
        self.draw_text(
            "PAUSED", center_x, center_y,
            'large', COLORS['ACCENT'][:3],
            anchor_x='center', anchor_y='center'
        )
        
        self.draw_text(
            "Press P to resume", center_x, center_y - 50,
            'medium', COLORS['TEXT'][:3],
            anchor_x='center', anchor_y='center'
        )
    
    def _calculate_flash_alpha(self) -> float:
        """Calculate the alpha value for flashing locked blocks.
        
        Returns:
            Alpha multiplier between 0.1 and 1.0 for flashing effect
        """
        # Create a sine wave that oscillates between 0.1 and 1.0
        # This provides a more noticeable flashing effect
        flash_intensity = 0.5 * math.sin(self.animation_time * 8) + 0.5
        return 0.7 + 0.9 * flash_intensity
    
    def update_animation(self, dt: float) -> None:
        """Update animation timers.
        
        Args:
            dt: Delta time in seconds
        """
        self.animation_time += dt
    
    def clear(self) -> None:
        """Clear the screen."""
        self.window.clear()
    
    def draw(self) -> None:
        """Draw all batches."""
        self.main_batch.draw()
        self.effect_batch.draw()
        self.ui_batch.draw()
        
    
    def cleanup(self) -> None:
        """Clean up resources."""
        # Pyglet handles most cleanup automatically
        pass