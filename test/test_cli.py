"""Test module for the refactored Backgammon CLI interface."""

import unittest
from unittest.mock import patch, MagicMock
from io import StringIO

from cli.CLI import (
    BackgammonCLI,
    BoardRenderer,
    UserInterface,
    InputValidator,
    CommandParser,
    GameStateManager,
)
from core.BackgammonGame import Game


class TestBoardRenderer(unittest.TestCase):
    """Tests for the BoardRenderer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.renderer = BoardRenderer()
        self.game = Game()

    def test_render_board(self):
        """Test board display output."""
        output = self.renderer.render_board(self.game)

        self.assertIn("Current Board:", output)
        self.assertIn("Points:", output)
        self.assertIn("Bar -", output)
        self.assertIn("Borne Off -", output)
        self.assertIn("W 2", output)
        self.assertIn("B 2", output)


class TestUserInterface(unittest.TestCase):
    """Tests for the UserInterface class."""

    def setUp(self):
        """Set up test fixtures."""
        self.ui = UserInterface()

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_message(self, mock_stdout):
        """Test that display_message prints to stdout."""
        self.ui.display_message("Test message")
        self.assertEqual(mock_stdout.getvalue(), "Test message\n")

    @patch("builtins.input", return_value="user input")
    def test_get_input(self, mock_input):
        """Test that get_input returns user's typed string."""
        prompt = "Enter value: "
        result = self.ui.get_input(prompt)
        mock_input.assert_called_once_with(prompt)
        self.assertEqual(result, "user input")

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_help(self, mock_stdout):
        """Test help display."""
        self.ui.display_help()
        output = mock_stdout.getvalue()
        self.assertIn("Commands:", output)
        self.assertIn("move", output)
        self.assertIn("roll", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_roll_doubles(self, mock_stdout):
        """Test display_roll for doubles."""
        self.ui.display_roll([6, 6, 6, 6])
        self.assertIn("Rolled DOUBLES: 6 and 6", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_remaining_dice_empty(self, mock_stdout):
        """Test display_remaining_dice when no dice are left."""
        self.ui.display_remaining_dice([])
        self.assertIn("All dice used!", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_winner(self, mock_stdout):
        """Test display_winner."""
        self.ui.display_winner("TEST_PLAYER")
        self.assertIn("TEST_PLAYER WINS!", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_must_roll(self, mock_stdout):
        """Test display_must_roll."""
        self.ui.display_must_roll()
        self.assertIn("You must roll the dice first!", mock_stdout.getvalue())

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_move_success(self, mock_stdout):
        """Test display_move_success."""
        self.ui.display_move_success("1", "5")
        self.assertIn("Moved from 1 to 5", mock_stdout.getvalue())


class TestInputValidator(unittest.TestCase):
    """Tests for the InputValidator class."""

    def setUp(self):
        """Set up test fixtures."""
        self.validator = InputValidator()

    def test_validate_move_valid(self):
        """Test valid move argument handling."""
        args = ["1", "3"]
        move = self.validator.validate_move(args)
        self.assertEqual(move, (1, 3))

    def test_validate_move_invalid_not_numbers(self):
        """Test move validation with non-numeric input."""
        args = ["a", "b"]
        move = self.validator.validate_move(args)
        self.assertIsNone(move)

    def test_validate_move_invalid_wrong_count(self):
        """Test move validation with too few/many arguments."""
        args_few = ["1"]
        args_many = ["1", "2", "3"]
        self.assertIsNone(self.validator.validate_move(args_few))
        self.assertIsNone(self.validator.validate_move(args_many))


class TestCommandParser(unittest.TestCase):
    """Tests for the CommandParser class."""

    def setUp(self):
        """Set up test fixtures."""
        self.parser = CommandParser()

    def test_parse_move_command(self):
        """Test parsing a 'move' command with arguments."""
        command, args = self.parser.parse_command("move 1 5")
        self.assertEqual(command, "move")
        self.assertEqual(args, ["1", "5"])

    def test_parse_simple_command_case_insensitive(self):
        """Test parsing a simple command, ignoring case."""
        command, args = self.parser.parse_command("   rOlL   ")
        self.assertEqual(command, "roll")
        self.assertEqual(args, [])

    def test_parse_unknown_command(self):
        """Test parsing an unrecognized command."""
        command, args = self.parser.parse_command("fly me to the moon")
        self.assertEqual(command, "unknown")
        self.assertEqual(args, [])

    def test_parse_empty_input(self):
        """Test parsing empty input."""
        command, args = self.parser.parse_command("")
        self.assertEqual(command, "unknown")
        self.assertEqual(args, [])


class TestGameStateManager(unittest.TestCase):
    """Tests for the GameStateManager class."""

    def setUp(self):
        self.game = MagicMock(spec=Game)
        self.manager = GameStateManager(self.game)

    def test_initial_state(self):
        """Test that the initial state is not rolled."""
        self.assertFalse(self.manager.has_rolled)
        self.assertFalse(self.manager.can_move())

    def test_set_roll(self):
        """Test setting the roll."""
        self.manager.set_roll((5, 2))
        self.assertTrue(self.manager.has_rolled)
        self.assertTrue(self.manager.can_move())
        self.assertEqual(self.manager.get_remaining(), [5, 2])

    def test_use_die(self):
        """Test using dice."""
        self.manager.set_roll([5, 2])
        self.assertTrue(self.manager.use_die(5))
        self.assertEqual(self.manager.get_remaining(), [2])
        self.assertTrue(self.manager.can_move())

    def test_use_die_invalid(self):
        """Test using a die that is not available."""
        self.manager.set_roll([5, 2])
        self.assertFalse(self.manager.use_die(1))
        self.assertEqual(self.manager.get_remaining(), [5, 2])

    def test_end_turn(self):
        """Test that end_turn resets state and switches player."""
        self.manager.set_roll([5, 2])
        self.manager.end_turn()
        self.assertFalse(self.manager.has_rolled)
        self.assertEqual(self.manager.get_remaining(), [])
        self.game.switch_player.assert_called_once()


class TestBackgammonCLI(unittest.TestCase):
    """
    Test cases for the BackgammonCLI coordinator class.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.cli = BackgammonCLI()
        # We can mock the components of the CLI
        self.cli.ui = MagicMock(spec=UserInterface)
        self.cli.renderer = MagicMock(spec=BoardRenderer)
        self.cli.parser = MagicMock(spec=CommandParser)
        self.cli.validator = MagicMock(spec=InputValidator)

        # Mock the game object
        self.cli.game = MagicMock(autospec=Game)

        # --- THIS IS THE FIX ---
        # Re-create the state_manager AFTER mocking self.cli.game
        # so that the manager holds a reference to the mock object.
        self.cli.state_manager = GameStateManager(self.cli.game)

    def test_handle_quit(self):
        """Test quit functionality."""
        self.cli.is_running = True
        self.cli.handle_quit()
        self.assertFalse(self.cli.is_running)
        self.cli.ui.display_goodbye.assert_called_once()

    def test_handle_roll(self):
        """Test the roll handler delegates correctly."""
        self.cli.game.dice.roll.return_value = (5, 2)
        self.cli.handle_roll()
        self.cli.game.dice.roll.assert_called_once()
        self.cli.ui.display_roll.assert_called_once_with((5, 2))

    def test_handle_roll_already_rolled(self):
        """Test rolling when already rolled."""
        self.cli.state_manager.has_rolled = True
        self.cli.handle_roll()
        self.cli.game.dice.roll.assert_not_called()
        self.cli.ui.display_error.assert_called_once()

    def test_handle_move_success(self):
        """Test a successful move command."""
        self.cli.state_manager.set_roll([4])
        self.cli.validator.validate_move.return_value = (1, 5)
        self.cli.game.make_move.return_value = True
        self.cli.game.must_move_from_bar.return_value = False

        self.cli.handle_move(["1", "5"])

        self.cli.game.make_move.assert_called_once_with(1, 5)
        self.cli.ui.display_move_success.assert_called_once()

    def test_handle_move_invalid_format(self):
        """Test a move command that fails validation."""
        self.cli.state_manager.set_roll([1])
        self.cli.validator.validate_move.return_value = None

        self.cli.handle_move(["bad", "input"])

        self.cli.game.make_move.assert_not_called()
        self.cli.ui.display_error.assert_called_once_with(
            "Invalid move format. Use: move <from> <to>"
        )

    def test_handle_move_invalid_game_logic(self):
        """Test a move that is valid format but fails game logic."""
        self.cli.state_manager.set_roll([8])
        self.cli.validator.validate_move.return_value = (1, 9)
        self.cli.game.make_move.return_value = False
        self.cli.game.must_move_from_bar.return_value = False

        self.cli.handle_move(["1", "9"])

        self.cli.game.make_move.assert_called_once_with(1, 9)
        self.cli.ui.display_move_failure.assert_called_once()

    def test_handle_move_must_roll_first(self):
        """Test that move fails if not rolled."""
        self.cli.handle_move(["1", "5"])
        self.cli.ui.display_must_roll.assert_called_once()
        self.cli.game.make_move.assert_not_called()

    def test_handle_move_no_dice_remaining(self):
        """Test move when no dice are left."""
        self.cli.state_manager.set_roll([])
        self.cli.handle_move(["1", "5"])
        self.cli.ui.display_error.assert_called_with(
            "No dice remaining. Type 'skip' to end turn."
        )

    def test_handle_move_wrong_die_value(self):
        """Test move with a distance not in remaining dice."""
        self.cli.state_manager.set_roll([1, 2])
        self.cli.validator.validate_move.return_value = (1, 5)  # Dist 4
        self.cli.game.must_move_from_bar.return_value = False
        self.cli.handle_move(["1", "5"])
        self.cli.ui.display_move_failure.assert_called_once()
        self.cli.game.make_move.assert_not_called()

    def test_process_input_routes_skip(self):
        """Test that process_input calls handle_skip."""
        self.cli.parser.parse_command.return_value = ("skip", [])
        with patch.object(self.cli, "handle_skip") as mock_hs:
            self.cli.process_input("skip")
            mock_hs.assert_called_once()

    def test_handle_skip_must_roll_first(self):
        """Test skipping before rolling."""
        self.cli.handle_skip()
        self.cli.ui.display_error.assert_called_with(
            "You must roll first before skipping!"
        )

    def test_handle_skip_success(self):
        """Test a valid skip."""
        self.cli.state_manager.set_roll([5])
        self.cli.handle_skip()
        self.cli.ui.display_message.assert_any_call(
            "Skipping turn with 1 unused dice: [5]"
        )
        # This assertion will now pass
        self.cli.game.switch_player.assert_called_once()

    def test_run_loop_winner(self):
        """Test the run loop exits when a winner is found."""
        with patch("builtins.input", return_value="quit"):
            self.cli.game.check_winner.side_effect = [True]
            self.cli.run()
            self.cli.ui.display_winner.assert_called_once()

    # --- Bar Move Tests ---

    def test_handle_move_from_bar_success_white(self):
        """Test a successful move from the bar for White."""
        self.cli.state_manager.set_roll([3])  # 25 - 22 = 3
        self.cli.validator.validate_move.return_value = (-1, 22)  # bar to 22
        self.cli.game.must_move_from_bar.return_value = True
        self.cli.game.get_current_player_color.return_value = "W"
        self.cli.game.make_bar_move.return_value = True

        self.cli.handle_move(["bar", "22"])

        self.cli.game.make_bar_move.assert_called_once_with(22)
        self.cli.ui.display_move_success.assert_called_once_with("bar", "22")
        self.assertEqual(self.cli.state_manager.get_remaining(), [])
        # This assertion will now pass
        self.cli.game.switch_player.assert_called_once()

    def test_handle_move_from_bar_success_black(self):
        """Test a successful move from the bar for Black."""
        self.cli.state_manager.set_roll([4])  # 3 + 1 = 4
        self.cli.validator.validate_move.return_value = (-1, 3)  # bar to 3
        self.cli.game.must_move_from_bar.return_value = True
        self.cli.game.get_current_player_color.return_value = "B"
        self.cli.game.make_bar_move.return_value = True

        self.cli.handle_move(["bar", "3"])

        self.cli.game.make_bar_move.assert_called_once_with(3)
        self.assertEqual(self.cli.state_manager.get_remaining(), [])

    def test_handle_move_from_bar_no_pieces(self):
        """Test moving from bar when bar is empty."""
        self.cli.state_manager.set_roll([3])
        self.cli.validator.validate_move.return_value = (-1, 22)
        self.cli.game.must_move_from_bar.return_value = False  # Bar is empty

        self.cli.handle_move(["bar", "22"])

        self.cli.ui.display_move_failure.assert_called_with("No pieces on the bar")
        self.cli.game.make_bar_move.assert_not_called()

    def test_handle_move_from_bar_to_off(self):
        """Test 'move bar off' which is invalid."""
        self.cli.state_manager.set_roll([3])
        self.cli.validator.validate_move.return_value = (-1, -1)  # bar to off
        self.cli.game.must_move_from_bar.return_value = True

        self.cli.handle_move(["bar", "off"])

        self.cli.ui.display_error.assert_called_with(
            "Invalid point for entering from bar"
        )
        self.cli.game.make_bar_move.assert_not_called()

    def test_handle_move_from_bar_wrong_die(self):
        """Test moving from bar with the wrong die."""
        self.cli.state_manager.set_roll([5])  # Need a 3
        self.cli.validator.validate_move.return_value = (-1, 22)  # bar to 22 (needs 3)
        self.cli.game.must_move_from_bar.return_value = True
        self.cli.game.get_current_player_color.return_value = "W"

        self.cli.handle_move(["bar", "22"])

        self.cli.ui.display_move_failure.assert_called_once()
        self.cli.game.make_bar_move.assert_not_called()

    def test_handle_move_from_bar_game_fail(self):
        """Test when game logic rejects the bar move."""
        self.cli.state_manager.set_roll([3])
        self.cli.validator.validate_move.return_value = (-1, 22)
        self.cli.game.must_move_from_bar.return_value = True
        self.cli.game.get_current_player_color.return_value = "W"
        self.cli.game.make_bar_move.return_value = False  # Game rejects move

        self.cli.handle_move(["bar", "22"])

        self.cli.game.make_bar_move.assert_called_once_with(22)
        self.cli.ui.display_move_failure.assert_called_once()

    # --- Bear Off Tests ---

    def test_handle_bear_off_success_white(self):
        """Test successful bear off for White."""
        self.cli.state_manager.set_roll([5])
        self.cli.validator.validate_move.return_value = (5, -1)  # 5 to off
        self.cli.game.can_bear_off.return_value = True
        self.cli.game.get_current_player_color.return_value = "W"
        self.cli.game.bear_off.return_value = True

        self.cli.handle_move(["5", "off"])

        self.cli.game.bear_off.assert_called_once_with(5)
        self.cli.ui.display_move_success.assert_called_once_with("5", "off")
        self.assertEqual(self.cli.state_manager.get_remaining(), [])

    def test_handle_bear_off_success_black(self):
        """Test successful bear off for Black."""
        self.cli.state_manager.set_roll([3])  # 25 - 22 = 3
        self.cli.validator.validate_move.return_value = (22, -1)  # 22 to off
        self.cli.game.can_bear_off.return_value = True
        self.cli.game.get_current_player_color.return_value = "B"
        self.cli.game.bear_off.return_value = True

        self.cli.handle_move(["22", "off"])

        self.cli.game.bear_off.assert_called_once_with(22)
        self.assertEqual(self.cli.state_manager.get_remaining(), [])

    def test_handle_bear_off_not_allowed(self):
        """Test bearing off when not all pieces are home."""
        self.cli.state_manager.set_roll([5])
        self.cli.validator.validate_move.return_value = (5, -1)
        self.cli.game.can_bear_off.return_value = False  # Not allowed

        self.cli.handle_move(["5", "off"])

        self.cli.ui.display_move_failure.assert_called_once()
        self.cli.game.bear_off.assert_not_called()

    def test_handle_bear_off_wrong_die(self):
        """Test bearing off with the wrong die."""
        self.cli.state_manager.set_roll([2])  # Need a 5
        self.cli.validator.validate_move.return_value = (5, -1)  # 5 to off
        self.cli.game.can_bear_off.return_value = True
        self.cli.game.get_current_player_color.return_value = "W"

        self.cli.handle_move(["5", "off"])

        self.cli.ui.display_move_failure.assert_called_once()
        self.cli.game.bear_off.assert_not_called()

    def test_handle_bear_off_game_fail(self):
        """Test when game logic rejects the bear off."""
        self.cli.state_manager.set_roll([5])
        self.cli.validator.validate_move.return_value = (5, -1)
        self.cli.game.can_bear_off.return_value = True
        self.cli.game.get_current_player_color.return_value = "W"
        self.cli.game.bear_off.return_value = False  # Game rejects

        self.cli.handle_move(["5", "off"])

        self.cli.game.bear_off.assert_called_once_with(5)
        self.cli.ui.display_move_failure.assert_called_once()

    # --- Test `run` loop integration ---

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", side_effect=["move 1 3", "quit"])
    def test_run_move_command_invalid_logic(self, mock_input, mock_stdout): # pylint: disable=unused-argument 
        """Test move command in game loop that fails game logic."""
        cli = BackgammonCLI()
        cli.state_manager.set_roll([2])

        with patch.object(cli.game, "make_move", return_value=False) as mock_make:
            with patch.object(cli.game, "must_move_from_bar", return_value=False):
                cli.run()
                mock_make.assert_called_once_with(1, 3)

        output = mock_stdout.getvalue()
        self.assertIn("Invalid move!", output)
        self.assertIn("Thanks for playing!", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", side_effect=["move invalid", "quit"])
    def test_run_invalid_move_format(self, mock_input, mock_stdout): # pylint: disable=unused-argument
        """Test invalid move *format* in game loop.""" #uso lo de pylint disable xq si lo saco el codigo no funciona 
        cli = BackgammonCLI()
        cli.state_manager.set_roll([1])

        cli.run()
        output = mock_stdout.getvalue()

        self.assertIn("Invalid move format", output)
        self.assertIn("Thanks for playing!", output)


if __name__ == "__main__":
    unittest.main()
