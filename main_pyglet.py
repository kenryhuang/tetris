#!/usr/bin/env python3
"""
Pyglet-based Tetris Game

A complete reimplementation of Tetris using the pyglet library for enhanced
visual effects and modern graphics capabilities.
"""

import sys
import os
import pyglet
from pyglet import shapes

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tetris_pyglet.pyglet_game import PygletTetrisGame
from tetris_pyglet.constants import WINDOW_WIDTH, WINDOW_HEIGHT


def setup_game():
    """Setup and return the game instance."""
    # Create game instance (it will create its own window)
    game = PygletTetrisGame()
    
    # Get the window from the game
    window = game.get_window()
    
    # Set up event handlers
    @window.event
    def on_draw():
        game.draw()
    
    @window.event
    def on_key_press(symbol, modifiers):
        game.on_key_press(symbol, modifiers)
    
    @window.event
    def on_key_release(symbol, modifiers):
        game.on_key_release(symbol, modifiers)
    
    # Schedule game update
    def update(dt):
        game.update(dt)
    
    pyglet.clock.schedule_interval(update, 1/60.0)  # 60 FPS
    
    return game, window


def main():
    """Main entry point for the Pyglet Tetris game."""
    print("Pyglet Tetris - Enhanced Edition")
    print("================================")
    print("Features:")
    print("  • OpenGL-accelerated graphics")
    print("  • Advanced particle effects")
    print("  • Smooth animations")
    print("  • Better performance")
    print("  • Modern flat design")
    print("  • Enhanced visual effects")
    print()
    print("Controls:")
    print("  Arrow Keys: Move and rotate")
    print("  Space: Hard drop")
    print("  P: Pause")
    print("  R: Restart")
    print("  Escape: Quit")
    print()
    
    try:
        # Create and setup the game
        print("Creating game window...")
        game, window = setup_game()
        print("Window created successfully")
        print("Starting game loop...")
        pyglet.app.run()
    except ImportError as e:
        print(f"Error: Missing dependency - {e}")
        print("Please install Pyglet: pip install pyglet")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        print("Game ended")


if __name__ == "__main__":
    main()