#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import pygame
from tetris.game import Game
from tetris.constants import *

def main():
    pygame.init()
    
    # Create game instance
    game = Game()
    
    print(f"Next piece shape: {game.next_piece.shape}")
    print(f"Next piece position: ({game.next_piece.x}, {game.next_piece.y})")
    print(f"Next piece blocks: {game.next_piece.get_blocks()}")
    
    # Debug draw_next_piece parameters
    sidebar_x = GAME_WIDTH + BORDER_WIDTH * 2
    preview_size = 120
    cell_size = 25
    
    print(f"\nDraw parameters:")
    print(f"GAME_WIDTH: {GAME_WIDTH}")
    print(f"BORDER_WIDTH: {BORDER_WIDTH}")
    print(f"sidebar_x: {sidebar_x}")
    print(f"preview_size: {preview_size}")
    print(f"cell_size: {cell_size}")
    
    # Calculate preview box position
    preview_x = sidebar_x + 20
    preview_y = 120
    
    print(f"\nPreview box:")
    print(f"preview_x: {preview_x}")
    print(f"preview_y: {preview_y}")
    print(f"preview box right edge: {preview_x + preview_size}")
    print(f"preview box bottom edge: {preview_y + preview_size}")
    
    print(f"\nWindow dimensions:")
    print(f"WINDOW_WIDTH: {WINDOW_WIDTH}")
    print(f"WINDOW_HEIGHT: {WINDOW_HEIGHT}")
    
    # Check if preview box is within window bounds
    if preview_x + preview_size > WINDOW_WIDTH:
        print(f"WARNING: Preview box extends beyond window width!")
        print(f"Box right edge: {preview_x + preview_size}, Window width: {WINDOW_WIDTH}")
    
    if preview_y + preview_size > WINDOW_HEIGHT:
        print(f"WARNING: Preview box extends beyond window height!")
        print(f"Box bottom edge: {preview_y + preview_size}, Window height: {WINDOW_HEIGHT}")
    
    # Calculate piece position within preview
    piece_blocks = game.next_piece.get_blocks()
    if piece_blocks:
        min_x = min(block[0] for block in piece_blocks)
        max_x = max(block[0] for block in piece_blocks)
        min_y = min(block[1] for block in piece_blocks)
        max_y = max(block[1] for block in piece_blocks)
        
        piece_width = (max_x - min_x + 1) * cell_size
        piece_height = (max_y - min_y + 1) * cell_size
        
        offset_x = (preview_size - piece_width) // 2
        offset_y = (preview_size - piece_height) // 2
        
        print(f"\nPiece dimensions:")
        print(f"Piece bounds: x({min_x}-{max_x}), y({min_y}-{max_y})")
        print(f"Piece size: {piece_width}x{piece_height}")
        print(f"Offset in preview: ({offset_x}, {offset_y})")
        
        # Calculate actual render positions
        for block in piece_blocks:
            block_x = preview_x + offset_x + (block[0] - min_x) * cell_size
            block_y = preview_y + offset_y + (block[1] - min_y) * cell_size
            print(f"Block at ({block[0]}, {block[1]}) -> render at ({block_x}, {block_y})")
            
            if block_x < 0 or block_y < 0 or block_x + cell_size > WINDOW_WIDTH or block_y + cell_size > WINDOW_HEIGHT:
                print(f"  WARNING: Block extends outside window bounds!")
    
    # Run the game briefly to test rendering
    print("\nStarting game for visual test...")
    clock = pygame.time.Clock()
    running = True
    frames = 0
    
    while running and frames < 60:  # Run for 1 second at 60fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        game.render()
        clock.tick(60)
        frames += 1
    
    pygame.quit()
    print("Debug complete.")

if __name__ == "__main__":
    main()