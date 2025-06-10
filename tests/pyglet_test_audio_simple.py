#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pyglet简单音频测试示例
测试pyglet的基本音频功能
"""

import pyglet
import math
import struct
from pyglet import shapes

# 创建窗口
window = pyglet.window.Window(600, 400, "Pyglet音频测试")

# 创建批处理对象
batch = pyglet.graphics.Batch()

def generate_beep(frequency=440, duration=0.2, sample_rate=22050):
    """
    生成简单的蜂鸣音
    """
    frames = int(duration * sample_rate)
    arr = []
    for i in range(frames):
        # 生成正弦波
        value = 0.3 * math.sin(2 * math.pi * frequency * i / sample_rate)
        # 添加衰减效果
        decay = 1 - (i / frames)
        value *= decay
        # 转换为16位整数
        packed_value = struct.pack('<h', int(value * 32767))
        arr.append(packed_value)
    
    return b''.join(arr)

# 创建音频源
try:
    beep_data = generate_beep(440, 0.3)  # A4音符
    audio_source = pyglet.media.StaticSource(
        pyglet.media.AudioData(
            beep_data,
            channels=1,
            sample_size=16,
            sample_rate=22050
        )
    )
    audio_available = True
    print("音频源创建成功")
except Exception as e:
    print(f"音频源创建失败: {e}")
    audio_available = False

# 创建可视化元素
play_button = shapes.Rectangle(x=250, y=200, width=100, height=50, color=(0, 255, 0), batch=batch)
status_circle = shapes.Circle(x=300, y=150, radius=20, color=(255, 0, 0), batch=batch)

# 播放状态
is_playing = False
player = None

def play_beep():
    global is_playing, player
    if audio_available and not is_playing:
        try:
            player = pyglet.media.Player()
            player.queue(audio_source)
            player.play()
            is_playing = True
            status_circle.color = (0, 255, 0)  # 绿色表示播放
            print("播放音频")
            
            # 0.5秒后重置状态
            def reset_status(dt):
                global is_playing
                is_playing = False
                status_circle.color = (255, 0, 0)  # 红色表示停止
            
            pyglet.clock.schedule_once(reset_status, 0.5)
            
        except Exception as e:
            print(f"播放音频时出错: {e}")
            is_playing = False
            status_circle.color = (255, 255, 0)  # 黄色表示错误

@window.event
def on_draw():
    window.clear()
    batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        window.close()
    elif symbol == pyglet.window.key.SPACE:
        play_beep()

@window.event
def on_mouse_press(x, y, button, modifiers):
    # 检查是否点击了播放按钮
    if 250 <= x <= 350 and 200 <= y <= 250:
        play_beep()
        play_button.color = (255, 255, 0)  # 黄色高亮
        
        # 0.2秒后恢复颜色
        def reset_button_color(dt):
            play_button.color = (0, 255, 0)
        
        pyglet.clock.schedule_once(reset_button_color, 0.2)

if __name__ == '__main__':
    print("Pyglet简单音频测试程序启动")
    print("操作说明:")
    print("- 按ESC键退出")
    print("- 按空格键或点击绿色按钮播放音频")
    print("- 红色圆圈表示停止，绿色表示播放")
    
    if not audio_available:
        print("警告: 音频功能不可用")
    
    try:
        pyglet.app.run()
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()