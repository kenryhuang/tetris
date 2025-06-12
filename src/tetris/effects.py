"""Visual effects system for Tetris game."""

import pygame
import random
import math
from typing import List, Tuple
from .constants import EFFECT_COLORS

# 尝试导入pyglet用于高级渲染
try:
    import pyglet
    from pyglet import shapes
    PYGLET_AVAILABLE = True
except ImportError:
    PYGLET_AVAILABLE = False


class Particle:
    """高级粒子类 - 支持pyglet风格渲染的混合实现"""
    
    def __init__(self, x, y, velocity_x, velocity_y, life_time, color, size=3):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.life_time = life_time
        self.max_life_time = life_time
        self.color = color
        self.size = size
        self.gravity = -200  # 重力效果
        self.drag = 0.98    # 阻力系数（pyglet风格）
        
    def update(self, delta_time):
        """更新粒子状态 - pyglet风格的物理模拟"""
        # 更新位置
        self.x += self.velocity_x * delta_time
        self.y += self.velocity_y * delta_time
        
        # 应用重力
        self.velocity_y += self.gravity * delta_time
        
        # 应用阻力（pyglet风格）
        self.velocity_x *= self.drag
        self.velocity_y *= self.drag
        
        # 减少生命时间
        self.life_time -= delta_time
        
    def is_alive(self):
        """检查粒子是否还活着"""
        return self.life_time > 0
        
    def get_alpha(self):
        """根据剩余生命获取透明度值"""
        return max(0, self.life_time / self.max_life_time)
        
    def get_current_size(self):
        """根据剩余生命获取当前大小"""
        life_ratio = self.life_time / self.max_life_time
        # pyglet风格的大小变化：开始小，中间大，结束小
        size_factor = 4 * life_ratio * (1 - life_ratio)  # 抛物线函数
        return self.size * (0.3 + 0.7 * size_factor)
        
    def draw_pyglet_style(self, screen):
        """使用pyglet风格的高级渲染"""
        if not self.is_alive():
            return
            
        alpha = self.get_alpha()
        current_size = self.get_current_size()
        
        # 创建多层渲染效果（模拟pyglet的高级渲染）
        layers = [
            (current_size * 1.5, 0.3),  # 外层光晕
            (current_size * 1.2, 0.6),  # 中层
            (current_size * 0.8, 1.0),  # 核心
        ]
        
        for layer_size, layer_alpha in layers:
            if layer_size < 1:
                continue
                
            # 计算层的颜色和透明度
            final_alpha = alpha * layer_alpha
            layer_color = (*self.color[:3], int(255 * final_alpha))
            
            # 创建层表面
            layer_surface = pygame.Surface((int(layer_size * 2), int(layer_size * 2)), pygame.SRCALPHA)
            
            # 绘制渐变圆形（模拟pyglet的光晕效果）
            center = (int(layer_size), int(layer_size))
            for r in range(int(layer_size), 0, -1):
                gradient_alpha = final_alpha * (r / layer_size)
                gradient_color = (*self.color[:3], int(255 * gradient_alpha))
                pygame.draw.circle(layer_surface, gradient_color, center, r)
            
            # 绘制到屏幕
            screen.blit(layer_surface, (int(self.x - layer_size), int(self.y - layer_size)))
    
    def draw(self, screen):
        """绘制粒子 - 自动选择最佳渲染方式"""
        # 使用pyglet风格的高级渲染
        self.draw_pyglet_style(screen)


