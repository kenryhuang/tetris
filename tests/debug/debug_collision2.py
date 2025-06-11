#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from tetris.board import Board
from tetris.piece import Piece
from tetris.constants import COLORS

# Create board
board = Board()
print(f"Board dimensions: {board.width} x {board.height}")

# Place a block manually at (5, 19)
board.grid[19][5] = COLORS['RED']
print("Placed block at (5, 19)")

# Test non-collision with O piece at (2, 18)
piece = Piece('O', 2, 18)
print(f"\nO piece at (2, 18) blocks:")
for block_x, block_y in piece.get_blocks():
    print(f"  Block at ({block_x}, {block_y})")
    if block_x >= 0 and block_x < board.width and block_y >= 0 and block_y < board.height:
        occupied = board.grid[block_y][block_x] is not None
        print(f"    Cell ({block_x}, {block_y}) is {'occupied' if occupied else 'empty'}")
    else:
        print(f"    Cell ({block_x}, {block_y}) is out of bounds")

print(f"\nIs O piece at (2, 18) valid? {board.is_valid_position(piece)}")