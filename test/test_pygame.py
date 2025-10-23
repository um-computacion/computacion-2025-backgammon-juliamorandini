"""
Unit tests for the refactored PygameUI.py (now using the Game class).

Tests cover:
- Helper functions (is_valid_direction, get_entry_point_for_dice)
- Game class initialization and initial state
- Keyboard event handling (K_SPACE, K_n, K_r)
- Button event handling (Roll, Reset, Next Turn)
- Mouse click logic on the board
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pygame

# We import from PygameUI_refactored (assuming you rename it to PygameUI.py)
# If you keep the name "PygameUI_refactored.py", change this import
from PygameUI import Game, is_valid_direction, get_entry_point_for_dice

from config import Config
from pygame_ui.button import Button
from pygame_ui.backgammon_board import BackgammonBoard
from pygame_ui.board_interaction import BoardInteraction


class TestHelperFunctions(unittest.TestCase):
    """Test suite for the standalone helper functions."""

    def test_white_moves_counter_clockwise_valid(self) -> None:
        """Test that White player can move counter-clockwise (high to low)."""
        self.assertTrue(is_valid_direction(23, 18, "W"))

    def test_white_moves_counter_clockwise_invalid(self) -> None:
        """Test that White player cannot move clockwise (low to high)."""
        self.assertFalse(is_valid_direction(5, 10, "W"))

    def test_black_moves_clockwise_valid(self) -> None:
        """Test that Black player can move clockwise (low to high)."""
        self.assertTrue(is_valid_direction(5, 10, "B"))

    def test_black_moves_clockwise_invalid(self) -> None:
        """Test that Black player cannot move counter-clockwise (high to low)."""
        self.assertFalse(is_valid_direction(15, 10, "B"))

    def test_get_entry_point_white(self) -> None:
        """Test entry point calculation for White player."""
        # Dice 1 → Point 23
        self.assertEqual(get_entry_point_for_dice(1, "W"), 23)
        # Dice 6 → Point 18
        self.assertEqual(get_entry_point_for_dice(6, "W"), 18)

    def test_get_entry_point_black(self) -> None:
        """Test entry point calculation for Black player."""
        # Dice 1 → Point 0
        self.assertEqual(get_entry_point_for_dice(1, "B"), 0)
        # Dice 6 → Point 5
        self.assertEqual(get_entry_point_for_dice(6, "B"), 5)


class TestGameLogic(unittest.TestCase):
    """
    Test suite for the main Game class logic.
    This class tests the actual game logic that was previously in main().
    """

    @patch("pygame.display.set_mode", Mock())
    @patch("pygame.display.set_caption", Mock())
    @patch(
        "pygame.font.Font", Mock(return_value=Mock(render=Mock(return_value=Mock())))
    )
    @patch("pygame.quit", Mock())
    def setUp(self):
        """Set up a new Game instance for each test."""
        # We must init pygame to be able to create pygame.event.Event
        pygame.init()
        # All pygame UI functions are mocked, so no window appears.
        self.game = Game()

    def tearDown(self):
        """Clean up after tests."""
        # This stops all patches started with patch.start()
        patch.stopall()
        pygame.quit()

    def test_initial_game_state(self):
        """Test that the game initializes with the correct default state."""
        self.assertIsInstance(self.game.backgammon_board, BackgammonBoard)
        self.assertIsNone(self.game.selected_point)
        self.assertFalse(self.game.bar_selected)
        self.assertFalse(self.game.dice_rolled)
        self.assertEqual(self.game.moves_made, 0)
        self.assertEqual(self.game.max_moves_this_turn, 0)
        self.assertTrue(self.game.running)

    def test_handle_keydown_k_n_next_turn(self):
        """Test that pressing 'N' key calls do_next_turn and resets state."""
        # Set up a pre-existing state
        self.game.dice_rolled = True
        self.game.moves_made = 1
        self.game.selected_point = 5
        initial_player = self.game.backgammon_board.current_player

        # Simulate the 'N' key press
        self.game.handle_keydown(pygame.K_n)

        # Assert that the state was correctly reset
        self.assertNotEqual(initial_player, self.game.backgammon_board.current_player)
        self.assertFalse(self.game.dice_rolled)
        self.assertEqual(self.game.moves_made, 0)
        self.assertIsNone(self.game.selected_point)

    def test_handle_keydown_k_r_reset(self):
        """Test that pressing 'R' key calls do_reset and resets state."""
        # Set up a pre-existing state
        self.game.dice_rolled = True
        self.game.selected_point = 5

        # Simulate the 'R' key press
        self.game.handle_keydown(pygame.K_r)

        # Assert that the state was correctly reset
        self.assertFalse(self.game.dice_rolled)
        self.assertIsNone(self.game.selected_point)

    def test_handle_keydown_k_space_roll_dice(self):
        """Test that 'SPACE' rolls dice if not already rolled."""
        self.assertFalse(self.game.dice_rolled)

        # Mock the roll_dice method to return a known value
        with patch.object(
            self.game.backgammon_board, "roll_dice", return_value=[3, 4]
        ) as mock_roll:
            self.game.handle_keydown(pygame.K_SPACE)

        mock_roll.assert_called_once()
        self.assertTrue(self.game.dice_rolled)
        self.assertEqual(self.game.moves_made, 0)
        self.assertEqual(self.game.max_moves_this_turn, 2)

    def test_handle_keydown_k_space_roll_dice_doubles(self):
        """Test that 'SPACE' correctly identifies doubles."""
        with patch.object(
            self.game.backgammon_board, "roll_dice", return_value=[6, 6, 6, 6]
        ) as mock_roll:
            self.game.handle_keydown(pygame.K_SPACE)

        mock_roll.assert_called_once()
        self.assertTrue(self.game.dice_rolled)
        self.assertEqual(self.game.max_moves_this_turn, 4)

    def test_handle_keydown_k_space_already_rolled(self):
        """Test that 'SPACE' does not roll dice if already rolled."""
        self.game.dice_rolled = True  # Set state to already rolled

        with patch.object(self.game.backgammon_board, "roll_dice") as mock_roll:
            self.game.handle_keydown(pygame.K_SPACE)

        # Assert that roll_dice was NOT called
        mock_roll.assert_not_called()
        self.assertTrue(self.game.dice_rolled)  # State remains unchanged

    def test_button_click_roll_dice(self):
        """Test that clicking the Roll Dice button calls do_roll_dice."""
        # Create a mock event positioned at the button's center
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"pos": self.game.roll_button.rect.center, "button": 1},
        )

        # Patch the actual action method to verify it's called
        with patch.object(self.game, "do_roll_dice") as mock_do_roll:
            self.game.handle_event(event)

        mock_do_roll.assert_called_once()

    def test_button_click_reset(self):
        """Test that clicking the Reset button calls do_reset."""
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"pos": self.game.reset_button.rect.center, "button": 1},
        )
        with patch.object(self.game, "do_reset") as mock_do_reset:
            self.game.handle_event(event)

        mock_do_reset.assert_called_once()

    def test_button_click_next_turn(self):
        """Test that clicking the Next Turn button calls do_next_turn."""
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN,
            {"pos": self.game.next_turn_button.rect.center, "button": 1},
        )
        with patch.object(self.game, "do_next_turn") as mock_do_next:
            self.game.handle_event(event)

        mock_do_next.assert_called_once()

    def test_mouse_click_board_before_roll_is_ignored(self):
        """Test that clicking the board before rolling dice does nothing."""
        self.game.dice_rolled = False  # Ensure dice are not rolled

        # Click somewhere on the board (not on a button)
        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (300, 300), "button": 1}
        )

        # We patch the move handlers to ensure they are NOT called
        with patch.object(
            self.game, "handle_normal_move"
        ) as mock_normal_move, patch.object(
            self.game, "handle_bar_move"
        ) as mock_bar_move:

            self.game.handle_event(event)

        mock_normal_move.assert_not_called()
        mock_bar_move.assert_not_called()

    def test_mouse_click_board_after_roll_is_handled(self):
        """Test that clicking the board after rolling dice calls the move handler."""
        self.game.dice_rolled = True  # Dice are rolled

        # Player has no pieces on the bar
        self.game.backgammon_board.board.bar[
            self.game.backgammon_board.current_player
        ] = 0

        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (300, 300), "button": 1}
        )

        with patch.object(self.game, "handle_normal_move") as mock_normal_move:
            self.game.handle_event(event)

        # It should call the normal move handler
        mock_normal_move.assert_called_once_with((300, 300))

    def test_mouse_click_with_bar_pieces_calls_bar_handler(self):
        """Test that clicking after rolling with bar pieces calls the bar handler."""
        self.game.dice_rolled = True  # Dice are rolled

        # Player HAS pieces on the bar
        self.game.backgammon_board.board.bar[
            self.game.backgammon_board.current_player
        ] = 1

        event = pygame.event.Event(
            pygame.MOUSEBUTTONDOWN, {"pos": (300, 300), "button": 1}
        )

        with patch.object(self.game, "handle_bar_move") as mock_bar_move:
            self.game.handle_event(event)

        # It should call the bar move handler
        mock_bar_move.assert_called_once_with((300, 300))


if __name__ == "__main__":
    unittest.main()
