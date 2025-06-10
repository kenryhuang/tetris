#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pygame
from tetris.renderer import GameRenderer
from tetris.piece import Piece
from tetris.constants import COLORS, PREVIEW_SIZE, CELL_SIZE

def main():
    pygame.init()
    
    # Create renderer
    renderer = GameRenderer()
    
    # Create a test piece
    test_piece = Piece('T')
    
    print(f"Test piece type: {test_piece.type}")
    print(f"Test piece color: {test_piece.color}")
    print(f"Test piece shape: {test_piece.shape}")
    print(f"PREVIEW_SIZE: {PREVIEW_SIZE}")
    print(f"CELL_SIZE: {CELL_SIZE}")
    print(f"preview_size calculation: {PREVIEW_SIZE * CELL_SIZE}")
    print(f"sidebar_x: {renderer.sidebar_x}")
    
    # Clear screen and draw
    renderer.clear_screen()
    
    # Draw the next piece
    renderer.draw_next_piece(test_piece)
    
    # Add some debug info on screen
    debug_text = renderer.font_small.render(f"Preview size: {PREVIEW_SIZE * CELL_SIZE}", True, COLORS['WHITE'])
    renderer.screen.blit(debug_text, (renderer.sidebar_x + 10, 200))
    
    debug_text2 = renderer.font_small.render(f"Sidebar X: {renderer.sidebar_x}", True, COLORS['WHITE'])
    renderer.screen.blit(debug_text2, (renderer.sidebar_x + 10, 220))
    
    # Update display
    renderer.update_display()
    
    # Wait for user input
    print("Press any key in the pygame window to quit...")
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()