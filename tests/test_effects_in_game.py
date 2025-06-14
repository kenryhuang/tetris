#!/usr/bin/env python3
"""
测试特效在游戏环境中的工作情况
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pyglet
import time
from tetris_pyglet.pyglet_game import PygletTetrisGame
from tetris_pyglet.effects import PygletEffectsManager
from tetris_pyglet.renderer import PygletRenderer

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
        self.renderer.clear()
        self.renderer.clear_effect_batch()

        # Draw board and pieces first
        self.renderer.draw_board(self.board)
        if self.ghost_piece and not self.pending_line_clear:
            self.renderer.draw_piece(self.ghost_piece, ghost=True)
        if self.current_piece and not self.pending_line_clear:
            self.renderer.draw_piece(self.current_piece)

        # Draw effects ON TOP of board and pieces
        self.effects_manager.draw(self.renderer.effect_batch, self.renderer.effect_group)

        # Draw UI
        game_time = int(time.time() - self.game_start_time) if hasattr(self, 'game_start_time') else 0
        self.renderer.draw_ui(self.score, self.level, self.lines_cleared, self.next_piece, 
                             self.current_piece, game_time)

        # Draw overlays
        if self.game_over:
            self.renderer.draw_game_over(self.score)
        if self.paused and not self.game_over:
            self.renderer.draw_pause_screen()

        # Render all batches
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