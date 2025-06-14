#!/usr/bin/env python3
"""
测试特效在游戏环境中的工作情况
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pyglet
import time
from src.tetris_pyglet.pyglet_game import PygletTetrisGame
from src.tetris_pyglet.effects import PygletEffectsManager
from src.tetris_pyglet.renderer import PygletRenderer

class EffectsTestGame(PygletTetrisGame):
    """测试特效的游戏类"""
    
    def __init__(self):
        super().__init__()
        self.test_timer = 0.0
        self.test_triggered = False
        self.game_start_time = time.time()
        
    def update(self, dt):
        super().update(dt)
        
        # 3秒后自动触发特效测试
        self.test_timer += dt
        if self.test_timer > 3.0 and not self.test_triggered:
            self.test_triggered = True
            print("\n=== 开始特效测试 ===")
            
            # 直接添加特效
            print("添加特效到第5行...")
            self.effects_manager.add_line_clear_effect(5)
            print(f"特效管理器现在有 {len(self.effects_manager.line_effects)} 个特效")
            
            # 检查特效状态
            if self.effects_manager.line_effects:
                effect = self.effects_manager.line_effects[0]
                print(f"特效活跃状态: {effect.active}")
                print(f"特效进度: {effect.progress}")
                print(f"特效持续时间: {effect.duration}")
            
    def draw(self):
        """重写draw方法以添加更多调试信息"""
        # 清屏
        self.renderer.clear()
        
        # 绘制游戏元素
        self.renderer.draw_board(self.board)
        
        if self.current_piece:
            self.renderer.draw_piece(self.current_piece)
        
        if self.next_piece:
            # 在侧边栏绘制预览方块
            preview_x = 500  # 侧边栏位置
            preview_y = 400  # 预览位置
            self.renderer.draw_preview_piece(self.next_piece, preview_x, preview_y)
        
        # 绘制UI
        game_time = int(time.time() - self.game_start_time) if hasattr(self, 'game_start_time') else 0
        self.renderer.draw_ui(self.score, self.level, self.lines_cleared, self.next_piece, 
                             self.current_piece, game_time)
        
        if self.game_over:
            self.renderer.draw_game_over()
        
        if self.paused:
            self.renderer.draw_pause_overlay()
        
        # 绘制特效 - 添加详细调试信息
        active_effects = len(self.effects_manager.line_effects)
        if active_effects > 0:
            print(f"正在绘制 {active_effects} 个活跃特效")
            for i, effect in enumerate(self.effects_manager.line_effects):
                print(f"  特效 {i}: 活跃={effect.active}, 进度={effect.progress:.2f}")
        
        # 调用特效绘制
        shapes = self.effects_manager.draw(self.renderer.effect_batch, self.renderer.effect_group)
        print(f"特效绘制返回了 {len(shapes)} 个形状")
        
        # 绘制所有批次
        self.renderer.draw()

def main():
    """主函数"""
    print("启动特效测试游戏...")
    
    # 创建游戏实例
    game = EffectsTestGame()
    
    # 设置窗口事件处理
    window = game.renderer.get_window()
    
    @window.event
    def on_draw():
        game.draw()
    
    @window.event
    def on_key_press(symbol, modifiers):
        game.on_key_press(symbol, modifiers)
    
    @window.event
    def on_key_release(symbol, modifiers):
        game.on_key_release(symbol, modifiers)
    
    # 设置更新调度
    def update(dt):
        game.update(dt)
    
    pyglet.clock.schedule_interval(update, 1/60.0)
    
    print("游戏启动成功，3秒后将自动触发特效测试")
    print("按ESC退出游戏")
    
    # 运行游戏循环
    pyglet.app.run()

if __name__ == "__main__":
    main()