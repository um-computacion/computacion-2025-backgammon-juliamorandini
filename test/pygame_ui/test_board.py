"""Tests for Board component."""

import unittest
import pygame
from pygame_ui.components.board import Board
from pygame_ui.constants import WINDOW_WIDTH, WINDOW_HEIGHT

class TestBoard(unittest.TestCase):
    """Test cases for Board class."""

    def setUp(self):
        """Setup test fixtures."""
        pygame.init()
        self.board = Board()
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

    def test_board_initialization(self):
        """Test board is initialized with correct components."""
        self.assertIsNotNone(self.board.surface)
        self.assertEqual(len(self.board.points), 24)
        self.assertIsNotNone(self.board.bar)
        self.assertIsNotNone(self.board.panel)

    def test_board_draw(self):
        """Test board can be drawn without errors."""
        try:
            self.board.draw(self.surface)
            success = True
        except:
            success = False
        self.assertTrue(success)

    def test_point_positions(self):
        """Test points are positioned correctly."""
        # Test first point position
        first_point = self.board.points[0]
        self.assertEqual(first_point.x, self.board.border_width)
        
        # Test last point position
        last_point = self.board.points[-1]
        self.assertLess(last_point.x + last_point.width, 
                       WINDOW_WIDTH - self.board.border_width)
        