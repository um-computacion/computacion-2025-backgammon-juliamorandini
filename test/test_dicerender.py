import unittest
from unittest.mock import Mock, patch, call
import pygame

# Assuming dice_renderer is in pygame_ui folder
from pygame_ui.dice_renderer import DiceRenderer
from config import Config


class TestDiceRenderer(unittest.TestCase):
    """Test suite for the DiceRenderer class."""

    def setUp(self):
        """Set up a new DiceRenderer and a mock surface for each test."""
        # Pygame needs to be init'd for pygame.Rect
        pygame.init()
        self.renderer = DiceRenderer()
        self.mock_surface = Mock(spec=pygame.Surface)

    def tearDown(self):
        """Clean up pygame after tests."""
        pygame.quit()

    @patch("pygame_ui.dice_renderer.DiceRenderer._draw_die")
    def test_draw_no_dice(self, mock_draw_die):
        """Test that draw() does nothing if dice_values is empty."""
        self.renderer.draw(self.mock_surface, [])
        mock_draw_die.assert_not_called()

    @patch("pygame_ui.dice_renderer.DiceRenderer._draw_die")
    def test_draw_one_die(self, mock_draw_die):
        """Test that draw() calls _draw_die once for one die."""
        self.renderer.draw(self.mock_surface, [5])

        # Check that _draw_die was called once with the correct value
        # We access the dunder attributes directly (no mangling)
        mock_draw_die.assert_called_once_with(
            self.mock_surface, self.renderer.__dice_x__, self.renderer.__dice_y__, 5
        )

    @patch("pygame_ui.dice_renderer.DiceRenderer._draw_die")
    def test_draw_two_dice(self, mock_draw_die):
        """Test that draw() calls _draw_die twice for two dice.

        This test covers the missing lines 53-62.
        """
        dice_values = [3, 6]
        self.renderer.draw(self.mock_surface, dice_values)

        # Check for two calls
        self.assertEqual(mock_draw_die.call_count, 2)

        # Check arguments of each call
        # Access dunder attributes directly (no mangling)
        x_pos = self.renderer.__dice_x__
        y_pos = self.renderer.__dice_y__

        call_1 = call(self.mock_surface, x_pos, y_pos, 3)
        call_2 = call(self.mock_surface, x_pos, y_pos + Config.DICE_SIZE + 20, 6)
        mock_draw_die.assert_has_calls([call_1, call_2])

    #
    # The following tests cover the missing lines 86-130 and 146
    # by directly testing the _draw_die and _draw_dot methods.
    #

    @patch("pygame.draw.rect")
    @patch("pygame_ui.dice_renderer.DiceRenderer._draw_dot")
    def test_draw_die_value_1(self, mock_draw_dot, mock_draw_rect):
        """Test _draw_die for value 1. Covers line 86."""
        self.renderer._draw_die(self.mock_surface, 100, 100, 1)
        # 2 calls for rect (bg + border) + 1 for rounded corner
        self.assertEqual(mock_draw_rect.call_count, 3)
        # Value 1 should have 1 dot
        self.assertEqual(mock_draw_dot.call_count, 1)

    @patch("pygame.draw.rect")
    @patch("pygame_ui.dice_renderer.DiceRenderer._draw_dot")
    def test_draw_die_value_2(self, mock_draw_dot, mock_draw_rect):
        """Test _draw_die for value 2."""
        self.renderer._draw_die(self.mock_surface, 100, 100, 2)
        self.assertEqual(mock_draw_dot.call_count, 2)

    @patch("pygame.draw.rect")
    @patch("pygame_ui.dice_renderer.DiceRenderer._draw_dot")
    def test_draw_die_value_3(self, mock_draw_dot, mock_draw_rect):
        """Test _draw_die for value 3."""
        self.renderer._draw_die(self.mock_surface, 100, 100, 3)
        self.assertEqual(mock_draw_dot.call_count, 3)

    @patch("pygame.draw.rect")
    @patch("pygame_ui.dice_renderer.DiceRenderer._draw_dot")
    def test_draw_die_value_4(self, mock_draw_dot, mock_draw_rect):
        """Test _draw_die for value 4."""
        self.renderer._draw_die(self.mock_surface, 100, 100, 4)
        self.assertEqual(mock_draw_dot.call_count, 4)

    @patch("pygame.draw.rect")
    @patch("pygame_ui.dice_renderer.DiceRenderer._draw_dot")
    def test_draw_die_value_5(self, mock_draw_dot, mock_draw_rect):
        """Test _draw_die for value 5."""
        self.renderer._draw_die(self.mock_surface, 100, 100, 5)
        self.assertEqual(mock_draw_dot.call_count, 5)

    @patch("pygame.draw.rect")
    @patch("pygame_ui.dice_renderer.DiceRenderer._draw_dot")
    def test_draw_die_value_6(self, mock_draw_dot, mock_draw_rect):
        """Test _draw_die for value 6. Covers lines up to 130."""
        self.renderer._draw_die(self.mock_surface, 100, 100, 6)
        self.assertEqual(mock_draw_dot.call_count, 6)

    @patch("pygame.draw.circle")
    def test_draw_dot(self, mock_draw_circle):
        """Test the _draw_dot helper method. Covers line 146."""
        self.renderer._draw_dot(self.mock_surface, 150, 150)

        # Check that pygame.draw.circle was called exactly once
        mock_draw_circle.assert_called_once_with(
            self.mock_surface, Config.DICE_DOT, (150, 150), Config.DICE_DOT_RADIUS
        )


if __name__ == "__main__":
    unittest.main()
