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
)
from core.BackgammonGame import Game


class TestBoardRenderer(unittest.TestCase):
    """Tests for the BoardRenderer class."""

    def setUp(self):
        """Set up test fixtures."""
        self.renderer = BoardRenderer()
        self.game = Game()  # Use the (Mock)Game from the CLI module

    def test_render_board(self):
        """Test board display output."""
        output = self.renderer.render_board(self.game)

        # Verify key board elements are in the rendered string
        self.assertIn("Current Board:", output)
        self.assertIn("Points:", output)
        self.assertIn("Bar -", output)
        self.assertIn("Borne Off -", output)
        # Check for an initial piece, e.g., W2 on point 23
        self.assertIn("W 2", output)
        # Check for an initial piece, e.g., B2 on point 0
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
        command, args = self.parser.parse_command("  rOlL  ")
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


class TestBackgammonCLI(unittest.TestCase):
    """
    Test cases for the BackgammonCLI coordinator class.
    These tests focus on integration and coordination.
    """

    def setUp(self):
        """Set up test fixtures."""
        self.cli = BackgammonCLI()
        # We can mock the components of the CLI
        self.cli.ui = MagicMock(spec=UserInterface)
        self.cli.renderer = MagicMock(spec=BoardRenderer)
        self.cli.parser = MagicMock(spec=CommandParser)
        self.cli.validator = MagicMock(spec=InputValidator)

        # --- FIX 1 ---
        # Use autospec=True to correctly mock instance attributes like 'dice'
        self.cli.game = MagicMock(autospec=Game)

    def test_handle_quit(self):
        """Test quit functionality."""
        self.cli.is_running = True
        self.cli.handle_quit()
        self.assertFalse(self.cli.is_running)
        self.cli.ui.display_goodbye.assert_called_once()

    def test_handle_roll(self):
        """Test the roll handler delegates correctly."""
        # This line will now work thanks to autospec=True
        self.cli.game.dice.roll.return_value = (5, 2)

        self.cli.handle_roll()

        self.cli.game.dice.roll.assert_called_once()
        self.cli.ui.display_roll.assert_called_once_with((5, 2))

    def test_handle_move_success(self):
        """Test a successful move command."""
        self.cli.validator.validate_move.return_value = (1, 5)
        self.cli.game.make_move.return_value = True

        self.cli.handle_move(["1", "5"])

        self.cli.validator.validate_move.assert_called_once_with(["1", "5"])
        self.cli.game.make_move.assert_called_once_with(1, 5)
        self.cli.ui.display_move_success.assert_called_once()
        self.cli.ui.display_move_failure.assert_not_called()

    def test_handle_move_invalid_format(self):
        """Test a move command that fails validation."""
        self.cli.validator.validate_move.return_value = None

        self.cli.handle_move(["bad", "input"])

        self.cli.validator.validate_move.assert_called_once_with(["bad", "input"])
        self.cli.game.make_move.assert_not_called()
        self.cli.ui.display_error.assert_called_once_with(
            "Invalid move format. Use: move <from> <to>"
        )

    def test_handle_move_invalid_game_logic(self):
        """Test a move that is valid format but fails game logic."""
        self.cli.validator.validate_move.return_value = (1, 9)
        self.cli.game.make_move.return_value = False  # Game rejects the move

        self.cli.handle_move(["1", "9"])

        self.cli.validator.validate_move.assert_called_once_with(["1", "9"])
        self.cli.game.make_move.assert_called_once_with(1, 9)
        self.cli.ui.display_move_success.assert_not_called()
        self.cli.ui.display_move_failure.assert_called_once()

    def test_process_input_routes_correctly(self):
        """Test that process_input calls the right handler."""
        # Mock parser return values
        self.cli.parser.parse_command.side_effect = [
            ("move", ["1", "5"]),
            ("roll", []),
            ("help", []),
            ("quit", []),
            ("unknown", []),
        ]

        # Patch the handler methods to check if they are called
        with patch.object(self.cli, "handle_move") as mock_hm:
            self.cli.process_input("move 1 5")
            mock_hm.assert_called_once_with(["1", "5"])

        with patch.object(self.cli, "handle_roll") as mock_hr:
            self.cli.process_input("roll")
            mock_hr.assert_called_once()

        with patch.object(self.cli.ui, "display_help") as mock_dh:
            self.cli.process_input("help")
            mock_dh.assert_called_once()

        with patch.object(self.cli, "handle_quit") as mock_hq:
            self.cli.process_input("quit")
            mock_hq.assert_called_once()

        # Test unknown
        self.cli.process_input("foo")
        self.cli.ui.display_error.assert_called_with(
            "Unknown command. Type 'help' for commands."
        )

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", side_effect=["roll", "quit"])
    def test_run_roll_command(self, mock_input, mock_stdout):
        """Test roll command in game loop."""
        # pylint: disable=unused-argument
        cli = BackgammonCLI()
        cli.run()
        output = mock_stdout.getvalue()

        self.assertIn("Welcome to Backgammon!", output)
        self.assertIn("Rolled:", output)  # From ui.display_roll
        self.assertIn("Thanks for playing!", output)  # From ui.display_goodbye

    @patch("sys.stdout", new_callable=StringIO)
    # --- FIX 2 ---
    # The input should be "move 1 3" on one line, not three separate inputs.
    @patch("builtins.input", side_effect=["move 1 3", "quit"])
    def test_run_move_command_invalid_logic(self, mock_input, mock_stdout):
        """Test move command in game loop that fails game logic."""
        # pylint: disable=unused-argument
        # This test assumes the mock move (1, 3) is invalid
        cli = BackgammonCLI()
        # Mock the game logic to fail this specific move
        with patch.object(cli.game, "make_move", return_value=False) as mock_make:
            cli.run()
            # This assertion will now pass
            mock_make.assert_called_once_with(1, 3)

        output = mock_stdout.getvalue()
        self.assertIn("Invalid move!", output)  # From ui.display_move_failure
        self.assertIn("Thanks for playing!", output)

    @patch("sys.stdout", new_callable=StringIO)
    # --- FIX 3 (Related to FIX 2) ---
    # The input should be "move invalid" on one line.
    @patch("builtins.input", side_effect=["move invalid", "quit"])
    def test_run_invalid_move_format(self, mock_input, mock_stdout):
        """Test invalid move *format* in game loop."""
        # pylint: disable=unused-argument
        cli = BackgammonCLI()
        cli.run()
        output = mock_stdout.getvalue()

        # Check for the new, specific error message
        self.assertIn("Invalid move format", output)
        self.assertIn("Thanks for playing!", output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("builtins.input", side_effect=["winner", "quit"])
    def test_run_invalid_command(self, mock_input, mock_stdout):
        """Test invalid command handling."""
        # pylint: disable=unused-argument
        cli = BackgammonCLI()
        cli.run()
        output = mock_stdout.getvalue()

        self.assertIn("Unknown command", output)
        self.assertIn("Type 'help' for commands", output)
        self.assertIn("Thanks for playing!", output)


if __name__ == "__main__":
    unittest.main()
