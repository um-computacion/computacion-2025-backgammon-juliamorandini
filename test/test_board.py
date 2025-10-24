import unittest
from core.board import Board


class TestBackgammonBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board.reset()

    # --- Utility & Boundary Tests ---

    def test_initial_state(self):
        self.assertEqual(len(self.board.points), 24)
        self.assertEqual(self.board.points[0], ["B", "B"])
        self.assertEqual(self.board.points[5], ["W"] * 5)
        self.assertTrue(self.board.is_valid())

    def test_get_set_point_boundaries(self):
        self.assertEqual(len(self.board.get_point(5)), 5)

        self.assertEqual(self.board.get_point(-1), [])
        self.assertEqual(self.board.get_point(24), [])

        self.board.set_point(1, ["B", "B", "B"])
        self.assertEqual(self.board.points[1], ["B", "B", "B"])

        initial_len = len(self.board.points)
        self.board.set_point(24, ["W"])
        self.assertEqual(len(self.board.points), initial_len)

    def test_is_valid_mixed_colors(self):
        self.assertTrue(self.board.is_valid())

        self.board.points[5] = ["W", "B"]
        self.assertFalse(self.board.is_valid())

        self.board.points = [[] for _ in range(24)]
        self.assertTrue(self.board.is_valid())

    # --- is_valid_move Tests ---

    def test_is_valid_move_comprehensive(self):
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = ["W"]
        self.board.points[15] = ["B"]

        self.assertFalse(self.board.is_valid_move(-1, 5, "W"))

        self.assertFalse(self.board.is_valid_move(10, 24, "W"))

        self.board.bar["W"] = 1
        self.assertFalse(self.board.is_valid_move(10, 12, "W"))
        self.board.bar["W"] = 0

        self.assertFalse(self.board.is_valid_move(1, 3, "W"))

        self.assertFalse(self.board.is_valid_move(15, 17, "W"))

        self.board.points[12] = ["B", "B"]
        self.assertFalse(self.board.is_valid_move(10, 12, "W"))

        self.assertTrue(self.board.is_valid_move(10, 11, "W"))

        self.assertTrue(self.board.is_valid_move(10, 15, "W"))

    def test_comprehensive_move_validation(self):
        """Test comprehensive move validation scenarios."""
        # Test invalid moves
        self.assertFalse(self.board.is_valid_move(-1, 5, "W"))
        self.assertFalse(self.board.is_valid_move(24, 5, "W"))
        self.assertFalse(self.board.is_valid_move(5, -1, "W"))
        self.assertFalse(self.board.is_valid_move(5, 24, "W"))

        # Test moves with pieces on bar
        self.board.bar["W"] = 1
        self.assertFalse(self.board.is_valid_move(5, 7, "W"))

        # Test moving opponent's piece
        self.board.points[5] = ["B"]
        self.assertFalse(self.board.is_valid_move(5, 7, "W"))

        # Test moving to blocked point
        self.board.points[7] = ["B", "B"]
        self.assertFalse(self.board.is_valid_move(5, 7, "W"))

    # --- move_checker Tests ---

    def test_move_checker_hit(self):
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = ["W"]
        self.board.points[15] = ["B"]
        self.board.bar["B"] = 0

        self.assertTrue(self.board.move_checker(10, 15, "W"))
        self.assertEqual(self.board.points[15], ["W"])
        self.assertEqual(self.board.points[10], [])
        self.assertEqual(self.board.bar["B"], 1)

    def test_move_checker_stack(self):
        self.board.points = [[] for _ in range(24)]
        self.board.points[5] = ["W", "W", "W"]
        self.board.points[10] = ["W"]

        self.assertTrue(self.board.move_checker(10, 5, "W"))
        self.assertEqual(len(self.board.points[5]), 4)
        self.assertEqual(self.board.points[5], ["W", "W", "W", "W"])

    def test_move_checker_invalid_move(self):
        self.assertFalse(self.board.move_checker(0, 1, "W"))
        self.assertFalse(self.board.move_checker(1, 2, "W"))

    # NEW: Test simple non-hitting move (covers the main success path)
    def test_move_checker_empty_target(self):
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = ["W"]
        self.assertTrue(self.board.move_checker(10, 14, "W"))
        self.assertEqual(self.board.points[14], ["W"])
        self.assertEqual(self.board.points[10], [])
        self.assertEqual(self.board.bar["B"], 0)

    # NEW: Test move_checker failure for an invalid move (separate from the pre-test failures)
    def test_move_checker_invalid_target_blocked(self):
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = ["W"]
        self.board.points[15] = ["B", "B"]
        # Attempt to move W from 10 to B's prime at 15
        self.assertFalse(self.board.move_checker(10, 15, "W"))
        self.assertEqual(len(self.board.points[15]), 2)  # State should be unchanged

    # --- Bar Entry Tests ---

    def test_can_enter_from_bar_comprehensive(self):
        self.board.points = [[] for _ in range(24)]
        self.board.set_point(19, ["B"])

        self.assertFalse(self.board.can_enter_from_bar("W", 24))

        self.assertTrue(self.board.can_enter_from_bar("W", 18))

        self.assertTrue(self.board.can_enter_from_bar("W", 19))

        self.board.set_point(20, ["B", "B"])
        self.assertFalse(self.board.can_enter_from_bar("W", 20))

        self.board.set_point(21, ["W"])
        self.assertTrue(self.board.can_enter_from_bar("W", 21))

    def test_move_checker_from_bar_comprehensive(self):
        self.board.bar = {"W": 1, "B": 1}
        self.board.points = [[] for _ in range(24)]

        self.assertFalse(self.board.move_checker_from_bar(5, "W"))

        self.assertFalse(self.board.move_checker_from_bar(18, "B"))

        self.board.set_point(20, ["B", "B"])
        self.assertFalse(self.board.move_checker_from_bar(20, "W"))
        self.board.set_point(20, [])

        self.assertTrue(self.board.move_checker_from_bar(22, "W"))
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.points[22], ["W"])

        self.board.bar["B"] = 1
        self.board.set_point(1, ["W"])
        self.assertTrue(self.board.move_checker_from_bar(1, "B"))
        self.assertEqual(self.board.bar["B"], 0)
        self.assertEqual(self.board.bar["W"], 1)
        self.assertEqual(self.board.points[1], ["B"])

    def test_move_checker_from_bar_no_pieces(self):
        self.board.bar = {"W": 0, "B": 0}
        self.assertFalse(self.board.move_checker_from_bar(22, "W"))

    # NEW: Test bar entry and stacking on own pieces
    def test_move_checker_from_bar_stack(self):
        self.board.points = [[] for _ in range(24)]
        self.board.bar["W"] = 1
        self.board.set_point(22, ["W"])

        self.assertTrue(self.board.move_checker_from_bar(22, "W"))
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.points[22], ["W", "W"])

    # NEW: Test bar entry failure due to incorrect home board range check
    def test_move_checker_from_bar_wrong_range(self):
        self.board.bar["W"] = 1
        # White must enter 18-23. Try 17.
        self.assertFalse(self.board.move_checker_from_bar(17, "W"))
        self.assertEqual(self.board.bar["W"], 1)  # Must remain on bar

    # --- Bear Off Tests ---

    def test_can_bear_off_comprehensive(self):
        self.board.points = [[] for _ in range(24)]

        self.board.bar["W"] = 1
        self.assertFalse(self.board.can_bear_off("W"))
        self.board.bar["W"] = 0

        self.board.points[17] = ["W"]
        self.assertFalse(self.board.can_bear_off("W"))
        self.board.points = [[] for _ in range(24)]

        self.board.points[6] = ["B"]
        self.assertFalse(self.board.can_bear_off("B"))
        self.board.points = [[] for _ in range(24)]

        self.board.points[18] = ["W"] * 15
        self.assertTrue(self.board.can_bear_off("W"))

        self.board.points = [[] for _ in range(24)]
        self.board.points[5] = ["B"] * 15
        self.assertTrue(self.board.can_bear_off("B"))

    # NEW: Test can_bear_off for Black with pieces spread across home board
    def test_can_bear_off_black_spread(self):
        self.board.points = [[] for _ in range(24)]
        self.board.points[0] = ["B"]
        self.board.points[5] = ["B"] * 14
        self.assertTrue(self.board.can_bear_off("B"))

    def test_bear_off_comprehensive(self):
        self.board.points = [[] for _ in range(24)]
        self.board.points[18] = ["W"] * 10
        self.board.points[19] = ["W"] * 5
        self.board.points[5] = ["B"] * 15
        self.assertTrue(self.board.can_bear_off("W"))
        self.assertTrue(self.board.can_bear_off("B"))

        self.assertFalse(self.board.bear_off("W", 23))

        self.assertFalse(self.board.bear_off("W", 5))

        self.assertTrue(self.board.bear_off("W", 19))
        self.assertEqual(self.board.borne_off["W"], 1)
        self.assertEqual(len(self.board.points[19]), 4)

        self.assertTrue(self.board.bear_off("B", 5))
        self.assertEqual(self.board.borne_off["B"], 1)
        self.assertEqual(len(self.board.points[5]), 14)

    # NEW: Test bear_off fails when can_bear_off is false
    def test_bear_off_not_eligible(self):
        # Initial setup: pieces outside home board
        self.board.reset()
        # Even though a piece is at P23, the player is not eligible.
        self.assertFalse(self.board.bear_off("W", 23))
        self.assertEqual(self.board.borne_off["W"], 0)


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)
