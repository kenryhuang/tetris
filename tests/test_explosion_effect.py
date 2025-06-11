#!/usr/bin/env python3
"""
Test cases for ExplosionEffect class from tetris_pyglet.effects module.

This module tests the ExplosionEffect class functionality including:
- Initialization with various parameters
- Particle creation and management
- Color variation generation
- Update logic and lifecycle
- Drawing functionality
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tetris_pyglet.effects import ExplosionEffect, Particle
from tetris_pyglet.constants import (
    COLORS, PARTICLE_COUNT_RANGE, PARTICLE_SPEED_RANGE,
    PARTICLE_LIFE_RANGE, PARTICLE_SIZE_RANGE
)


class TestExplosionEffect(unittest.TestCase):
    """Test cases for ExplosionEffect class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_x = 100.0
        self.test_y = 200.0
        self.test_color = COLORS['RED']
        self.test_intensity = 1.5
        
    def test_init_default_parameters(self):
        """Test ExplosionEffect initialization with default parameters."""
        explosion = ExplosionEffect(self.test_x, self.test_y)
        
        self.assertEqual(explosion.x, self.test_x)
        self.assertEqual(explosion.y, self.test_y)
        self.assertEqual(explosion.color, COLORS['WHITE'])
        self.assertEqual(explosion.intensity, 1.0)
        self.assertTrue(explosion.active)
        self.assertIsInstance(explosion.particles, list)
        self.assertGreater(len(explosion.particles), 0)
        
    def test_init_custom_parameters(self):
        """Test ExplosionEffect initialization with custom parameters."""
        explosion = ExplosionEffect(
            self.test_x, self.test_y, 
            color=self.test_color, 
            intensity=self.test_intensity
        )
        
        self.assertEqual(explosion.x, self.test_x)
        self.assertEqual(explosion.y, self.test_y)
        self.assertEqual(explosion.color, self.test_color)
        self.assertEqual(explosion.intensity, self.test_intensity)
        self.assertTrue(explosion.active)
        
    def test_init_intensity_bounds(self):
        """Test ExplosionEffect initialization with various intensity values."""
        # Test minimum intensity
        explosion_min = ExplosionEffect(self.test_x, self.test_y, intensity=0.0)
        self.assertEqual(explosion_min.intensity, 0.0)
        
        # Test maximum intensity
        explosion_max = ExplosionEffect(self.test_x, self.test_y, intensity=2.0)
        self.assertEqual(explosion_max.intensity, 2.0)
        
        # Test beyond maximum (should still work)
        explosion_over = ExplosionEffect(self.test_x, self.test_y, intensity=3.0)
        self.assertEqual(explosion_over.intensity, 3.0)
        
    @patch('tetris_pyglet.effects.random.randint')
    @patch('tetris_pyglet.effects.random.uniform')
    def test_create_particles_count(self, mock_uniform, mock_randint):
        """Test that particle creation respects intensity multiplier."""
        # Mock random functions to return predictable values
        mock_randint.return_value = 20  # Base particle count
        
        # Use return_value instead of side_effect for simpler mocking
        mock_uniform.return_value = 1.0  # Default return value
        
        intensity = 1.5
        explosion = ExplosionEffect(self.test_x, self.test_y, intensity=intensity)
        
        # Expected particle count: base_count * intensity + spark_count
        expected_main_particles = int(20 * intensity)
        expected_spark_particles = int(expected_main_particles * 0.3)
        expected_total = expected_main_particles + expected_spark_particles
        
        self.assertEqual(len(explosion.particles), expected_total)
        
    def test_get_color_variation(self):
        """Test color variation generation."""
        explosion = ExplosionEffect(self.test_x, self.test_y, color=self.test_color)
        
        # Test multiple color variations
        variations = [explosion._get_color_variation() for _ in range(10)]
        
        for variation in variations:
            self.assertIsInstance(variation, tuple)
            self.assertEqual(len(variation), 4)  # RGBA
            
            # Check that all values are within valid range
            for component in variation[:3]:  # RGB components
                self.assertGreaterEqual(component, 0)
                self.assertLessEqual(component, 255)
            
            # Alpha should always be 255
            self.assertEqual(variation[3], 255)
            
        # Check that variations are actually different (with high probability)
        unique_variations = set(variations)
        self.assertGreater(len(unique_variations), 1)
        
    def test_update_active_effect(self):
        """Test update method with active effect."""
        explosion = ExplosionEffect(self.test_x, self.test_y)
        
        # Mock particles to control their behavior
        mock_particle1 = Mock()
        mock_particle1.update.return_value = True  # Still alive
        mock_particle2 = Mock()
        mock_particle2.update.return_value = False  # Dead
        mock_particle3 = Mock()
        mock_particle3.update.return_value = True  # Still alive
        
        explosion.particles = [mock_particle1, mock_particle2, mock_particle3]
        
        dt = 0.016  # ~60 FPS
        result = explosion.update(dt)
        
        # Should return True (still active)
        self.assertTrue(result)
        self.assertTrue(explosion.active)
        
        # Should remove dead particles
        self.assertEqual(len(explosion.particles), 2)
        self.assertIn(mock_particle1, explosion.particles)
        self.assertIn(mock_particle3, explosion.particles)
        self.assertNotIn(mock_particle2, explosion.particles)
        
        # All particles should have been updated
        mock_particle1.update.assert_called_once_with(dt)
        mock_particle2.update.assert_called_once_with(dt)
        mock_particle3.update.assert_called_once_with(dt)
        
    def test_update_all_particles_dead(self):
        """Test update method when all particles are dead."""
        explosion = ExplosionEffect(self.test_x, self.test_y)
        
        # Mock all particles as dead
        mock_particle1 = Mock()
        mock_particle1.update.return_value = False
        mock_particle2 = Mock()
        mock_particle2.update.return_value = False
        
        explosion.particles = [mock_particle1, mock_particle2]
        
        dt = 0.016
        result = explosion.update(dt)
        
        # Should return False (no longer active)
        self.assertFalse(result)
        self.assertFalse(explosion.active)
        
        # Should have no particles left
        self.assertEqual(len(explosion.particles), 0)
        
    def test_update_inactive_effect(self):
        """Test update method with inactive effect."""
        explosion = ExplosionEffect(self.test_x, self.test_y)
        explosion.active = False
        
        result = explosion.update(0.016)
        
        # Should return False immediately
        self.assertFalse(result)
        self.assertFalse(explosion.active)
        
    @patch('pyglet.graphics.Batch')
    @patch('pyglet.graphics.Group')
    def test_draw_with_particles(self, mock_group, mock_batch):
        """Test draw method with active particles."""
        explosion = ExplosionEffect(self.test_x, self.test_y)
        
        # Mock particles
        mock_particle1 = Mock()
        mock_particle1.draw.return_value = ['shape1', 'shape2']
        mock_particle2 = Mock()
        mock_particle2.draw.return_value = ['shape3']
        
        explosion.particles = [mock_particle1, mock_particle2]
        
        batch = mock_batch
        group = mock_group
        
        result = explosion.draw(batch, group)
        
        # Should return all shapes from all particles
        expected_shapes = ['shape1', 'shape2', 'shape3']
        self.assertEqual(result, expected_shapes)
        
        # All particles should have been drawn
        mock_particle1.draw.assert_called_once_with(batch, group)
        mock_particle2.draw.assert_called_once_with(batch, group)
        
    @patch('pyglet.graphics.Batch')
    @patch('pyglet.graphics.Group')
    def test_draw_no_particles(self, mock_group, mock_batch):
        """Test draw method with no particles."""
        explosion = ExplosionEffect(self.test_x, self.test_y)
        explosion.particles = []
        
        batch = mock_batch
        group = mock_group
        
        result = explosion.draw(batch, group)
        
        # Should return empty list
        self.assertEqual(result, [])
        
    def test_particle_types_created(self):
        """Test that both main particles and spark particles are created."""
        with patch('tetris_pyglet.effects.random.randint', return_value=20), \
             patch('tetris_pyglet.effects.random.uniform', return_value=1.0):
            
            explosion = ExplosionEffect(self.test_x, self.test_y, intensity=1.0)
            
            # Should have main particles + spark particles
            # 20 main + 6 spark (30% of 20) = 26 total
            self.assertEqual(len(explosion.particles), 26)
            
            # Verify all particles are Particle instances
            for particle in explosion.particles:
                self.assertIsInstance(particle, Particle)
                
    def test_explosion_lifecycle(self):
        """Test complete explosion lifecycle from creation to completion."""
        explosion = ExplosionEffect(self.test_x, self.test_y)
        
        # Initially should be active with particles
        self.assertTrue(explosion.active)
        self.assertGreater(len(explosion.particles), 0)
        
        # Simulate time passing until all particles die
        dt = 0.1  # Large time step to speed up the process
        max_iterations = 100  # Prevent infinite loop
        iterations = 0
        
        while explosion.active and iterations < max_iterations:
            explosion.update(dt)
            iterations += 1
            
        # Should eventually become inactive
        self.assertFalse(explosion.active)
        self.assertEqual(len(explosion.particles), 0)
        self.assertLess(iterations, max_iterations, "Explosion took too long to complete")
        

