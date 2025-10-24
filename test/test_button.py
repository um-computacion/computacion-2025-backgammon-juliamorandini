import unittest
import pygame
from unittest.mock import patch, Mock

# Import the class to test and the Config
from pygame_ui.button import Button


# Helper function to create a mock event
def create_mock_event(event_type, pos=(0, 0), button=1):
    """Creates a mock pygame event."""
    return pygame.event.Event(event_type, {"pos": pos, "button": button})


class TestButton(unittest.TestCase):
    """Test suite for the Button class."""

    @classmethod
    def setUpClass(cls):
        """Initialize pygame once for font rendering."""
        # We must init pygame to be able to create Rects and other objects
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Quit pygame after all tests."""
        pygame.quit()

    def setUp(self):
        """Set up a new Button instance for each test."""
        self.button = Button(
            x=100,
            y=100,
            width=200,
            height=50,
            text="Click Me",
            color=(10, 10, 10),
            hover_color=(50, 50, 50),
        )
        self.mock_surface = Mock(spec=pygame.Surface)

        # --- FIX: Mock the font instance, not the class ---
        # 1. Create a mock font object
        self.mock_font = Mock(spec=pygame.font.Font)

        # 2. Create a mock text surface that font.render() will return
        self.mock_text_surface = Mock(spec=pygame.Surface)
        # 3. Set up the mock text surface's get_rect() method
        self.mock_text_surface.get_rect.return_value = pygame.Rect(150, 125, 100, 20)

        # 4. Configure the mock font's render() method to return the mock text surface
        self.mock_font.render.return_value = self.mock_text_surface

        # 5. Replace the real font object on the button instance with our mock
        self.button.font = self.mock_font
        # --- End Fix ---

    #
    # Tests for draw() method (covers lines 35-46)
    #

    @patch("pygame.mouse.get_pos")
    @patch("pygame.draw.rect")
    def test_draw_normal_state(self, mock_draw_rect, mock_get_pos):
        """Test drawing the button when not hovered."""
        # Mouse position is outside the button
        mock_get_pos.return_value = (0, 0)

        self.button.draw(self.mock_surface)

        # Check if hover is false
        self.assertFalse(self.button.is_hovered)

        # Check that it drew with the normal color
        # The first call to draw.rect is the background
        args, _ = mock_draw_rect.call_args_list[0]
        self.assertEqual(args[1], self.button.color)

        # Check that text was rendered (using the mock from setUp)
        self.mock_font.render.assert_called_with(
            "Click Me", True, self.button.text_color
        )

        # Check that the text was blitted to the correct, centered position
        expected_center = self.button.rect.center
        text_rect = self.mock_text_surface.get_rect(center=expected_center)
        self.mock_surface.blit.assert_called_once_with(
            self.mock_text_surface, text_rect
        )

    @patch("pygame.mouse.get_pos")
    @patch("pygame.draw.rect")
    def test_draw_hover_state(self, mock_draw_rect, mock_get_pos):
        """Test drawing the button when hovered. Covers lines 38, 41."""
        # Mouse position is inside the button (150, 125)
        mock_get_pos.return_value = (150, 125)

        self.button.draw(self.mock_surface)

        # Check if hover is true
        self.assertTrue(self.button.is_hovered)

        # Check that it drew with the hover color
        # The first call to draw.rect is the background
        args, _ = mock_draw_rect.call_args_list[0]
        self.assertEqual(args[1], self.button.hover_color)

        # Check that text was still rendered
        self.mock_font.render.assert_called_with(
            "Click Me", True, self.button.text_color
        )
        self.mock_surface.blit.assert_called_once()

    #
    # Tests for handle_event() method (covers line 53)
    #

    def test_handle_event_click_inside(self):
        """Test a click inside the button returns True."""
        # Click at (150, 125) which is inside the button
        click_event = create_mock_event(
            pygame.MOUSEBUTTONDOWN, pos=(150, 125), button=1
        )
        self.assertTrue(self.button.handle_event(click_event))

    def test_handle_event_click_outside(self):
        """Test a click outside the button returns False."""
        # Click at (0, 0) which is outside
        click_event = create_mock_event(pygame.MOUSEBUTTONDOWN, pos=(0, 0), button=1)
        self.assertFalse(self.button.handle_event(click_event))

    def test_handle_event_not_mouse_down(self):
        """Test a non-MOUSEBUTTONDOWN event returns False. Covers line 53."""
        # Any other event type
        key_event = create_mock_event(pygame.KEYDOWN)
        self.assertFalse(self.button.handle_event(key_event))

    def test_handle_event_wrong_mouse_button(self):
        """Test a right-click event returns False. Covers line 53."""
        # Click with right mouse button (button=3)
        right_click_event = create_mock_event(
            pygame.MOUSEBUTTONDOWN, pos=(150, 125), button=3
        )
        self.assertFalse(self.button.handle_event(right_click_event))


if __name__ == "__main__":
    unittest.main()
