"""Advanced visual effects system using Pyglet and OpenGL.

This module provides particle systems, animations, and visual effects
optimized for Pyglet's OpenGL rendering pipeline.
"""

import pyglet
from pyglet import shapes
from pyglet.gl import *
import random
import math
from typing import List, Tuple, Optional
from .constants import (
    EFFECT_DURATION, PARTICLE_COUNT, PARTICLE_SPEED, PARTICLE_LIFE,
    EXPLOSION_RADIUS, EFFECT_COLORS, CELL_SIZE, WINDOW_HEIGHT
)


class Particle:
    """A single particle for visual effects."""
    
    def __init__(self, x: float, y: float, vx: float, vy: float, 
                 color: Tuple[int, int, int], life: float, size: float = 3.0):
        """Initialize a particle.
        
        Args:
            x: Initial X position
            y: Initial Y position
            vx: X velocity
            vy: Y velocity
            color: RGB color tuple
            life: Particle lifetime in milliseconds
            size: Particle size
        """
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = color
        self.life = life
        self.max_life = life
        self.size = size
        self.gravity = -200.0  # Gravity acceleration
        self.alive = True
        
        # Create the visual representation
        self.shape = None
        self._create_shape()
    
    def _create_shape(self) -> None:
        """Create the Pyglet shape for this particle."""
        # Calculate alpha based on life remaining
        alpha = int(255 * (self.life / self.max_life))
        color_with_alpha = (*self.color, alpha)
        
        self.shape = shapes.Circle(
            self.x, self.y, self.size,
            color=color_with_alpha
        )
    
    def update(self, dt: float) -> None:
        """Update particle position and state.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.alive:
            return
            
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Apply gravity
        self.vy += self.gravity * dt
        
        # Update life
        self.life -= dt * 1000  # Convert to milliseconds
        
        if self.life <= 0:
            self.alive = False
            return
        
        # Update visual representation
        if self.shape:
            self.shape.x = self.x
            self.shape.y = self.y
            
            # Fade out over time
            alpha = int(255 * (self.life / self.max_life))
            self.shape.color = (*self.color, alpha)
            
            # Shrink over time
            size_factor = self.life / self.max_life
            self.shape.radius = self.size * size_factor
    
    def draw(self, batch: pyglet.graphics.Batch) -> None:
        """Draw the particle.
        
        Args:
            batch: Pyglet batch for efficient rendering
        """
        if self.alive and self.shape:
            self.shape.batch = batch





class LineFlashEffect:
    """Flash effect for cleared lines."""
    
    def __init__(self, y: int, width: int, board_x: int, board_y: int):
        """Initialize line flash effect.
        
        Args:
            y: Line Y coordinate
            width: Line width in cells
            board_x: Board X offset
            board_y: Board Y offset
        """
        self.y = y
        self.width = width
        self.board_x = board_x
        self.board_y = board_y
        self.duration = 0.0
        self.max_duration = 0.3  # Flash duration in seconds
        self.active = True
        
        # Create flash rectangle
        pixel_y = WINDOW_HEIGHT - (board_y + (y + 1) * CELL_SIZE)
        self.flash_rect = shapes.Rectangle(
            board_x, pixel_y,
            width * CELL_SIZE, CELL_SIZE,
            color=(255, 255, 255, 200)
        )
    
    def update(self, dt: float) -> None:
        """Update flash effect.
        
        Args:
            dt: Delta time in seconds
        """
        self.duration += dt
        
        if self.duration >= self.max_duration:
            self.active = False
            return
        
        # Pulsing alpha effect
        progress = self.duration / self.max_duration
        alpha = int(200 * (1 - progress) * (1 + 0.5 * math.sin(progress * 20)))
        
        if self.flash_rect:
            self.flash_rect.color = (255, 255, 255, max(0, alpha))
    
    def draw(self, batch: pyglet.graphics.Batch) -> None:
        """Draw the flash effect.
        
        Args:
            batch: Pyglet batch for efficient rendering
        """
        if self.active and self.flash_rect:
            self.flash_rect.batch = batch


class SparkleEffect:
    """Sparkle effect with twinkling particles."""
    
    def __init__(self, x: float, y: float):
        """Initialize sparkle effect.
        
        Args:
            x: Center X position
            y: Center Y position
        """
        self.x = x
        self.y = y
        self.particles: List[Particle] = []
        self.active = True
        self.spawn_timer = 0.0
        self.spawn_interval = 0.05  # Spawn new particles every 50ms
        self.total_duration = 1.0  # Total effect duration
        self.elapsed_time = 0.0
        
    def update(self, dt: float) -> None:
        """Update sparkle effect.
        
        Args:
            dt: Delta time in seconds
        """
        self.elapsed_time += dt
        self.spawn_timer += dt
        
        # Spawn new particles
        if (self.spawn_timer >= self.spawn_interval and 
            self.elapsed_time < self.total_duration):
            self._spawn_sparkle_particle()
            self.spawn_timer = 0.0
        
        # Update existing particles
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.alive:
                self.particles.remove(particle)
        
        # Check if effect should end
        if (self.elapsed_time >= self.total_duration and 
            len(self.particles) == 0):
            self.active = False
    
    def _spawn_sparkle_particle(self) -> None:
        """Spawn a new sparkle particle."""
        # Random position around center
        offset_x = random.uniform(-20, 20)
        offset_y = random.uniform(-20, 20)
        
        x = self.x + offset_x
        y = self.y + offset_y
        
        # Gentle floating motion
        vx = random.uniform(-30, 30)
        vy = random.uniform(20, 60)
        
        # Sparkle colors
        color = random.choice(EFFECT_COLORS['SPARKLE'])
        life = random.uniform(500, 1000)
        size = random.uniform(1, 3)
        
        particle = Particle(x, y, vx, vy, color, life, size)
        self.particles.append(particle)
    
    def draw(self, batch: pyglet.graphics.Batch) -> None:
        """Draw all sparkle particles.
        
        Args:
            batch: Pyglet batch for efficient rendering
        """
        for particle in self.particles:
            particle.draw(batch)


class PygletEffectsManager:
    """Manages all visual effects using Pyglet."""
    
    def __init__(self):
        """Initialize the effects manager."""
        self.effects: List = []
        self.batch = pyglet.graphics.Batch()
    
    def add_line_clear_effect(self, lines: List[int], board_x: int, board_y: int) -> None:
        """Add line clear effects.
        
        Args:
            lines: List of line indices that were cleared
            board_x: Board X offset
            board_y: Board Y offset
        """
        for line_y in lines:
            # Flash effect
            flash = LineFlashEffect(line_y, 10, board_x, board_y)  # 10 cells wide
            self.effects.append(flash)
            
            # Line flash effect only (explosion effects removed)
    
    def add_piece_land_effect(self, piece_blocks: List[Tuple[int, int]], 
                             board_x: int, board_y: int) -> None:
        """Add effect when a piece lands.
        
        Args:
            piece_blocks: List of (x, y) coordinates where piece landed
            board_x: Board X offset
            board_y: Board Y offset
        """
        for x, y in piece_blocks:
            if y >= 0:  # Only for visible blocks
                pixel_x = board_x + x * CELL_SIZE + CELL_SIZE // 2
                pixel_y = WINDOW_HEIGHT - (board_y + y * CELL_SIZE + CELL_SIZE // 2)
                
                sparkle = SparkleEffect(pixel_x, pixel_y)
                self.effects.append(sparkle)
    
    def add_level_up_effect(self, center_x: float, center_y: float) -> None:
        """Add level up celebration effect.
        
        Args:
            center_x: Center X position
            center_y: Center Y position
        """
        # Level up effect (explosion effects removed)
        # Only visual feedback without explosion particles
    
    def update(self, dt: float) -> None:
        """Update all active effects.
        
        Args:
            dt: Delta time in seconds
        """
        for effect in self.effects[:]:
            effect.update(dt)
            if not effect.active:
                self.effects.remove(effect)
    
    def draw(self, batch: pyglet.graphics.Batch) -> None:
        """Draw all active effects.
        
        Args:
            batch: Pyglet batch for efficient rendering
        """
        for effect in self.effects:
            effect.draw(batch)
    
    def has_active_effects(self) -> bool:
        """Check if there are any active effects.
        
        Returns:
            True if there are active effects
        """
        return len(self.effects) > 0
    
    def clear_all_effects(self) -> None:
        """Clear all active effects."""
        self.effects.clear()