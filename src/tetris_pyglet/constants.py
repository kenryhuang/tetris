"""Constants for the Pyglet Tetris implementation.

This module contains all game constants including dimensions, colors,
timing values, and configuration settings optimized for pyglet.
"""

# Game board dimensions
BOARD_WIDTH = 10
BOARD_HEIGHT = 20

# Display settings
CELL_SIZE = 50
BORDER_WIDTH = 6
PREVIEW_SIZE = 8

# Window dimensions
GAME_WIDTH = BOARD_WIDTH * CELL_SIZE
GAME_HEIGHT = BOARD_HEIGHT * CELL_SIZE
SIDEBAR_WIDTH = 300
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH + BORDER_WIDTH * 3
WINDOW_HEIGHT = GAME_HEIGHT + BORDER_WIDTH * 2

# Modern color scheme with RGBA support for pyglet
COLORS = {
    'BACKGROUND': (248, 248, 248, 255),    # Light gray background
    'WHITE': (255, 255, 255, 255),         # Pure white
    'BORDER': (200, 200, 200, 255),        # Light border
    'TEXT': (60, 60, 60, 255),             # Dark gray text
    'ACCENT': (0, 122, 255, 255),          # Apple blue accent
    'SIDEBAR': (240, 240, 240, 255),       # Sidebar background
    
    # Tetris piece colors - softer, modern palette with alpha
    'CYAN': (88, 196, 221, 255),           # Soft cyan
    'YELLOW': (255, 204, 0, 255),          # Warm yellow
    'PURPLE': (175, 82, 222, 255),         # Soft purple
    'GREEN': (52, 199, 89, 255),           # Fresh green
    'RED': (255, 59, 48, 255),             # Vibrant red
    'BLUE': (0, 122, 255, 255),            # Apple blue
    'ORANGE': (255, 149, 0, 255),          # Warm orange
    
    # 不规则方块专用颜色
    'MAGENTA': (255, 45, 85, 255),         # 洋红色
    'TEAL': (90, 200, 250, 255),           # 青绿色
    'LIME': (50, 215, 75, 255),            # 酸橙色
    'INDIGO': (88, 86, 214, 255),          # 靛蓝色
    'PINK': (255, 55, 95, 255),            # 粉红色
    'CORAL': (255, 69, 58, 255),           # 珊瑚色
    
    # Legacy colors for compatibility
    'BLACK': (0, 0, 0, 255),
    'GRAY': (128, 128, 128, 255),
    'LIGHT_GRAY': (192, 192, 192, 255),
}

# Tetris piece colors - Apple-style flat colors
PIECE_COLORS = {
    'I': COLORS['CYAN'],
    'O': COLORS['YELLOW'],
    'T': COLORS['PURPLE'],
    'S': COLORS['GREEN'],
    'Z': COLORS['RED'],
    'J': COLORS['BLUE'],
    'L': COLORS['ORANGE'],
    
    # 不规则方块颜色
    'X': COLORS['MAGENTA'],     # 十字形 - 洋红色
    'U': COLORS['TEAL'],        # U形 - 青绿色
    'P': COLORS['LIME'],        # P形 - 酸橙色
    'Y': COLORS['INDIGO'],      # Y形 - 靛蓝色
    'W': COLORS['PINK'],        # W形 - 粉红色
    'H': COLORS['CORAL'],       # H形 - 珊瑚色
}

# Game timing (in seconds for pyglet)
INITIAL_FALL_TIME = 1.0
FAST_FALL_TIME = 0.05
MIN_FALL_TIME = 0.1
FALL_TIME_DECREASE = 0.05
EFFECT_DURATION = 0.5

# Scoring system
SCORE_VALUES = {
    1: 10,    # Single line
    2: 30,    # Double lines
    3: 50,    # Triple lines
    4: 100,   # Tetris (4 lines)
}

# Level progression
LINES_PER_LEVEL = 10
LEVEL_SCORE_BASE = 1000
LEVEL_SCORE_MULTIPLIER = 1.5
SPEED_MULTIPLIER = 0.9

# Key mappings for pyglet
from pyglet.window import key

KEY_MAPPINGS = {
    'LEFT': key.LEFT,
    'RIGHT': key.RIGHT,
    'DOWN': key.DOWN,
    'UP': key.UP,
    'ROTATE_CW': key.UP,
    'ROTATE_CCW': key.Z,
    'DROP': key.SPACE,
    'PAUSE': key.P,
    'RESTART': key.R,
    'QUIT': key.ESCAPE,
}

# Alternative key mappings
ALT_KEY_MAPPINGS = {
    'LEFT': key.A,
    'RIGHT': key.D,
    'DOWN': key.S,
    'ROTATE_CW': key.W,
    'DROP': key.ENTER,
}

# Particle system constants
PARTICLE_COUNT_RANGE = (15, 25)
PARTICLE_SPEED_RANGE = (50, 150)
PARTICLE_LIFE_RANGE = (0.5, 1.5)
PARTICLE_SIZE_RANGE = (2, 8)
PARTICLE_GRAVITY = 200
PARTICLE_DRAG = 0.98

# Animation constants
ANIMATION_SPEED = 2.0
LINE_CLEAR_ANIMATION_TIME = 0.6
PIECE_LOCK_ANIMATION_TIME = 0.1
GAME_OVER_ANIMATION_TIME = 1.0

# Visual effects
GLOW_INTENSITY = 0.3
SHADOW_OFFSET = 2
BORDER_RADIUS = 4
GRID_ALPHA = 0.5

# Audio settings (for future implementation)
AUDIO_ENABLED = True
MUSIC_VOLUME = 0.7
SFX_VOLUME = 0.8

# Performance settings
TARGET_FPS = 60
VSYNC_ENABLED = True
ANTIALIASING = True