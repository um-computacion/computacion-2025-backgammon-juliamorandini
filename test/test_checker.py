"""Test module for Checker class."""

import unittest
from core.Checker import Checker


class TestChecker(unittest.TestCase):
    def setUp(self):
        self.white_checker = Checker("white", 1)
        self.black_checker = Checker("black", 3)
        self.board = {
            1: [self.white_checker],
            2: [],
            3: [self.black_checker],
            4: [Checker("black", 4), Checker("black", 4)],
            5: [Checker("white", 5)],
        }

    # --- Tests for can_move_to ---

    def test_move_to_empty_point(self):
        self.assertTrue(self.white_checker.can_move_to(2, self.board))

    def test_move_to_own_point(self):
        self.assertTrue(self.white_checker.can_move_to(5, self.board))

    def test_move_to_single_opponent_checker(self):
        self.assertTrue(self.white_checker.can_move_to(3, self.board))

    def test_move_to_blocked_point(self):
        self.assertFalse(self.white_checker.can_move_to(4, self.board))

    def test_can_move_to_out_of_bounds(self):
        # Covers 'if not (0 <= point < 24):' branch in can_move_to
        self.assertFalse(self.white_checker.can_move_to(24, self.board))
        self.assertFalse(self.white_checker.can_move_to(-1, self.board))

    # --- Tests for move_to / move ---

    def test_move_to_updates_position(self):
        initial_pos = self.white_checker.position
        # Use move_to to cover its success path
        self.assertTrue(self.white_checker.move_to(23))
        self.assertNotEqual(initial_pos, 23)
        self.assertEqual(self.white_checker.position, 23)
        self.assertFalse(self.white_checker.is_on_bar)
        self.assertFalse(self.white_checker.is_borne_off)

    def test_move_to_out_of_bounds_fails(self):
        # Covers the 'return False' branch in move_to
        initial_pos = self.white_checker.position
        self.assertFalse(self.white_checker.move_to(24))
        self.assertEqual(self.white_checker.position, initial_pos)

    def test_move_to_blocked_point_fails(self):
        initial_pos = self.white_checker.position
        moved = self.white_checker.move(4, self.board)
        self.assertFalse(moved)
        self.assertEqual(self.white_checker.position, initial_pos)

    def test_move_success_removes_from_old_position(self):
        # Tests the board update logic within move (where old_position is an int)
        self.white_checker.move(2, self.board)
        self.assertEqual(self.white_checker.position, 2)
        # Check that checker was removed from old position (point 1)
        self.assertEqual(self.board[1], [])
        # Check that checker was added to new position (point 2)
        self.assertEqual(self.board[2][0], self.white_checker)

    def test_move_comprehensive(self):
        """Test comprehensive move scenarios."""
        # Test moving from bar
        self.white_checker.send_to_bar()
        self.assertTrue(self.white_checker.move(1, self.board))
        self.assertEqual(self.white_checker.position, 1)

        # Test moving to occupied point
        self.white_checker.position = 2
        self.board[3] = [self.black_checker]
        self.assertTrue(self.white_checker.move(3, self.board))

        # Test moving to blocked point
        self.board[4] = [Checker("black", 4), Checker("black", 4)]
        self.assertFalse(self.white_checker.move(4, self.board))

    def test_position_property(self):
        """Test position property behavior."""
        self.assertEqual(self.white_checker.position, 1)
        self.white_checker.position = 5
        self.assertEqual(self.white_checker.position, 5)
        self.white_checker.send_to_bar()
        self.assertEqual(self.white_checker.position, "bar")
        self.white_checker.bear_off()
        self.assertEqual(self.white_checker.position, "off")

    def test_state_transitions(self):
        """Test state transitions of checker."""
        # Initial state
        self.assertFalse(self.white_checker.is_on_bar)
        self.assertFalse(self.white_checker.is_borne_off)

        # Send to bar
        self.white_checker.send_to_bar()
        self.assertTrue(self.white_checker.is_on_bar)
        self.assertFalse(self.white_checker.is_borne_off)

        # Move from bar
        self.white_checker.move(1, self.board)
        self.assertFalse(self.white_checker.is_on_bar)

        # Bear off
        self.white_checker.bear_off()
        self.assertTrue(self.white_checker.is_borne_off)
        self.assertFalse(self.white_checker.is_on_bar)

    # --- Utility Tests ---

    def test_checker_color(self):
        self.assertIn(self.white_checker.color, ["white", "black"])
        self.assertIn(self.black_checker.color, ["white", "black"])

    def test_invalid_color(self):
        with self.assertRaises(ValueError):
            Checker("red", 1)

    # --- Bar and Bear Off Tests ---

    def test_send_to_bar(self):
        self.white_checker.send_to_bar()
        self.assertTrue(self.white_checker.is_on_bar)
        self.assertEqual(self.white_checker.position, "bar")

    def test_bear_off_updates_state(self):
        self.white_checker.bear_off()
        self.assertTrue(self.white_checker.is_borne_off)
        self.assertFalse(self.white_checker.is_on_bar)
        self.assertEqual(self.white_checker.position, "off")

    def test_cannot_move_from_bar_to_blocked(self):
        self.white_checker.send_to_bar()
        self.board[1] = [Checker("black", 1), Checker("black", 1)]
        self.assertFalse(self.white_checker.can_move_to(1, self.board))
        self.assertTrue(self.white_checker.is_on_bar)

    # NEW: Comprehensive can_bear_off tests
    def test_can_bear_off_comprehensive(self):
        # 1. Failure: All home is False
        self.assertFalse(self.white_checker.can_bear_off(False))

        # 2. Failure: Not an int position ('bar') - covers 'if not isinstance(self.position, int):'
        self.white_checker.send_to_bar()
        self.assertFalse(self.white_checker.can_bear_off(True))

        # 3. Failure: Not in home board (White, P1) - covers 'self.position >= 18' failure
        self.white_checker.position = 1
        self.assertFalse(self.white_checker.can_bear_off(True))

        # 4. Success: White in home board (P18) - covers 'self.position >= 18' success
        self.white_checker.position = 18
        self.assertTrue(self.white_checker.can_bear_off(True))

        # 5. Failure: Not in home board (Black, P6) - covers 'self.position <= 5' failure
        self.black_checker.position = 6
        self.assertFalse(self.black_checker.can_bear_off(True))

        # 6. Success: Black in home board (P5) - covers 'self.position <= 5' success
        self.black_checker.position = 5
        self.assertTrue(self.black_checker.can_bear_off(True))


if __name__ == "__main__":
    unittest.main()
