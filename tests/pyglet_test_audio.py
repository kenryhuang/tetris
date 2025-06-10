#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pyglet音频测试示例
测试pyglet的音频播放功能（使用程序生成的音频）
"""

import pyglet
import math
import struct
from pyglet import shapes

# 创建窗口
window = pyglet.window.Window(600, 400, "Pyglet音频测试")

# 创建批处理对象
batch = pyglet.graphics.Batch()

def generate_tone(frequency, duration, sample_rate=22050, amplitude=0.5):
    """
    生成指定频率和持续时间的音调
    """
    frames = int(duration * sample_rate)
    arr = []
    for i in range(frames):
        # 生成正弦波
        value = amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)
        # 转换为16位整数
        packed_value = struct.pack('<h', int(value * 32767))
        arr.append(packed_value)
    
    return b''.join(arr)

# 生成不同频率的音调
tones = {
    'C': generate_tone(261.63, 0.5),  # C4
    'D': generate_tone(293.66, 0.5),  # D4
    'E': generate_tone(329.63, 0.5),  # E4
    'F': generate_tone(349.23, 0.5),  # F4
    'G': generate_tone(392.00, 0.5),  # G4
    'A': generate_tone(440.00, 0.5),  # A4
    'B': generate_tone(493.88, 0.5),  # B4
}

# 创建音频源
audio_sources = {}
for note, tone_data in tones.items():
    try:
        # 创建音频源
        audio_source = pyglet.media.StaticSource(
            pyglet.media.AudioData(
                tone_data,
                channels=1,
                sample_size=16,
                sample_rate=22050
            )
        )
        audio_sources[note] = audio_source
    except Exception as e:
        print(f"创建音频源 {note} 时出错: {e}")

# 创建钢琴键盘界面
keys = []
key_labels = []
key_width = 80
key_height = 200
start_x = 50
start_y = 100

key_colors = {
    'C': (255, 255, 255),
    'D': (255, 255, 255),
    'E': (255, 255, 255),
    'F': (255, 255, 255),
    'G': (255, 255, 255),
    'A': (255, 255, 255),
    'B': (255, 255, 255),
}

for i, note in enumerate(['C', 'D', 'E', 'F', 'G', 'A', 'B']):
    x = start_x + i * key_width
    
    # 创建键盘按键
    key_rect = shapes.Rectangle(
        x=x, y=start_y, 
        width=key_width-2, height=key_height,
        color=key_colors[note], 
        batch=batch
    )
    
    # 创建按键边框
    key_border = shapes.Rectangle(
        x=x, y=start_y, 
        width=key_width-2, height=key_height,
        color=(0, 0, 0), 
        batch=batch
    )
    key_border.opacity = 0  # 透明，只显示边框
    
    keys.append((key_rect, note, x, start_y, key_width-2, key_height))
    
    # 创建音符标签
    label = pyglet.text.Label(
        note,
        font_name='Arial',
        font_size=24,
        x=x + key_width//2 - 1,
        y=start_y + 20,
        anchor_x='center',
        anchor_y='center',
        color=(0, 0, 0, 255)
    )
    key_labels.append(label)

# 标题和说明
title_label = pyglet.text.Label(
    'Pyglet音频测试 - 虚拟钢琴',
    font_name='Arial',
    font_size=20,
    x=window.width//2,
    y=window.height - 50,
    anchor_x='center',
    anchor_y='center'
)

instruction_label = pyglet.text.Label(
    '点击琴键或按对应字母键播放音符 (C D E F G A B)',
    font_name='Arial',
    font_size=14,
    x=window.width//2,
    y=50,
    anchor_x='center',
    anchor_y='center'
)

# 当前播放的音符显示
current_note_label = pyglet.text.Label(
    '',
    font_name='Arial',
    font_size=16,
    x=window.width//2,
    y=window.height - 100,
    anchor_x='center',
    anchor_y='center',
    color=(255, 0, 0, 255)
)

def play_note(note):
    """播放指定音符"""
    if note in audio_sources:
        try:
            player = pyglet.media.Player()
            player.queue(audio_sources[note])
            player.play()
            current_note_label.text = f'正在播放: {note}'
            print(f"播放音符: {note}")
            
            # 高亮按键
            for key_rect, key_note, x, y, w, h in keys:
                if key_note == note:
                    key_rect.color = (255, 255, 0)  # 黄色高亮
                    # 0.1秒后恢复原色
                    pyglet.clock.schedule_once(lambda dt, kr=key_rect: setattr(kr, 'color', (255, 255, 255)), 0.1)
                    break
                    
        except Exception as e:
            print(f"播放音符 {note} 时出错: {e}")
            current_note_label.text = f'播放 {note} 失败'
    else:
        print(f"音符 {note} 不可用")
        current_note_label.text = f'音符 {note} 不可用'

def get_clicked_key(x, y):
    """获取点击的琴键"""
    for key_rect, note, kx, ky, kw, kh in keys:
        if kx <= x <= kx + kw and ky <= y <= ky + kh:
            return note
    return None

@window.event
def on_draw():
    window.clear()
    batch.draw()
    title_label.draw()
    instruction_label.draw()
    current_note_label.draw()
    
    for label in key_labels:
        label.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        window.close()
    else:
        # 键盘映射
        key_map = {
            pyglet.window.key.C: 'C',
            pyglet.window.key.D: 'D',
            pyglet.window.key.E: 'E',
            pyglet.window.key.F: 'F',
            pyglet.window.key.G: 'G',
            pyglet.window.key.A: 'A',
            pyglet.window.key.B: 'B',
        }
        
        if symbol in key_map:
            play_note(key_map[symbol])

@window.event
def on_mouse_press(x, y, button, modifiers):
    clicked_note = get_clicked_key(x, y)
    if clicked_note:
        play_note(clicked_note)

if __name__ == '__main__':
    print("Pyglet音频测试程序启动")
    print("操作说明:")
    print("- 按ESC键退出")
    print("- 点击琴键播放音符")
    print("- 按键盘字母键 C D E F G A B 播放对应音符")
    print("- 程序使用数学生成的音调")
    
    if not audio_sources:
        print("警告: 没有可用的音频源")
    else:
        print(f"成功创建了 {len(audio_sources)} 个音频源")
    
    pyglet.app.run()