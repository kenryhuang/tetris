#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pyglet动画测试示例（无文本版本）
测试pyglet的动画和精灵功能，避免文本渲染问题
"""

import pyglet
import math
import random
from pyglet import shapes

# 创建窗口
window = pyglet.window.Window(800, 600, "Pyglet动画测试")

# 创建批处理对象
batch = pyglet.graphics.Batch()

# 动画对象列表
animated_objects = []

class BouncingBall:
    """弹跳球类"""
    def __init__(self, x, y, vx, vy, radius, color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.shape = shapes.Circle(x=x, y=y, radius=radius, color=color, batch=batch)
        
    def update(self, dt):
        # 更新位置
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # 边界碰撞检测
        if self.x - self.radius <= 0 or self.x + self.radius >= window.width:
            self.vx = -self.vx
            self.x = max(self.radius, min(window.width - self.radius, self.x))
            
        if self.y - self.radius <= 0 or self.y + self.radius >= window.height:
            self.vy = -self.vy
            self.y = max(self.radius, min(window.height - self.radius, self.y))
            
        # 更新图形位置
        self.shape.x = self.x
        self.shape.y = self.y

class RotatingSquare:
    """旋转方块类"""
    def __init__(self, x, y, size, color, rotation_speed):
        self.x = x
        self.y = y
        self.size = size
        self.rotation = 0
        self.rotation_speed = rotation_speed
        self.shape = shapes.Rectangle(x=x-size//2, y=y-size//2, width=size, height=size, color=color, batch=batch)
        
    def update(self, dt):
        self.rotation += self.rotation_speed * dt
        # 简单的旋转效果（通过改变颜色模拟）
        intensity = int(128 + 127 * math.sin(self.rotation))
        self.shape.color = (intensity, intensity, 255)

class PulsatingCircle:
    """脉动圆形类"""
    def __init__(self, x, y, base_radius, color, pulse_speed):
        self.x = x
        self.y = y
        self.base_radius = base_radius
        self.pulse_speed = pulse_speed
        self.time = 0
        self.shape = shapes.Circle(x=x, y=y, radius=base_radius, color=color, batch=batch)
        
    def update(self, dt):
        self.time += dt
        # 脉动效果
        scale = 1 + 0.5 * math.sin(self.pulse_speed * self.time)
        self.shape.radius = int(self.base_radius * scale)

# 创建动画对象
for i in range(5):
    # 创建弹跳球
    ball = BouncingBall(
        x=random.randint(50, window.width-50),
        y=random.randint(50, window.height-50),
        vx=random.randint(-200, 200),
        vy=random.randint(-200, 200),
        radius=random.randint(10, 30),
        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    )
    animated_objects.append(ball)

# 创建旋转方块
for i in range(3):
    square = RotatingSquare(
        x=random.randint(100, window.width-100),
        y=random.randint(100, window.height-100),
        size=random.randint(30, 60),
        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        rotation_speed=random.uniform(1, 3)
    )
    animated_objects.append(square)

# 创建脉动圆形
for i in range(3):
    circle = PulsatingCircle(
        x=random.randint(100, window.width-100),
        y=random.randint(100, window.height-100),
        base_radius=random.randint(20, 40),
        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        pulse_speed=random.uniform(2, 5)
    )
    animated_objects.append(circle)

# 更新函数
def update(dt):
    for obj in animated_objects:
        obj.update(dt)

# 注册更新函数，60FPS
pyglet.clock.schedule_interval(update, 1/60.0)

@window.event
def on_draw():
    window.clear()
    batch.draw()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.ESCAPE:
        window.close()
    elif symbol == pyglet.window.key.SPACE:
        # 添加新的弹跳球
        new_ball = BouncingBall(
            x=window.width//2,
            y=window.height//2,
            vx=random.randint(-300, 300),
            vy=random.randint(-300, 300),
            radius=random.randint(15, 25),
            color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        )
        animated_objects.append(new_ball)
        print(f"添加了新球，当前总数: {len([obj for obj in animated_objects if isinstance(obj, BouncingBall)])}")

@window.event
def on_mouse_press(x, y, button, modifiers):
    # 在鼠标位置添加脉动圆形
    new_circle = PulsatingCircle(
        x=x, y=y,
        base_radius=20,
        color=(255, 255, 0),
        pulse_speed=3
    )
    animated_objects.append(new_circle)
    print(f"在 ({x}, {y}) 添加了脉动圆形")

if __name__ == '__main__':
    print("Pyglet动画测试程序启动（无文本版本）")
    print("操作说明:")
    print("- 按ESC键退出")
    print("- 按空格键添加弹跳球")
    print("- 点击鼠标添加脉动圆形")
    print("- 观察各种动画效果")
    
    try:
        pyglet.app.run()
    except Exception as e:
        print(f"程序运行出错: {e}")
        import traceback
        traceback.print_exc()