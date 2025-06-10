"""Tetris piece definitions and logic."""

import random
from typing import List, Tuple, Dict
from .constants import PIECE_COLORS


class Piece:
    """Represents a Tetris piece with its shape, position, and rotation."""
    
    # Tetris piece shapes (4x4 grid, 0=empty, 1=filled)
    SHAPES: Dict[str, List[List[List[int]]]] = {
        'I': [
            [[0, 0, 0, 0],
             [1, 1, 1, 1],
             [0, 0, 0, 0],
             [0, 0, 0, 0]],
            [[0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0]],
        ],
        'O': [
            [[0, 0, 0, 0],
             [0, 1, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]],
        ],
        'T': [
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [1, 1, 1, 0],
             [0, 0, 0, 0]],
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 1, 0, 0]],
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 1, 0],
             [0, 1, 0, 0]],
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [1, 1, 0, 0],
             [0, 1, 0, 0]],
        ],
        'S': [
            [[0, 0, 0, 0],
             [0, 1, 1, 0],
             [1, 1, 0, 0],
             [0, 0, 0, 0]],
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 0, 1, 0]],
        ],
        'Z': [
            [[0, 0, 0, 0],
             [1, 1, 0, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0]],
            [[0, 0, 0, 0],
             [0, 0, 1, 0],
             [0, 1, 1, 0],
             [0, 1, 0, 0]],
        ],
        'J': [
            [[0, 0, 0, 0],
             [1, 0, 0, 0],
             [1, 1, 1, 0],
             [0, 0, 0, 0]],
            [[0, 0, 0, 0],
             [0, 1, 1, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]],
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 1, 0],
             [0, 0, 1, 0]],
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [1, 1, 0, 0]],
        ],
        'L': [
            [[0, 0, 0, 0],
             [0, 0, 1, 0],
             [1, 1, 1, 0],
             [0, 0, 0, 0]],
            [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 1, 0]],
            [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 1, 0],
             [1, 0, 0, 0]],
            [[0, 0, 0, 0],
             [1, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]],
        ],
    }
    
    def __init__(self, piece_type: str = None, x: int = 3, y: int = 0):
        """Initialize a new piece.
        
        Args:
            piece_type: Type of piece ('I', 'O', 'T', 'S', 'Z', 'J', 'L')
            x: Initial x position
            y: Initial y position
        """
        if piece_type is None:
            piece_type = random.choice(list(self.SHAPES.keys()))
        
        self.type = piece_type
        self.x = x
        self.y = y
        self.rotation = 0
        self.color = PIECE_COLORS[piece_type]
    
    @property
    def shape(self) -> List[List[int]]:
        """Get current shape based on rotation."""
        shapes = self.SHAPES[self.type]
        return shapes[self.rotation % len(shapes)]
    
    def get_blocks(self) -> List[Tuple[int, int]]:
        """Get list of (x, y) coordinates for all blocks in the piece."""
        blocks = []
        for row in range(4):
            for col in range(4):
                if self.shape[row][col]:
                    blocks.append((self.x + col, self.y + row))
        return blocks
    
    def rotate(self) -> 'Piece':
        """Return a new piece rotated clockwise."""
        new_piece = Piece(self.type, self.x, self.y)
        new_piece.rotation = (self.rotation + 1) % len(self.SHAPES[self.type])
        return new_piece
    
    def move(self, dx: int, dy: int) -> 'Piece':
        """Return a new piece moved by dx, dy."""
        new_piece = Piece(self.type, self.x + dx, self.y + dy)
        new_piece.rotation = self.rotation
        return new_piece
    
    def copy(self) -> 'Piece':
        """Create a copy of this piece."""
        new_piece = Piece(self.type, self.x, self.y)
        new_piece.rotation = self.rotation
        return new_piece
    
    @classmethod
    def get_random_type(cls) -> str:
        """Get a random piece type."""
        return random.choice(list(cls.SHAPES.keys()))