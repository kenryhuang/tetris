"""Unit tests for the Piece class."""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tetris.piece import Piece
from tetris.constants import PIECE_COLORS


class TestPiece(unittest.TestCase):
    """Test cases for the Piece class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.piece = Piece('T', 5, 10)
    
    def test_piece_initialization(self):
        """Test piece initialization."""
        self.assertEqual(self.piece.type, 'T')
        self.assertEqual(self.piece.x, 5)
        self.assertEqual(self.piece.y, 10)
        self.assertEqual(self.piece.rotation, 0)
        self.assertEqual(self.piece.color, PIECE_COLORS['T'])
    
    def test_random_piece_creation(self):
        """Test creating a random piece."""
        piece = Piece()
        self.assertIn(piece.type, Piece.SHAPES.keys())
        self.assertEqual(piece.x, 3)
        self.assertEqual(piece.y, 0)
        self.assertEqual(piece.rotation, 0)
    
    def test_piece_shapes(self):
        """Test that all piece types have valid shapes."""
        for piece_type in Piece.SHAPES.keys():
            piece = Piece(piece_type)
            self.assertIsInstance(piece.shape, list)
            self.assertEqual(len(piece.shape), 4)
            for row in piece.shape:
                self.assertEqual(len(row), 4)
                for cell in row:
                    self.assertIn(cell, [0, 1])
    
    def test_get_blocks(self):
        """Test getting block positions."""
        piece = Piece('O', 0, 0)  # 2x2 square
        blocks = piece.get_blocks()
        expected_blocks = [(1, 1), (2, 1), (1, 2), (2, 2)]
        self.assertEqual(sorted(blocks), sorted(expected_blocks))
    
    def test_piece_rotation(self):
        """Test piece rotation."""
        original_rotation = self.piece.rotation
        rotated_piece = self.piece.rotate()
        
        # Original piece should be unchanged
        self.assertEqual(self.piece.rotation, original_rotation)
        
        # Rotated piece should have different rotation
        expected_rotation = (original_rotation + 1) % len(Piece.SHAPES['T'])
        self.assertEqual(rotated_piece.rotation, expected_rotation)
        
        # Position should be the same
        self.assertEqual(rotated_piece.x, self.piece.x)
        self.assertEqual(rotated_piece.y, self.piece.y)
        self.assertEqual(rotated_piece.type, self.piece.type)
    
    def test_piece_movement(self):
        """Test piece movement."""
        moved_piece = self.piece.move(2, -3)
        
        # Original piece should be unchanged
        self.assertEqual(self.piece.x, 5)
        self.assertEqual(self.piece.y, 10)
        
        # Moved piece should have new position
        self.assertEqual(moved_piece.x, 7)
        self.assertEqual(moved_piece.y, 7)
        self.assertEqual(moved_piece.type, self.piece.type)
        self.assertEqual(moved_piece.rotation, self.piece.rotation)
    
    def test_piece_copy(self):
        """Test piece copying."""
        copied_piece = self.piece.copy()
        
        self.assertEqual(copied_piece.type, self.piece.type)
        self.assertEqual(copied_piece.x, self.piece.x)
        self.assertEqual(copied_piece.y, self.piece.y)
        self.assertEqual(copied_piece.rotation, self.piece.rotation)
        self.assertEqual(copied_piece.color, self.piece.color)
        
        # Should be different objects
        self.assertIsNot(copied_piece, self.piece)
    
    def test_o_piece_rotation(self):
        """Test that O piece doesn't change when rotated."""
        o_piece = Piece('O', 0, 0)
        original_blocks = o_piece.get_blocks()
        
        rotated_piece = o_piece.rotate()
        rotated_blocks = rotated_piece.get_blocks()
        
        self.assertEqual(sorted(original_blocks), sorted(rotated_blocks))
    
    def test_i_piece_rotation(self):
        """Test I piece rotation (horizontal to vertical)."""
        i_piece = Piece('I', 0, 0)
        original_blocks = i_piece.get_blocks()
        
        rotated_piece = i_piece.rotate()
        rotated_blocks = rotated_piece.get_blocks()
        
        # Should have different block positions
        self.assertNotEqual(sorted(original_blocks), sorted(rotated_blocks))
        
        # Should have same number of blocks
        self.assertEqual(len(original_blocks), len(rotated_blocks))
    
    def test_get_random_type(self):
        """Test getting random piece type."""
        piece_type = Piece.get_random_type()
        self.assertIn(piece_type, Piece.SHAPES.keys())
    
    def test_all_piece_types(self):
        """Test that all piece types can be created and have valid properties."""
        for piece_type in ['I', 'O', 'T', 'S', 'Z', 'J', 'L']:
            piece = Piece(piece_type)
            self.assertEqual(piece.type, piece_type)
            self.assertIn(piece_type, PIECE_COLORS)
            self.assertEqual(piece.color, PIECE_COLORS[piece_type])
            
            # Test that piece has at least one block
            blocks = piece.get_blocks()
            self.assertGreater(len(blocks), 0)
            
            # Test that all rotations are valid
            for _ in range(4):  # Test up to 4 rotations
                piece = piece.rotate()
                blocks = piece.get_blocks()
                self.assertGreater(len(blocks), 0)


if __name__ == '__main__':
    unittest.main()