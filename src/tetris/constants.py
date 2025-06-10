"""Game constants and configuration."""

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

# Modern flat color scheme inspired by Apple OS
COLORS = {
    'BACKGROUND': (248, 248, 248),    # Light gray background
    'WHITE': (255, 255, 255),         # Pure white
    'BORDER': (200, 200, 200),        # Light border
    'TEXT': (60, 60, 60),             # Dark gray text
    'ACCENT': (0, 122, 255),          # Apple blue accent
    'SIDEBAR': (240, 240, 240),       # Sidebar background
    
    # Tetris piece colors - softer, modern palette
    'CYAN': (88, 196, 221),           # Soft cyan
    'YELLOW': (255, 204, 0),          # Warm yellow
    'PURPLE': (175, 82, 222),         # Soft purple
    'GREEN': (52, 199, 89),           # Fresh green
    'RED': (255, 59, 48),             # Vibrant red
    'BLUE': (0, 122, 255),            # Apple blue
    'ORANGE': (255, 149, 0),          # Warm orange
    
    # Legacy colors for compatibility
    'BLACK': (0, 0, 0),
    'GRAY': (128, 128, 128),
    'LIGHT_GRAY': (192, 192, 192),
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
}

# Game timing (milliseconds)
INITIAL_FALL_TIME = 1000
FAST_FALL_TIME = 50
MIN_FALL_TIME = 100
FALL_TIME_DECREASE = 50

# Scoring
SCORE_VALUES = {
    1: 10,   # Single line
    2: 30,   # Double lines
    3: 60,   # Triple lines
    4: 100,  # Tetris (four lines)
}

# Level progression - new score-based system
LEVEL_SCORE_BASE = 200  # First level requires 200 points
LEVEL_SCORE_MULTIPLIER = 1.5  # Each level multiplies score requirement by 1.5
SPEED_MULTIPLIER = 1.2  # Speed increases by 20% each level

# Legacy line-based progression (kept for compatibility)
LINES_PER_LEVEL = 10

# Key mappings
KEY_MAPPINGS = {
    'LEFT': 'left',
    'RIGHT': 'right',
    'UP': 'rotate',
    'DOWN': 'soft_drop',
    'SPACE': 'hard_drop',
    'ESCAPE': 'quit',
}

# Line clear effects
EFFECT_DURATION = 3000  # Effect duration in milliseconds - 延长以匹配新的特效时间
PARTICLE_COUNT = 8      # Number of particles per cleared cell
PARTICLE_SPEED = (2, 8) # Particle speed range (min, max)
PARTICLE_LIFE = (800, 1500)  # Particle lifetime range in milliseconds
EXPLOSION_RADIUS = 50   # Maximum explosion radius

# Effect colors - 优化为在白色背景上更明显的颜色
EFFECT_COLORS = {
    'EXPLOSION': [(255, 100, 0), (255, 50, 50), (200, 0, 100), (150, 0, 255)],  # 深橙、深红、深紫
    'FLASH': (0, 100, 255),  # 深蓝色
    'SPARKLE': [(0, 0, 255), (255, 0, 0), (0, 150, 0), (255, 0, 255)]  # 蓝、红、绿、紫
}