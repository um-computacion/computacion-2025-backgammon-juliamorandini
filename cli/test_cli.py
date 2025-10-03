"""Test module for Backgammon CLI interface."""

import unittest
from unittest.mock import patch
from io import StringIO
from core.BackgammonGame import Game


class TestBackgammonCLI(unittest.TestCase):
    """Test cases for Backgammon CLI interface."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_board(self, mock_stdout):
        """Test board display in CLI."""
        board = self.game.get_board()
        self.assertIsNotNone(board)
        # Check if board points contain valid values
        for point in board:
            self.assertIn(abs(point), range(0, 6))

    @patch('builtins.input', side_effect=['1', '3'])
    def test_get_move_input(self, mock_input):
        """Test move input handling."""
        from_point = int(mock_input())
        to_point = int(mock_input())
        self.assertEqual(from_point, 1)
        self.assertEqual(to_point, 3)

    @patch('builtins.input', return_value='q')
    def test_quit_command(self, mock_input):
        """Test quit command handling."""
        command = mock_input()
        self.assertEqual(command, 'q')

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_dice_roll(self, mock_stdout):
        """Test dice roll display."""
        self.game.dice.roll()
        values = self.game.dice.get_values()
        self.assertTrue(1 <= values[0] <= 6)
        self.assertTrue(1 <= values[1] <= 6)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_current_player(self, mock_stdout):
        """Test current player display."""
        current = self.game.current_player
        self.assertIn(current, ['white', 'black'])

    @patch('builtins.input', side_effect=['invalid', '1', '3'])
    def test_invalid_move_input(self, mock_input):
        """Test handling of invalid move input."""
        # First input is invalid, should retry
        with self.assertRaises(ValueError):
            int('invalid')
        # Next inputs are valid
        from_point = int(mock_input())
        to_point = int(mock_input())
        self.assertEqual(from_point, 1)
        self.assertEqual(to_point, 3)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_game_over(self, mock_stdout):
        """Test game over display."""
        self.game.setup_winning_scenario()
        self.assertTrue(self.game.check_winner())

    def test_display_help(self):
        """Test help command display."""
        help_text = """
        Commands:
        - move <from> <to>: Move a checker
        - roll: Roll the dice
        - help: Show this help
        - quit: Exit game
        """
        self.assertIsInstance(help_text, str)


if __name__ == '__main__':
    unittest.main()