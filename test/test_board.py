"""
Unit tests for the core Board class.

This module tests all aspects of the Board class, including initialization,
move validation, checker movement, bar entry, and bearing off.
"""

import unittest
from core.board import Board


class TestBackgammonBoard(unittest.TestCase):
    """Test suite for the Board class."""

    def setUp(self):
        """Set up a new, reset board instance before each test."""
        self.board = Board()
        self.board.reset()

    # --- Utility & Boundary Tests ---

    def test_initial_state(self):
        """Test the board's default initial checker setup."""
        self.assertEqual(len(self.board.points), 24)
        self.assertEqual(self.board.points[0], ["B", "B"])
        self.assertEqual(self.board.points[5], ["W"] * 5)
        self.assertTrue(self.board.is_valid())

    def test_get_set_point_boundaries(self):
        """Test getting/setting points, including out-of-bounds cases."""
        self.assertEqual(len(self.board.get_point(5)), 5)

        # Test out-of-bounds get
        self.assertEqual(self.board.get_point(-1), [])
        self.assertEqual(self.board.get_point(24), [])

        # Test valid set
        self.board.set_point(1, ["B", "B", "B"])
        self.assertEqual(self.board.points[1], ["B", "B", "B"])

        # Test out-of-bounds set
        initial_len = len(self.board.points)
        self.board.set_point(24, ["W"])
        self.assertEqual(len(self.board.points), initial_len)

    def test_is_valid_mixed_colors(self):
        """Test that is_valid() detects points with mixed checker colors."""
        self.assertTrue(self.board.is_valid())

        self.board.points[5] = ["W", "B"]
        self.assertFalse(self.board.is_valid())

        self.board.points = [[] for _ in range(24)]
        self.assertTrue(self.board.is_valid())

    # --- is_valid_move Tests ---

    def test_is_valid_move_comprehensive(self):
        """Test various valid and invalid move scenarios."""
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = ["W"]
        self.board.points[15] = ["B"]

        # Test out-of-bounds
        self.assertFalse(self.board.is_valid_move(-1, 5, "W"))
        self.assertFalse(self.board.is_valid_move(10, 24, "W"))

        # Test moving from point while on bar
        self.board.bar["W"] = 1
        self.assertFalse(self.board.is_valid_move(10, 12, "W"))
        self.board.bar["W"] = 0

        # Test moving from an empty point
        self.assertFalse(self.board.is_valid_move(1, 3, "W"))

        # Test moving opponent's piece
        self.assertFalse(self.board.is_valid_move(15, 17, "W"))

        # Test moving to a blocked point
        self.board.points[12] = ["B", "B"]
        self.assertFalse(self.board.is_valid_move(10, 12, "W"))

        # Test valid move to empty point
        self.assertTrue(self.board.is_valid_move(10, 11, "W"))

        # Test valid move (hit)
        self.assertTrue(self.board.is_valid_move(10, 15, "W"))

    def test_comprehensive_move_validation(self):
        """Test comprehensive move validation scenarios."""
        # Test invalid moves (out of bounds)
        self.assertFalse(self.board.is_valid_move(-1, 5, "W"))
        self.assertFalse(self.board.is_valid_move(24, 5, "W"))
        self.assertFalse(self.board.is_valid_move(5, -1, "W"))
        self.assertFalse(self.board.is_valid_move(5, 24, "W"))

        # Test moves with pieces on bar
        self.board.bar["W"] = 1
        self.assertFalse(self.board.is_valid_move(5, 7, "W"))
        self.board.bar["W"] = 0  # Reset for next test

        # Test moving opponent's piece
        self.board.points[5] = ["B"]
        self.assertFalse(self.board.is_valid_move(5, 7, "W"))
        self.board.points[5] = ["W"] * 5  # Reset for next test

        # Test moving to blocked point
        self.board.points[7] = ["B", "B"]
        self.assertFalse(self.board.is_valid_move(5, 7, "W"))

    # --- move_checker Tests ---

    def test_move_checker_hit(self):
        """Test moving a checker to hit an opponent's blot."""
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = ["W"]
        self.board.points[15] = ["B"]
        self.board.bar["B"] = 0

        self.assertTrue(self.board.move_checker(10, 15, "W"))
        self.assertEqual(self.board.points[15], ["W"])
        self.assertEqual(self.board.points[10], [])
        self.assertEqual(self.board.bar["B"], 1)

    def test_move_checker_stack(self):
        """Test moving a checker to stack on one's own pieces."""
        self.board.points = [[] for _ in range(24)]
        self.board.points[5] = ["W", "W", "W"]
        self.board.points[10] = ["W"]

        self.assertTrue(self.board.move_checker(10, 5, "W"))
        self.assertEqual(len(self.board.points[5]), 4)
        self.assertEqual(self.board.points[5], ["W", "W", "W", "W"])

    def test_move_checker_invalid_move(self):
        """Test that move_checker fails for an invalid move (e.g., wrong color)."""
        # White trying to move Black's piece at 0
        self.assertFalse(self.board.move_checker(0, 1, "W"))
        # White trying to move from an empty point
        self.assertFalse(self.board.move_checker(1, 2, "W"))

    def test_move_checker_empty_target(self):
        """Test a simple move to an empty target point."""
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = ["W"]
        self.assertTrue(self.board.move_checker(10, 14, "W"))
        self.assertEqual(self.board.points[14], ["W"])
        self.assertEqual(self.board.points[10], [])
        self.assertEqual(self.board.bar["B"], 0)

    def test_move_checker_invalid_target_blocked(self):
        """Test that move_checker fails if the target point is blocked."""
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = ["W"]
        self.board.points[15] = ["B", "B"]
        # Attempt to move W from 10 to B's prime at 15
        self.assertFalse(self.board.move_checker(10, 15, "W"))
        self.assertEqual(len(self.board.points[15]), 2)  # State should be unchanged

    # --- Bar Entry Tests ---

    def test_can_enter_from_bar_comprehensive(self):
        """Test various scenarios for entering from the bar."""
        self.board.points = [[] for _ in range(24)]
        self.board.set_point(19, ["B"])

        # Test out of bounds
        self.assertFalse(self.board.can_enter_from_bar("W", 24))

        # Test valid empty point
        self.assertTrue(self.board.can_enter_from_bar("W", 18))

        # Test valid hit
        self.assertTrue(self.board.can_enter_from_bar("W", 19))

        # Test blocked point
        self.board.set_point(20, ["B", "B"])
        self.assertFalse(self.board.can_enter_from_bar("W", 20))

        # Test stacking on own piece
        self.board.set_point(21, ["W"])
        self.assertTrue(self.board.can_enter_from_bar("W", 21))

    def test_move_checker_from_bar_comprehensive(self):
        """Test moving checkers from the bar for both players."""
        self.board.bar = {"W": 1, "B": 1}
        self.board.points = [[] for _ in range(24)]

        # Test White entering Black's home
        self.assertFalse(self.board.move_checker_from_bar(5, "W"))

        # Test Black entering White's home
        self.assertFalse(self.board.move_checker_from_bar(18, "B"))

        # Test entering a blocked point
        self.board.set_point(20, ["B", "B"])
        self.assertFalse(self.board.move_checker_from_bar(20, "W"))
        self.board.set_point(20, [])

        # Test valid entry for White
        self.assertTrue(self.board.move_checker_from_bar(22, "W"))
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.points[22], ["W"])

        # Test valid entry for Black (with hit)
        self.board.bar["B"] = 1
        self.board.set_point(1, ["W"])
        self.assertTrue(self.board.move_checker_from_bar(1, "B"))
        self.assertEqual(self.board.bar["B"], 0)
        self.assertEqual(self.board.bar["W"], 1)  # White checker sent to bar
        self.assertEqual(self.board.points[1], ["B"])

    def test_move_checker_from_bar_no_pieces(self):
        """Test moving from bar fails when the bar is empty."""
        self.board.bar = {"W": 0, "B": 0}
        self.assertFalse(self.board.move_checker_from_bar(22, "W"))

    def test_move_checker_from_bar_stack(self):
        """Test entering from bar and stacking on an existing piece."""
        self.board.points = [[] for _ in range(24)]
        self.board.bar["W"] = 1
        self.board.set_point(22, ["W"])

        self.assertTrue(self.board.move_checker_from_bar(22, "W"))
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.points[22], ["W", "W"])

    def test_move_checker_from_bar_wrong_range(self):
        """Test that entry from bar fails if target is outside home board."""
        self.board.bar["W"] = 1
        # White must enter 18-23. Try 17.
        self.assertFalse(self.board.move_checker_from_bar(17, "W"))
        self.assertEqual(self.board.bar["W"], 1)  # Must remain on bar

    # --- Bear Off Tests ---

    def test_can_bear_off_comprehensive(self):
        """Test eligibility to bear off under various conditions."""
        self.board.points = [[] for _ in range(24)]

        # Test failure if on bar
        self.board.bar["W"] = 1
        self.assertFalse(self.board.can_bear_off("W"))
        self.board.bar["W"] = 0

        # Test failure if pieces are outside home (White)
        self.board.points[17] = ["W"]
        self.assertFalse(self.board.can_bear_off("W"))
        self.board.points = [[] for _ in range(24)]

        # Test failure if pieces are outside home (Black)
        self.board.points[6] = ["B"]
        self.assertFalse(self.board.can_bear_off("B"))
        self.board.points = [[] for _ in range(24)]

        # Test success (White)
        self.board.points[18] = ["W"] * 15
        self.assertTrue(self.board.can_bear_off("W"))

        # Test success (Black)
        self.board.points = [[] for _ in range(24)]
        self.board.points[5] = ["B"] * 15
        self.assertTrue(self.board.can_bear_off("B"))

    def test_can_bear_off_black_spread(self):
        """Test can_bear_off for Black with pieces spread across home."""
        self.board.points = [[] for _ in range(24)]
        self.board.points[0] = ["B"]
        self.board.points[5] = ["B"] * 14
        self.assertTrue(self.board.can_bear_off("B"))

    def test_bear_off_comprehensive(self):
        """Test the bear_off action for both players."""
        self.board.points = [[] for _ in range(24)]
        self.board.points[18] = ["W"] * 10
        self.board.points[19] = ["W"] * 5
        self.board.points[5] = ["B"] * 15
        self.assertTrue(self.board.can_bear_off("W"))
        self.assertTrue(self.board.can_bear_off("B"))

        # Test bearing off from an empty point
        self.assertFalse(self.board.bear_off("W", 23))

        # Test bearing off from an opponent's point
        self.assertFalse(self.board.bear_off("W", 5))

        # Test valid bear off (White)
        self.assertTrue(self.board.bear_off("W", 19))
        self.assertEqual(self.board.borne_off["W"], 1)
        self.assertEqual(len(self.board.points[19]), 4)

        # Test valid bear off (Black)
        self.assertTrue(self.board.bear_off("B", 5))
        self.assertEqual(self.board.borne_off["B"], 1)
        self.assertEqual(len(self.board.points[5]), 14)

    def test_bear_off_not_eligible(self):
        """Test that bear_off fails if can_bear_off is false."""
        # Initial setup: pieces outside home board
        self.board.reset()
        # Even though a piece is at P23, the player is not eligible.
        self.assertFalse(self.board.bear_off("W", 23))
        self.assertEqual(self.board.borne_off["W"], 0)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
