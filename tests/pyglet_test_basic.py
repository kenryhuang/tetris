#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pyglet基础测试示例
测试pyglet的基本功能：创建窗口、绘制图形、处理事件
"""

import pyglet
from pyglet import shapes

# 创建窗口
window = pyglet.window.Window(800, 600, "Pyglet基础测试")

# 创建一个批处理对象用于高效渲染
batch = pyglet.graphics.Batch()

# 创建一些基本图形
circle = shapes.Circle(x=200, y=300, radius=50, color=(255, 0, 0), batch=batch)
rectangle = shapes.Rectangle(x=400, y=250, width=100, height=100, color=(0, 255, 0), batch=batch)
# 创建三角形 (使用正确的参数格式)
triangle = shapes.Triangle(600, 200, 550, 350, 650, 350, color=(0, 0, 255), batch=batch)

# 创建文本标签
label = pyglet.text.Label('Pyglet测试成功！',
                         font_name='Arial',
                         font_size=24,
                         x=window.width//2, y=window.height//2 + 150,
                         anchor_x='center', anchor_y='center')

# 窗口绘制事件
@window.event
def on_draw():
    window.clear()
    batch.draw()
    label.draw()

# 键盘事件处理
@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        window.close()
    elif symbol == pyglet.window.key.SPACE:
        # 改变图形颜色
        circle.color = (255, 255, 0)  # 黄色
        rectangle.color = (255, 0, 255)  # 紫色
        triangle.color = (0, 255, 255)  # 青色

# 鼠标点击事件
@window.event
def on_mouse_press(x, y, button, modifiers):
    print(f"鼠标点击位置: ({x}, {y})")
    # 在点击位置创建一个小圆点
    dot = shapes.Circle(x=x, y=y, radius=5, color=(255, 255, 255), batch=batch)

if __name__ == '__main__':
    print("Pyglet测试程序启动")
    print("操作说明:")
    print("- 按ESC键退出")
    print("- 按空格键改变图形颜色")
    print("- 点击鼠标在该位置创建白点")
    
    # 运行应用
    pyglet.app.run()