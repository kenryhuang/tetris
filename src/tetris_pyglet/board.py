"""Board module for Pyglet Tetris implementation.

This module contains the Board class that manages the game grid,
piece placement, line clearing, and collision detection.
"""

from typing import List, Tuple, Optional
from .constants import BOARD_WIDTH, BOARD_HEIGHT, COLORS
from .piece import Piece


class Board:
    """Represents the Tetris game board with enhanced features for pyglet."""
    
    def __init__(self):
        """Initialize an empty board."""
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        
        # Animation states for visual effects
        self.clearing_lines = set()  # Lines currently being cleared
        self.line_clear_progress = {}  # Progress of line clearing animation
        self.locked_blocks = set()  # Recently locked blocks for animation
        
    def clear(self) -> None:
        """Clear the entire board."""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.clearing_lines.clear()
        self.line_clear_progress.clear()
        self.locked_blocks.clear()
    
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
        """Place a piece on the board with animation support.
        
        Args:
            piece: The piece to place
        """
        placed_blocks = []
        for x, y in piece.get_blocks():
            if 0 <= y < self.height and 0 <= x < self.width:
                self.grid[y][x] = piece.color
                placed_blocks.append((x, y))
        
        # Add to locked blocks for animation
        self.locked_blocks.update(placed_blocks)
    
    def get_full_lines(self) -> List[int]:
        """Get list of row indices that are completely filled.
        
        Returns:
            List of row indices (from bottom to top)
        """
        full_lines = []
        for y in range(self.height):
            # Skip lines that are already being cleared
            if y not in self.clearing_lines:
                if all(self.grid[y][x] is not None for x in range(self.width)):
                    full_lines.append(y)
        return full_lines
    
    def start_line_clear_animation(self, lines: List[int]) -> None:
        """Start the line clearing animation.
        
        Args:
            lines: List of line indices to clear
        """
        for line in lines:
            self.clearing_lines.add(line)
            self.line_clear_progress[line] = 0.0
    
    def update_line_clear_animation(self, dt: float) -> bool:
        """Update line clearing animation.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            True if animation is complete, False otherwise
        """
        if not self.clearing_lines:
            return True
        
        from .constants import LINE_CLEAR_ANIMATION_TIME
        
        completed_lines = []
        for line in self.clearing_lines:
            self.line_clear_progress[line] += dt / LINE_CLEAR_ANIMATION_TIME
            if self.line_clear_progress[line] >= 1.0:
                completed_lines.append(line)
        
        # Remove completed animations
        for line in completed_lines:
            self.clearing_lines.discard(line)
            del self.line_clear_progress[line]
        
        return len(self.clearing_lines) == 0
    
    def clear_lines(self, lines: List[int]) -> int:
        """Clear the specified lines and move rows down.
        
        Args:
            lines: List of row indices to clear
            
        Returns:
            Number of lines cleared
        """
        if not lines:
            return 0
        
        # Sort lines from bottom to top for proper removal
        lines_to_clear = sorted(lines, reverse=True)
        
        # Create new grid without the cleared lines
        new_grid = []
        lines_set = set(lines_to_clear)
        
        # Copy all rows except the ones to be cleared
        for y in range(self.height):
            if y not in lines_set:
                new_grid.append(self.grid[y])
        
        # Add empty lines at the top to maintain board height
        empty_lines_count = len(lines_to_clear)
        for _ in range(empty_lines_count):
            new_grid.insert(0, [None for _ in range(self.width)])
        
        # Replace the grid
        self.grid = new_grid
        
        # Clear animation states
        self.clearing_lines.clear()
        self.line_clear_progress.clear()
        
        return len(lines)
    
    def get_block_at(self, x: int, y: int) -> Optional[Tuple[int, int, int, int]]:
        """Get the color of the block at the specified position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            RGBA color tuple if block exists, None otherwise
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None
    
    def is_line_clearing(self, y: int) -> bool:
        """Check if a line is currently being cleared.
        
        Args:
            y: Line index
            
        Returns:
            True if line is being cleared
        """
        return y in self.clearing_lines
    
    def get_line_clear_progress(self, y: int) -> float:
        """Get the clearing progress of a line.
        
        Args:
            y: Line index
            
        Returns:
            Progress from 0.0 to 1.0
        """
        return self.line_clear_progress.get(y, 0.0)
    
    def is_block_locked(self, x: int, y: int) -> bool:
        """Check if a block was recently locked.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if block was recently locked
        """
        return (x, y) in self.locked_blocks
    
    def clear_locked_blocks(self) -> None:
        """Clear the locked blocks animation state."""
        self.locked_blocks.clear()
    
    def get_height_at_column(self, x: int) -> int:
        """Get the height of blocks in a column.
        
        Args:
            x: Column index
            
        Returns:
            Height of the column (number of blocks from bottom)
        """
        if not (0 <= x < self.width):
            return 0
        
        height = 0
        for y in reversed(range(self.height)):
            if self.grid[y][x] is not None:
                height = self.height - y
                break
        return height
    
    def get_holes_count(self) -> int:
        """Count the number of holes in the board.
        
        Returns:
            Number of empty cells with blocks above them
        """
        holes = 0
        for x in range(self.width):
            block_found = False
            for y in range(self.height):
                if self.grid[y][x] is not None:
                    block_found = True
                elif block_found and self.grid[y][x] is None:
                    holes += 1
        return holes
    
    def get_bumpiness(self) -> int:
        """Calculate the bumpiness of the board.
        
        Returns:
            Sum of absolute differences between adjacent column heights
        """
        heights = [self.get_height_at_column(x) for x in range(self.width)]
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])
        return bumpiness