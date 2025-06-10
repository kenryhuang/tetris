#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from tetris.board import Board
from tetris.piece import Piece
from tetris.constants import COLORS

# Create board
board = Board()

# Place a block manually at (5, 19)
board.grid[19][5] = COLORS['RED']
print("Placed block at (5, 19)")

# Test collision with O piece at (4, 18)
piece1 = Piece('O', 4, 18)
print(f"\nO piece at (4, 18) blocks:")
for block_x, block_y in piece1.get_blocks():
    print(f"  Block at ({block_x}, {block_y})")
    if block_y < board.height and block_x < board.width:
        occupied = board.grid[block_y][block_x] is not None
        print(f"    Cell ({block_x}, {block_y}) is {'occupied' if occupied else 'empty'}")

print(f"\nIs O piece at (4, 18) valid? {board.is_valid_position(piece1)}")

# Test non-collision with O piece at (6, 18)
piece2 = Piece('O', 6, 18)
print(f"\nO piece at (6, 18) blocks:")
for block_x, block_y in piece2.get_blocks():
    print(f"  Block at ({block_x}, {block_y})")
    if block_y < board.height and block_x < board.width:
        occupied = board.grid[block_y][block_x] is not None
        print(f"    Cell ({block_x}, {block_y}) is {'occupied' if occupied else 'empty'}")

print(f"\nIs O piece at (6, 18) valid? {board.is_valid_position(piece2)}")