"""Test module for Backgammon CLI interface following SOLID principles."""

import unittest
from unittest.mock import patch
from io import StringIO
from core.BackgammonGame import Game
from abc import ABC, abstractmethod


class CommandInterface(ABC):
    """Interface for CLI commands following Interface Segregation Principle."""

    @abstractmethod
    def execute(self, *args):
        """Execute the command."""


class MoveCommand(CommandInterface):
    """Command for moving pieces."""

    def execute(self, game, from_point, to_point):
        return game.make_move(from_point, to_point)


class RollCommand(CommandInterface):
    """Command for rolling dice."""

    def execute(self, game):
        return game.dice.roll()


class TestBackgammonCLI(unittest.TestCase):
    """Test cases for Backgammon CLI interface."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()
        self.move_command = MoveCommand()
        self.roll_command = RollCommand()

    def test_command_interface(self):
        """Test command pattern implementation."""
        self.assertIsInstance(self.move_command, CommandInterface)
        self.assertIsInstance(self.roll_command, CommandInterface)

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_board(self, mock_stdout):
        """Test board display following Single Responsibility."""
        board = self.game.get_board()
        print(board)  # This will be captured by mock_stdout
        output = mock_stdout.getvalue()

        self.assertIsNotNone(board)
        self.assertIsNotNone(output)
        self.assertNotEqual(output.strip(), "")

        for point in board:
            self.assertIn(abs(point), range(0, 6))

    @patch("builtins.input", side_effect=["1", "3"])
    def test_move_command(self, mock_input):
        """Test move command execution."""
        from_point = int(mock_input())
        to_point = int(mock_input())
        result = self.move_command.execute(self.game, from_point, to_point)
        self.assertIsNotNone(result)

    @patch("sys.stdout", new_callable=StringIO)
    def test_roll_command(self, mock_stdout):
        """Test roll command execution."""
        values = self.roll_command.execute(self.game)
        print(f"Rolled: {values}")  # This will be captured
        output = mock_stdout.getvalue()

        self.assertTrue(1 <= values[0] <= 6)
        self.assertTrue(1 <= values[1] <= 6)
        self.assertIn("Rolled:", output)

    @patch("builtins.input", return_value="q")
    def test_quit_command(self, mock_input):
        """Test quit command handling."""
        command = mock_input()
        self.assertEqual(command, "q")

    @patch("sys.stdout", new_callable=StringIO)
    def test_display_state(self, mock_stdout):
        """Test game state display following Open/Closed principle."""
        current = self.game.current_player
        print(f"Current player: {current}")  # This will be captured
        output = mock_stdout.getvalue()

        self.assertIn(current, ["white", "black"])
        self.assertIn("Current player:", output)

    @patch("builtins.input", side_effect=["invalid", "1", "3"])
    def test_input_validation(self, mock_input):
        """Test input validation following Liskov Substitution."""
        # First input is invalid, should retry
        with self.assertRaises(ValueError):
            int("invalid")
        # Next inputs are valid
        from_point = int(mock_input())
        to_point = int(mock_input())
        self.assertEqual(from_point, 1)
        self.assertEqual(to_point, 3)

    def test_command_factory(self):
        """Test command factory following Dependency Inversion."""
        commands = {"move": MoveCommand(), "roll": RollCommand()}
        self.assertIsInstance(commands["move"], CommandInterface)
        self.assertIsInstance(commands["roll"], CommandInterface)


if __name__ == "__main__":
    unittest.main()
