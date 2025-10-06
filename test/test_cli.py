"""Test module for Backgammon CLI interface."""

import unittest
from unittest.mock import patch
from io import StringIO
from cli.CLI import BackgammonCLI


class TestBackgammonCLI(unittest.TestCase):
    """Test cases for BackgammonCLI."""

    def setUp(self):
        """Set up test fixtures."""
        self.cli = BackgammonCLI()

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_board(self, mock_stdout):
        """Test board display output."""
        self.cli.display_board()
        output = mock_stdout.getvalue()

        # Verify board elements are displayed
        self.assertIn("Current Board:", output)
        self.assertIn("Points:", output)
        self.assertIn("Bar -", output)
        self.assertIn("Borne Off -", output)

    @patch("builtins.input", side_effect=["1", "3"])
    def test_get_move_input_valid(self, mock_input):
        """Test valid move input handling."""
        move = self.cli.get_move_input()
        self.assertEqual(move, (1, 3))

    @patch("builtins.input", side_effect=["invalid"])
    def test_get_move_input_invalid(self, mock_input):
        """Test invalid move input handling."""
        move = self.cli.get_move_input()
        self.assertIsNone(move)

    @patch("sys.stdout", new_callable=StringIO)
    def test_show_help(self, mock_stdout):
        """Test help display."""
        self.cli.show_help()
        output = mock_stdout.getvalue()

        self.assertIn("Commands:", output)
        self.assertIn("move", output)
        self.assertIn("roll", output)
        self.assertIn("help", output)
        self.assertIn("quit", output)

    def test_quit_game(self):
        """Test quit functionality."""
        self.cli.quit_game()
        self.assertFalse(self.cli.is_running)

    @patch("builtins.input", side_effect=["roll", "quit"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_roll_command(self, mock_stdout, mock_input):
        """Test roll command in game loop."""
        self.cli.run()
        output = mock_stdout.getvalue()

        self.assertIn("Welcome to Backgammon!", output)
        self.assertIn("Rolled:", output)
        self.assertIn("Thanks for playing!", output)

    @patch("builtins.input", side_effect=["move", "1", "3", "quit"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_move_command(self, mock_stdout, mock_input):
        """Test move command in game loop."""
        self.cli.run()
        output = mock_stdout.getvalue()

        self.assertIn("Welcome to Backgammon!", output)
        self.assertIn("Enter move", output)
        self.assertIn("Thanks for playing!", output)

    @patch("builtins.input", side_effect=["invalid", "quit"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_invalid_command(self, mock_stdout, mock_input):
        """Test invalid command handling."""
        self.cli.run()
        output = mock_stdout.getvalue()

        self.assertIn("Unknown command", output)
        self.assertIn("Type 'help' for commands", output)

    @patch("builtins.input", side_effect=["help", "quit"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_help_command(self, mock_stdout, mock_input):
        """Test help command in game loop."""
        self.cli.run()
        output = mock_stdout.getvalue()

        self.assertIn("Commands:", output)
        self.assertIn("move", output)
        self.assertIn("roll", output)

    @patch("builtins.input", side_effect=["move", "invalid", "quit"])
    @patch("sys.stdout", new_callable=StringIO)
    def test_run_invalid_move(self, mock_stdout, mock_input):
        """Test invalid move input in game loop."""
        self.cli.run()
        output = mock_stdout.getvalue()

        self.assertIn("Invalid input", output)


if __name__ == "__main__":
    unittest.main()
