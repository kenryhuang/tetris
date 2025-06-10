#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pyglet功能测试报告
总结pyglet库的各项功能测试结果
"""

import pyglet
from pyglet import shapes
import sys
import traceback

def test_basic_window():
    """测试基本窗口功能"""
    try:
        window = pyglet.window.Window(400, 300, "测试窗口")
        window.close()
        return True, "窗口创建成功"
    except Exception as e:
        return False, f"窗口创建失败: {e}"

def test_shapes():
    """测试图形绘制功能"""
    try:
        window = pyglet.window.Window(400, 300, "图形测试")
        batch = pyglet.graphics.Batch()
        
        # 测试各种图形
        circle = shapes.Circle(x=100, y=100, radius=30, color=(255, 0, 0), batch=batch)
        rectangle = shapes.Rectangle(x=200, y=100, width=50, height=50, color=(0, 255, 0), batch=batch)
        
        window.close()
        return True, "图形绘制功能正常"
    except Exception as e:
        return False, f"图形绘制失败: {e}"

def test_events():
    """测试事件处理功能"""
    try:
        window = pyglet.window.Window(400, 300, "事件测试")
        
        @window.event
        def on_key_press(symbol, modifiers):
            pass
            
        @window.event
        def on_mouse_press(x, y, button, modifiers):
            pass
            
        window.close()
        return True, "事件处理功能正常"
    except Exception as e:
        return False, f"事件处理失败: {e}"

def test_clock():
    """测试时钟和定时器功能"""
    try:
        def dummy_update(dt):
            pass
            
        pyglet.clock.schedule_interval(dummy_update, 1/60.0)
        pyglet.clock.unschedule(dummy_update)
        return True, "时钟功能正常"
    except Exception as e:
        return False, f"时钟功能失败: {e}"

def test_media():
    """测试媒体功能"""
    try:
        # 尝试创建播放器
        player = pyglet.media.Player()
        return True, "媒体播放器创建成功"
    except Exception as e:
        return False, f"媒体功能失败: {e}"

def run_all_tests():
    """运行所有测试"""
    print("=" * 50)
    print("Pyglet功能测试报告")
    print("=" * 50)
    print(f"Python版本: {sys.version}")
    print(f"Pyglet版本: {pyglet.version}")
    print("-" * 50)
    
    tests = [
        ("基本窗口功能", test_basic_window),
        ("图形绘制功能", test_shapes),
        ("事件处理功能", test_events),
        ("时钟定时器功能", test_clock),
        ("媒体播放功能", test_media),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            success, message = test_func()
            status = "✓ 通过" if success else "✗ 失败"
            if success:
                passed += 1
            print(f"{test_name:15} {status:8} - {message}")
        except Exception as e:
            print(f"{test_name:15} ✗ 失败   - 测试异常: {e}")
    
    print("-" * 50)
    print(f"测试结果: {passed}/{total} 项测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！Pyglet安装和配置正常。")
    elif passed > 0:
        print("⚠️  部分测试通过，Pyglet基本功能可用。")
    else:
        print("❌ 所有测试失败，Pyglet可能存在问题。")
    
    print("\n推荐的测试程序:")
    print("- pyglet_test_minimal.py (基础图形测试)")
    print("- pyglet_test_animation_no_text.py (动画测试)")
    print("- pyglet_test_audio_simple.py (音频测试)")
    
    return passed, total

if __name__ == '__main__':
    try:
        run_all_tests()
    except Exception as e:
        print(f"测试程序运行出错: {e}")
        traceback.print_exc()