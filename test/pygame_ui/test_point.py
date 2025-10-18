"""Tests for Point component."""

import unittest
import pygame
from pygame_ui.components.point import Point

class TestPoint(unittest.TestCase):
    """Test cases for Point class."""

    def setUp(self):
        """Setup test fixtures."""
        pygame.init()
        self.surface = pygame.Surface((100, 100))
        self.point = Point(0, 0, 50, 50)

    def test_point_initialization(self):
        """Test point attributes are set correctly."""
        self.assertEqual(self.point.x, 0)
        self.assertEqual(self.point.y, 0)
        self.assertEqual(self.point.width, 50)
        self.assertEqual(self.point.height, 50)

    def test_point_draw(self):
        """Test point can be drawn without errors."""
        try:
            self.point.draw(self.surface)
            success = True
        except:
            success = False
        self.assertTrue(success)