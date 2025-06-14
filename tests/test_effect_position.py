#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tetris_pyglet.effects import RainbowWaveEffect
from tetris_pyglet.constants import BOARD_HEIGHT, CELL_SIZE

# Test effect position calculation
print("Testing effect position calculation...")
print(f"BOARD_HEIGHT: {BOARD_HEIGHT}")
print(f"CELL_SIZE: {CELL_SIZE}")

# Test different board_y and line_y values
test_cases = [
    (0, 50, 100),   # line_y=0, board_x=50, board_y=100 (bottom line)
    (5, 50, 100),   # line_y=5, board_x=50, board_y=100 (middle)
    (19, 50, 100),  # line_y=19, board_x=50, board_y=100 (top line)
    (5, 50, 200),   # line_y=5, board_x=50, board_y=200
]

for line_y, board_x, board_y in test_cases:
    print(f"\nCreating effect for line_y={line_y}, board_x={board_x}, board_y={board_y}")
    effect = RainbowWaveEffect(line_y, board_x, board_y)
    print(f"Calculated pixel_y: {effect.pixel_y}")
    
    # Manual calculation for verification
    expected_pixel_y = board_y + (BOARD_HEIGHT - 1 - line_y) * CELL_SIZE
    print(f"Expected pixel_y: {expected_pixel_y}")
    print(f"Match: {effect.pixel_y == expected_pixel_y}")

print("\nTest completed.")