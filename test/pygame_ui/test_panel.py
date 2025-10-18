"""Tests for Panel component."""

import unittest
import pygame
from pygame_ui.components.panel import Panel

class TestPanel(unittest.TestCase):
    """Test cases for Panel class."""

    def setUp(self):
        """Setup test fixtures."""
        pygame.init()
        self.surface = pygame.Surface((200, 600))
        self.panel = Panel(150, 50, 100, 500)

    def test_panel_initialization(self):
        """Test panel attributes are set correctly."""
        self.assertEqual(self.panel.x, 150)
        self.assertEqual(self.panel.y, 50)
        self.assertEqual(self.panel.width, 100)
        self.assertEqual(self.panel.height, 500)

    def test_panel_draw(self):
        """Test panel can be drawn without errors."""
        try:
            self.panel.draw(self.surface)
            success = True
        except:
            success = False
        self.assertTrue(success)

    def test_panel_sections(self):
        """Test panel has correct section heights."""
        section_height = self.panel.height // 3
        self.assertEqual(self.panel._get_section_height(), section_height)