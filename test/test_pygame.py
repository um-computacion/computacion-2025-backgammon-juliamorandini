import unittest
from unittest.mock import MagicMock, patch

# We import the real Config, pygame (for constants), and the game file
from config import Config
import pygame
import PygameUI
from PygameUI import GameUI, is_valid_direction, get_entry_point_for_dice

# ---
# Test Cases for Helper Functions
# ---


class TestHelperFunctions(unittest.TestCase):
    """Tests the pure helper functions in the game module."""

    def test_is_valid_direction(self):
        """Tests the checker move direction logic."""
        self.assertTrue(is_valid_direction(from_point=10, to_point=5, player="W"))
        self.assertFalse(is_valid_direction(from_point=5, to_point=10, player="W"))
        self.assertTrue(is_valid_direction(from_point=5, to_point=10, player="B"))
        self.assertFalse(is_valid_direction(from_point=10, to_point=5, player="B"))

    def test_get_entry_point_for_dice(self):
        """Tests the calculation for bar entry points."""
        self.assertEqual(get_entry_point_for_dice(dice_value=1, player="W"), 23)
        self.assertEqual(get_entry_point_for_dice(dice_value=6, player="W"), 18)
        self.assertEqual(get_entry_point_for_dice(dice_value=1, player="B"), 0)
        self.assertEqual(get_entry_point_for_dice(dice_value=6, player="B"), 5)


# ---
# Main Test Case for the Game Class
# ---


