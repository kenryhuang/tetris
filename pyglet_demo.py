#!/usr/bin/env python3
"""Pyglet Particle Explosion Effect Demo

This demo showcases a particle explosion effect using the Pyglet library.
Click anywhere on the screen to create an explosion at that location.
"""

import pyglet
import random
import math
from typing import List, Tuple

# Window dimensions
WIDTH = 800
HEIGHT = 600

class Particle:
    """A single particle in the explosion effect."""
    
    def __init__(self, x: float, y: float, velocity_x: float, velocity_y: float, 
                 life_time: float, color: Tuple[int, int, int], size: float):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.life_time = life_time
        self.max_life_time = life_time
        self.color = color
        self.size = size
        self.gravity = -200  # Gravity effect
        
    def update(self, dt: float):
        """Update particle position and life."""
        # Update position
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        
        # Apply gravity
        self.velocity_y += self.gravity * dt
        
        # Reduce life time
        self.life_time -= dt
        
    def is_alive(self) -> bool:
        """Check if particle is still alive."""
        return self.life_time > 0
        
    def get_alpha(self) -> float:
        """Get alpha value based on remaining life."""
        return max(0, self.life_time / self.max_life_time)
        
    def get_current_size(self) -> float:
        """Get current size based on remaining life."""
        life_ratio = self.life_time / self.max_life_time
        return self.size * (0.5 + 0.5 * life_ratio)

class ExplosionEffect:
    """Manages a collection of particles for an explosion effect."""
    
    def __init__(self, x: float, y: float, particle_count: int = 50):
        self.particles: List[Particle] = []
        self.create_particles(x, y, particle_count)
        
    def create_particles(self, x: float, y: float, particle_count: int):
        """Create particles for the explosion."""
        colors = [
            (255, 100, 100),  # Red
            (255, 200, 100),  # Orange
            (255, 255, 100),  # Yellow
            (100, 255, 100),  # Green
            (100, 100, 255),  # Blue
            (255, 100, 255),  # Magenta
            (255, 255, 255),  # White
        ]
        
        for _ in range(particle_count):
            # Random angle and speed
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(100, 300)
            
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            # Random position offset
            offset_x = random.uniform(-10, 10)
            offset_y = random.uniform(-10, 10)
            
            # Random properties
            life_time = random.uniform(2.0, 4.0)
            color = random.choice(colors)
            size = random.uniform(3, 8)
            
            particle = Particle(
                x + offset_x, y + offset_y,
                velocity_x, velocity_y,
                life_time, color, size
            )
            self.particles.append(particle)
    
    def update(self, dt: float):
        """Update all particles and remove dead ones."""
        for particle in self.particles[:]:
            particle.update(dt)
            if not particle.is_alive():
                self.particles.remove(particle)
    
    def is_active(self) -> bool:
        """Check if explosion still has active particles."""
        return len(self.particles) > 0
    
    def draw(self, batch):
        """Draw all particles using pyglet shapes."""
        for particle in self.particles:
            alpha = int(particle.get_alpha() * 255)
            size = particle.get_current_size()
            
            # Create color with alpha
            r, g, b = particle.color
            color = (r, g, b, alpha)
            
            # Draw particle as a circle using pyglet shapes
            circle = pyglet.shapes.Circle(
                particle.x, particle.y, size,
                color=color[:3], batch=batch
            )
            circle.opacity = alpha
            
    def get_shapes(self):
        """Get all particle shapes for batch rendering."""
        shapes = []
        for particle in self.particles:
            alpha = int(particle.get_alpha() * 255)
            size = particle.get_current_size()
            
            # Create color with alpha
            r, g, b = particle.color
            
            # Create circle shape
            circle = pyglet.shapes.Circle(
                particle.x, particle.y, size,
                color=(r, g, b)
            )
            circle.opacity = alpha
            shapes.append(circle)
        return shapes

class ParticleExplosionDemo(pyglet.window.Window):
    """Main demo window for particle explosion effects."""
    
    def __init__(self):
        super().__init__(WIDTH, HEIGHT, caption="Pyglet Particle Explosion Demo")
        
        # Set background color to dark blue
        pyglet.gl.glClearColor(0.1, 0.1, 0.2, 1.0)
        
        self.explosions: List[ExplosionEffect] = []
        self.batch = pyglet.graphics.Batch()
        
        # Create initial explosion in center
        self.create_explosion(WIDTH // 2, HEIGHT // 2)
        
        # Instructions label
        self.instruction_label = pyglet.text.Label(
            'Click anywhere to create explosions!',
            font_name='Arial',
            font_size=16,
            x=WIDTH // 2,
            y=HEIGHT - 30,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255)
        )
        
        # Explosion count label
        self.count_label = pyglet.text.Label(
            'Active explosions: 0',
            font_name='Arial',
            font_size=14,
            x=10,
            y=HEIGHT - 30,
            anchor_x='left',
            anchor_y='center',
            color=(255, 255, 255, 255)
        )
        
        # Schedule update
        pyglet.clock.schedule_interval(self.update, 1/60.0)
    
    def create_explosion(self, x: float, y: float):
        """Create a new explosion at the specified position."""
        particle_count = random.randint(30, 80)
        explosion = ExplosionEffect(x, y, particle_count)
        self.explosions.append(explosion)
    
    def update(self, dt: float):
        """Update all explosions."""
        # Update all explosions
        for explosion in self.explosions[:]:
            explosion.update(dt)
            if not explosion.is_active():
                self.explosions.remove(explosion)
        
        # Update count label
        self.count_label.text = f'Active explosions: {len(self.explosions)}'
    
    def on_draw(self):
        """Render the scene."""
        self.clear()
        
        # Draw all explosion particles
        for explosion in self.explosions:
            shapes = explosion.get_shapes()
            for shape in shapes:
                shape.draw()
        
        # Draw labels
        self.instruction_label.draw()
        self.count_label.draw()
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse clicks to create explosions."""
        if button == pyglet.window.mouse.LEFT:
            self.create_explosion(x, y)
    
    def on_key_press(self, symbol, modifiers):
        """Handle key presses."""
        if symbol == pyglet.window.key.ESCAPE:
            self.close()
        elif symbol == pyglet.window.key.SPACE:
            # Create random explosion
            x = random.uniform(50, WIDTH - 50)
            y = random.uniform(50, HEIGHT - 50)
            self.create_explosion(x, y)
        elif symbol == pyglet.window.key.C:
            # Clear all explosions
            self.explosions.clear()

def main():
    """Run the particle explosion demo."""
    print("Starting Pyglet Particle Explosion Demo...")
    print("Controls:")
    print("  - Left click: Create explosion at mouse position")
    print("  - Space: Create random explosion")
    print("  - C: Clear all explosions")
    print("  - Escape: Exit")
    
    demo = ParticleExplosionDemo()
    pyglet.app.run()

if __name__ == '__main__':
    main()