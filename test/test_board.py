import unittest
from core.board import Board


class TestBackgammonBoard(unittest.TestCase):
    """Test suite for Backgammon board functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.board = Board()
        self.board.reset()

    def test_board_has_24_points(self):
        self.assertEqual(len(self.board.points), 24, "El tablero debe tener 24 puntos.")

    def test_initial_setup(self):
        """Test initial board setup"""
        expected_setup = {
            0: ["B", "B"],
            5: ["W"] * 5,
            7: ["W"] * 3,
            11: ["W"] * 5,
            12: ["B"] * 5,
            16: ["B"] * 3,
            18: ["B"] * 5,
            23: ["W", "W"],
        }

        for point, expected_checkers in expected_setup.items():
            with self.subTest(point=point):
                self.assertEqual(
                    self.board.points[point],
                    expected_checkers,
                    f"Point {point+1} should have {expected_checkers}",
                )

    def test_no_mixed_checkers_on_point(self):
        self.board.points[0] = ["W", "B"]
        self.assertFalse(
            self.board.is_valid(),
            "No puede haber fichas de ambos colores en el mismo punto.",
        )

    def test_move_checker(self):
        """Test moving a checker"""
        self.board.points[0] = ["B"]
        result = self.board.move_checker(0, 1, "B")
        self.assertTrue(result)
        self.assertEqual(len(self.board.points[0]), 0)
        self.assertEqual(self.board.points[1], ["B"])

    def test_capture_checker(self):
        self.board.points[5] = ["B"]
        self.board.points[4] = ["W"]
        self.board.move_checker(4, 5, "W")
        self.assertEqual(self.board.bar["B"], 1)
        self.assertEqual(self.board.points[5], ["W"])

    def test_illegal_move(self):
        self.board.points[5] = ["B", "B"]
        self.assertFalse(self.board.is_valid_move(4, 5, "W"))

    def test_cannot_move_from_empty_point(self):
        self.board.points[10] = []
        self.assertFalse(self.board.is_valid_move(10, 12, "W"))

    def test_cannot_move_opponent_checker(self):
        self.board.points[8] = ["B"]
        self.assertFalse(self.board.is_valid_move(8, 10, "W"))

    def test_bar_priority(self):
        self.board.bar["W"] = 1
        self.assertFalse(self.board.is_valid_move(0, 2, "W"))

    def test_bear_off_only_when_all_in_home(self):
        self.board.points = [[] for _ in range(24)]
        self.board.points[18] = ["W"] * 15
        result = self.board.bear_off("W", 18)
        self.assertTrue(result)
        self.assertEqual(len(self.board.points[18]), 14)
        self.assertEqual(self.board.borne_off["W"], 1)

    def test_bear_off(self):
        self.board.points = [[] for _ in range(24)]
        self.board.points[18] = ["W"]
        result = self.board.bear_off("W", 18)
        self.assertTrue(result)
        self.assertEqual(self.board.points[18], [])
        self.assertEqual(self.board.borne_off["W"], 1)

    def test_bear_off_invalid(self):
        self.board.points = [[] for _ in range(24)]
        result = self.board.bear_off("W", 18)
        self.assertFalse(result)

        self.board.points[10] = ["B"]
        result = self.board.bear_off("W", 10)
        self.assertFalse(result)

    def test_blocked_entry_from_bar(self):
        self.board.bar["W"] = 1
        self.board.points[0] = ["B", "B"]
        self.assertFalse(self.board.can_enter_from_bar("W", 0))

    def test_move_checker_from_bar_white(self):
        self.board.bar["W"] = 1
        self.assertFalse(self.board.move_checker_from_bar(0, "W"))
        self.assertTrue(self.board.move_checker_from_bar(18, "W"))
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.points[18][-1], "W")

    def test_move_checker_from_bar_black(self):
        self.board.bar["B"] = 1
        self.assertFalse(self.board.move_checker_from_bar(18, "B"))
        self.assertTrue(self.board.move_checker_from_bar(0, "B"))
        self.assertEqual(self.board.bar["B"], 0)
        self.assertEqual(self.board.points[0][-1], "B")

    def test_move_checker_from_empty_bar(self):
        self.assertFalse(self.board.move_checker_from_bar(18, "W"))
        self.assertFalse(self.board.move_checker_from_bar(0, "B"))

    def test_move_checker_to_blocked_point(self):
        self.board.points[18] = ["B", "B"]
        self.board.bar["W"] = 1
        self.assertFalse(self.board.move_checker_from_bar(18, "W"))

    def test_invalid_point_moves(self):
        self.assertFalse(self.board.is_valid_move(-1, 5, "W"))
        self.assertFalse(self.board.is_valid_move(5, 24, "W"))
        self.assertFalse(self.board.is_valid_move(24, 5, "W"))

    def test_hit_opponent_from_bar(self):
        self.board.points[18] = ["B"]
        self.board.bar["W"] = 1
        self.assertTrue(self.board.move_checker_from_bar(18, "W"))
        self.assertEqual(self.board.bar["B"], 1)
        self.assertEqual(self.board.points[18], ["W"])

    def test_bear_off_with_pieces_outside(self):
        # Test for White
        self.board.points = [[] for _ in range(24)]
        self.board.points[0] = ["W"]
        self.board.points[23] = ["W"]
        self.assertFalse(self.board.bear_off("W", 23))

        # Test for Black
        self.board.points = [[] for _ in range(24)]
        self.board.points[23] = ["B"]
        self.board.points[0] = ["B"]
        self.assertFalse(self.board.bear_off("B", 0))

    def test_can_bear_off_edge_cases(self):
        self.board.points = [[] for _ in range(24)]
        self.assertTrue(self.board.can_bear_off("W"))
        self.assertTrue(self.board.can_bear_off("B"))

        self.board.bar["W"] = 1
        self.assertFalse(self.board.can_bear_off("W"))
        self.board.bar["B"] = 1
        self.assertFalse(self.board.can_bear_off("B"))

    def test_move_checker_invalid_color(self):
        self.board.points[0] = ["X"]
        self.assertFalse(self.board.move_checker(0, 1, "W"))

    def test_enter_from_bar_invalid_points(self):
        self.board.bar["W"] = 1
        self.board.bar["B"] = 1

        for point in range(18):
            self.assertFalse(self.board.move_checker_from_bar(point, "W"))

        for point in range(6, 24):
            self.assertFalse(self.board.move_checker_from_bar(point, "B"))

    def test_point_manipulation(self):
        point = 0
        self.board.points[point] = ["W"]
        self.assertEqual(self.board.points[point], ["W"])
        self.board.points[point] = []
        self.assertEqual(self.board.points[point], [])

    def test_bar_manipulation(self):
        self.board.bar["W"] = 2
        self.assertEqual(self.board.bar["W"], 2)
        self.board.bar["W"] = 0
        self.assertEqual(self.board.bar["W"], 0)

    def test_borne_off_manipulation(self):
        self.board.borne_off["B"] = 3
        self.assertEqual(self.board.borne_off["B"], 3)
        self.board.borne_off["B"] = 0
        self.assertEqual(self.board.borne_off["B"], 0)

    def test_move_checker_to_empty_point(self):
        self.board.points[0] = ["W"]
        self.board.points[1] = []
        self.assertTrue(self.board.move_checker(0, 1, "W"))
        self.assertEqual(self.board.points[0], [])
        self.assertEqual(self.board.points[1], ["W"])

    def test_bar_entrance_with_hit(self):
        self.board.bar["W"] = 1
        self.board.points[18] = ["B"]
        self.assertTrue(self.board.move_checker_from_bar(18, "W"))
        self.assertEqual(self.board.bar["B"], 1)
        self.assertEqual(self.board.points[18], ["W"])
        self.assertEqual(self.board.bar["W"], 0)

    def test_board_state_validation(self):
        self.assertTrue(self.board.is_valid())
        self.board.points[0] = ["W", "B"]
        self.assertFalse(self.board.is_valid())
        self.board.points[0] = []
        self.assertTrue(self.board.is_valid())

    def test_initial_bar_and_borne_off(self):
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.bar["B"], 0)
        self.assertEqual(self.board.borne_off["W"], 0)
        self.assertEqual(self.board.borne_off["B"], 0)

    def test_can_enter_from_bar_empty_point(self):
        empty_point = 18
        self.board.points[empty_point] = []
        self.assertTrue(self.board.can_enter_from_bar("W", empty_point))

    def test_can_enter_from_bar_single_checker(self):
        point = 18
        self.board.points[point] = ["W"]
        self.assertTrue(self.board.can_enter_from_bar("W", point))
        self.board.points[point] = ["B"]
        self.assertTrue(self.board.can_enter_from_bar("W", point))

    def test_can_bear_off_with_all_pieces_home(self):
        self.board.points = [[] for _ in range(24)]
        for i in range(18, 24):
            self.board.points[i] = ["W", "W"]
        self.assertTrue(self.board.can_bear_off("W"))

    def test_move_checker_validation(self):
        self.assertFalse(self.board.move_checker(-1, 5, "W"))
        self.assertFalse(self.board.move_checker(5, 24, "W"))
        self.board.bar["W"] = 1
        self.assertFalse(self.board.move_checker(5, 7, "W"))

    def test_bear_off_from_invalid_point(self):
        self.assertFalse(self.board.bear_off("W", 18))
        self.board.points[18] = ["B"]
        self.assertFalse(self.board.bear_off("W", 18))
        self.board.points[18] = ["W"]
        self.board.bar["W"] = 1
        self.assertFalse(self.board.bear_off("W", 18))

    def test_get_and_set_point(self):
        """Test get_point and set_point methods."""
        # Test get_point with valid point
        self.assertEqual(self.board.get_point(0), ["B", "B"])
        
        # Test get_point with invalid point
        self.assertEqual(self.board.get_point(-1), [])
        self.assertEqual(self.board.get_point(24), [])
        
        # Test set_point with valid point
        self.board.set_point(10, ["W", "W"])
        self.assertEqual(self.board.get_point(10), ["W", "W"])
        
        # Test set_point with invalid point (should not change anything)
        original_point_0 = self.board.get_point(0)
        self.board.set_point(-1, ["W"])
        self.board.set_point(24, ["W"])
        self.assertEqual(self.board.get_point(0), original_point_0)

    def test_move_to_point_with_same_color(self):
        """Test moving to a point with same color checkers."""
        self.board.points[0] = ["B"]
        self.board.points[1] = ["B", "B"]
        self.assertTrue(self.board.move_checker(0, 1, "B"))
        self.assertEqual(self.board.points[1], ["B", "B", "B"])

    def test_can_enter_from_bar_invalid_point(self):
        """Test can_enter_from_bar with invalid point."""
        self.assertFalse(self.board.can_enter_from_bar("W", -1))
        self.assertFalse(self.board.can_enter_from_bar("W", 24))

    def test_reset_functionality(self):
        """Test that reset properly initializes the board."""
        # Modify the board
        self.board.points[0] = ["W"]
        self.board.bar["W"] = 2
        self.board.borne_off["B"] = 3
        
        # Reset and check
        self.board.reset()
        self.assertEqual(self.board.points[0], ["B", "B"])
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.borne_off["B"], 0)


if __name__ == "__main__":
    unittest.main()