class TestExplosionEffectIntegration(unittest.TestCase):
    """Integration tests for ExplosionEffect with real dependencies."""
    
    def test_real_particle_creation(self):
        """Test explosion with real particle creation (no mocks)."""
        explosion = ExplosionEffect(100.0, 200.0, color=COLORS['BLUE'], intensity=1.2)
        
        # Should create particles within expected range
        min_particles = int(PARTICLE_COUNT_RANGE[0] * 1.2)  # Main particles
        max_particles = int(PARTICLE_COUNT_RANGE[1] * 1.2 * 1.3)  # Main + sparks
        
        self.assertGreaterEqual(len(explosion.particles), min_particles)
        self.assertLessEqual(len(explosion.particles), max_particles)
        
        # All particles should be valid Particle instances
        for particle in explosion.particles:
            self.assertIsInstance(particle, Particle)
            self.assertGreater(particle.life, 0)
            self.assertGreater(particle.size, 0)
            
    def test_real_update_cycle(self):
        """Test explosion update with real particles."""
        explosion = ExplosionEffect(50.0, 100.0, intensity=0.5)
        
        initial_particle_count = len(explosion.particles)
        self.assertGreater(initial_particle_count, 0)
        
        # Update several times
        for _ in range(10):
            result = explosion.update(0.05)
            if not result:
                break
                
        # Should still be active or have completed naturally
        # (depending on particle lifetimes)
        if explosion.active:
            self.assertGreaterEqual(len(explosion.particles), 0)
        else:
            self.assertEqual(len(explosion.particles), 0)
            

if __name__ == '__main__':
    unittest.main()