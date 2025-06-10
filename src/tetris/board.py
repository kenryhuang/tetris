"""Game board logic for Tetris."""

from typing import List, Tuple, Optional
from .constants import BOARD_WIDTH, BOARD_HEIGHT, COLORS
from .piece import Piece


class Board:
    """Represents the Tetris game board."""
    
    def __init__(self):
        """Initialize an empty board."""
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def is_valid_position(self, piece: Piece) -> bool:
        """Check if a piece can be placed at its current position.
        
        Args:
            piece: The piece to check
            
        Returns:
            True if the position is valid, False otherwise
        """
        for x, y in piece.get_blocks():
            # Check boundaries
            if x < 0 or x >= self.width or y >= self.height:
                return False
            
            # Check collision with existing blocks (ignore negative y for spawning)
            if y >= 0 and self.grid[y][x] is not None:
                return False
        
        return True
    
    def place_piece(self, piece: Piece) -> None:
        """Place a piece on the board.
        
        Args:
            piece: The piece to place
        """
        for x, y in piece.get_blocks():
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = piece.color
    
    def get_full_lines(self) -> List[int]:
        """Get list of row indices that are completely filled.
        
        Returns:
            List of row indices (from bottom to top)
        """
        full_lines = []
        for y in range(self.height):
            if all(cell is not None for cell in self.grid[y]):
                full_lines.append(y)
        return full_lines
    
    def clear_lines(self, lines: List[int]) -> int:
        """Clear the specified lines and drop rows above.
        
        Args:
            lines: List of row indices to clear
            
        Returns:
            Number of lines cleared
        """
        if not lines:
            return 0
        
        # Sort lines from top to bottom to avoid index issues
        lines.sort()
        
        # Remove full lines
        for line in reversed(lines):
            del self.grid[line]
        
        # Add new empty lines at the top
        for _ in range(len(lines)):
            self.grid.insert(0, [None for _ in range(self.width)])
        
        return len(lines)
    
    def is_game_over(self) -> bool:
        """Check if the game is over (top row has blocks).
        
        Returns:
            True if game is over, False otherwise
        """
        return any(cell is not None for cell in self.grid[0])
    
    def get_drop_position(self, piece: Piece) -> int:
        """Get the y position where the piece would land if dropped.
        
        Args:
            piece: The piece to drop
            
        Returns:
            The y position where the piece would land
        """
        test_piece = piece.copy()
        while self.is_valid_position(test_piece):
            test_piece = test_piece.move(0, 1)
        return test_piece.y - 1
    
    def get_ghost_piece(self, piece: Piece) -> Optional[Piece]:
        """Get a ghost piece showing where the current piece would land.
        
        Args:
            piece: The current piece
            
        Returns:
            Ghost piece at drop position, or None if invalid
        """
        if not self.is_valid_position(piece):
            return None
        
        ghost_y = self.get_drop_position(piece)
        ghost_piece = piece.copy()
        ghost_piece.y = ghost_y
        return ghost_piece
    
    def get_cell(self, x: int, y: int) -> Optional[Tuple[int, int, int]]:
        """Get the color of a cell.
        
        Args:
            x: Column index
            y: Row index
            
        Returns:
            Color tuple (R, G, B) or None if empty
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def clear(self) -> None:
        """Clear the entire board."""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def get_height_map(self) -> List[int]:
        """Get the height of blocks in each column.
        
        Returns:
            List of heights for each column
        """
        heights = []
        for x in range(self.width):
            height = 0
            for y in range(self.height):
                if self.grid[y][x] is not None:
                    height = self.height - y
                    break
            heights.append(height)
        return heights