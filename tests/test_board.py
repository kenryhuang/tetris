"""Unit tests for the Board class."""

import unittest
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tetris.board import Board
from tetris.piece import Piece
from tetris.constants import BOARD_WIDTH, BOARD_HEIGHT, COLORS


class TestBoard(unittest.TestCase):
    """Test cases for the Board class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.board = Board()
    
    def test_board_initialization(self):
        """Test board initialization."""
        self.assertEqual(self.board.width, BOARD_WIDTH)
        self.assertEqual(self.board.height, BOARD_HEIGHT)
        self.assertEqual(len(self.board.grid), BOARD_HEIGHT)
        self.assertEqual(len(self.board.grid[0]), BOARD_WIDTH)
        
        # All cells should be empty initially
        for row in self.board.grid:
            for cell in row:
                self.assertIsNone(cell)
    
    def test_is_valid_position_empty_board(self):
        """Test position validation on empty board."""
        piece = Piece('O', 4, 17)  # Near bottom
        self.assertTrue(self.board.is_valid_position(piece))
        
        # Test boundaries
        piece = Piece('O', -2, 0)  # Left boundary
        self.assertFalse(self.board.is_valid_position(piece))
        
        piece = Piece('O', 7, 0)  # Right boundary (O piece is 2 wide)
        self.assertTrue(self.board.is_valid_position(piece))
        
        piece = Piece('O', 9, 0)  # Beyond right boundary
        self.assertFalse(self.board.is_valid_position(piece))
        
        piece = Piece('O', 4, 19)  # Bottom boundary (O piece is 2 tall)
        self.assertFalse(self.board.is_valid_position(piece))
    
    def test_is_valid_position_with_collision(self):
        """Test position validation with existing blocks."""
        # Place a block manually
        self.board.grid[19][5] = COLORS['RED']
        
        # Test collision
        piece = Piece('O', 4, 17)  # Would overlap with placed block
        self.assertFalse(self.board.is_valid_position(piece))
        
        # Test non-collision
        piece = Piece('O', 2, 17)
        self.assertTrue(self.board.is_valid_position(piece))
    
    def test_place_piece(self):
        """Test placing a piece on the board."""
        piece = Piece('O', 4, 17)
        original_color = piece.color
        
        self.board.place_piece(piece)
         
        # Check that blocks were placed
        expected_positions = [(5, 18), (6, 18), (5, 19), (6, 19)]
        for x, y in expected_positions:
            self.assertEqual(self.board.grid[y][x], original_color)
    
    def test_get_full_lines_empty(self):
        """Test getting full lines on empty board."""
        full_lines = self.board.get_full_lines()
        self.assertEqual(full_lines, [])
    
    def test_get_full_lines_partial(self):
        """Test getting full lines with partially filled rows."""
        # Fill part of bottom row
        for x in range(5):
            self.board.grid[19][x] = COLORS['RED']
        
        full_lines = self.board.get_full_lines()
        self.assertEqual(full_lines, [])
    
    def test_get_full_lines_complete(self):
        """Test getting full lines with completely filled rows."""
        # Fill bottom row completely
        for x in range(BOARD_WIDTH):
            self.board.grid[19][x] = COLORS['RED']
        
        # Fill another row
        for x in range(BOARD_WIDTH):
            self.board.grid[17][x] = COLORS['BLUE']
        
        full_lines = self.board.get_full_lines()
        self.assertEqual(sorted(full_lines), [17, 19])
    
    def test_clear_lines_single(self):
        """Test clearing a single line."""
        # Fill bottom row
        for x in range(BOARD_WIDTH):
            self.board.grid[19][x] = COLORS['RED']
        
        # Place a block above
        self.board.grid[18][5] = COLORS['BLUE']
        
        lines_cleared = self.board.clear_lines([19])
        
        self.assertEqual(lines_cleared, 1)
        
        # Blue block should have moved down to bottom row
        self.assertEqual(self.board.grid[19][5], COLORS['BLUE'])
        self.assertIsNone(self.board.grid[18][5])
        
        # Rest of bottom row should be empty
        for x in range(BOARD_WIDTH):
            if x != 5:
                self.assertIsNone(self.board.grid[19][x])
    
    def test_clear_lines_multiple(self):
        """Test clearing multiple lines."""
        # Fill two rows
        for x in range(BOARD_WIDTH):
            self.board.grid[19][x] = COLORS['RED']
            self.board.grid[18][x] = COLORS['GREEN']
        
        # Place blocks above
        self.board.grid[17][3] = COLORS['BLUE']
        self.board.grid[16][7] = COLORS['YELLOW']
        
        lines_cleared = self.board.clear_lines([18, 19])
        
        self.assertEqual(lines_cleared, 2)
        
        # Blocks should have moved down
        self.assertEqual(self.board.grid[19][3], COLORS['BLUE'])
        self.assertEqual(self.board.grid[18][7], COLORS['YELLOW'])
        
        # Rest of bottom two rows should be empty
        for y in [18, 19]:
            for x in range(BOARD_WIDTH):
                if not ((y == 19 and x == 3) or (y == 18 and x == 7)):
                    self.assertIsNone(self.board.grid[y][x])
    
    def test_is_game_over_empty(self):
        """Test game over detection on empty board."""
        self.assertFalse(self.board.is_game_over())
    
    def test_is_game_over_with_blocks(self):
        """Test game over detection with blocks at top."""
        # Place block in top row
        self.board.grid[0][5] = COLORS['RED']
        self.assertTrue(self.board.is_game_over())
    
    def test_get_drop_position(self):
        """Test getting drop position for a piece."""
        piece = Piece('O', 4, 0)
        drop_y = self.board.get_drop_position(piece)
        self.assertEqual(drop_y, 17)  # O piece is 2 tall, so lands at y=17
        
        # Place obstacle
        self.board.grid[15][5] = COLORS['RED']
        drop_y = self.board.get_drop_position(piece)
        self.assertEqual(drop_y, 12)  # Should land above the obstacle
    
    def test_get_ghost_piece(self):
        """Test getting ghost piece."""
        piece = Piece('O', 4, 5)
        ghost = self.board.get_ghost_piece(piece)
        
        self.assertIsNotNone(ghost)
        self.assertEqual(ghost.type, piece.type)
        self.assertEqual(ghost.x, piece.x)
        self.assertEqual(ghost.y, 17)  # Should be at drop position
        
        # Test with invalid piece
        invalid_piece = Piece('O', -2, 0)
        ghost = self.board.get_ghost_piece(invalid_piece)
        self.assertIsNone(ghost)
    
    def test_get_cell(self):
        """Test getting cell color."""
        # Empty cell
        self.assertIsNone(self.board.get_cell(5, 10))
        
        # Place a block
        self.board.grid[10][5] = COLORS['RED']
        self.assertEqual(self.board.get_cell(5, 10), COLORS['RED'])
        
        # Out of bounds
        self.assertIsNone(self.board.get_cell(-1, 0))
        self.assertIsNone(self.board.get_cell(0, -1))
        self.assertIsNone(self.board.get_cell(BOARD_WIDTH, 0))
        self.assertIsNone(self.board.get_cell(0, BOARD_HEIGHT))
    
    def test_clear_board(self):
        """Test clearing the entire board."""
        # Place some blocks
        self.board.grid[10][5] = COLORS['RED']
        self.board.grid[15][3] = COLORS['BLUE']
        
        self.board.clear()
        
        # All cells should be empty
        for row in self.board.grid:
            for cell in row:
                self.assertIsNone(cell)
    
    def test_get_height_map(self):
        """Test getting height map of the board."""
        # Empty board
        heights = self.board.get_height_map()
        self.assertEqual(heights, [0] * BOARD_WIDTH)
        
        # Place some blocks
        self.board.grid[19][0] = COLORS['RED']  # Height 1 in column 0
        self.board.grid[18][0] = COLORS['RED']  # Height 2 in column 0
        self.board.grid[17][2] = COLORS['BLUE']  # Height 3 in column 2
        
        heights = self.board.get_height_map()
        expected = [2, 0, 3, 0, 0, 0, 0, 0, 0, 0]
        self.assertEqual(heights, expected)
    
    def test_piece_spawning_above_board(self):
        """Test that pieces can spawn above the visible board."""
        piece = Piece('I', 3, -1)  # Spawn above board
        self.assertTrue(self.board.is_valid_position(piece))
        
        # Should be able to place piece partially above board
        self.board.place_piece(piece)
        
        # Only visible parts should be placed
        visible_blocks = [(x, y) for x, y in piece.get_blocks() if y >= 0]
        for x, y in visible_blocks:
            self.assertIsNotNone(self.board.grid[y][x])


if __name__ == '__main__':
    unittest.main()