"""Test module for Board class."""

import unittest
from core.board import Board


class TestBackgammonBoard(unittest.TestCase):
    """Test suite for Backgammon board functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.board = Board()

    def test_initialization(self):
        """Test board initialization."""
        self.assertEqual(len(self.board.points), 24)
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.bar["B"], 0)
        self.assertEqual(self.board.borne_off["W"], 0)
        self.assertEqual(self.board.borne_off["B"], 0)

    def test_reset(self):
        """Test board reset to initial position."""
        self.board.reset()
        # Check initial setup
        self.assertEqual(self.board.points[0], ["B", "B"])
        self.assertEqual(len(self.board.points[5]), 5)  # 5 white at point 6
        self.assertEqual(len(self.board.points[23]), 2)  # 2 white at point 24

    def test_is_valid_move_comprehensive(self):
        """Test all validation scenarios for moves."""
        # Test invalid bounds
        self.assertFalse(self.board.is_valid_move(-1, 5, "W"))
        self.assertFalse(self.board.is_valid_move(5, 24, "W"))
        
        # Test bar priority
        self.board.bar["W"] = 1
        self.assertFalse(self.board.is_valid_move(5, 6, "W"))
        self.board.bar["W"] = 0
        
        # Test empty from point
        self.assertFalse(self.board.is_valid_move(10, 11, "W"))
        
        # Test wrong color
        self.board.points[5] = ["B"]
        self.assertFalse(self.board.is_valid_move(5, 6, "W"))
        
        # Test blocked point
        self.board.points[6] = ["B", "B"]
        self.board.points[5] = ["W"]
        self.assertFalse(self.board.is_valid_move(5, 6, "W"))
        
        # Test valid moves
        self.board.points[7] = ["W"]
        self.board.points[8] = []
        self.assertTrue(self.board.is_valid_move(7, 8, "W"))
        
        # Test valid move to own color point
        self.board.points[9] = ["W", "W"]
        self.board.points[10] = ["W"]
        self.assertTrue(self.board.is_valid_move(10, 9, "W"))

    def test_move_checker_comprehensive(self):
        """Test all move scenarios."""
        # Test invalid move returns False
        self.assertFalse(self.board.move_checker(-1, 5, "W"))
        
        # Test valid move to empty point
        self.board.points[5] = ["W"]
        self.board.points[6] = []
        self.assertTrue(self.board.move_checker(5, 6, "W"))
        self.assertEqual(self.board.points[5], [])
        self.assertEqual(self.board.points[6], ["W"])
        
        # Test hitting opponent
        self.board.points[7] = ["B"]
        self.board.points[8] = ["W"]
        self.assertTrue(self.board.move_checker(8, 7, "W"))
        self.assertEqual(self.board.bar["B"], 1)
        self.assertEqual(self.board.points[7], ["W"])
        
        # Test color consistency after move
        self.board.points[9] = ["W"]
        self.board.points[10] = ["B"]  # Different color
        self.assertTrue(self.board.move_checker(9, 10, "W"))
        self.assertTrue(all(checker == "W" for checker in self.board.points[10]))

    def test_bar_operations_comprehensive(self):
        """Test all bar-related operations."""
        self.assertFalse(self.board.move_checker_from_bar(18, "W"))
        
        # Test white bar entry
        self.board.set_point(18, [])
        self.board.bar["W"] = 1
        self.assertTrue(self.board.move_checker_from_bar(18, "W"))
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.points[18][-1], "W")
        
        # Test black bar entry
        self.board.set_point(0, [])
        self.board.bar["B"] = 1
        self.assertTrue(self.board.move_checker_from_bar(0, "B"))
        self.assertEqual(self.board.bar["B"], 0)
        self.assertEqual(self.board.points[0][-1], "B")
        
        # Test hit from bar
        self.board.bar["W"] = 1
        self.board.points[19] = ["B"]
        self.assertTrue(self.board.move_checker_from_bar(19, "W"))
        self.assertEqual(self.board.bar["B"], 1)
        self.assertEqual(self.board.points[19], ["W"])
        
        # Test cannot enter blocked point
        self.board.bar["W"] = 1
        self.board.points[20] = ["B", "B"]
        self.assertFalse(self.board.move_checker_from_bar(20, "W"))
        
        # Test invalid entry points
        self.board.bar["W"] = 1
        self.assertFalse(self.board.move_checker_from_bar(0, "W"))
        self.board.bar["B"] = 1
        self.assertFalse(self.board.move_checker_from_bar(18, "B"))

    def test_can_enter_from_bar_comprehensive(self):
        """Test bar entry validation."""
        # Test invalid point
        self.assertFalse(self.board.can_enter_from_bar("W", -1))
        self.assertFalse(self.board.can_enter_from_bar("W", 24))
        
        # Test empty point
        self.board.set_point(18, [])
        self.assertTrue(self.board.can_enter_from_bar("W", 18))
        
        # Test point with own checkers
        self.board.set_point(19, ["W", "W"])
        self.assertTrue(self.board.can_enter_from_bar("W", 19))
        
        # Test point with single opponent (hittable)
        self.board.set_point(20, ["B"])
        self.assertTrue(self.board.can_enter_from_bar("W", 20))
        
        # Test blocked point
        self.board.set_point(21, ["B", "B"])
        self.assertFalse(self.board.can_enter_from_bar("W", 21))

    def test_bear_off_comprehensive(self):
        """Test all bear off scenarios."""
        # Setup all white pieces in home
        self.board.points = [[] for _ in range(24)]
        for i in range(18, 24):
            self.board.points[i] = ["W"]
        
        # Test valid bear off
        self.assertTrue(self.board.bear_off("W", 18))
        self.assertEqual(self.board.borne_off["W"], 1)
        self.assertEqual(len(self.board.points[18]), 0)
        
        # Test cannot bear off with bar pieces
        self.board.bar["W"] = 1
        self.assertFalse(self.board.bear_off("W", 19))
        self.board.bar["W"] = 0
        
        # Test cannot bear off opponent piece
        self.board.points[19] = ["B"]
        self.assertFalse(self.board.bear_off("W", 19))
        
        # Clear point 20 which still contained a checker from setup
        self.board.set_point(20, [])
        
        # Test cannot bear off from empty point
        self.assertFalse(self.board.bear_off("W", 20))
        
        # Test cannot bear off if not all in home
        self.board.points[0] = ["W"]  # Outside home
        self.assertFalse(self.board.bear_off("W", 21))


    def test_can_bear_off_comprehensive(self):
        """Test bear off eligibility."""
        # Test cannot bear off with pieces on bar
        self.board.bar["W"] = 1
        self.assertFalse(self.board.can_bear_off("W"))
        self.board.bar["W"] = 0
        
        # Test white with pieces outside home
        self.board.points = [[] for _ in range(24)]
        self.board.points[0] = ["W"]  # Point 1 - outside white home
        self.assertFalse(self.board.can_bear_off("W"))
        
        # Test black with pieces outside home
        self.board.points = [[] for _ in range(24)]
        self.board.points[23] = ["B"]  # Point 24 - outside black home
        self.assertFalse(self.board.can_bear_off("B"))
        
        # Test valid bear off for white
        self.board.points = [[] for _ in range(24)]
        for i in range(18, 24):
            self.board.points[i] = ["W"]
        self.assertTrue(self.board.can_bear_off("W"))
        
        # Test valid bear off for black
        self.board.points = [[] for _ in range(24)]
        for i in range(0, 6):
            self.board.points[i] = ["B"]
        self.assertTrue(self.board.can_bear_off("B"))

    def test_bar_operations_comprehensive(self):
        """Test all bar-related operations."""
        self.assertFalse(self.board.move_checker_from_bar(18, "W"))
        
        # Test white bar entry
        self.board.set_point(18, [])
        self.board.bar["W"] = 1
        self.assertTrue(self.board.move_checker_from_bar(18, "W"))
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.points[18][-1], "W")
        
        # Test black bar entry
        self.board.set_point(0, [])
        self.board.bar["B"] = 1
        self.assertTrue(self.board.move_checker_from_bar(0, "B"))
        self.assertEqual(self.board.bar["B"], 0)
        self.assertEqual(self.board.points[0][-1], "B")
        
        # Test hit from bar
        self.board.bar["W"] = 1
        self.board.points[19] = ["B"]
        self.assertTrue(self.board.move_checker_from_bar(19, "W"))
        self.assertEqual(self.board.bar["B"], 1)
        self.assertEqual(self.board.points[19], ["W"])
        
        # Test cannot enter blocked point
        self.board.bar["W"] = 1
        self.board.points[20] = ["B", "B"]
        self.assertFalse(self.board.move_checker_from_bar(20, "W"))
        
        # Test invalid entry points
        self.board.bar["W"] = 1
        self.assertFalse(self.board.move_checker_from_bar(0, "W"))
        self.board.bar["B"] = 1
        self.assertFalse(self.board.move_checker_from_bar(18, "B"))


    def test_bar_operations_comprehensive(self):
        """Test all bar-related operations."""
        self.assertFalse(self.board.move_checker_from_bar(18, "W"))
        
        # Test white bar entry
        self.board.set_point(18, [])
        self.board.bar["W"] = 1
        self.assertTrue(self.board.move_checker_from_bar(18, "W"))
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.points[18][-1], "W")
        
        # Test black bar entry
        self.board.set_point(0, [])
        self.board.bar["B"] = 1
        self.assertTrue(self.board.move_checker_from_bar(0, "B"))
        self.assertEqual(self.board.bar["B"], 0)
        self.assertEqual(self.board.points[0][-1], "B")
        
        # Test hit from bar
        self.board.bar["W"] = 1
        self.board.points[19] = ["B"]
        self.assertTrue(self.board.move_checker_from_bar(19, "W"))
        self.assertEqual(self.board.bar["B"], 1)
        self.assertEqual(self.board.points[19], ["W"])
        
        # Test cannot enter blocked point
        self.board.bar["W"] = 1
        self.board.points[20] = ["B", "B"]
        self.assertFalse(self.board.move_checker_from_bar(20, "W"))
        
        # Test invalid entry points
        self.board.bar["W"] = 1
        self.assertFalse(self.board.move_checker_from_bar(0, "W"))
        self.board.bar["B"] = 1
        self.assertFalse(self.board.move_checker_from_bar(18, "B"))

    def test_can_enter_from_bar_comprehensive(self):
        """Test bar entry validation."""
        # Test invalid point
        self.assertFalse(self.board.can_enter_from_bar("W", -1))
        self.assertFalse(self.board.can_enter_from_bar("W", 24))
        
        # Test empty point
        self.board.set_point(18, [])
        self.assertTrue(self.board.can_enter_from_bar("W", 18))
        
        # Test point with own checkers
        self.board.set_point(19, ["W", "W"])
        self.assertTrue(self.board.can_enter_from_bar("W", 19))
        
        # Test point with single opponent (hittable)
        self.board.set_point(20, ["B"])
        self.assertTrue(self.board.can_enter_from_bar("W", 20))
        
        # Test blocked point
        self.board.set_point(21, ["B", "B"])
        self.assertFalse(self.board.can_enter_from_bar("W", 21))


    def test_board_validation(self):
        """Test board state validation."""
        # Test valid initial board
        self.board.reset()
        self.assertTrue(self.board.is_valid())
        
        # Test invalid board with mixed colors
        self.board.points[10] = ["W", "B"]
        self.assertFalse(self.board.is_valid())
        
        # Test empty board is valid
        self.board.points = [[] for _ in range(24)]
        self.assertTrue(self.board.is_valid())

    def test_point_operations(self):
        """Test get_point and set_point methods."""
        # Test get_point with valid point
        self.board.points[5] = ["W", "W"]
        self.assertEqual(self.board.get_point(5), ["W", "W"])
        
        # Test get_point with invalid point
        self.assertEqual(self.board.get_point(-1), [])
        self.assertEqual(self.board.get_point(24), [])
        
        # Test set_point with valid point
        self.board.set_point(10, ["B", "B"])
        self.assertEqual(self.board.points[10], ["B", "B"])
        
        # Test set_point with invalid point (should not change anything)
        original = self.board.points[0] if self.board.points[0] else []
        self.board.set_point(-1, ["W"])
        self.board.set_point(24, ["W"])
        if original:
            self.assertEqual(self.board.points[0], original)

    def test_complex_scenarios(self):
        """Test complex game scenarios."""
        # Test multiple consecutive moves
        self.board.points[5] = ["W"]
        self.board.points[6] = []
        self.assertTrue(self.board.move_checker(5, 6, "W"))
        
        self.board.points[7] = ["B"]
        self.assertTrue(self.board.move_checker(6, 7, "W"))
        self.assertEqual(self.board.bar["B"], 1)
        
        # Test bearing off after clearing bar
        self.board.points = [[] for _ in range(24)]
        for i in range(18, 24):
            self.board.points[i] = ["W"]
        self.assertTrue(self.board.bear_off("W", 18))
        self.assertEqual(self.board.borne_off["W"], 1)



if __name__ == "__main__":
    unittest.main()