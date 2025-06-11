#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from tetris.board import Board
from tetris.piece import Piece

# Create empty board
board = Board()
print(f"Board dimensions: {board.width} x {board.height}")

# Test O piece at (9, 0) - right boundary
piece = Piece('O', 9, 0)
print(f"\nO piece at (9, 0) blocks:")
for block_x, block_y in piece.get_blocks():
    print(f"  Block at ({block_x}, {block_y})")
    if block_x >= 0 and block_x < board.width and block_y >= 0 and block_y < board.height:
        print(f"    Cell ({block_x}, {block_y}) is within bounds")
    else:
        print(f"    Cell ({block_x}, {block_y}) is out of bounds")
        if block_x < 0:
            print(f"      x={block_x} < 0")
        if block_x >= board.width:
            print(f"      x={block_x} >= {board.width}")
        if block_y < 0:
            print(f"      y={block_y} < 0")
        if block_y >= board.height:
            print(f"      y={block_y} >= {board.height}")

print(f"\nIs O piece at (9, 0) valid? {board.is_valid_position(piece)}")
print("Expected: False (should be out of bounds)")