class LineEffect:
    """行消除效果类"""
    
    def __init__(self, row, board_width):
        self.row = row
        self.board_width = board_width
        self.flash_duration = 1.5  # 闪烁持续时间（秒）- 延长到1.5秒
        self.flash_timer = 0
        self.particles = []
        
        # 创建爆炸粒子 - 使用正确的坐标系统
        from .constants import CELL_SIZE, BORDER_WIDTH
        center_x = BORDER_WIDTH + (board_width * CELL_SIZE) // 2
        center_y = BORDER_WIDTH + row * CELL_SIZE + CELL_SIZE // 2
        
        for _ in range(20):  # 创建20个粒子增强效果
            # 随机速度和方向
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(80, 200)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            # 随机位置偏移 - 覆盖整行
            offset_x = random.uniform(-board_width * CELL_SIZE // 2, board_width * CELL_SIZE // 2)
            offset_y = random.uniform(-CELL_SIZE // 4, CELL_SIZE // 4)
            
            # 随机颜色
            explosion_colors = EFFECT_COLORS['EXPLOSION']
            sparkle_colors = EFFECT_COLORS['SPARKLE']
            all_colors = explosion_colors + sparkle_colors + [EFFECT_COLORS['FLASH']]
            color = random.choice(all_colors)
            
            particle = Particle(
                center_x + offset_x, center_y + offset_y,
                velocity_x, velocity_y,
                random.uniform(2.0, 3.0),  # 生命时间 - 延长到2-3秒
                color,
                random.uniform(1, 3)  # 大小
            )
            self.particles.append(particle)
        
    def update(self, delta_time):
        """更新效果"""
        self.flash_timer += delta_time
        
        # 更新所有粒子
        for particle in self.particles[:]:
            particle.update(delta_time)
            if not particle.is_alive():
                self.particles.remove(particle)
        
        # Return True if effect is still active
        return (self.flash_timer < self.flash_duration or 
                len(self.particles) > 0)
        
    def is_active(self):
        """检查效果是否仍然活跃"""
        return (self.flash_timer < self.flash_duration or 
                len(self.particles) > 0)
    
    def draw(self, screen):
        """绘制效果"""
        from .constants import CELL_SIZE, BORDER_WIDTH
        
        # 绘制闪烁效果 - 使用正确的坐标和尺寸
        if self.flash_timer < self.flash_duration:
            flash_intensity = 1 - (self.flash_timer / self.flash_duration)
            # 创建闪烁效果 - 深蓝色闪光（在白色背景上更明显）
            flash_color = (0, 100, 255)  # 深蓝色
            
            # 计算正确的矩形位置
            rect_x = BORDER_WIDTH
            rect_y = BORDER_WIDTH + self.row * CELL_SIZE
            rect_width = self.board_width * CELL_SIZE
            rect_height = CELL_SIZE
            
            # 绘制闪烁矩形 - 增强可见性
            flash_surface = pygame.Surface((rect_width, rect_height))
            flash_surface.set_alpha(int(200 * flash_intensity))  # 提高透明度
            flash_surface.fill(flash_color)
            screen.blit(flash_surface, (rect_x, rect_y))
            
            # 添加对比色边框效果
            border_color = (255, 165, 0)  # 橙色边框
            pygame.draw.rect(screen, border_color, (rect_x, rect_y, rect_width, rect_height), 4)
        
        # 绘制所有粒子
        for particle in self.particles:
            particle.draw(screen)


class EffectsManager:
    """特效管理器"""
    
    def __init__(self):
        """初始化特效管理器"""
        self.effects = []
        
    def add_line_clear_effect(self, cleared_rows, board_width=10):
        """添加行消除特效
        
        Args:
            cleared_rows: 被消除的行索引列表
            board_width: 游戏板宽度
        """
        for row in cleared_rows:
            effect = LineEffect(row, board_width)
            self.effects.append(effect)
        
    def update(self, delta_time):
        """更新所有特效
        
        Args:
            delta_time: 距离上次更新的时间（秒）
        """
        # 更新所有特效并移除不活跃的
        active_effects = []
        for effect in self.effects:
            effect.update(delta_time)
            if effect.is_active():
                active_effects.append(effect)
        self.effects = active_effects
        
    def draw(self, screen):
        """绘制所有特效"""
        for effect in self.effects:
            effect.draw(screen)
        
    def has_active_effects(self):
        """检查是否有活跃的特效
        
        Returns:
            如果有活跃特效返回True，否则返回False
        """
        return len(self.effects) > 0
        
    def add_sparkle_effect(self, x, y):
        """在指定位置添加闪烁特效
        
        Args:
            x: X坐标
            y: Y坐标
        """
        # 创建简单的闪烁粒子效果
        particles = []
        for _ in range(8):  # 创建8个闪烁粒子
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(30, 80)
            velocity_x = math.cos(angle) * speed
            velocity_y = math.sin(angle) * speed
            
            particle = Particle(
                x + random.uniform(-5, 5),
                y + random.uniform(-5, 5),
                velocity_x, velocity_y,
                random.uniform(0.3, 0.8),  # 生命时间
                random.choice(EFFECT_COLORS['SPARKLE']),
                random.uniform(1, 2)  # 大小
            )
            particles.append(particle)
        
        # 创建一个简单的闪烁效果（可以扩展为独立的效果类）
        class SparkleEffect:
            def __init__(self, particles):
                self.particles = particles
                
            def update(self, delta_time):
                for particle in self.particles[:]:
                    particle.update(delta_time)
                    if not particle.is_alive():
                        self.particles.remove(particle)
                        
            def is_active(self):
                return len(self.particles) > 0
                
            def draw(self, screen):
                for particle in self.particles:
                    particle.draw(screen)
        
        sparkle_effect = SparkleEffect(particles)
        self.effects.append(sparkle_effect)