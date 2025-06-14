#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tetris_pyglet.effects import RainbowWaveEffect
from tetris_pyglet.constants import BOARD_HEIGHT, CELL_SIZE, BORDER_WIDTH, WINDOW_HEIGHT

# Test with real game values
print("Testing with real game values...")
print(f"BOARD_HEIGHT: {BOARD_HEIGHT}")
print(f"CELL_SIZE: {CELL_SIZE}")
print(f"BORDER_WIDTH (board_y): {BORDER_WIDTH}")
print(f"WINDOW_HEIGHT: {WINDOW_HEIGHT}")
print(f"Game board height in pixels: {BOARD_HEIGHT * CELL_SIZE}")
print(f"Game board bottom: {BORDER_WIDTH}")
print(f"Game board top: {BORDER_WIDTH + BOARD_HEIGHT * CELL_SIZE}")

# Test effects for different lines with real board position
board_x = BORDER_WIDTH
board_y = BORDER_WIDTH

print("\n=== Testing line clear effects ===")
for line_y in [0, 5, 10, 15, 19]:  # Test various lines
    print(f"\nLine {line_y}:")
    effect = RainbowWaveEffect(line_y, board_x, board_y)
    print(f"  pixel_y: {effect.pixel_y}")
    print(f"  Within window (0-{WINDOW_HEIGHT}): {0 <= effect.pixel_y <= WINDOW_HEIGHT}")
    
    # Check if effect is visible
    if effect.pixel_y < 0:
        print(f"  ❌ Effect is ABOVE the window (negative Y)")
    elif effect.pixel_y > WINDOW_HEIGHT:
        print(f"  ❌ Effect is BELOW the window (Y > {WINDOW_HEIGHT})")
    else:
        print(f"  ✅ Effect is VISIBLE in window")

print("\n=== Analysis ===")
print(f"Line 0 (bottom) should be at: {board_y + (BOARD_HEIGHT - 1 - 0) * CELL_SIZE} pixels")
print(f"Line 19 (top) should be at: {board_y + (BOARD_HEIGHT - 1 - 19) * CELL_SIZE} pixels")
print(f"Window coordinate system: Y=0 is at bottom, Y={WINDOW_HEIGHT} is at top")