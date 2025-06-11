#!/usr/bin/env python3
"""
LineExplosionEffect 独立测试脚本
用于测试和验证行消除爆炸效果的表现
"""

import pyglet
import time
import sys
import os

# 添加项目路径到sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from tetris_pyglet.effects import PygletEffectsManager, LineExplosionEffect
from tetris_pyglet.constants import *

class LineExplosionTestWindow(pyglet.window.Window):
    """LineExplosionEffect测试窗口"""
    
    def __init__(self):
        super().__init__(width=800, height=600, caption="LineExplosion Effect Test")
        
        # 设置OpenGL混合模式以支持透明度
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        
        # 创建批次和组
        self.batch = pyglet.graphics.Batch()
        self.group = pyglet.graphics.Group()
        
        # 创建效果管理器
        self.effects_manager = PygletEffectsManager()
        
        # 测试状态
        self.test_active = False
        self.last_test_time = 0
        self.test_interval = 3.0  # 每3秒触发一次测试
        
        # 创建标签显示信息
        self.info_label = pyglet.text.Label(
            'Press SPACE to trigger LineExplosion effect\nPress ESC to exit',
            font_name='Arial',
            font_size=16,
            x=10, y=self.height - 30,
            multiline=True,
            width=self.width - 20
        )
        
        self.status_label = pyglet.text.Label(
            'Ready to test...',
            font_name='Arial',
            font_size=14,
            x=10, y=50,
            color=(255, 255, 255, 255)
        )
        
        print("LineExplosion Effect Test Window Created")
        print("Controls:")
        print("  SPACE - Trigger LineExplosion effect")
        print("  ESC - Exit")
        print("  Auto-trigger every 3 seconds")
    
    def trigger_line_explosion(self, line_y=10):
        """触发行爆炸效果"""
        print(f"Triggering LineExplosion effect at line {line_y}")
        
        # 计算屏幕中央位置
        center_x = self.width // 2
        center_y = self.height // 2
        
        # 创建LineExplosionEffect
        # 使用屏幕坐标，确保Y坐标为正数
        board_x = center_x - (BOARD_WIDTH * CELL_SIZE) // 2
        board_y = center_y + (BOARD_HEIGHT // 2 - line_y) * CELL_SIZE
        
        self.effects_manager.add_line_clear_effect_at_position(board_x, board_y)
        
        self.status_label.text = f"LineExplosion triggered at ({board_x}, {board_y})"
        self.test_active = True
    
    def on_key_press(self, symbol, modifiers):
        """处理按键事件"""
        if symbol == pyglet.window.key.SPACE:
            # 随机选择一个行位置
            import random
            line_y = random.randint(5, 15)
            self.trigger_line_explosion(line_y)
        elif symbol == pyglet.window.key.ESCAPE:
            self.close()
    
    def on_draw(self):
        """绘制窗口内容"""
        self.clear()
        
        # 绘制背景
        pyglet.shapes.Rectangle(
            0, 0, self.width, self.height,
            color=(30, 30, 30)
        ).draw()
        
        # 绘制游戏区域边框
        center_x = self.width // 2
        center_y = self.height // 2
        board_width = BOARD_WIDTH * CELL_SIZE
        board_height = BOARD_HEIGHT * CELL_SIZE
        
        board_x = center_x - board_width // 2
        board_y = center_y - board_height // 2
        
        # 绘制边框
        pyglet.shapes.Rectangle(
            board_x - 2, board_y - 2,
            board_width + 4, board_height + 4,
            color=(100, 100, 100)
        ).draw()
        
        # 绘制游戏区域
        pyglet.shapes.Rectangle(
            board_x, board_y,
            board_width, board_height,
            color=(50, 50, 50)
        ).draw()
        
        # 绘制网格线
        for x in range(BOARD_WIDTH + 1):
            line_x = board_x + x * CELL_SIZE
            pyglet.shapes.Line(
                line_x, board_y,
                line_x, board_y + board_height,
                color=(70, 70, 70)
            ).draw()
        
        for y in range(BOARD_HEIGHT + 1):
            line_y = board_y + y * CELL_SIZE
            pyglet.shapes.Line(
                board_x, line_y,
                board_x + board_width, line_y,
                color=(70, 70, 70)
            ).draw()
        
        # 绘制效果 - 先调用draw方法将效果添加到batch，再绘制batch
        self.effects_manager.draw(self.effects_manager.batch, self.effects_manager.group)
        self.effects_manager.batch.draw()
        
        # 绘制UI
        self.info_label.draw()
        self.status_label.draw()
        
        # 显示活跃效果数量
        effect_count = len(self.effects_manager.line_effects) + len(self.effects_manager.explosion_effects)
        if effect_count > 0:
            count_label = pyglet.text.Label(
                f'Active effects: {effect_count}',
                font_name='Arial',
                font_size=12,
                x=self.width - 150, y=50,
                color=(255, 255, 0, 255)
            )
            count_label.draw()
    
    def update(self, dt):
        """更新游戏状态"""
        # 更新效果
        self.effects_manager.update(dt)
        
        # 自动触发测试
        current_time = time.time()
        if current_time - self.last_test_time > self.test_interval:
            if not self.test_active or len(self.effects_manager.line_effects) == 0:
                import random
                line_y = random.randint(5, 15)
                self.trigger_line_explosion(line_y)
                self.last_test_time = current_time
        
        # 检查效果是否完成
        if self.test_active and len(self.effects_manager.line_effects) == 0:
            self.test_active = False
            self.status_label.text = "Effect completed. Ready for next test..."

# 为PygletEffectsManager添加位置指定的方法
def add_line_clear_effect_at_position(self, board_x, board_y):
    """在指定位置添加行清除效果"""
    line_effect = LineExplosionEffect(0, board_x, board_y)  # line_y=0, 使用指定的board坐标
    self.line_effects.append(line_effect)
    print(f"Added LineExplosionEffect at position ({board_x}, {board_y})")

# 动态添加方法到PygletEffectsManager
PygletEffectsManager.add_line_clear_effect_at_position = add_line_clear_effect_at_position

def main():
    """主函数"""
    print("Starting LineExplosion Effect Test...")
    
    # 创建窗口
    window = LineExplosionTestWindow()
    
    # 设置更新频率
    pyglet.clock.schedule_interval(window.update, 1/60.0)
    
    # 启动事件循环
    pyglet.app.run()

if __name__ == '__main__':
    main()