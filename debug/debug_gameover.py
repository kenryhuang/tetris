#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from tetris.game import Game
from tetris.piece import Piece

# Create game
game = Game()

print(f"Initial game_over: {game.game_over}")
print(f"Current piece position: ({game.current_piece.x}, {game.current_piece.y})")
print(f"Current piece type: {game.current_piece.type}")

# Fill top row to trigger game over
for x in range(game.board.width):
    game.board.grid[0][x] = (255, 0, 0)

print("\nFilled top row")
print("Top row:", ['X' if cell is not None else '.' for cell in game.board.grid[0]])

# Test if current piece is valid
print(f"\nIs current piece valid? {game.board.is_valid_position(game.current_piece)}")

# Spawn new piece
print("\nSpawning new piece...")
game.spawn_new_piece()

print(f"Game over after spawn: {game.game_over}")
print(f"New current piece position: ({game.current_piece.x}, {game.current_piece.y})")
print(f"New current piece type: {game.current_piece.type}")
print(f"Is new piece valid? {game.board.is_valid_position(game.current_piece)}")

# Show piece blocks
print("\nNew piece blocks:")
for block_x, block_y in game.current_piece.get_blocks():
    print(f"  Block at ({block_x}, {block_y})")
    if block_y >= 0 and block_y < game.board.height and block_x >= 0 and block_x < game.board.width:
        print(f"    Cell at ({block_x}, {block_y}) is {'occupied' if game.board.grid[block_y][block_x] is not None else 'empty'}")