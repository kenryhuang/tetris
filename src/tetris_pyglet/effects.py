"""Effects module for Pyglet Tetris implementation.

This module contains advanced particle effects and animations
using pyglet's OpenGL capabilities for enhanced visual experience.
"""

import pyglet
from pyglet import shapes, gl
import random
import math
from typing import List, Tuple, Optional
from .constants import (
    PARTICLE_COUNT_RANGE, PARTICLE_SPEED_RANGE, PARTICLE_LIFE_RANGE,
    PARTICLE_SIZE_RANGE, PARTICLE_GRAVITY, PARTICLE_DRAG,
    COLORS, CELL_SIZE, BOARD_WIDTH, BOARD_HEIGHT
)


class Particle:
    """Advanced particle with physics and visual effects."""
    
    def __init__(self, x: float, y: float, vx: float = 0, vy: float = 0,
                 life: float = 1.0, color: Tuple[int, int, int, int] = None,
                 size: float = 4.0):
        """Initialize a particle.
        
        Args:
            x: Initial X position
            y: Initial Y position
            vx: Initial X velocity
            vy: Initial Y velocity
            life: Particle lifetime in seconds
            color: RGBA color tuple
            size: Initial particle size
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.initial_life = life
        self.life = life
        self.color = color or COLORS['WHITE']
        self.initial_size = size
        self.size = size
        
        # Physics properties
        self.gravity = PARTICLE_GRAVITY
        self.drag = PARTICLE_DRAG
        self.bounce = 0.3
        
        # Visual properties
        self.rotation = 0.0
        self.rotation_speed = random.uniform(-360, 360)
        self.alpha_decay = 1.0
        self.size_decay = 1.0
        
        # Trail effect
        self.trail_positions = []
        self.max_trail_length = 5
        
    def update(self, dt: float) -> bool:
        """Update particle physics and properties.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            True if particle is still alive
        """
        if self.life <= 0:
            return False
        
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Apply gravity
        self.vy -= self.gravity * dt
        
        # Apply drag
        self.vx *= self.drag
        self.vy *= self.drag
        
        # Update rotation
        self.rotation += self.rotation_speed * dt
        
        # Update life
        self.life -= dt
        life_ratio = self.life / self.initial_life
        
        # Update visual properties based on life
        self.alpha_decay = life_ratio
        self.size_decay = 0.5 + 0.5 * life_ratio  # Size fades from 100% to 50%
        self.size = self.initial_size * self.size_decay
        
        # Update trail
        self.trail_positions.append((self.x, self.y))
        if len(self.trail_positions) > self.max_trail_length:
            self.trail_positions.pop(0)
        
        return self.life > 0
    
    def get_current_color(self) -> Tuple[int, int, int, int]:
        """Get current color with alpha based on life.
        
        Returns:
            RGBA color tuple
        """
        r, g, b = self.color[:3]
        alpha = int(255 * self.alpha_decay)
        return (r, g, b, alpha)
    
    def draw(self, batch: pyglet.graphics.Batch, group: pyglet.graphics.Group) -> List:
        """Draw the particle with advanced effects.
        
        Args:
            batch: Pyglet batch for rendering
            group: Pyglet group for layering
            
        Returns:
            List of created shapes
        """
        if self.life <= 0 or self.size <= 0:
            return []
        
        shapes_list = []
        current_color = self.get_current_color()
        
        # Draw trail
        if len(self.trail_positions) > 1:
            for i, (tx, ty) in enumerate(self.trail_positions[:-1]):
                trail_alpha = int(current_color[3] * (i / len(self.trail_positions)) * 0.5)
                trail_size = self.size * (i / len(self.trail_positions)) * 0.5
                
                if trail_alpha > 0 and trail_size > 0:
                    trail_circle = shapes.Circle(
                        tx, ty, trail_size,
                        color=current_color[:3],
                        batch=batch, group=group
                    )
                    trail_circle.opacity = trail_alpha
                    shapes_list.append(trail_circle)
        
        # Draw glow effect
        glow_size = self.size * 2
        glow_alpha = int(current_color[3] * 0.3)
        if glow_alpha > 0:
            glow_circle = shapes.Circle(
                self.x, self.y, glow_size,
                color=current_color[:3],
                batch=batch, group=group
            )
            glow_circle.opacity = glow_alpha
            shapes_list.append(glow_circle)
        
        # Draw main particle
        main_circle = shapes.Circle(
            self.x, self.y, self.size,
            color=current_color[:3],
            batch=batch, group=group
        )
        main_circle.opacity = current_color[3]
        shapes_list.append(main_circle)
        
        # Draw core highlight
        core_size = self.size * 0.4
        core_color = tuple(min(255, c + 100) for c in current_color[:3])
        core_alpha = int(current_color[3] * 0.8)
        
        if core_alpha > 0 and core_size > 0:
            core_circle = shapes.Circle(
                self.x, self.y, core_size,
                color=core_color,
                batch=batch, group=group
            )
            core_circle.opacity = core_alpha
            shapes_list.append(core_circle)
        
        return shapes_list


class ExplosionEffect:
    """Advanced explosion effect with multiple particle types."""
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int, int] = None,
                 intensity: float = 1.0):
        """Initialize explosion effect.
        
        Args:
            x: Explosion center X
            y: Explosion center Y
            color: Base color for particles
            intensity: Effect intensity (0.0 to 2.0)
        """
        self.x = x
        self.y = y
        self.color = color or COLORS['WHITE']
        self.intensity = intensity
        self.particles: List[Particle] = []
        self.active = True
        
        self._create_particles()
    
    def _create_particles(self) -> None:
        """Create explosion particles."""
        # Calculate particle count based on intensity
        min_count, max_count = PARTICLE_COUNT_RANGE
        particle_count = int(random.randint(min_count, max_count) * self.intensity)
        
        # Create main explosion particles
        for _ in range(particle_count):
            # Random direction and speed
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*PARTICLE_SPEED_RANGE) * self.intensity
            
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            # Random position offset
            offset_x = random.uniform(-5, 5)
            offset_y = random.uniform(-5, 5)
            
            # Random life and size
            life = random.uniform(*PARTICLE_LIFE_RANGE)
            size = random.uniform(*PARTICLE_SIZE_RANGE) * self.intensity
            
            # Color variation
            color_variation = self._get_color_variation()
            
            particle = Particle(
                self.x + offset_x, self.y + offset_y,
                vx, vy, life, color_variation, size
            )
            
            self.particles.append(particle)
        
        # Create spark particles
        spark_count = int(particle_count * 0.3)
        for _ in range(spark_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 300) * self.intensity
            
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            life = random.uniform(0.1, 0.5)
            size = random.uniform(1, 3)
            
            # Bright spark colors
            spark_color = (255, 255, 200, 255)  # Bright yellow-white
            
            spark = Particle(
                self.x, self.y, vx, vy, life, spark_color, size
            )
            spark.gravity *= 0.5  # Less gravity for sparks
            
            self.particles.append(spark)
    
    def _get_color_variation(self) -> Tuple[int, int, int, int]:
        """Get a color variation of the base color.
        
        Returns:
            RGBA color tuple with variation
        """
        base_r, base_g, base_b = self.color[:3]
        
        # Add some randomness to the color
        variation = 50
        r = max(0, min(255, base_r + random.randint(-variation, variation)))
        g = max(0, min(255, base_g + random.randint(-variation, variation)))
        b = max(0, min(255, base_b + random.randint(-variation, variation)))
        
        return (r, g, b, 255)
    
    def update(self, dt: float) -> bool:
        """Update explosion effect.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            True if effect is still active
        """
        if not self.active:
            return False
        
        # Update all particles
        self.particles = [p for p in self.particles if p.update(dt)]
        
        # Effect is done when all particles are dead
        if not self.particles:
            self.active = False
        
        return self.active
    
    def draw(self, batch: pyglet.graphics.Batch, group: pyglet.graphics.Group) -> List:
        """Draw explosion effect.
        
        Args:
            batch: Pyglet batch for rendering
            group: Pyglet group for layering
            
        Returns:
            List of created shapes
        """
        shapes_list = []
        for particle in self.particles:
            shapes_list.extend(particle.draw(batch, group))
        return shapes_list


class LineEffect:
    """Advanced line clearing effect with waves and particles."""
    
    def __init__(self, line_y: int, board_x: int, board_y: int):
        """Initialize line effect.
        
        Args:
            line_y: Line index being cleared
            board_x: Board X position in pixels
            board_y: Board Y position in pixels
        """
        self.line_y = line_y
        self.board_x = board_x
        self.board_y = board_y
        self.progress = 0.0
        self.duration = 0.5
        self.active = True
        
        # Calculate line position in pixels
        self.pixel_y = board_y + (BOARD_HEIGHT - 1 - line_y) * CELL_SIZE
        
        # Create particles along the line
        self.particles: List[Particle] = []
        self._create_line_particles()
    
    def _create_line_particles(self) -> None:
        """Create particles along the clearing line."""
        # Create particles across the width of the board
        for x in range(BOARD_WIDTH * 2):  # More particles for smoother effect
            pixel_x = self.board_x + (x / 2) * CELL_SIZE
            
            # Random upward velocity
            vx = random.uniform(-50, 50)
            vy = random.uniform(100, 200)
            
            life = random.uniform(0.3, 0.8)
            size = random.uniform(2, 6)
            
            # Bright clearing colors
            colors = [
                COLORS['YELLOW'],
                COLORS['WHITE'],
                COLORS['CYAN'],
                (255, 255, 200, 255)  # Bright yellow-white
            ]
            color = random.choice(colors)
            
            particle = Particle(
                pixel_x, self.pixel_y, vx, vy, life, color, size
            )
            particle.gravity *= 0.7  # Less gravity for line particles
            
            self.particles.append(particle)
    
    def update(self, dt: float) -> bool:
        """Update line effect.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            True if effect is still active
        """
        if not self.active:
            return False
        
        self.progress += dt / self.duration
        
        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]
        
        # Effect is done when progress is complete and particles are gone
        if self.progress >= 1.0 and not self.particles:
            self.active = False
        
        return self.active
    
    def draw(self, batch: pyglet.graphics.Batch, group: pyglet.graphics.Group) -> List:
        """Draw line effect.
        
        Args:
            batch: Pyglet batch for rendering
            group: Pyglet group for layering
            
        Returns:
            List of created shapes
        """
        shapes_list = []
        
        # Draw wave effect
        if self.progress < 1.0:
            wave_width = self.progress * BOARD_WIDTH * CELL_SIZE
            wave_height = 4
            wave_alpha = int(255 * (1.0 - self.progress))
            
            if wave_alpha > 0:
                wave_rect = shapes.Rectangle(
                    self.board_x, self.pixel_y - wave_height // 2,
                    wave_width, wave_height,
                    color=COLORS['YELLOW'][:3],
                    batch=batch, group=group
                )
                wave_rect.opacity = wave_alpha
                shapes_list.append(wave_rect)
        
        # Draw particles
        for particle in self.particles:
            shapes_list.extend(particle.draw(batch, group))
        
        return shapes_list


class PygletEffectsManager:
    """Manages all visual effects for the pyglet Tetris game."""
    
    def __init__(self):
        """Initialize the effects manager."""
        self.explosion_effects: List[ExplosionEffect] = []
        self.line_effects: List[LineEffect] = []
        
        # Create batch and group for effects
        self.batch = pyglet.graphics.Batch()
        self.group = pyglet.graphics.Group(order=10)
        
    def add_explosion_effect(self, x: int, y: int, color: Tuple[int, int, int, int] = None,
                           intensity: float = 1.0) -> None:
        """Add an explosion effect at the specified grid position.
        
        Args:
            x: Grid X coordinate
            y: Grid Y coordinate
            color: Explosion color
            intensity: Effect intensity
        """
        # Convert grid coordinates to pixel coordinates
        from .constants import BORDER_WIDTH
        pixel_x = BORDER_WIDTH + (x + 0.5) * CELL_SIZE
        pixel_y = BORDER_WIDTH + (BOARD_HEIGHT - y - 0.5) * CELL_SIZE
        
        explosion = ExplosionEffect(pixel_x, pixel_y, color, intensity)
        self.explosion_effects.append(explosion)
    
    def add_line_clear_effect(self, line_y: int) -> None:
        """Add a line clearing effect.
        
        Args:
            line_y: Line index being cleared
        """
        from .constants import BORDER_WIDTH
        line_effect = LineEffect(line_y, BORDER_WIDTH, BORDER_WIDTH)
        self.line_effects.append(line_effect)
    
    def add_sparkle_effect(self, x: int, y: int, count: int = 5) -> None:
        """Add sparkle effects at the specified position.
        
        Args:
            x: Grid X coordinate
            y: Grid Y coordinate
            count: Number of sparkles
        """
        for _ in range(count):
            # Small, quick sparkles
            self.add_explosion_effect(x, y, COLORS['YELLOW'], 0.3)
    
    def update(self, dt: float) -> None:
        """Update all effects.
        
        Args:
            dt: Delta time in seconds
        """
        # Update explosion effects
        self.explosion_effects = [
            effect for effect in self.explosion_effects
            if effect.update(dt)
        ]
        
        # Update line effects
        self.line_effects = [
            effect for effect in self.line_effects
            if effect.update(dt)
        ]
    
    def draw(self, batch: pyglet.graphics.Batch, 
             group: pyglet.graphics.Group = None) -> List:
        """Draw all effects.
        
        Args:
            batch: Pyglet batch for rendering
            group: Pyglet group for layering
            
        Returns:
            List of created shapes
        """
        if batch is None:
            batch = self.batch
        if group is None:
            group = self.group
        
        shapes_list = []
        
        # Draw explosion effects
        for effect in self.explosion_effects:
            shapes_list.extend(effect.draw(batch, group))
        
        # Draw line effects
        for effect in self.line_effects:
            shapes_list.extend(effect.draw(batch, group))
        
        return shapes_list
    
    def has_active_effects(self) -> bool:
        """Check if there are any active effects.
        
        Returns:
            True if there are active effects
        """
        return len(self.explosion_effects) > 0 or len(self.line_effects) > 0
    
    def clear_all_effects(self) -> None:
        """Clear all active effects."""
        self.explosion_effects.clear()
        self.line_effects.clear()