"""Unit tests for the Game class."""

import unittest
import sys
import os
from unittest.mock import Mock, patch

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tetris.game import Game
from tetris.piece import Piece
from tetris.constants import SCORE_VALUES, LINES_PER_LEVEL


class TestGame(unittest.TestCase):
    """Test cases for the Game class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock pygame to avoid GUI dependencies in tests
        with patch('tetris.renderer.pygame'):
            self.game = Game()
    
    def test_game_initialization(self):
        """Test game initialization."""
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.lines_cleared, 0)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.paused)
        self.assertIsNotNone(self.game.current_piece)
        self.assertIsNotNone(self.game.next_piece)
    
    def test_reset_game(self):
        """Test game reset functionality."""
        # Modify game state
        self.game.score = 1000
        self.game.level = 5
        self.game.lines_cleared = 50
        self.game.game_over = True
        
        self.game.reset_game()
        
        # Should be back to initial state
        self.assertEqual(self.game.score, 0)
        self.assertEqual(self.game.level, 1)
        self.assertEqual(self.game.lines_cleared, 0)
        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.paused)
    
    def test_move_piece_valid(self):
        """Test valid piece movement."""
        original_x = self.game.current_piece.x
        result = self.game.move_piece(1, 0)
        
        self.assertTrue(result)
        self.assertEqual(self.game.current_piece.x, original_x + 1)
    
    def test_move_piece_invalid(self):
        """Test invalid piece movement."""
        # Move piece to left edge
        self.game.current_piece.x = 0
        original_x = self.game.current_piece.x
        
        # Try to move further left
        result = self.game.move_piece(-1, 0)
        
        self.assertFalse(result)
        self.assertEqual(self.game.current_piece.x, original_x)
    
    def test_move_piece_when_paused(self):
        """Test that pieces don't move when game is paused."""
        self.game.paused = True
        original_x = self.game.current_piece.x
        
        result = self.game.move_piece(1, 0)
        
        self.assertFalse(result)
        self.assertEqual(self.game.current_piece.x, original_x)
    
    def test_move_piece_when_game_over(self):
        """Test that pieces don't move when game is over."""
        self.game.game_over = True
        original_x = self.game.current_piece.x
        
        result = self.game.move_piece(1, 0)
        
        self.assertFalse(result)
        self.assertEqual(self.game.current_piece.x, original_x)
    
    def test_rotate_piece_valid(self):
        """Test valid piece rotation."""
        # Use T piece which has multiple rotations
        self.game.current_piece = Piece('T', 4, 5)
        original_rotation = self.game.current_piece.rotation
        
        result = self.game.rotate_piece()
        
        self.assertTrue(result)
        expected_rotation = (original_rotation + 1) % len(Piece.SHAPES['T'])
        self.assertEqual(self.game.current_piece.rotation, expected_rotation)
    
    def test_rotate_piece_with_wall_kick(self):
        """Test piece rotation with wall kick."""
        # Place T piece near right wall where normal rotation would fail
        self.game.current_piece = Piece('T', 8, 5)
        
        result = self.game.rotate_piece()
        
        # Should succeed with wall kick
        self.assertTrue(result)
    
    def test_soft_drop(self):
        """Test soft drop functionality."""
        original_y = self.game.current_piece.y
        result = self.game.soft_drop()
        
        self.assertTrue(result)
        self.assertEqual(self.game.current_piece.y, original_y + 1)
    
    def test_hard_drop(self):
        """Test hard drop functionality."""
        original_piece_type = self.game.current_piece.type
        next_piece_type = self.game.next_piece.type
        
        self.game.hard_drop()
        
        # Should have spawned new piece (current piece should be the old next piece)
        self.assertEqual(self.game.current_piece.type, next_piece_type)
        # Should have a new next piece
        self.assertIsNotNone(self.game.next_piece)
    
    def test_add_score_single_line(self):
        """Test scoring for single line clear."""
        original_score = self.game.score
        self.game.add_score(1)
        
        expected_score = original_score + SCORE_VALUES[1] * self.game.level
        self.assertEqual(self.game.score, expected_score)
    
    def test_add_score_tetris(self):
        """Test scoring for Tetris (4 lines)."""
        original_score = self.game.score
        self.game.level = 3
        self.game.add_score(4)
        
        expected_score = original_score + SCORE_VALUES[4] * 3
        self.assertEqual(self.game.score, expected_score)
    
    def test_update_level(self):
        """Test level progression."""
        self.game.lines_cleared = LINES_PER_LEVEL - 1
        original_level = self.game.level
        original_fall_time = self.game.fall_time
        
        self.game.lines_cleared = LINES_PER_LEVEL
        self.game.update_level()
        
        self.assertEqual(self.game.level, original_level + 1)
        self.assertLess(self.game.fall_time, original_fall_time)
    
    def test_spawn_new_piece(self):
        """Test spawning a new piece."""
        old_next_piece_type = self.game.next_piece.type
        
        self.game.spawn_new_piece()
        
        # Current piece should be the old next piece
        self.assertEqual(self.game.current_piece.type, old_next_piece_type)
        # Should have a new next piece
        self.assertIsNotNone(self.game.next_piece)
    
    def test_lock_piece_with_line_clear(self):
        """Test locking piece and clearing lines."""
        # Fill bottom row except for current piece area
        for x in range(self.game.board.width):
            if x < 4 or x > 6:  # Leave space for piece
                self.game.board.grid[19][x] = (255, 0, 0)
        
        # Place piece to complete the line
        self.game.current_piece = Piece('I', 3, 18)  # Horizontal I piece
        original_score = self.game.score
        
        self.game.lock_piece()
        
        # Should have cleared a line and increased score
        self.assertGreater(self.game.score, original_score)
        self.assertGreater(self.game.lines_cleared, 0)
    
    def test_game_over_detection(self):
        """Test game over detection when piece can't spawn."""
        # Fill top rows to trigger game over
        for y in range(3):  # Fill first 3 rows
            for x in range(self.game.board.width):
                self.game.board.grid[y][x] = (255, 0, 0)
        
        self.game.spawn_new_piece()
        
        self.assertTrue(self.game.game_over)
    
    def test_get_state(self):
        """Test getting game state."""
        state = self.game.get_state()
        
        required_keys = [
            'score', 'level', 'lines_cleared', 'game_over', 'paused',
            'current_piece_type', 'next_piece_type'
        ]
        
        for key in required_keys:
            self.assertIn(key, state)
        
        self.assertEqual(state['score'], self.game.score)
        self.assertEqual(state['level'], self.game.level)
        self.assertEqual(state['lines_cleared'], self.game.lines_cleared)
        self.assertEqual(state['game_over'], self.game.game_over)
        self.assertEqual(state['paused'], self.game.paused)
    
    def test_piece_collision_at_spawn(self):
        """Test that game ends when piece can't spawn due to collision."""
        # Fill the spawn area
        spawn_y = 0
        for x in range(3, 7):  # Typical spawn area
            for y in range(spawn_y, spawn_y + 4):
                if y < self.game.board.height:
                    self.game.board.grid[y][x] = (255, 0, 0)
        
        self.game.spawn_new_piece()
        
        self.assertTrue(self.game.game_over)
    
    def test_multiple_line_clear_scoring(self):
        """Test scoring for multiple line clears."""
        test_cases = [
            (1, SCORE_VALUES[1]),
            (2, SCORE_VALUES[2]),
            (3, SCORE_VALUES[3]),
            (4, SCORE_VALUES[4]),
        ]
        
        for lines, expected_base_score in test_cases:
            with self.subTest(lines=lines):
                self.game.score = 0
                self.game.level = 2
                self.game.add_score(lines)
                
                expected_score = expected_base_score * 2
                self.assertEqual(self.game.score, expected_score)
    
    @patch('tetris.game.time.time')
    def test_automatic_fall(self, mock_time):
        """Test automatic piece falling."""
        # Mock time to control fall timing
        mock_time.return_value = 0
        self.game.last_fall_time = 0
        
        original_y = self.game.current_piece.y
        
        # Advance time beyond fall time
        mock_time.return_value = self.game.fall_time / 1000 + 1
        
        self.game.update()
        
        # Piece should have moved down
        self.assertGreater(self.game.current_piece.y, original_y)


if __name__ == '__main__':
    unittest.main()