"""Test module for Checker class."""

import unittest
from core.Checker import Checker


class TestChecker(unittest.TestCase):
    """Test cases for Checker piece functionality."""

    def setUp(self):
        """Set up test fixtures before each test."""
        self.white_checker = Checker("white", 1)
        self.black_checker = Checker("black", 1)
        self.board = {
            1: [self.white_checker],
            2: [],
            3: [self.black_checker],
            4: [Checker("black", 4), Checker("black", 4)],
            5: [Checker("white", 5)],
        }

    def test_move_to_empty_point(self):
        """Test moving to an empty point."""
        self.assertTrue(self.white_checker.can_move_to(2, self.board))

    def test_move_to_own_point(self):
        """Test moving to a point with own checkers."""
        self.assertTrue(self.white_checker.can_move_to(5, self.board))

    def test_move_to_single_opponent_checker(self):
        """Test hitting a single opponent checker."""
        self.assertTrue(self.white_checker.can_move_to(3, self.board))

    def test_move_to_blocked_point(self):
        """Test moving to a blocked point (2+ opponent checkers)."""
        self.assertFalse(self.white_checker.can_move_to(4, self.board))

    def test_move_updates_position(self):
        """Test position update after moving."""
        initial_pos = self.white_checker.position
        self.white_checker.move(2, self.board)
        self.assertNotEqual(self.white_checker.position, initial_pos)
        self.assertEqual(self.white_checker.position, 2)

    def test_move_to_blocked_point_fails(self):
        """Test failed move to blocked point."""
        initial_pos = self.white_checker.position
        moved = self.white_checker.move(4, self.board)
        self.assertFalse(moved)
        self.assertEqual(self.white_checker.position, initial_pos)

    def test_checker_color(self):
        """Test valid checker colors."""
        self.assertIn(self.white_checker.color, ["white", "black"])
        self.assertIn(self.black_checker.color, ["white", "black"])

    def test_cannot_move_from_bar_to_blocked(self):
        """Test moving from bar to blocked point."""
        self.white_checker.send_to_bar()
        self.board[1] = [Checker("black", 1), Checker("black", 1)]
        self.assertFalse(self.white_checker.can_move_to(1, self.board))
        self.assertTrue(self.white_checker.is_on_bar)

    def test_bear_off(self):
        """Test bearing off conditions."""
        self.white_checker.position = 23  # Home board position
        all_home = True  # All checkers in home board
        self.assertTrue(self.white_checker.can_bear_off(all_home))
        self.white_checker.bear_off()
        self.assertTrue(self.white_checker.is_borne_off)

    def test_invalid_color(self):
        """Test invalid checker color handling."""
        with self.assertRaises(ValueError):
            Checker("red", 1)


if __name__ == "__main__":
    unittest.main()
