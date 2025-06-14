#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pyglet
from pyglet import shapes
from tetris_pyglet.effects import RainbowWaveEffect
from tetris_pyglet.constants import (
    BOARD_HEIGHT, CELL_SIZE, BORDER_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT,
    BOARD_WIDTH, GAME_WIDTH, GAME_HEIGHT
)

class EffectVisualizationTest:
    def __init__(self):
        self.window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, caption="Effect Position Test")
        self.batch = pyglet.graphics.Batch()
        self.group = pyglet.graphics.Group()
        
        # Board position (same as in real game)
        self.board_x = BORDER_WIDTH
        self.board_y = BORDER_WIDTH
        
        # Create effects for different lines
        self.effects = []
        for line_y in [0, 5, 10, 15, 19]:  # Test various lines
            effect = RainbowWaveEffect(line_y, self.board_x, self.board_y)
            self.effects.append((line_y, effect))
        
        # Create visual guides
        self.create_visual_guides()
        
        # Event handlers
        @self.window.event
        def on_draw():
            self.window.clear()
            
            # Draw visual guides
            self.batch.draw()
            
            # Draw effects
            for line_y, effect in self.effects:
                effect_shapes = effect.draw(self.batch, self.group)
                print(f"Line {line_y}: Drew {len(effect_shapes)} shapes at pixel_y={effect.pixel_y}")
        
        @self.window.event
        def on_key_press(symbol, modifiers):
            if symbol == pyglet.window.key.ESCAPE:
                self.window.close()
    
    def create_visual_guides(self):
        """Create visual guides to show board boundaries and coordinate system."""
        # Draw board outline
        board_outline = shapes.Rectangle(
            self.board_x, self.board_y, GAME_WIDTH, GAME_HEIGHT,
            color=(200, 200, 200), batch=self.batch, group=self.group
        )
        board_outline.opacity = 100
        
        # Draw horizontal lines for each row
        for y in range(BOARD_HEIGHT + 1):
            line_y = self.board_y + y * CELL_SIZE
            line = shapes.Line(
                self.board_x, line_y,
                self.board_x + GAME_WIDTH, line_y,
                color=(150, 150, 150), batch=self.batch, group=self.group
            )
        
        # Draw coordinate labels
        self.labels = []
        for line_y in [0, 5, 10, 15, 19]:
            pixel_y = self.board_y + (BOARD_HEIGHT - 1 - line_y) * CELL_SIZE
            label = pyglet.text.Label(
                f'Line {line_y}',
                font_name='Arial', font_size=12,
                x=self.board_x + GAME_WIDTH + 10, y=pixel_y,
                anchor_x='left', anchor_y='center'
            )
            self.labels.append(label)
        
        # Window info label
        self.info_label = pyglet.text.Label(
            f'Window: {WINDOW_WIDTH}x{WINDOW_HEIGHT}, Board: {self.board_x},{self.board_y} to {self.board_x+GAME_WIDTH},{self.board_y+GAME_HEIGHT}',
            font_name='Arial', font_size=10,
            x=10, y=WINDOW_HEIGHT - 20,
            anchor_x='left', anchor_y='top'
        )
    
    def update(self, dt):
        # Update effects
        for line_y, effect in self.effects:
            effect.update(dt)
    
    def run(self):
        # Schedule update
        pyglet.clock.schedule_interval(self.update, 1/60.0)
        
        # Draw labels separately (not in batch)
        @self.window.event
        def on_draw():
            self.window.clear()
            
            # Draw visual guides
            self.batch.draw()
            
            # Draw effects
            effect_batch = pyglet.graphics.Batch()
            effect_group = pyglet.graphics.Group()
            
            for line_y, effect in self.effects:
                effect_shapes = effect.draw(effect_batch, effect_group)
            
            effect_batch.draw()
            
            # Draw labels
            for label in self.labels:
                label.draw()
            self.info_label.draw()
        
        print("Starting effect visualization test...")
        print("Press ESC to exit")
        print(f"Board position: ({self.board_x}, {self.board_y})")
        print(f"Window size: {WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        
        pyglet.app.run()

if __name__ == '__main__':
    test = EffectVisualizationTest()
    test.run()