class TestGameUI(unittest.TestCase):
    """Groups all tests for the Game class."""

    def setUp(self):
        """Mocks all pygame and external dependencies before each test."""

        # We need a list to stop all patchers in tearDown
        self.patchers = []

        # Mock all pygame functions
        self.mock_pygame_init = self.start_patcher("pygame.init")
        self.mock_pygame_quit = self.start_patcher("pygame.quit")
        self.mock_set_mode = self.start_patcher(
            "pygame.display.set_mode", return_value=MagicMock()
        )
        self.mock_set_caption = self.start_patcher("pygame.display.set_caption")
        self.mock_flip = self.start_patcher("pygame.display.flip")
        self.mock_clock = self.start_patcher(
            "pygame.time.Clock", return_value=MagicMock()
        )

        # Mock font
        self.mock_font_render = MagicMock(return_value=MagicMock())
        self.mock_font = self.start_patcher(
            "pygame.font.Font", return_value=MagicMock(render=self.mock_font_render)
        )

        # Mock drawing
        self.mock_draw_rect = self.start_patcher("pygame.draw.rect")
        self.mock_draw_circle = self.start_patcher("pygame.draw.circle")

        # Mock Rect class - create proper mock Rect instances
        def mock_rect_factory(*args):
            mock_rect = MagicMock()
            mock_rect.collidepoint = MagicMock(return_value=False)
            # Set some default attributes
            if len(args) >= 4:
                mock_rect.x = args[0]
                mock_rect.y = args[1]
                mock_rect.width = args[2]
                mock_rect.height = args[3]
                mock_rect.centerx = args[0] + args[2] // 2
                mock_rect.centery = args[1] + args[3] // 2
                mock_rect.top = args[1]
                mock_rect.bottom = args[1] + args[3]
            return mock_rect

        self.mock_rect_cls = self.start_patcher(
            "pygame.Rect", side_effect=mock_rect_factory
        )

        # Mock external dependencies (the classes from your other files)
        # We patch them in the 'PygameUI' module's namespace
        self.mock_board_cls = self.start_patcher("PygameUI.BackgammonBoard")
        self.mock_interaction_cls = self.start_patcher("PygameUI.BoardInteraction")
        self.mock_button_cls = self.start_patcher("PygameUI.Button")

        # Configure the INSTANCES that Game.__init__ will create
        self.mock_board = self.mock_board_cls.return_value
        self.mock_board.current_player = "W"
        self.mock_board.dice_values = []
        self.mock_board.board = MagicMock()
        self.mock_board.board.bar = {"W": 0, "B": 0}
        self.mock_board.board.borne_off = {"W": 0, "B": 0}
        self.mock_board.board.points = [[] for _ in range(24)]
        self.mock_board.roll_dice.return_value = [3, 4]
        self.mock_board.board.can_bear_off.return_value = False
        self.mock_board.move_checker.return_value = True
        self.mock_board.board.move_checker_from_bar.return_value = True
        self.mock_board.board.bear_off.return_value = True

        self.mock_interaction = self.mock_interaction_cls.return_value
        self.mock_interaction.get_clicked_point.return_value = None

        # Button instances
        self.mock_roll_btn = MagicMock(handle_event=MagicMock(return_value=False))
        self.mock_reset_btn = MagicMock(handle_event=MagicMock(return_value=False))
        self.mock_next_turn_btn = MagicMock(handle_event=MagicMock(return_value=False))
        self.mock_button_cls.side_effect = [
            self.mock_roll_btn,
            self.mock_reset_btn,
            self.mock_next_turn_btn,
        ]

        # --- FINALLY, create the Game instance ---
        self.game = GameUI()

    def start_patcher(self, target, **kwargs):
        """Helper to create, start, and track patchers."""
        patcher = patch(target, **kwargs)
        self.patchers.append(patcher)
        return patcher.start()

    def tearDown(self):
        """Stops all patchers started in setUp."""
        for patcher in self.patchers:
            patcher.stop()

    # ---
    # Test Cases
    # ---

    def test_init(self):
        """Tests if the Game class initializes correctly."""
        # Check Pygame setup
        self.mock_pygame_init.assert_called_once()
        self.mock_set_mode.assert_called_with(
            (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        )
        self.mock_set_caption.assert_called_with("Backgammon Game")
        self.mock_clock.assert_called_once()
        self.mock_font.assert_called_with(None, 36)

        # Check dependency creation
        self.mock_board_cls.assert_called_once()
        self.mock_interaction_cls.assert_called_once()
        self.assertEqual(self.mock_button_cls.call_count, 3)

        # Check initial game state
        self.assertTrue(self.game.running)
        self.assertIsNone(self.game.selected_point)
        self.assertFalse(self.game.bar_selected)
        self.assertFalse(self.game.dice_rolled)
        self.assertEqual(self.game.moves_made, 0)

        # Check that the Rect class was called (at least twice)
        self.assertGreaterEqual(self.mock_rect_cls.call_count, 2)

    @patch("PygameUI.pygame.event.get")
    def test_run_loop(self, mock_event_get):
        """Tests the main game loop's logic (exit condition)."""
        # Mock the methods called inside the loop
        self.game.handle_event = MagicMock()
        self.game.update = MagicMock()
        self.game.render = MagicMock()

        # Track how many times the loop has run
        loop_count = [0]

        # Simulate the loop running twice and then stopping
        def stop_loop():
            loop_count[0] += 1
            if loop_count[0] >= 2:
                self.game.running = False

        self.game.update.side_effect = stop_loop

        # Mock pygame.event.get to return events each time
        mock_event_get.return_value = [MagicMock()]

        self.game.run()

        # Each event in the list gets processed
        self.assertEqual(self.game.update.call_count, 2)
        self.assertEqual(self.game.render.call_count, 2)
        self.mock_pygame_quit.assert_called_once()

    # --- Event Handling Tests ---

    def test_handle_event_quit(self):
        """Tests the QUIT event."""
        mock_event = MagicMock(type=pygame.QUIT)  # pylint: disable=no-member
        self.game.handle_event(mock_event)
        self.assertFalse(self.game.running)

    def test_handle_event_keydown(self):
        """Tests delegation to handle_keydown."""
        with patch.object(self.game, "handle_keydown") as mock_keydown:
            mock_event = MagicMock(
                type=pygame.KEYDOWN, key=pygame.K_SPACE # pylint: disable=no-member
            )  # pylint: disable=no-member
            self.game.handle_event(mock_event)
            mock_keydown.assert_called_with(pygame.K_SPACE)  # pylint: disable=no-member

    def test_handle_event_button_clicks(self):
        """Tests button click events."""
        mock_event = MagicMock(type=pygame.MOUSEBUTTONDOWN)  # pylint: disable=no-member

        with patch.object(self.game, "do_roll_dice") as mock_roll, patch.object(
            self.game, "do_reset"
        ) as mock_reset, patch.object(self.game, "do_next_turn") as mock_next:

            # Test Roll Button
            self.mock_roll_btn.handle_event.return_value = True
            self.game.handle_event(mock_event)
            mock_roll.assert_called_once()
            self.mock_roll_btn.handle_event.return_value = False  # Reset

            # Test Reset Button
            self.mock_reset_btn.handle_event.return_value = True
            self.game.handle_event(mock_event)
            mock_reset.assert_called_once()
            self.mock_reset_btn.handle_event.return_value = False

            # Test Next Turn Button
            self.mock_next_turn_btn.handle_event.return_value = True
            self.game.handle_event(mock_event)
            mock_next.assert_called_once()
            self.mock_next_turn_btn.handle_event.return_value = False

    def test_handle_event_board_click(self):
        """Tests delegation to handle_mouse_click when no button is pressed."""
        with patch.object(self.game, "handle_mouse_click") as mock_click:
            # Ensure all buttons return False
            self.mock_roll_btn.handle_event.return_value = False
            self.mock_reset_btn.handle_event.return_value = False
            self.mock_next_turn_btn.handle_event.return_value = False

            mock_event = MagicMock(
                type=pygame.MOUSEBUTTONDOWN, pos=(123, 456) # pylint: disable=no-member
            )  # pylint: disable=no-member
            self.game.handle_event(mock_event)

            mock_click.assert_called_with((123, 456))

    def test_handle_keydown(self):
        """Tests all keyboard shortcuts."""
        with patch.object(self.game, "do_roll_dice") as mock_roll, patch.object(
            self.game, "do_reset"
        ) as mock_reset, patch.object(self.game, "do_next_turn") as mock_next:

            self.game.handle_keydown(pygame.K_SPACE)  # pylint: disable=no-member
            mock_roll.assert_called_once()

            self.game.handle_keydown(pygame.K_n)  # pylint: disable=no-member
            mock_next.assert_called_once()

            self.game.handle_keydown(pygame.K_r)  # pylint: disable=no-member
            mock_reset.assert_called_once()

            self.game.running = True
            self.game.handle_keydown(pygame.K_ESCAPE)  # pylint: disable=no-member
            self.assertFalse(self.game.running)

    # --- Action Method Tests ---

    def test_do_roll_dice_success(self):
        """Tests a successful dice roll."""
        self.game.dice_rolled = False
        self.mock_board.roll_dice.return_value = [3, 4]

        self.game.do_roll_dice()

        self.mock_board.roll_dice.assert_called_once()
        self.assertTrue(self.game.dice_rolled)
        self.assertEqual(self.game.moves_made, 0)
        self.assertEqual(self.game.max_moves_this_turn, 2)

    def test_do_roll_dice_doubles(self):
        """Tests rolling doubles."""
        self.game.dice_rolled = False
        self.mock_board.roll_dice.return_value = [5, 5, 5, 5]

        self.game.do_roll_dice()

        self.assertEqual(self.game.max_moves_this_turn, 4)

    def test_do_roll_dice_already_rolled(self):
        """Tests trying to roll when dice are already rolled."""
        self.game.dice_rolled = True

        self.game.do_roll_dice()

        self.mock_board.roll_dice.assert_not_called()

    def test_do_reset(self):
        """Tests the game reset logic."""
        # Set some state to ensure it gets reset
        self.game.selected_point = 10
        self.game.bar_selected = True
        self.game.dice_rolled = True
        self.game.moves_made = 1
        self.game.max_moves_this_turn = 2

        self.game.do_reset()

        self.mock_board.reset.assert_called_once()
        self.assertIsNone(self.game.selected_point)
        self.assertFalse(self.game.bar_selected)
        self.assertFalse(self.game.dice_rolled)
        self.assertEqual(self.game.moves_made, 0)
        self.assertEqual(self.game.max_moves_this_turn, 0)

    def test_do_next_turn(self):
        """Tests the next turn logic."""
        # Set some state
        self.game.selected_point = 10
        self.game.bar_selected = True
        self.game.dice_rolled = True
        self.game.moves_made = 1
        self.game.max_moves_this_turn = 2

        self.game.do_next_turn()

        self.mock_board.switch_player.assert_called_once()
        self.assertIsNone(self.game.selected_point)
        self.assertFalse(self.game.bar_selected)
        self.assertFalse(self.game.dice_rolled)
        self.assertEqual(self.game.moves_made, 0)
        self.assertEqual(self.game.max_moves_this_turn, 0)

    # --- Mouse Click Logic Tests ---

    def test_handle_mouse_click_not_rolled(self):
        """Tests clicking before rolling dice."""
        self.game.dice_rolled = False

        with patch.object(self.game, "handle_bar_move") as mock_bar, patch.object(
            self.game, "handle_normal_move"
        ) as mock_normal:

            self.game.handle_mouse_click((100, 100))

            mock_bar.assert_not_called()
            mock_normal.assert_not_called()

    def test_handle_mouse_click_delegates_to_bar_move(self):
        """Tests that a click delegates to bar move if pieces are on bar."""
        self.game.dice_rolled = True
        self.mock_board.board.bar["W"] = 1  # Player W has a piece on the bar

        with patch.object(self.game, "handle_bar_move") as mock_bar, patch.object(
            self.game, "handle_normal_move"
        ) as mock_normal:

            self.game.handle_mouse_click((100, 100))

            mock_bar.assert_called_with((100, 100))
            mock_normal.assert_not_called()

    def test_handle_mouse_click_delegates_to_normal_move(self):
        """Tests that a click delegates to normal move if bar is empty."""
        self.game.dice_rolled = True
        self.mock_board.board.bar["W"] = 0  # Bar is empty

        with patch.object(self.game, "handle_bar_move") as mock_bar, patch.object(
            self.game, "handle_normal_move"
        ) as mock_normal:

            self.game.handle_mouse_click((100, 100))

            mock_bar.assert_not_called()
            mock_normal.assert_called_with((100, 100))

    # --- Bar Move Logic Tests ---

    def test_handle_bar_move_select_bar(self):
        """Tests clicking on the bar area to select a checker."""
        self.game.bar_selected = False
        # Use the REAL Config values for the click coordinates
        pos = (Config.BAR_X + 5, Config.BOARD_Y + 100)

        self.game.handle_bar_move(pos)

        self.assertTrue(self.game.bar_selected)

    def test_handle_bar_move_no_bar_selected(self):
        """Tests clicking a point *without* selecting the bar first."""
        self.game.bar_selected = False
        self.mock_interaction.get_clicked_point.return_value = 22

        self.game.handle_bar_move((100, 100))

        self.mock_board.board.move_checker_from_bar.assert_not_called()
        self.assertEqual(self.game.moves_made, 0)

    def test_handle_bar_move_invalid_entry_point(self):
        """Tests clicking an invalid entry point."""
        self.game.bar_selected = True
        self.game.backgammon_board.dice_values = [3]  # Valid entry for W is 21
        self.mock_interaction.get_clicked_point.return_value = 10

        self.game.handle_bar_move((100, 100))

        self.mock_board.board.move_checker_from_bar.assert_not_called()

    def test_handle_bar_move_blocked_entry_point(self):
        """Tests clicking a valid entry point that is blocked."""
        self.game.bar_selected = True
        self.game.backgammon_board.dice_values = [3]  # Valid entry for W is 21
        self.mock_interaction.get_clicked_point.return_value = 21
        self.mock_board.board.move_checker_from_bar.return_value = False  # Blocked

        self.game.handle_bar_move((100, 100))

        self.mock_board.board.move_checker_from_bar.assert_called_with(21, "W")
        self.assertEqual(self.game.moves_made, 0)
        self.assertTrue(self.game.bar_selected)  # Remain selected

    def test_handle_bar_move_success(self):
        """Tests a successful entry from the bar."""
        self.game.bar_selected = True
        self.game.backgammon_board.dice_values = [3, 6]
        self.game.max_moves_this_turn = 2
        self.mock_interaction.get_clicked_point.return_value = 21
        self.mock_board.board.move_checker_from_bar.return_value = True  # Open

        self.game.handle_bar_move((100, 100))

        self.mock_board.board.move_checker_from_bar.assert_called_with(21, "W")
        self.assertEqual(self.game.moves_made, 1)
        self.assertFalse(self.game.bar_selected)
        self.assertEqual(self.game.backgammon_board.dice_values, [6])  # 3 was used

    def test_handle_bar_move_success_ends_turn(self):
        """Tests a successful bar entry that also ends the turn."""
        with patch.object(self.game, "do_next_turn") as mock_next_turn:
            self.game.bar_selected = True
            self.game.backgammon_board.dice_values = [3]  # Last dice
            self.game.max_moves_this_turn = 1  # Last move
            self.mock_interaction.get_clicked_point.return_value = 21
            self.mock_board.board.move_checker_from_bar.return_value = True

            self.game.handle_bar_move((100, 100))

            self.assertEqual(self.game.moves_made, 1)
            self.assertEqual(self.game.backgammon_board.dice_values, [])
            mock_next_turn.assert_called_once()

    # --- Normal Move Logic Tests ---

    def test_handle_normal_move_select_piece(self):
        """Tests selecting a valid friendly piece."""
        self.game.selected_point = None
        self.mock_interaction.get_clicked_point.return_value = 10
        self.mock_board.board.points[10] = ["W", "W"]  # Friendly

        self.game.handle_normal_move((100, 100))

        self.assertEqual(self.game.selected_point, 10)

    def test_handle_normal_move_select_invalid_piece(self):
        """Tests clicking an empty or opponent-occupied point."""
        for point_contents in ([[]], [["B", "B"]]):
            with self.subTest(point_contents=point_contents):
                self.game.selected_point = None
                self.mock_interaction.get_clicked_point.return_value = 10
                self.mock_board.board.points[10] = point_contents

                self.game.handle_normal_move((100, 100))

                self.assertIsNone(self.game.selected_point)

    def test_handle_normal_move_click_outside_points(self):
        """Tests clicking outside all points when no piece is selected."""
        self.game.selected_point = None
        self.mock_interaction.get_clicked_point.return_value = None

        self.game.handle_normal_move((100, 100))

        self.assertIsNone(self.game.selected_point)

    def test_handle_normal_move_deselect_piece(self):
        """Tests deselecting a piece by clicking it again."""
        self.game.selected_point = 10
        self.mock_interaction.get_clicked_point.return_value = 10

        self.game.handle_normal_move((100, 100))

        self.assertIsNone(self.game.selected_point)

    def test_handle_normal_move_invalid_destination_click(self):
        """Tests clicking outside a point or bear-off area."""
        self.game.selected_point = 10
        self.mock_interaction.get_clicked_point.return_value = None  # Clicked off-board
        self.game.bear_off_rect_w.collidepoint.return_value = False

        self.game.handle_normal_move((100, 100))

        self.assertIsNone(self.game.selected_point)  # Deselects
        self.mock_board.move_checker.assert_not_called()

    def test_handle_normal_move_wrong_direction(self):
        """Tests moving a piece in the wrong direction."""
        self.game.selected_point = 10
        self.game.backgammon_board.dice_values = [3]
        self.mock_interaction.get_clicked_point.return_value = 13  # Wrong way for W

        self.game.handle_normal_move((100, 100))

        self.mock_board.move_checker.assert_not_called()
        self.assertIsNone(self.game.selected_point)  # Deselects

    def test_handle_normal_move_no_matching_dice(self):
        """Tests moving a piece with no matching dice value."""
        self.game.selected_point = 10
        self.game.backgammon_board.dice_values = [5, 6]
        self.mock_interaction.get_clicked_point.return_value = 7  # Distance is 3

        self.game.handle_normal_move((100, 100))

        self.mock_board.move_checker.assert_not_called()
        self.assertIsNone(self.game.selected_point)  # Deselects

    def test_handle_normal_move_blocked(self):
        """Tests moving to a valid point that is blocked."""
        self.game.selected_point = 10
        self.game.backgammon_board.dice_values = [3]
        self.mock_interaction.get_clicked_point.return_value = 7  # Distance is 3
        self.mock_board.move_checker.return_value = False  # Blocked

        self.game.handle_normal_move((100, 100))

        self.mock_board.move_checker.assert_called_with(10, 7)
        self.assertEqual(self.game.moves_made, 0)
        self.assertIsNone(self.game.selected_point)

    def test_handle_normal_move_success(self):
        """Tests a successful regular move."""
        with patch.object(self.game, "do_next_turn") as mock_next_turn:
            self.game.selected_point = 10
            self.game.backgammon_board.dice_values = [3, 5]
            self.game.max_moves_this_turn = 2
            self.mock_interaction.get_clicked_point.return_value = 7  # Distance 3
            self.mock_board.move_checker.return_value = True  # Success

            self.game.handle_normal_move((100, 100))

            self.mock_board.move_checker.assert_called_with(10, 7)
            self.assertEqual(self.game.moves_made, 1)
            self.assertEqual(self.game.backgammon_board.dice_values, [5])
            self.assertIsNone(self.game.selected_point)
            mock_next_turn.assert_not_called()

    def test_handle_normal_move_win_game(self):
        """Tests if the game correctly identifies a win and resets."""
        with patch.object(self.game, "do_reset") as mock_reset:
            self.game.selected_point = 10
            self.game.backgammon_board.dice_values = [3]
            self.game.max_moves_this_turn = 1  # Last move
            self.mock_interaction.get_clicked_point.return_value = 7
            self.mock_board.move_checker.return_value = True

            # Simulate this move being the winning one
            self.mock_board.board.borne_off["W"] = 15

            self.game.handle_normal_move((100, 100))

            self.assertEqual(self.game.moves_made, 1)
            self.assertIsNone(self.game.selected_point)
            mock_reset.assert_called_once()  # Game resets on win

    # --- Bear Off Logic Tests ---

    def test_handle_bear_off_not_allowed(self):
        """Tests clicking bear-off area when not all pieces are home."""
        self.game.selected_point = 3
        self.mock_interaction.get_clicked_point.return_value = None
        self.game.bear_off_rect_w.collidepoint.return_value = True  # Clicked
        self.mock_board.board.can_bear_off.return_value = False  # NOT allowed

        self.game.handle_normal_move((100, 100))

        self.mock_board.board.bear_off.assert_not_called()
        self.assertIsNone(self.game.selected_point)

    def test_handle_bear_off_exact_dice_w(self):
        """Tests bearing off for White with an exact dice."""
        self.game.selected_point = 3  # Requires a 4 (point 3+1)
        self.game.backgammon_board.dice_values = [4, 2]
        self.game.max_moves_this_turn = 2
        self.mock_interaction.get_clicked_point.return_value = None
        self.game.bear_off_rect_w.collidepoint.return_value = True  # Clicked
        self.mock_board.board.can_bear_off.return_value = True  # Allowed
        self.mock_board.board.bear_off.return_value = True
        self.mock_board.board.borne_off["W"] = 14  # Not yet winning

        self.game.handle_normal_move((100, 100))

        self.mock_board.board.bear_off.assert_called_with("W", 3)
        self.assertEqual(self.game.backgammon_board.dice_values, [2])  # 4 used
        self.assertEqual(self.game.moves_made, 1)

    def test_handle_bear_off_exact_dice_b(self):
        """Tests bearing off for Black with an exact dice."""
        self.game.backgammon_board.current_player = "B"
        self.game.selected_point = 22  # Requires a 2 (24-22)
        self.game.backgammon_board.dice_values = [2, 5]
        self.game.max_moves_this_turn = 2
        self.mock_interaction.get_clicked_point.return_value = None
        self.game.bear_off_rect_b.collidepoint.return_value = True  # Clicked
        self.mock_board.board.can_bear_off.return_value = True  # Allowed
        self.mock_board.board.bear_off.return_value = True
        self.mock_board.board.borne_off["B"] = 14  # Not yet winning

        self.game.handle_normal_move((100, 100))

        self.mock_board.board.bear_off.assert_called_with("B", 22)
        self.assertEqual(self.game.backgammon_board.dice_values, [5])  # 2 used
        self.assertEqual(self.game.moves_made, 1)

    def test_handle_bear_off_higher_dice_success(self):
        """Tests bearing off with a higher dice roll (furthest piece)."""
        self.game.selected_point = 3  # Requires a 4
        self.game.backgammon_board.dice_values = [5, 6]  # Dice are higher
        self.game.max_moves_this_turn = 2
        self.mock_interaction.get_clicked_point.return_value = None
        self.game.bear_off_rect_w.collidepoint.return_value = True
        self.mock_board.board.can_bear_off.return_value = True
        self.mock_board.board.bear_off.return_value = True
        self.mock_board.board.borne_off["W"] = 14  # Not yet winning

        # Mock that this IS the furthest piece
        self.mock_board.board.points[4] = []
        self.mock_board.board.points[5] = []

        self.game.handle_normal_move((100, 100))

        self.mock_board.board.bear_off.assert_called_with("W", 3)
        self.assertEqual(self.game.backgammon_board.dice_values, [6])  # 5 used
        self.assertEqual(self.game.moves_made, 1)

    def test_handle_bear_off_higher_dice_not_furthest_w(self):
        """Tests failing to bear off (not furthest piece) for White."""
        self.game.selected_point = 3  # Requires a 4
        self.game.backgammon_board.dice_values = [5, 6]  # Dice are higher
        self.mock_interaction.get_clicked_point.return_value = None
        self.game.bear_off_rect_w.collidepoint.return_value = True
        self.mock_board.board.can_bear_off.return_value = True

        # Mock that this is NOT the furthest piece
        self.mock_board.board.points[4] = ["W"]
        self.mock_board.board.points[5] = []

        self.game.handle_normal_move((100, 100))

        self.mock_board.board.bear_off.assert_not_called()
        self.assertEqual(self.game.moves_made, 0)

    def test_handle_bear_off_higher_dice_not_furthest_b(self):
        """Tests failing to bear off (not furthest piece) for Black."""
        self.game.backgammon_board.current_player = "B"
        self.game.selected_point = 22  # Requires a 2
        self.game.backgammon_board.dice_values = [3, 4]  # Dice are higher
        self.mock_interaction.get_clicked_point.return_value = None
        self.game.bear_off_rect_b.collidepoint.return_value = True
        self.mock_board.board.can_bear_off.return_value = True

        # Mock that this is NOT the furthest piece
        self.mock_board.board.points[21] = ["B"]
        self.mock_board.board.points[20] = []

        self.game.handle_normal_move((100, 100))

        self.mock_board.board.bear_off.assert_not_called()
        self.assertEqual(self.game.moves_made, 0)

    def test_handle_bear_off_no_valid_dice(self):
        """Tests failing to bear off (no exact, dice are smaller)."""
        self.game.selected_point = 3  # Requires a 4
        self.game.backgammon_board.dice_values = [1, 2]  # Dice are smaller
        self.mock_interaction.get_clicked_point.return_value = None
        self.game.bear_off_rect_w.collidepoint.return_value = True
        self.mock_board.board.can_bear_off.return_value = True

        self.game.handle_normal_move((100, 100))

        self.mock_board.board.bear_off.assert_not_called()
        self.assertEqual(self.game.moves_made, 0)

    # --- Update and Render Tests ---

    def test_update(self):
        """Tests the update method."""
        self.game.update()
        self.mock_board.update.assert_called_once()

    def test_render_base(self):
        """Tests the main render call stack."""
        self.game.render()

        self.game.screen.fill.assert_called_with(Config.DARK_BROWN)

        self.mock_board.render.assert_called_with(self.game.screen)
        self.mock_roll_btn.draw.assert_called_with(self.game.screen)
        self.mock_reset_btn.draw.assert_called_with(self.game.screen)
        self.mock_next_turn_btn.draw.assert_called_with(self.game.screen)

        self.mock_draw_rect.assert_any_call(
            self.game.screen, Config.WOOD_BROWN, self.game.bear_off_rect_b, 0, 8
        )
        self.mock_draw_rect.assert_any_call(
            self.game.screen, Config.WOOD_BROWN, self.game.bear_off_rect_w, 0, 8
        )

        self.mock_font_render.assert_any_call(
            "Current Player: White", True, (255, 255, 255)
        )
        self.game.screen.blit.assert_called()

        self.mock_flip.assert_called_once()

    def test_render_conditional_elements(self):
        """Tests the rendering of conditional elements (bar, dice, etc.)."""
        # 1. Setup state
        self.game.backgammon_board.board.bar["W"] = 2
        self.game.backgammon_board.dice_values = [1, 6]
        self.game.backgammon_board.board.borne_off["W"] = 3
        self.game.backgammon_board.board.borne_off["B"] = 1

        self.game.render()

        # Check for bar text
        self.mock_font_render.assert_any_call("On Bar: 2", True, (255, 100, 100))
        # Check for dice text
        self.mock_font_render.assert_any_call("Dice: [1, 6]", True, (255, 255, 255))
        # Check for borne-off text
        self.mock_font_render.assert_any_call("White Off: 3", True, (200, 200, 200))
        self.mock_font_render.assert_any_call("Black Off: 1", True, (200, 200, 200))
        # Check for borne-off checkers (3 + 1 = 4)
        # 2 calls per circle (fill + outline)
        self.assertEqual(self.mock_draw_circle.call_count, (3 + 1) * 2)

    def test_render_all_dice_used(self):
        """Tests the 'All dice used!' message."""
        self.game.dice_rolled = True
        self.game.backgammon_board.dice_values = []  # No dice left

        self.game.render()

        self.mock_font_render.assert_any_call("All dice used!", True, (255, 255, 0))


# ---
# Test Case for the main() function
# ---


class TestMainFunction(unittest.TestCase):
    """Tests the main() function to ensure full coverage."""

    @patch("PygameUI.GameUI")  # Mock the Game class in the 'PygameUI' module
    def test_main(self, mock_game_cls):
        """Tests if main() creates a Game and calls run()."""
        # Create a mock instance that will be returned by mock_game_cls()
        mock_game_instance = mock_game_cls.return_value

        # Call the main function
        PygameUI.main()

        # Check that Game() was called once
        mock_game_cls.assert_called_once_with()

        # Check that game.run() was called once on the instance
        mock_game_instance.run.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
