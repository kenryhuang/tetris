"""Piece module for Pyglet Tetris implementation.

This module contains the Piece class that represents Tetris pieces
with their shapes, rotations, and movement logic.
"""

import random
import math
from typing import List, Tuple, Dict
from .constants import PIECE_COLORS


class Piece:
    """Represents a Tetris piece with enhanced features for pyglet."""
    
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
    
    def __init__(self, piece_type: str = None, x: int = 4, y: int = 0):
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
        
        # Animation properties
        self.visual_x = float(x)  # For smooth movement animation
        self.visual_y = float(y)  # For smooth falling animation
        self.rotation_angle = 0.0  # For smooth rotation animation
        self.scale = 1.0  # For scaling effects
        self.glow_intensity = 0.0  # For glow effects
        
        # Movement state
        self.is_falling = True
        self.lock_delay = 0.0
        self.move_reset_count = 0
        
    @classmethod
    def get_random_type(cls) -> str:
        """Get a random piece type.
        
        Returns:
            Random piece type string
        """
        return random.choice(list(cls.SHAPES.keys()))
    
    def get_shape(self) -> List[List[int]]:
        """Get the current shape matrix.
        
        Returns:
            4x4 matrix representing the piece shape
        """
        shapes = self.SHAPES[self.type]
        return shapes[self.rotation % len(shapes)]
    
    def get_blocks(self) -> List[Tuple[int, int]]:
        """Get list of block positions relative to the piece position.
        
        Returns:
            List of (x, y) tuples for each block
        """
        blocks = []
        shape = self.get_shape()
        
        for row in range(4):
            for col in range(4):
                if shape[row][col]:
                    blocks.append((self.x + col, self.y + row))
        
        return blocks
    
    def get_visual_blocks(self) -> List[Tuple[float, float]]:
        """Get list of visual block positions for smooth animation.
        
        Returns:
            List of (x, y) tuples for each block with float precision
        """
        blocks = []
        shape = self.get_shape()
        
        for row in range(4):
            for col in range(4):
                if shape[row][col]:
                    blocks.append((self.visual_x + col, self.visual_y + row))
        
        return blocks
    
    def move(self, dx: int, dy: int) -> None:
        """Move the piece by the specified offset.
        
        Args:
            dx: Horizontal movement
            dy: Vertical movement
        """
        self.x += dx
        self.y += dy
        
        # Reset lock delay on movement
        if dx != 0:
            self.lock_delay = 0.0
            self.move_reset_count += 1
    
    def rotate(self, clockwise: bool = True) -> None:
        """Rotate the piece.
        
        Args:
            clockwise: True for clockwise rotation, False for counter-clockwise
        """
        shapes = self.SHAPES[self.type]
        if clockwise:
            self.rotation = (self.rotation + 1) % len(shapes)
        else:
            self.rotation = (self.rotation - 1) % len(shapes)
        
        # Reset lock delay on rotation
        self.lock_delay = 0.0
        self.move_reset_count += 1
    
    def copy(self) -> 'Piece':
        """Create a copy of this piece.
        
        Returns:
            New Piece instance with same properties
        """
        new_piece = Piece(self.type, self.x, self.y)
        new_piece.rotation = self.rotation
        new_piece.visual_x = self.visual_x
        new_piece.visual_y = self.visual_y
        new_piece.rotation_angle = self.rotation_angle
        new_piece.scale = self.scale
        new_piece.glow_intensity = self.glow_intensity
        new_piece.is_falling = self.is_falling
        new_piece.lock_delay = self.lock_delay
        new_piece.move_reset_count = self.move_reset_count
        return new_piece
    
    def update_visual_position(self, dt: float, speed: float = 8.0) -> None:
        """Update visual position for smooth animation.
        
        Args:
            dt: Delta time in seconds
            speed: Animation speed multiplier
        """
        # Smooth movement animation
        target_x = float(self.x)
        target_y = float(self.y)
        
        # Interpolate towards target position
        self.visual_x += (target_x - self.visual_x) * speed * dt
        self.visual_y += (target_y - self.visual_y) * speed * dt
        
        # Snap to target if close enough
        if abs(self.visual_x - target_x) < 0.01:
            self.visual_x = target_x
        if abs(self.visual_y - target_y) < 0.01:
            self.visual_y = target_y
    
    def update_rotation_animation(self, dt: float, speed: float = 10.0) -> None:
        """Update rotation animation.
        
        Args:
            dt: Delta time in seconds
            speed: Rotation animation speed
        """
        target_angle = self.rotation * 90.0
        
        # Handle angle wrapping
        angle_diff = target_angle - self.rotation_angle
        if angle_diff > 180:
            angle_diff -= 360
        elif angle_diff < -180:
            angle_diff += 360
        
        # Interpolate towards target angle
        self.rotation_angle += angle_diff * speed * dt
        
        # Normalize angle
        self.rotation_angle = self.rotation_angle % 360
    
    def update_effects(self, dt: float) -> None:
        """Update visual effects.
        
        Args:
            dt: Delta time in seconds
        """
        # Update glow effect based on movement
        if self.move_reset_count > 0:
            self.glow_intensity = min(1.0, self.glow_intensity + dt * 3.0)
        else:
            self.glow_intensity = max(0.0, self.glow_intensity - dt * 2.0)
        
        # Update scale effect
        if self.is_falling:
            # Subtle breathing effect while falling
            self.scale = 1.0 + 0.05 * math.sin(self.lock_delay * 5.0)
        else:
            self.scale = 1.0
    
    def update_lock_delay(self, dt: float, max_delay: float = 0.5) -> bool:
        """Update lock delay timer.
        
        Args:
            dt: Delta time in seconds
            max_delay: Maximum lock delay in seconds
            
        Returns:
            True if piece should be locked
        """
        if not self.is_falling:
            self.lock_delay += dt
            return self.lock_delay >= max_delay
        return False
    
    def reset_lock_delay(self) -> None:
        """Reset the lock delay timer."""
        self.lock_delay = 0.0
        self.move_reset_count = 0
    
    def get_bounding_box(self) -> Tuple[int, int, int, int]:
        """Get the bounding box of the piece.
        
        Returns:
            Tuple of (min_x, min_y, max_x, max_y)
        """
        blocks = self.get_blocks()
        if not blocks:
            return (self.x, self.y, self.x, self.y)
        
        xs = [x for x, y in blocks]
        ys = [y for x, y in blocks]
        
        return (min(xs), min(ys), max(xs), max(ys))
    
    def get_ghost_position(self, board) -> int:
        """Get the Y position where this piece would land if dropped.
        
        Args:
            board: The game board
            
        Returns:
            Y position of the ghost piece
        """
        ghost_piece = self.copy()
        
        while board.is_valid_position(ghost_piece):
            ghost_piece.y += 1
        
        return ghost_piece.y - 1
    
    def can_rotate(self, board, clockwise: bool = True) -> bool:
        """Check if the piece can rotate in the given direction.
        
        Args:
            board: The game board
            clockwise: Rotation direction
            
        Returns:
            True if rotation is possible
        """
        test_piece = self.copy()
        test_piece.rotate(clockwise)
        return board.is_valid_position(test_piece)
    
    def try_wall_kick(self, board, clockwise: bool = True) -> bool:
        """Try wall kick rotation with offset tests.
        
        Args:
            board: The game board
            clockwise: Rotation direction
            
        Returns:
            True if wall kick succeeded
        """
        # Standard SRS wall kick offsets
        if self.type == 'I':
            # I-piece has special wall kick rules
            offsets = [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)]
        else:
            # Standard pieces
            offsets = [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)]
        
        original_x, original_y = self.x, self.y
        
        for dx, dy in offsets:
            test_piece = self.copy()
            test_piece.x = original_x + dx
            test_piece.y = original_y + dy
            test_piece.rotate(clockwise)
            
            if board.is_valid_position(test_piece):
                self.x = test_piece.x
                self.y = test_piece.y
                self.rotate(clockwise)
                return True
        
        return False