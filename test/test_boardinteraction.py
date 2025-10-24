import unittest
import pygame
from unittest.mock import patch, Mock

# Import the class to test and the Config
from pygame_ui.board_interaction import BoardInteraction
from config import Config


# Helper function to create a mock event
def create_mock_event(event_type, pos=(0, 0), button=1):
    """Creates a mock pygame event."""
    return pygame.event.Event(event_type, {"pos": pos, "button": button})


class TestBoardInteraction(unittest.TestCase):
    """Test suite for the BoardInteraction class."""

    @classmethod
    def setUpClass(cls):
        """Initialize pygame once for event creation."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Quit pygame after all tests."""
        pygame.quit()

    def setUp(self):
        """Set up a new BoardInteraction instance for each test."""
        self.interaction = BoardInteraction()

    def test_init(self):
        """Test that attributes are initialized correctly."""
        self.assertIsNone(self.interaction._selected_point)
        self.assertEqual(self.interaction._mouse_pos, (0, 0))

    def test_handle_event_mouse_motion(self):
        """Test MOUSEMOTION event updates mouse_pos. Covers lines 12-14."""
        mock_event = create_mock_event(pygame.MOUSEMOTION, pos=(123, 456))
        result = self.interaction.handle_event(mock_event)

        self.assertIsNone(result)
        self.assertEqual(self.interaction._mouse_pos, (123, 456))

    @patch("pygame_ui.board_interaction.BoardInteraction.get_clicked_point")
    @patch("pygame.mouse.get_pos")
    def test_handle_event_mouse_button_down_on_board(
        self, mock_get_pos, mock_get_clicked_point
    ):
        """Test MOUSEBUTTONDOWN on the board. Covers lines 17-21."""
        mock_get_pos.return_value = (200, 200)  # y < 600
        mock_get_clicked_point.return_value = 10  # A valid point

        mock_event = create_mock_event(pygame.MOUSEBUTTONDOWN, pos=(200, 200))
        result = self.interaction.handle_event(mock_event)

        mock_get_clicked_point.assert_called_with((200, 200))
        self.assertEqual(result, {"type": "point_click", "point": 10})

    @patch("pygame_ui.board_interaction.BoardInteraction.get_clicked_point")
    @patch("pygame.mouse.get_pos")
    def test_handle_event_mouse_button_down_off_board(
        self, mock_get_pos, mock_get_clicked_point
    ):
        """Test MOUSEBUTTONDOWN off the board (e.g., on the bar)."""
        mock_get_pos.return_value = (400, 300)  # y < 600
        mock_get_clicked_point.return_value = None  # No point clicked

        mock_event = create_mock_event(pygame.MOUSEBUTTONDOWN, pos=(400, 300))
        result = self.interaction.handle_event(mock_event)

        mock_get_clicked_point.assert_called_with((400, 300))
        self.assertIsNone(result)

    @patch("pygame_ui.board_interaction.BoardInteraction.get_clicked_point")
    @patch("pygame.mouse.get_pos")
    def test_handle_event_mouse_button_down_in_button_area(
        self, mock_get_pos, mock_get_clicked_point
    ):
        """Test MOUSEBUTTONDOWN in the button area (y > 600). Covers line 18."""
        mock_get_pos.return_value = (300, 650)  # y > 600

        mock_event = create_mock_event(pygame.MOUSEBUTTONDOWN, pos=(300, 650))
        result = self.interaction.handle_event(mock_event)

        mock_get_clicked_point.assert_not_called()
        self.assertIsNone(result)

    def test_handle_event_other_event(self):
        """Test that other events return None."""
        mock_event = create_mock_event(pygame.KEYDOWN)
        result = self.interaction.handle_event(mock_event)
        self.assertIsNone(result)

    #
    # Tests for get_clicked_point (static method)
    # These tests cover the complex logic from lines 25-66
    #
    @classmethod
    def setUpClass_for_clicks(cls):
        """Set up constants based on Config for click tests."""
        cls.inner_left = Config.BOARD_X + Config.BORDER_THICKNESS
        cls.inner_right = Config.BOARD_X + Config.BOARD_WIDTH - Config.BORDER_THICKNESS
        cls.inner_top = Config.BOARD_Y + Config.BORDER_THICKNESS
        cls.inner_bottom = (
            Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
        )

        left_section_width = Config.BAR_X - cls.inner_left
        cls.point_width = left_section_width // 6

        cls.mid_y = (Config.BOARD_Y + Config.BOARD_HEIGHT) // 2
        cls.bar_right = Config.BAR_X + Config.BAR_WIDTH

        # Define test coordinates
        cls.click_top = cls.mid_y - 10
        cls.click_bottom = cls.mid_y + 10

        # X-coordinates for points in left quadrant
        cls.left_quad_x_points = [
            cls.inner_left + (i * cls.point_width) + 10 for i in range(6)
        ]
        # X-coordinates for points in right quadrant
        cls.right_quad_x_points = [
            cls.bar_right + (i * cls.point_width) + 10 for i in range(6)
        ]

    def test_get_clicked_point_outside_boundaries(self):
        """Test clicks outside the board's inner area. Covers lines 33-34."""
        self.setUpClass_for_clicks()
        # Click left
        self.assertIsNone(
            BoardInteraction.get_clicked_point((self.inner_left - 5, self.mid_y))
        )
        # Click right
        self.assertIsNone(
            BoardInteraction.get_clicked_point((self.inner_right + 5, self.mid_y))
        )
        # Click top
        self.assertIsNone(
            BoardInteraction.get_clicked_point((Config.BAR_X + 10, self.inner_top - 5))
        )
        # Click bottom
        self.assertIsNone(
            BoardInteraction.get_clicked_point(
                (Config.BAR_X + 10, self.inner_bottom + 5)
            )
        )

    def test_get_clicked_point_on_bar(self):
        """Test clicks on the bar."""
        self.setUpClass_for_clicks()
        click_on_bar = (Config.BAR_X + 5, self.mid_y)
        self.assertIsNone(BoardInteraction.get_clicked_point(click_on_bar))

    def test_get_clicked_point_top_left(self):
        """Test points 12-17 (Top Left). Covers lines 45-52."""
        self.setUpClass_for_clicks()
        expected_points = [12, 13, 14, 15, 16, 17]
        for i, x in enumerate(self.left_quad_x_points):
            point = BoardInteraction.get_clicked_point((x, self.click_top))
            self.assertEqual(
                point,
                expected_points[i],
                f"Failed for point {expected_points[i]} at x={x}",
            )

    def test_get_clicked_point_bottom_left(self):
        """Test points 11-6 (Bottom Left). Covers lines 53-55."""
        self.setUpClass_for_clicks()
        expected_points = [11, 10, 9, 8, 7, 6]
        for i, x in enumerate(self.left_quad_x_points):
            point = BoardInteraction.get_clicked_point((x, self.click_bottom))
            self.assertEqual(
                point,
                expected_points[i],
                f"Failed for point {expected_points[i]} at x={x}",
            )

    def test_get_clicked_point_top_right(self):
        """Test points 18-23 (Top Right). Covers lines 58-63."""
        self.setUpClass_for_clicks()
        expected_points = [18, 19, 20, 21, 22, 23]
        for i, x in enumerate(self.right_quad_x_points):
            point = BoardInteraction.get_clicked_point((x, self.click_top))
            self.assertEqual(
                point,
                expected_points[i],
                f"Failed for point {expected_points[i]} at x={x}",
            )

    def test_get_clicked_point_bottom_right(self):
        """Test points 5-0 (Bottom Right). Covers lines 64-66."""
        self.setUpClass_for_clicks()
        expected_points = [5, 4, 3, 2, 1, 0]
        for i, x in enumerate(self.right_quad_x_points):
            point = BoardInteraction.get_clicked_point((x, self.click_bottom))
            self.assertEqual(
                point,
                expected_points[i],
                f"Failed for point {expected_points[i]} at x={x}",
            )

    #
    # Tests for get_point_coords
    # These tests cover the logic from lines 70-104
    #

    def test_get_point_coords_invalid(self):
        """Test invalid point numbers. Covers line 72."""
        self.assertIsNone(self.interaction.get_point_coords(-1))
        self.assertIsNone(self.interaction.get_point_coords(24))

    def test_get_point_coords_logic(self):
        """
        Test that get_point_coords is the inverse of get_clicked_point.
        This covers all logic branches from 83-104.
        """
        self.setUpClass_for_clicks()

        for point_num in range(24):
            with self.subTest(point=point_num):
                # 1. Get the expected coordinates for the center of a point
                coords = self.interaction.get_point_coords(point_num)
                self.assertIsNotNone(
                    coords, f"get_point_coords({point_num}) returned None"
                )

                # 2. "Click" on those exact coordinates
                clicked_point = BoardInteraction.get_clicked_point(coords)

                # 3. Check that the click returns the original point number
                self.assertEqual(
                    clicked_point,
                    point_num,
                    f"get_point_coords({point_num}) -> {coords}, but clicking {coords} returns {clicked_point}",
                )


if __name__ == "__main__":
    unittest.main()
