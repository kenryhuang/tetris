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


class TetrisWindow(pyglet.window.Window):
    """Main window class for the Pyglet Tetris game."""
    
    def __init__(self):
        """Initialize the game window."""
        super().__init__(
            width=WINDOW_WIDTH,
            height=WINDOW_HEIGHT,
            caption="Tetris - Pyglet Edition",
            resizable=False,
            vsync=True
        )
        
        # Initialize the game with this window
        self.game = PygletTetrisGame(self)
        
        # Schedule game update
        pyglet.clock.schedule_interval(self.update, 1/60.0)  # 60 FPS
        
    def on_draw(self):
        """Handle window drawing."""
        self.clear()
        self.game.draw()
        
    def update(self, dt):
        """Update game state."""
        self.game.update(dt)
        
    def on_key_press(self, symbol, modifiers):
        """Handle key press events."""
        self.game.on_key_press(symbol, modifiers)
        
    def on_key_release(self, symbol, modifiers):
        """Handle key release events."""
        self.game.on_key_release(symbol, modifiers)


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
        # Create and run the game window
        print("Creating game window...")
        window = TetrisWindow()
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