#!/usr/bin/env python3
"""
ExplosionEffect Demo

This demo showcases the ExplosionEffect class with visual representation.
Click anywhere on the window to create explosion effects.

Controls:
- Left Click: Create explosion at mouse position
- Right Click: Create high-intensity explosion
- Space: Create multiple random explosions
- ESC: Exit demo
"""

import sys
import os
import random
import math

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pyglet
from pyglet import shapes
from pyglet.window import key, mouse

from tetris_pyglet.effects import ExplosionEffect
from tetris_pyglet.constants import COLORS, PIECE_COLORS

class ExplosionDemo:
    def __init__(self):
        # Create window with explicit visibility
        self.window = pyglet.window.Window(
            width=800, 
            height=600, 
            caption="ExplosionEffect Demo - Click to create explosions!",
            visible=True
        )
        print(f"Window created: {self.window.width}x{self.window.height}")
        
        # List to store active explosions
        self.explosions = []
        
        # Create batch and group for rendering
        self.batch = pyglet.graphics.Batch()
        self.group = pyglet.graphics.Group()
        
        # Background color (dark)
        pyglet.gl.glClearColor(0.1, 0.1, 0.15, 1.0)
        
        # Create some background grid for visual reference
        self.grid_lines = []
        self._create_background_grid()
        
        # Instructions text
        self.instructions = pyglet.text.Label(
            'Left Click: Normal Explosion | Right Click: High Intensity | Space: Random Explosions | ESC: Exit',
            font_name='Arial',
            font_size=12,
            x=10, y=self.window.height - 30,
            color=(255, 255, 255, 200)
        )
        
        # FPS display
        self.fps_display = pyglet.window.FPSDisplay(self.window)
        
        # Event handlers
        self.window.on_draw = self.on_draw
        self.window.on_mouse_press = self.on_mouse_press
        self.window.on_key_press = self.on_key_press
        
        # Schedule update
        pyglet.clock.schedule_interval(self.update, 1/60.0)  # 60 FPS
        
    def _create_background_grid(self):
        """Create a subtle background grid for visual reference."""
        grid_size = 50
        grid_color = (40, 40, 60, 100)
        
        # Vertical lines
        for x in range(0, self.window.width, grid_size):
            line = shapes.Line(
                x, 0, x, self.window.height,
                color=grid_color
            )
            self.grid_lines.append(line)
            
        # Horizontal lines
        for y in range(0, self.window.height, grid_size):
            line = shapes.Line(
                0, y, self.window.width, y,
                color=grid_color
            )
            self.grid_lines.append(line)
    
    def on_draw(self):
        """Draw everything."""
        self.window.clear()
        
        # Draw background grid
        for line in self.grid_lines:
            line.draw()
        
        # Draw all active explosions directly (without batch)
        total_particles = 0
        for explosion in self.explosions:
            for particle in explosion.particles:
                if particle.life > 0 and particle.size > 0:
                    # Get current color
                    current_color = particle.get_current_color()
                    
                    # Draw main particle directly
                    main_circle = pyglet.shapes.Circle(
                        particle.x, particle.y, particle.size,
                        color=current_color[:3]
                    )
                    main_circle.opacity = current_color[3]
                    main_circle.draw()
                    
                    # Draw glow effect
                    glow_size = particle.size * 1.5
                    glow_alpha = int(current_color[3] * 0.3)
                    if glow_alpha > 0:
                        glow_circle = pyglet.shapes.Circle(
                            particle.x, particle.y, glow_size,
                            color=current_color[:3]
                        )
                        glow_circle.opacity = glow_alpha
                        glow_circle.draw()
                    
                    total_particles += 1
        
        # Draw UI
        self.instructions.draw()
        self.fps_display.draw()
        
        # Draw explosion count and particle info
        count_label = pyglet.text.Label(
            f'Active Explosions: {len(self.explosions)} | Particles: {total_particles}',
            font_name='Arial',
            font_size=12,
            x=10, y=50,
            color=(255, 255, 255, 200)
        )
        count_label.draw()
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Handle mouse clicks to create explosions."""
        print(f"Mouse clicked at ({x}, {y})")
        
        if button == mouse.LEFT:
            # Normal explosion
            color = random.choice(list(PIECE_COLORS.values()))
            explosion = ExplosionEffect(x, y, color=color, intensity=1.0)
            self.explosions.append(explosion)
            print(f"Created normal explosion at ({x}, {y}) with {len(explosion.particles)} particles")
            
        elif button == mouse.RIGHT:
            # High intensity explosion
            color = random.choice(list(PIECE_COLORS.values()))
            explosion = ExplosionEffect(x, y, color=color, intensity=2.5)
            self.explosions.append(explosion)
            print(f"Created high intensity explosion at ({x}, {y}) with {len(explosion.particles)} particles")
    
    def on_key_press(self, symbol, modifiers):
        """Handle key presses."""
        if symbol == key.ESCAPE:
            pyglet.app.exit()
            
        elif symbol == key.SPACE:
            # Create multiple random explosions
            for _ in range(5):
                x = random.randint(50, self.window.width - 50)
                y = random.randint(50, self.window.height - 50)
                color = random.choice(list(PIECE_COLORS.values()))
                intensity = random.uniform(0.5, 2.0)
                explosion = ExplosionEffect(x, y, color=color, intensity=intensity)
                self.explosions.append(explosion)
                
        elif symbol == key.C:
            # Clear all explosions
            self.explosions.clear()
            
        elif symbol == key.R:
            # Create rainbow explosion
            x = self.window.width // 2
            y = self.window.height // 2
            colors = list(PIECE_COLORS.values())
            for i, color in enumerate(colors):
                angle = (i / len(colors)) * 2 * math.pi
                offset_x = math.cos(angle) * 100
                offset_y = math.sin(angle) * 100
                explosion = ExplosionEffect(
                    x + offset_x, y + offset_y, 
                    color=color, intensity=1.5
                )
                self.explosions.append(explosion)
    
    def update(self, dt):
        """Update all explosions and remove finished ones."""
        # Update all explosions
        for explosion in self.explosions[:]:
            old_particle_count = len(explosion.particles)
            explosion.update(dt)
            new_particle_count = len(explosion.particles)
            
            # Debug: Print particle info for first few frames
            if old_particle_count > 0 and len(self.explosions) <= 3:
                print(f"Explosion at ({explosion.x}, {explosion.y}): {old_particle_count} -> {new_particle_count} particles")
                if explosion.particles:
                    first_particle = explosion.particles[0]
                    print(f"  First particle: pos=({first_particle.x:.1f}, {first_particle.y:.1f}), life={first_particle.life:.2f}, size={first_particle.size:.1f}")
            
            # Remove finished explosions
            if not explosion.active:
                print(f"Removing finished explosion at ({explosion.x}, {explosion.y})")
                self.explosions.remove(explosion)
    
    def run(self):
        """Start the demo."""
        print("ExplosionEffect Demo Started!")
        print("Controls:")
        print("  Left Click: Create normal explosion")
        print("  Right Click: Create high-intensity explosion")
        print("  Space: Create multiple random explosions")
        print("  R: Create rainbow explosion pattern")
        print("  C: Clear all explosions")
        print("  ESC: Exit")
        print()
        
        try:
            # Create initial welcome explosion
            welcome_explosion = ExplosionEffect(
                self.window.width // 2, 
                self.window.height // 2,
                color=PIECE_COLORS['I'],  # Cyan
                intensity=2.0
            )
            self.explosions.append(welcome_explosion)
            print(f"Created welcome explosion with {len(welcome_explosion.particles)} particles")
            
            # Make sure window is visible
            self.window.set_visible(True)
            self.window.activate()
            print("Starting pyglet app...")
            
            pyglet.app.run()
            print("Pyglet app finished.")
        except Exception as e:
            print(f"Error running demo: {e}")
            import traceback
            traceback.print_exc()

def main():
    """Main entry point."""
    try:
        demo = ExplosionDemo()
        demo.run()
    except Exception as e:
        print(f"Error creating demo: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())