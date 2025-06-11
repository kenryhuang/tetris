#!/usr/bin/env python3

import pygame
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tetris.piece import Piece
from tetris.renderer import GameRenderer
from tetris.constants import *

def test_next_piece_preview():
    """Test the next piece preview functionality."""
    pygame.init()
    
    # Create renderer
    renderer = GameRenderer()
    
    # Create a test piece
    test_piece = Piece('T')
    
    print(f"Test piece type: {test_piece.type}")
    print(f"Test piece color: {test_piece.color}")
    print(f"Test piece shape:")
    for row in test_piece.shape:
        print(row)
    
    # Clear screen and draw preview
    renderer.clear_screen()
    
    # Draw next piece preview
    renderer.draw_next_piece(test_piece)
    
    # Add some text to show what we're testing
    font = pygame.font.Font(None, 24)
    text = font.render("Next Piece Preview Test", True, COLORS['WHITE'])
    renderer.screen.blit(text, (10, 10))
    
    # Update display
    renderer.update_display()
    
    print("Preview should be visible on screen. Press any key to continue...")
    
    # Wait for user input
    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(60)
    
    renderer.quit()

if __name__ == "__main__":
    test_next_piece_preview()