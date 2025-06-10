#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from tetris.piece import Piece

# Create O piece at position (4, 18)
piece = Piece('O', 4, 18)

print(f"O piece at ({piece.x}, {piece.y})")
print(f"O piece color: {piece.color}")
print("O piece blocks:")
for block_x, block_y in piece.get_blocks():
    print(f"  Block at ({block_x}, {block_y})")

print("\nExpected positions in test: [(5, 19), (6, 19), (5, 18), (6, 18)]")