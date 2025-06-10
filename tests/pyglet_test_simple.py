#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pyglet简单测试示例
最基础的pyglet功能测试，避免复杂的字体渲染
"""

import pyglet
from pyglet import shapes

# 创建窗口
window = pyglet.window.Window(800, 600, "Pyglet简单测试")

# 创建批处理对象
batch = pyglet.graphics.Batch()

# 创建基本图形
circle = shapes.Circle(x=200, y=300, radius=50, color=(255, 0, 0), batch=batch)
rectangle = shapes.Rectangle(x=400, y=250, width=100, height=100, color=(0, 255, 0), batch=batch)
line = shapes.Line(100, 100, 700, 500, width=5, color=(255, 255, 0), batch=batch)

# 颜色变化变量
color_time = 0

def update(dt):
    global color_time
    color_time += dt
    
    # 让圆形颜色变化
    import math
    red = int(128 + 127 * math.sin(color_time))
    green = int(128 + 127 * math.sin(color_time + 2))
    blue = int(128 + 127 * math.sin(color_time + 4))
    circle.color = (red, green, blue)

# 注册更新函数
pyglet.clock.schedule_interval(update, 1/60.0)

@window.event
def on_draw():
    window.clear()
    batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        window.close()
        print("程序退出")
    elif symbol == pyglet.window.key.SPACE:
        # 改变矩形颜色
        import random
        rectangle.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        print("矩形颜色已改变")

@window.event
def on_mouse_press(x, y, button, modifiers):
    # 在鼠标位置创建新圆形
    import random
    new_circle = shapes.Circle(
        x=x, y=y, radius=20, 
        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), 
        batch=batch
    )
    print(f"在 ({x}, {y}) 创建了新圆形")

if __name__ == '__main__':
    print("Pyglet简单测试程序启动")
    print("操作说明:")
    print("- 按ESC键退出")
    print("- 按空格键改变矩形颜色")
    print("- 点击鼠标创建新圆形")
    print("- 观察圆形的颜色变化动画")
    
    try:
        pyglet.app.run()
    except Exception as e:
        print(f"程序运行出错: {e}")