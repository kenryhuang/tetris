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


class RainbowWaveEffect:
    """Creative rainbow wave line clearing effect with dynamic color transitions."""
    
    def __init__(self, line_y: int, board_x: int, board_y: int):
        """Initialize rainbow wave effect.
        
        Args:
            line_y: Line index being cleared
            board_x: Board X position in pixels
            board_y: Board Y position in pixels
        """
        self.line_y = line_y
        self.board_x = board_x
        self.board_y = board_y
        self.progress = 0.0
        self.duration = 6.0  # Total duration of wave effect
        self.active = True
        
        # Calculate line position in pixels
        # Match the coordinate system used in renderer: y=0 is bottom of board, y=19 is top
        # Use the same formula as renderer._get_pixel_coords
        self.pixel_y = board_y + (BOARD_HEIGHT - 1 - line_y) * CELL_SIZE
        print(f"Effect for line {line_y}: board_y={board_y}, pixel_y={self.pixel_y}, BOARD_HEIGHT={BOARD_HEIGHT}, CELL_SIZE={CELL_SIZE}")
        
        # Wave properties
        self.wave_center = BOARD_WIDTH // 2
        self.wave_speed = 8.0  # Speed of wave propagation
        self.wave_amplitude = 15.0  # Height of wave oscillation
        self.wave_frequency = 2.0  # Frequency of wave oscillation
        
        # Rainbow colors for the wave
        self.rainbow_colors = [
            (255, 0, 0, 255),    # Red
            (255, 127, 0, 255),  # Orange
            (255, 255, 0, 255),  # Yellow
            (0, 255, 0, 255),    # Green
            (0, 0, 255, 255),    # Blue
            (75, 0, 130, 255),   # Indigo
            (148, 0, 211, 255),  # Violet
        ]
        
        # Particle effects for sparkles
        self.sparkle_particles: List[Particle] = []
        self.last_sparkle_time = 0.0
        
        # Lightning effect
        self.lightning_segments = []
        self.lightning_timer = 0.0
        self.lightning_duration = 1
        
    def _get_rainbow_color(self, position: float) -> Tuple[int, int, int, int]:
        """Get rainbow color based on position (0.0 to 1.0).
        
        Args:
            position: Position along rainbow (0.0 to 1.0)
            
        Returns:
            RGBA color tuple
        """
        # Normalize position to rainbow color array
        color_index = position * (len(self.rainbow_colors) - 1)
        index = int(color_index)
        fraction = color_index - index
        
        if index >= len(self.rainbow_colors) - 1:
            return self.rainbow_colors[-1]
        
        # Interpolate between two colors
        color1 = self.rainbow_colors[index]
        color2 = self.rainbow_colors[index + 1]
        
        r = int(color1[0] + (color2[0] - color1[0]) * fraction)
        g = int(color1[1] + (color2[1] - color1[1]) * fraction)
        b = int(color1[2] + (color2[2] - color1[2]) * fraction)
        
        return (r, g, b, 255)
    
    def _create_sparkles(self, dt: float) -> None:
        """Create sparkle particles along the wave.
        
        Args:
            dt: Delta time in seconds
        """
        self.last_sparkle_time += dt
        if self.last_sparkle_time >= 0.05:  # Create sparkles every 50ms
            self.last_sparkle_time = 0.0
            
            # Create sparkles at random positions along the line
            for _ in range(3):
                x = random.randint(0, BOARD_WIDTH - 1)
                pixel_x = self.board_x + (x + 0.5) * CELL_SIZE
                
                # Wave offset
                wave_offset = math.sin(self.progress * self.wave_frequency * 2 * math.pi + x * 0.5) * self.wave_amplitude
                
                # Random sparkle properties
                vx = random.uniform(-50, 50)
                vy = random.uniform(50, 150)
                life = random.uniform(0.3, 0.8)
                size = random.uniform(2, 6)
                
                # Rainbow color based on position
                color_pos = (x / BOARD_WIDTH + self.progress * 2) % 1.0
                color = self._get_rainbow_color(color_pos)
                
                sparkle = Particle(
                    pixel_x, self.pixel_y + wave_offset,
                    vx, vy, life, color, size
                )
                sparkle.gravity *= 0.3  # Reduced gravity for floating effect
                self.sparkle_particles.append(sparkle)
    
    def _create_lightning(self) -> None:
        """Create lightning effect across the line."""
        self.lightning_segments.clear()
        
        # Create jagged lightning path
        points = []
        for x in range(BOARD_WIDTH + 1):
            pixel_x = self.board_x + x * CELL_SIZE
            offset_y = random.uniform(-10, 10)
            points.append((pixel_x, self.pixel_y + offset_y))
        
        # Store lightning segments
        for i in range(len(points) - 1):
            self.lightning_segments.append((points[i], points[i + 1]))
        
        self.lightning_timer = self.lightning_duration
    
    def update(self, dt: float) -> bool:
        """Update rainbow wave effect.
        
        Args:
            dt: Delta time in seconds
            
        Returns:
            True if effect is still active
        """
        if not self.active:
            return False
        
        self.progress += dt / self.duration
        
        # Create sparkles
        self._create_sparkles(dt)
        
        # Update sparkle particles
        self.sparkle_particles = [p for p in self.sparkle_particles if p.update(dt)]
        
        # Create lightning effect at certain intervals
        if self.progress > 0.2 and self.progress < 0.8 and random.random() < 0.1:
            self._create_lightning()
        
        # Update lightning timer
        if self.lightning_timer > 0:
            self.lightning_timer -= dt
        
        # Effect is done when progress reaches 1.0
        if self.progress >= 1.0:
            self.active = False
        
        return self.active
    
    def draw(self, batch: pyglet.graphics.Batch, group: pyglet.graphics.Group) -> List:
        """Draw rainbow wave effect.
        
        Args:
            batch: Pyglet batch for rendering
            group: Pyglet group for layering
            
        Returns:
            List of created shapes
        """
        shapes_list = []
        
        if not self.active:
            return shapes_list

        
        # Draw wave effect
        wave_alpha = int(255 * (1.0 - self.progress) * 0.8)
        if wave_alpha > 0:
            for x in range(BOARD_WIDTH):
                pixel_x = self.board_x + (x + 0.5) * CELL_SIZE
                
                # Calculate wave properties
                wave_phase = self.progress * self.wave_speed + x * 0.3
                wave_offset = math.sin(wave_phase) * self.wave_amplitude * (1.0 - self.progress)
                
                # Rainbow color based on position and time
                color_pos = (x / BOARD_WIDTH + self.progress) % 1.0
                color = self._get_rainbow_color(color_pos)
                
                # Draw main wave circle
                wave_size = CELL_SIZE * 0.4 * (1.0 - self.progress * 0.5)
                if wave_size > 0:
                    wave_circle = shapes.Circle(
                        pixel_x, self.pixel_y + wave_offset, wave_size,
                        color=color[:3], batch=batch, group=group
                    )
                    wave_circle.opacity = wave_alpha
                    shapes_list.append(wave_circle)
                
                # Draw glow effect
                glow_size = wave_size * 2
                glow_alpha = int(wave_alpha * 0.3)
                if glow_size > 0 and glow_alpha > 0:
                    glow_circle = shapes.Circle(
                        pixel_x, self.pixel_y + wave_offset, glow_size,
                        color=color[:3], batch=batch, group=group
                    )
                    glow_circle.opacity = glow_alpha
                    shapes_list.append(glow_circle)
        
        # Draw lightning effect
        if self.lightning_timer > 0:
            lightning_alpha = int(255 * (self.lightning_timer / self.lightning_duration))
            for start, end in self.lightning_segments:
                # Calculate line properties
                dx = end[0] - start[0]
                dy = end[1] - start[1]
                length = math.sqrt(dx*dx + dy*dy)
                if length > 0:
                    # Create a thin rectangle to represent the lightning
                    center_x = (start[0] + end[0]) / 2
                    center_y = (start[1] + end[1]) / 2
                    
                    lightning_rect = shapes.Rectangle(
                        center_x - length/2, center_y - 1.5, length, 3,
                        color=(255, 255, 255), batch=batch, group=group
                    )
                    lightning_rect.opacity = lightning_alpha
                    
                    # Rotate the rectangle to match the line angle
                    if dx != 0:
                        angle = math.atan2(dy, dx)
                        lightning_rect.rotation = math.degrees(angle)
                    
                    shapes_list.append(lightning_rect)
        
        # Draw sparkle particles
        for particle in self.sparkle_particles:
            shapes_list.extend(particle.draw(batch, group))
        
        return shapes_list





