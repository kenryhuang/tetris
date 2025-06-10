#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from tetris.board import Board
from tetris.piece import Piece
from tetris.game import Game

# Create a board and test line clearing
board = Board()

# Fill bottom row except for positions 3-6 (where I piece will go)
for x in range(board.width):
    if x < 3 or x > 6:  # Leave space for I piece
        board.grid[19][x] = (255, 0, 0)

print("Board before placing piece:")
for y in range(18, 20):
    row = []
    for x in range(board.width):
        row.append('X' if board.grid[y][x] is not None else '.')
    print(f"Row {y}: {''.join(row)}")

# Create I piece at position (3, 18) - this should be horizontal and fill row 19
piece = Piece('I', 3, 18)
print(f"\nI piece at ({piece.x}, {piece.y}), rotation {piece.rotation}")
print("I piece blocks:")
for block_x, block_y in piece.get_blocks():
    print(f"  Block at ({block_x}, {block_y})")

# Check if piece can be placed
if board.is_valid_position(piece):
    print("\nPiece can be placed")
    board.place_piece(piece)
    
    print("\nBoard after placing piece:")
    for y in range(18, 20):
        row = []
        for x in range(board.width):
            row.append('X' if board.grid[y][x] is not None else '.')
        print(f"Row {y}: {''.join(row)}")
    
    # Check for full lines
    full_lines = board.get_full_lines()
    print(f"\nFull lines: {full_lines}")
    
    if full_lines:
        lines_cleared = board.clear_lines(full_lines)
        print(f"Lines cleared: {lines_cleared}")
else:
    print("\nPiece cannot be placed!")