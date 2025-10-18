"""Tests for Bar component."""

import unittest
import pygame
from pygame_ui.components.bar import Bar

class TestBar(unittest.TestCase):
    """Test cases for Bar class."""

    def setUp(self):
        """Setup test fixtures."""
        pygame.init()
        self.surface = pygame.Surface((200, 400))
        self.bar = Bar(100, 50, 40, 300)

    def test_bar_initialization(self):
        """Test bar attributes are set correctly."""
        self.assertEqual(self.bar.x, 100)
        self.assertEqual(self.bar.y, 50)
        self.assertEqual(self.bar.width, 40)
        self.assertEqual(self.bar.height, 300)

    def test_bar_draw(self):
        """Test bar can be drawn without errors."""
        try:
            self.bar.draw(self.surface)
            success = True
        except:
            success = False
        self.assertTrue(success)