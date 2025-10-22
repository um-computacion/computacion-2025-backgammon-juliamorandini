"""Test module for BackgammonGame class."""

import unittest
from core.BackgammonGame import Game


class TestBackgammonGame(unittest.TestCase):
    """Test cases for BackgammonGame."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_initial_board_setup(self):
        """Test initial board configuration."""
        board = self.game.get_board()
        self.assertEqual(board[0], -2)
        self.assertEqual(board[23], 2)

    def test_valid_moves(self):
        """Test valid moves based on dice values."""
        self.game.set_dice([3, 4])
        moves = self.game.get_available_moves()
        self.assertEqual(moves, [3, 4])

    def test_invalid_move(self):
        """Test invalid move detection."""
        result = self.game.make_move(1, 8)
        self.assertFalse(result)

    def test_hitting_blot(self):
        """Test capturing opponent's single piece."""
        self.game.board.points[3] = ["W"]
        self.game.board.points[5] = ["B"]
        result = self.game.make_move(3, 5)
        self.assertTrue(result)

    def test_bearing_off(self):
        """Test bearing off rules."""
        self.game.setup_bearing_off_scenario()
        if self.game.current_player == "white":
            result = self.game.bear_off(18)
        else:
            result = self.game.bear_off(0)
        self.assertTrue(result)

    def test_winner_detection(self):
        """Test winner detection."""
        self.game.setup_winning_scenario()
        self.assertTrue(self.game.check_winner())

    def test_bar_piece_movement(self):
        """Test mandatory bar piece movement."""
        self.game.add_to_bar()
        self.assertTrue(self.game.must_move_from_bar())

    def test_get_entry_point_for_dice(self):
        """Test conversion of dice values to entry points."""
        self.game.current_player = "white"
        self.assertEqual(self.game.get_entry_point_for_dice(1), 23)

        self.game.current_player = "black"
        self.assertEqual(self.game.get_entry_point_for_dice(1), 0)

    def test_switch_player(self):
        """Test switching players."""
        initial = self.game.current_player
        self.game.switch_player()
        self.assertNotEqual(self.game.current_player, initial)

    def test_roll_dice(self):
        """Test dice rolling."""
        moves = self.game.roll_dice()
        self.assertEqual(len(moves), 2)
        for move in moves:
            self.assertTrue(1 <= move <= 6)

    def test_can_bear_off(self):
        """Test bearing off eligibility."""
        self.game.setup_bearing_off_scenario()
        self.assertTrue(self.game.can_bear_off())

    def test_get_current_player_color(self):
        """Test getting current player color code."""
        self.game.current_player = "white"
        self.assertEqual(self.game.get_current_player_color(), "W")

    def test_make_bar_move(self):
        """Test bar moves."""
        self.game.add_to_bar()
        self.game.set_dice([1, 2])

        if self.game.current_player == "white":
            point = 23
        else:
            point = 0

        result = self.game.make_bar_move(point)
        self.assertTrue(result)

    def test_get_bar_pieces(self):
        """Test getting bar pieces count."""
        self.game.add_to_bar()
        self.assertEqual(self.game.get_bar_pieces(), 1)

    def test_set_piece_with_color(self):
        """Test setting pieces with specific color."""
        self.game.set_piece(10, 3, "W")
        self.assertEqual(len(self.game.board.points[10]), 3)


if __name__ == "__main__":
    unittest.main()
