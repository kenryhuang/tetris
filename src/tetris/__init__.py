"""Tetris game package."""

__version__ = "0.1.0"
__all__ = ["Game", "Board", "Piece", "GameRenderer"]

# Import core classes that don't depend on pygame
from .board import Board
from .piece import Piece

# Import pygame-dependent classes only when needed
def get_game():
    """Get Game class (lazy import to avoid pygame dependency in tests)."""
    from .game import Game
    return Game

def get_renderer():
    """Get GameRenderer class (lazy import to avoid pygame dependency in tests)."""
    from .renderer import GameRenderer
    return GameRenderer

# For backward compatibility - use functions to avoid immediate imports
Game = get_game()
GameRenderer = get_renderer()