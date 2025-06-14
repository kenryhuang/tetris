#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RainbowWaveEffect Demo
彩虹波浪效果演示程序

这个demo用于测试和展示RainbowWaveEffect的视觉效果。
按空格键触发效果，按ESC退出。
"""

import pyglet
import time
import sys
import os
import random

# 添加项目路径到sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tetris_pyglet.effects import PygletEffectsManager, RainbowWaveEffect
from tetris_pyglet.constants import *

class RainbowWaveDemo(pyglet.window.Window):
    """RainbowWaveEffect演示窗口"""
    
    def __init__(self):
        super().__init__(width=WINDOW_WIDTH, height=WINDOW_HEIGHT, 
                         caption="RainbowWave Effect Demo - 彩虹波浪效果演示")
        
        # 设置OpenGL混合模式以支持透明度
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)
        
        # 创建效果管理器
        self.effects_manager = PygletEffectsManager()
        
        # 演示状态
        self.auto_demo = True
        self.last_auto_trigger = 0
        self.auto_interval = 2.5  # 自动触发间隔（秒）
        
        # 创建UI标签
        self.create_ui_labels()
        
        # 游戏板位置
        self.board_x = BORDER_WIDTH
        self.board_y = BORDER_WIDTH
        
        print("RainbowWave Effect Demo Started!")
        print("Controls:")
        print("  SPACE - 手动触发彩虹波浪效果")
        print("  A - 切换自动演示模式")
        print("  C - 清除所有效果")
        print("  ESC - 退出程序")
        print("  自动演示: 每2.5秒触发一次效果")
    
    def create_ui_labels(self):
        """创建UI标签"""
        self.title_label = pyglet.text.Label(
            'RainbowWave Effect Demo',
            font_name='Arial',
            font_size=24,
            x=self.width // 2, y=self.height - 40,
            anchor_x='center', anchor_y='center',
            color=COLORS['TEXT']
        )
        
        self.info_label = pyglet.text.Label(
            'SPACE: 触发效果 | A: 自动模式 | C: 清除 | ESC: 退出',
            font_name='Arial',
            font_size=14,
            x=self.width // 2, y=self.height - 70,
            anchor_x='center', anchor_y='center',
            color=COLORS['TEXT']
        )
        
        self.status_label = pyglet.text.Label(
            '准备就绪 - 按空格键触发效果',
            font_name='Arial',
            font_size=12,
            x=20, y=50,
            color=COLORS['ACCENT']
        )
        
        self.mode_label = pyglet.text.Label(
            '自动模式: 开启',
            font_name='Arial',
            font_size=12,
            x=20, y=30,
            color=COLORS['GREEN']
        )
    
    def trigger_rainbow_wave(self, line_y=None):
        """触发彩虹波浪效果
        
        Args:
            line_y: 指定行号，如果为None则随机选择
        """
        if line_y is None:
            line_y = random.randint(2, BOARD_HEIGHT - 3)
        
        # 创建RainbowWaveEffect
        effect = RainbowWaveEffect(line_y, self.board_x, self.board_y)
        self.effects_manager.line_effects.append(effect)
        
        self.status_label.text = f'彩虹波浪效果已触发 - 行 {line_y}'
        
        print(f"Rainbow wave effect triggered at line {line_y}")
    
    def on_key_press(self, symbol, modifiers):
        """处理按键事件"""
        if symbol == pyglet.window.key.SPACE:
            self.trigger_rainbow_wave()
        elif symbol == pyglet.window.key.A:
            self.auto_demo = not self.auto_demo
            mode_text = "开启" if self.auto_demo else "关闭"
            color = COLORS['GREEN'] if self.auto_demo else COLORS['RED']
            self.mode_label.text = f'自动模式: {mode_text}'
            self.mode_label.color = color
            print(f"Auto demo mode: {'ON' if self.auto_demo else 'OFF'}")
        elif symbol == pyglet.window.key.C:
            self.effects_manager.clear_all_effects()
            self.status_label.text = '所有效果已清除'
            print("All effects cleared")
        elif symbol == pyglet.window.key.ESCAPE:
            self.close()
    
    def draw_game_board(self):
        """绘制游戏板背景和网格"""
        # 绘制游戏板背景
        board_bg = pyglet.shapes.Rectangle(
            self.board_x, self.board_y,
            GAME_WIDTH, GAME_HEIGHT,
            color=COLORS['WHITE'][:3]
        )
        board_bg.draw()
        
        # 绘制游戏板边框
        border = pyglet.shapes.Rectangle(
            self.board_x - BORDER_WIDTH, self.board_y - BORDER_WIDTH,
            GAME_WIDTH + BORDER_WIDTH * 2, GAME_HEIGHT + BORDER_WIDTH * 2,
            color=COLORS['BORDER'][:3]
        )
        border.draw()
        
        # 绘制网格线
        grid_color = (220, 220, 220)
        
        # 垂直线
        for x in range(BOARD_WIDTH + 1):
            line_x = self.board_x + x * CELL_SIZE
            line = pyglet.shapes.Line(
                line_x, self.board_y,
                line_x, self.board_y + GAME_HEIGHT,
                color=grid_color
            )
            line.draw()
        
        # 水平线
        for y in range(BOARD_HEIGHT + 1):
            line_y = self.board_y + y * CELL_SIZE
            line = pyglet.shapes.Line(
                self.board_x, line_y,
                self.board_x + GAME_WIDTH, line_y,
                color=grid_color
            )
            line.draw()
        
        # 绘制行号标识
        for y in range(BOARD_HEIGHT):
            line_y = self.board_y + (BOARD_HEIGHT - 1 - y) * CELL_SIZE + CELL_SIZE // 2
            line_label = pyglet.text.Label(
                str(y),
                font_name='Arial',
                font_size=10,
                x=self.board_x - 20, y=line_y,
                anchor_x='center', anchor_y='center',
                color=(150, 150, 150, 255)
            )
            line_label.draw()
    
    def draw_sidebar(self):
        """绘制侧边栏信息"""
        sidebar_x = self.board_x + GAME_WIDTH + BORDER_WIDTH
        
        # 侧边栏背景
        sidebar_bg = pyglet.shapes.Rectangle(
            sidebar_x, 0,
            SIDEBAR_WIDTH, self.height,
            color=COLORS['SIDEBAR'][:3]
        )
        sidebar_bg.draw()
        
        # 效果统计信息
        active_effects = len(self.effects_manager.line_effects)
        stats_y = self.height - 120
        
        stats_title = pyglet.text.Label(
            '效果统计',
            font_name='Arial',
            font_size=16,
            x=sidebar_x + 20, y=stats_y,
            color=COLORS['TEXT']
        )
        stats_title.draw()
        
        active_label = pyglet.text.Label(
            f'活跃效果: {active_effects}',
            font_name='Arial',
            font_size=12,
            x=sidebar_x + 20, y=stats_y - 30,
            color=COLORS['ACCENT']
        )
        active_label.draw()
        
        # 效果详情
        if active_effects > 0:
            details_y = stats_y - 60
            for i, effect in enumerate(self.effects_manager.line_effects):
                if i >= 5:  # 最多显示5个效果
                    break
                progress_percent = int(effect.progress * 100)
                detail_text = f'行{effect.line_y}: {progress_percent}%'
                detail_label = pyglet.text.Label(
                    detail_text,
                    font_name='Arial',
                    font_size=10,
                    x=sidebar_x + 30, y=details_y - i * 20,
                    color=COLORS['TEXT']
                )
                detail_label.draw()
        
        # 演示说明
        demo_y = 200
        demo_title = pyglet.text.Label(
            '演示说明',
            font_name='Arial',
            font_size=16,
            x=sidebar_x + 20, y=demo_y,
            color=COLORS['TEXT']
        )
        demo_title.draw()
        
        demo_texts = [
            '彩虹波浪效果特点:',
            '• 动态彩虹色彩变化',
            '• 波浪形状动画',
            '• 闪电效果',
            '• 粒子闪烁效果',
            '• 渐变透明度',
            '',
            '效果持续时间: 6秒',
            '波浪频率: 可调节',
            '颜色: 7色彩虹渐变'
        ]
        
        for i, text in enumerate(demo_texts):
            text_label = pyglet.text.Label(
                text,
                font_name='Arial',
                font_size=10,
                x=sidebar_x + 20, y=demo_y - 30 - i * 18,
                color=COLORS['TEXT']
            )
            text_label.draw()
    
    def on_draw(self):
        """绘制窗口内容"""
        self.clear()
        
        # 设置背景色
        pyglet.gl.glClearColor(*[c/255.0 for c in COLORS['BACKGROUND']])
        
        # 绘制游戏板
        self.draw_game_board()
        
        # 绘制侧边栏
        self.draw_sidebar()
        
        # 绘制效果
        shapes = self.effects_manager.draw(self.effects_manager.batch, self.effects_manager.group)
        
        # 绘制batch中的所有内容
        self.effects_manager.batch.draw()
        
        # 绘制UI标签
        self.title_label.draw()
        self.info_label.draw()
        self.status_label.draw()
        self.mode_label.draw()
    
    def update(self, dt):
        """更新游戏状态"""
        # 更新效果
        self.effects_manager.update(dt)
        
        # 自动演示模式
        if self.auto_demo:
            current_time = time.time()
            if current_time - self.last_auto_trigger > self.auto_interval:
                self.trigger_rainbow_wave()
                self.last_auto_trigger = current_time
        
        # 更新状态显示
        if not self.effects_manager.has_active_effects() and not self.auto_demo:
            self.status_label.text = '准备就绪 - 按空格键触发效果'

def main():
    """主函数"""
    print("Starting RainbowWave Effect Demo...")
    print("Loading pyglet and effects...")
    
    try:
        # 创建演示窗口
        demo = RainbowWaveDemo()
        
        # 设置更新频率
        pyglet.clock.schedule_interval(demo.update, 1/60.0)
        
        print("Demo window created successfully!")
        print("Starting event loop...")
        
        # 启动事件循环
        pyglet.app.run()
        
    except Exception as e:
        print(f"Error running demo: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    print("Demo finished.")
    return 0

if __name__ == '__main__':
    sys.exit(main())