class PygletEffectsManager:
    """Manages all visual effects for the pyglet Tetris game."""
    
    def __init__(self):
        """Initialize the effects manager."""
        self.line_effects: List[RainbowWaveEffect] = []
        # Remove self.batch and self.group
        # Effects manager should always use the batch/group provided by the renderer

    def add_line_clear_effect(self, line_y: int) -> None:
        """Add a line clearing explosion effect.
        
        Args:
            line_y: Line index being cleared
        """
        from .constants import BORDER_WIDTH
        # Calculate correct board position
        board_x = BORDER_WIDTH
        board_y = BORDER_WIDTH
        line_effect = RainbowWaveEffect(line_y, board_x, board_y)
        self.line_effects.append(line_effect)
    
    def update(self, dt: float) -> None:
        """Update all effects.
        
        Args:
            dt: Delta time in seconds
        """
        # Update line explosion effects
        self.line_effects = [
            effect for effect in self.line_effects
            if effect.update(dt)
        ]
    
    def draw(self, batch: pyglet.graphics.Batch, 
             group: pyglet.graphics.Group = None) -> List:
        """Draw all effects.
        
        Args:
            batch: Pyglet batch for rendering (must not be None)
            group: Pyglet group for layering (must not be None)
            
        Returns:
            List of created shapes
        """
        if batch is None or group is None:
            raise ValueError("EffectsManager.draw() must be called with a valid batch and group from the renderer.")
        shapes_list = []
        # Draw line explosion effects (now RainbowWaveEffect)
        for effect in self.line_effects:
            shapes_list.extend(effect.draw(batch, group))
        return shapes_list
    
    def has_active_effects(self) -> bool:
        """Check if there are any active effects.
        
        Returns:
            True if there are active effects
        """
        return len(self.line_effects) > 0
    
    def clear_all_effects(self) -> None:
        """Clear all active effects."""
        self.line_effects.clear()





def create_line_explosion_chain(line_y: int, board_x: int, board_y: int, 
                               delay_between_explosions: float = 0.05) -> RainbowWaveEffect:
    """独立的行消除爆炸链特效创建函数。
    
    创建一个沿着指定行的连锁爆炸效果，从左到右依次引爆。
    
    Args:
        line_y: 行索引
        board_x: 游戏板X坐标（像素）
        board_y: 游戏板Y坐标（像素）
        delay_between_explosions: 每个爆炸之间的延迟时间（秒）
        
    Returns:
        RainbowWaveEffect: 创建的行爆炸效果对象
        
    Example:
        # 创建快速连锁爆炸
        line_explosion = create_line_explosion_chain(5, 50, 50, 0.03)
        
        # 创建慢速连锁爆炸
        line_explosion = create_line_explosion_chain(3, 50, 50, 0.1)
    """
    effect = RainbowWaveEffect(line_y, board_x, board_y)
    
    # 自定义爆炸间隔
    if delay_between_explosions != 0.05:  # 如果不是默认值
        for i in range(len(effect.explosion_timers)):
            effect.explosion_timers[i] = i * delay_between_explosions
    
    return effect