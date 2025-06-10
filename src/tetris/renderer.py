"""Game rendering using Pygame."""

import pygame
from typing import Optional, Tuple
from .constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, GAME_WIDTH, GAME_HEIGHT,
    CELL_SIZE, BORDER_WIDTH, SIDEBAR_WIDTH, PREVIEW_SIZE,
    COLORS, BOARD_WIDTH, BOARD_HEIGHT
)
from .board import Board
from .piece import Piece


class GameRenderer:
    """Handles all game rendering using Pygame."""
    
    def __init__(self):
        """Initialize the renderer."""
        pygame.init()
        pygame.font.init()
        
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Calculate positions
        self.board_x = BORDER_WIDTH
        self.board_y = BORDER_WIDTH
        self.sidebar_x = GAME_WIDTH + BORDER_WIDTH * 2
        
    def draw_cell(self, x: int, y: int, color: Tuple[int, int, int], 
                  offset_x: int = 0, offset_y: int = 0, size: int = CELL_SIZE) -> None:
        """Draw a single cell with flat design.
        
        Args:
            x: Grid x coordinate
            y: Grid y coordinate
            color: RGB color tuple
            offset_x: X offset for drawing position
            offset_y: Y offset for drawing position
            size: Size of the cell
        """
        pixel_x = offset_x + x * size
        pixel_y = offset_y + y * size
        
        # Draw filled rectangle with rounded corners effect
        pygame.draw.rect(self.screen, color, 
                        (pixel_x + 1, pixel_y + 1, size - 2, size - 2))
        
        # Add subtle shadow/depth with lighter edge
        shadow_color = tuple(min(255, c + 20) for c in color)
        pygame.draw.rect(self.screen, shadow_color, 
                        (pixel_x, pixel_y, size, size), 1)
    
    def draw_board(self, board: Board) -> None:
        """Draw the game board with flat design.
        
        Args:
            board: The game board to draw
        """
        # Draw board background with subtle border
        pygame.draw.rect(self.screen, COLORS['WHITE'],
                        (self.board_x, self.board_y, GAME_WIDTH, GAME_HEIGHT))
        
        # Draw subtle border around the board
        pygame.draw.rect(self.screen, COLORS['BORDER'],
                        (self.board_x - 1, self.board_y - 1, GAME_WIDTH + 2, GAME_HEIGHT + 2), 1)
        
        # Draw subtle grid lines for flat design
        grid_color = (250, 250, 250)  # Very light gray for minimal visual impact
        
        # Vertical grid lines
        for x in range(1, BOARD_WIDTH):
            line_x = self.board_x + x * CELL_SIZE
            pygame.draw.line(self.screen, grid_color,
                           (line_x, self.board_y),
                           (line_x, self.board_y + GAME_HEIGHT))
        
        # Horizontal grid lines
        for y in range(1, BOARD_HEIGHT):
            line_y = self.board_y + y * CELL_SIZE
            pygame.draw.line(self.screen, grid_color,
                           (self.board_x, line_y),
                           (self.board_x + GAME_WIDTH, line_y))
        
        # Draw placed pieces
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                color = board.get_cell(x, y)
                if color:
                    self.draw_cell(x, y, color, self.board_x, self.board_y)
    
    def draw_piece(self, piece: Piece, offset_x: int = None, offset_y: int = None,
                   alpha: int = 255, size: int = CELL_SIZE) -> None:
        """Draw a piece.
        
        Args:
            piece: The piece to draw
            offset_x: X offset (defaults to board position)
            offset_y: Y offset (defaults to board position)
            alpha: Transparency (0-255)
            size: Size of each cell
        """
        if offset_x is None:
            offset_x = self.board_x
        if offset_y is None:
            offset_y = self.board_y
        
        color = piece.color
        if alpha < 255:
            # Create transparent version of the color
            transparent_color = (*color, alpha)
            for x, y in piece.get_blocks():
                if y >= 0:  # Don't draw blocks above the board
                    pixel_x = offset_x + x * size
                    pixel_y = offset_y + y * size
                    # Create surface with per-pixel alpha
                    temp_surface = pygame.Surface((size - 2, size - 2), pygame.SRCALPHA)
                    temp_surface.fill(transparent_color)
                    self.screen.blit(temp_surface, (pixel_x + 1, pixel_y + 1))
        else:
            for x, y in piece.get_blocks():
                if y >= 0:  # Don't draw blocks above the board
                    self.draw_cell(x, y, color, offset_x, offset_y, size)
    
    def draw_ghost_piece(self, piece: Piece) -> None:
        """Draw a ghost piece showing where the current piece would land.
        
        Args:
            piece: The ghost piece to draw
        """
        self.draw_piece(piece, alpha=100)
    
    def draw_next_piece(self, piece: Piece) -> None:
        """Draw the next piece preview.
        
        Args:
            piece: The next piece to draw
        """
        # Draw "NEXT" label with modern styling
        text = self.font_medium.render("NEXT", True, COLORS['TEXT'])
        text_rect = text.get_rect()
        text_rect.x = self.sidebar_x + 20
        text_rect.y = 20
        self.screen.blit(text, text_rect)
        
        # Draw preview box with flat design
        preview_x = self.sidebar_x + 20
        preview_y = 60
        preview_size = 120  # Fixed size that fits in 200px sidebar

        # Draw background with subtle shadow
        pygame.draw.rect(self.screen, COLORS['WHITE'],
                        (preview_x, preview_y, preview_size, preview_size))
        pygame.draw.rect(self.screen, COLORS['BORDER'],
                        (preview_x, preview_y, preview_size, preview_size), 1)

        # Draw piece centered in preview
        cell_size = 25  # Smaller cell size for preview
        
        # Get piece blocks and calculate bounds
        blocks = piece.get_blocks()
        if not blocks:
            return
            
        min_x = min(block[0] for block in blocks)
        max_x = max(block[0] for block in blocks)
        min_y = min(block[1] for block in blocks)
        max_y = max(block[1] for block in blocks)
        
        piece_width = (max_x - min_x + 1) * cell_size
        piece_height = (max_y - min_y + 1) * cell_size
        
        offset_x = (preview_size - piece_width) // 2
        offset_y = (preview_size - piece_height) // 2
        
        # Draw each block of the piece with flat design
        for block in blocks:
            x = preview_x + offset_x + (block[0] - min_x) * cell_size
            y = preview_y + offset_y + (block[1] - min_y) * cell_size
            # Draw with slight padding for modern look
            pygame.draw.rect(self.screen, piece.color,
                           (x + 1, y + 1, cell_size - 2, cell_size - 2))
            # Add subtle highlight
            highlight_color = tuple(min(255, c + 20) for c in piece.color)
            pygame.draw.rect(self.screen, highlight_color,
                           (x, y, cell_size, cell_size), 1)
    
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
        # Draw sidebar background with flat design
        pygame.draw.rect(self.screen, COLORS['SIDEBAR'],
                        (self.sidebar_x, 0, SIDEBAR_WIDTH, WINDOW_HEIGHT))
        
        # Draw next piece preview if available
        if next_piece:
            self.draw_next_piece(next_piece)
        
        # Draw text elements with modern styling
        y_offset = 200  # Start below the next piece preview
        
        # Score section
        text = self.font_medium.render("SCORE", True, COLORS['TEXT'])
        self.screen.blit(text, (self.sidebar_x + 20, y_offset))
        y_offset += 30
        text = self.font_large.render(str(score), True, COLORS['ACCENT'])
        self.screen.blit(text, (self.sidebar_x + 20, y_offset))
        y_offset += 60
        
        # Level section
        text = self.font_medium.render("LEVEL", True, COLORS['TEXT'])
        self.screen.blit(text, (self.sidebar_x + 20, y_offset))
        y_offset += 30
        text = self.font_large.render(str(level), True, COLORS['ACCENT'])
        self.screen.blit(text, (self.sidebar_x + 20, y_offset))
        y_offset += 60
        
        # Lines section
        text = self.font_medium.render("LINES", True, COLORS['TEXT'])
        self.screen.blit(text, (self.sidebar_x + 20, y_offset))
        y_offset += 30
        text = self.font_large.render(str(lines), True, COLORS['ACCENT'])
        self.screen.blit(text, (self.sidebar_x + 20, y_offset))
        y_offset += 50
        
        # Next level progress
        lines_to_next_level = (level * 10) - lines
        if lines_to_next_level > 0:
            text = self.font_small.render(f"Next Level: {lines_to_next_level} lines", True, COLORS['TEXT'])
            self.screen.blit(text, (self.sidebar_x + 20, y_offset))
        y_offset += 30
        
        # Current piece type
        if current_piece:
            text = self.font_medium.render("CURRENT", True, COLORS['TEXT'])
            self.screen.blit(text, (self.sidebar_x + 20, y_offset))
            y_offset += 25
            text = self.font_small.render(f"Type: {current_piece.type}", True, COLORS['ACCENT'])
            self.screen.blit(text, (self.sidebar_x + 20, y_offset))
            y_offset += 40
        
        # Game time
        if game_time is not None:
            text = self.font_medium.render("TIME", True, COLORS['TEXT'])
            self.screen.blit(text, (self.sidebar_x + 20, y_offset))
            y_offset += 25
            minutes = game_time // 60
            seconds = game_time % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            text = self.font_small.render(time_str, True, COLORS['ACCENT'])
            self.screen.blit(text, (self.sidebar_x + 20, y_offset))
            y_offset += 40
        
        # Controls section with modern styling
        text = self.font_medium.render("CONTROLS", True, COLORS['TEXT'])
        self.screen.blit(text, (self.sidebar_x + 20, y_offset))
        y_offset += 40
        
        controls = [
            "← → Move",
            "↑ Rotate",
            "↓ Soft Drop",
            "Space Hard Drop",
            "Esc Quit"
        ]
        
        for control in controls:
            text = self.font_small.render(control, True, COLORS['TEXT'])
            self.screen.blit(text, (self.sidebar_x + 20, y_offset))
            y_offset += 22
    
    def draw_game_over(self, score: int) -> None:
        """Draw game over screen with modern flat design.
        
        Args:
            score: Final score
        """
        # Draw semi-transparent overlay with modern color
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw game over text with accent color
        text = self.font_large.render("GAME OVER", True, COLORS['ACCENT'])
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(text, text_rect)
        
        # Draw final score
        text = self.font_medium.render(f"Final Score: {score}", True, COLORS['WHITE'])
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(text, text_rect)
        
        # Draw restart instruction
        text = self.font_small.render("Press R to restart or ESC to quit", True, COLORS['WHITE'])
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(text, text_rect)
    
    def draw_game(self, screen, board, current_piece, score, level, lines_cleared, 
                  next_piece, game_over, paused) -> None:
        """Draw the complete game state.
        
        Args:
            screen: Pygame screen surface
            board: Game board
            current_piece: Current falling piece
            score: Current score
            level: Current level
            lines_cleared: Total lines cleared
            next_piece: Next piece to spawn
            game_over: Game over state
            paused: Pause state
        """
        self.clear_screen()
        
        # Draw board
        self.draw_board(board)
        
        if not game_over:
            # Draw ghost piece
            ghost_piece = board.get_ghost_piece(current_piece)
            if ghost_piece and ghost_piece.y != current_piece.y:
                self.draw_ghost_piece(ghost_piece)
            
            # Draw current piece
            self.draw_piece(current_piece)
        
        # Draw UI with next piece preview
        self.draw_ui(score, level, lines_cleared, next_piece if not game_over else None)
        
        # Draw game over screen if needed
        if game_over:
            self.draw_game_over(score)
        
        # Draw pause indicator
        if paused and not game_over:
            font = pygame.font.Font(None, 48)
            text = font.render("PAUSED", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.screen.get_width() // 2, 
                                            self.screen.get_height() // 2))
            # Draw semi-transparent background
            overlay = pygame.Surface((self.screen.get_width(), 
                                    self.screen.get_height()))
            overlay.set_alpha(128)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            self.screen.blit(text, text_rect)
    
    def clear_screen(self) -> None:
        """Clear the screen with background color."""
        self.screen.fill(COLORS['BACKGROUND'])
    
    def update_display(self) -> None:
        """Update the display."""
        pygame.display.flip()
    
    def quit(self) -> None:
        """Clean up pygame resources."""
        pygame.quit()