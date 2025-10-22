import unittest
from core.board import Board

class TestBackgammonBoard(unittest.TestCase):
    def setUp(self):
        """Reset the board before every test."""
        self.board = Board()
        self.board.reset()

    # --- Utility & Boundary Tests (get_point, set_point, is_valid) ---

    def test_initial_state(self):
        """Verify the board starts in the correct initial configuration."""
        self.assertEqual(len(self.board.points), 24)
        self.assertEqual(self.board.points[0], ["B", "B"])
        self.assertEqual(self.board.points[5], ["W"] * 5)
        self.assertTrue(self.board.is_valid())

    def test_get_set_point_boundaries(self):
        """Test point access with valid and invalid indices."""
        # Test valid get
        self.assertEqual(len(self.board.get_point(5)), 5)
        
        # Test out-of-bounds get (Covers `return []` branch in get_point)
        self.assertEqual(self.board.get_point(-1), [])
        self.assertEqual(self.board.get_point(24), [])
        
        # Test valid set
        self.board.set_point(1, ["B", "B", "B"])
        self.assertEqual(self.board.points[1], ["B", "B", "B"])
        
        # Test out-of-bounds set (Covers implicit no-op/no-return)
        initial_len = len(self.board.points) 
        self.board.set_point(24, ["W"]) 
        self.assertEqual(len(self.board.points), initial_len)

    def test_is_valid_mixed_colors(self):
        """Test board validation, including the failure condition for mixed colors."""
        # Test valid state (Initial state is valid)
        self.assertTrue(self.board.is_valid())
        
        # Test invalid state (Mixed colors on point 5) - Covers `return False` branch
        self.board.points[5] = ["W", "B"]
        self.assertFalse(self.board.is_valid())
        
        # Test valid state (Empty point)
        self.board.points = [[] for _ in range(24)]
        self.assertTrue(self.board.is_valid())

    # --- Move Validation Tests (is_valid_move) ---

    def test_is_valid_move_comprehensive(self):
        """Covers all failure branches in is_valid_move."""
        # Setup clean board with specific pieces
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = ["W"]
        self.board.points[15] = ["B"]
        
        # 1. Out of bounds (from_point)
        self.assertFalse(self.board.is_valid_move(-1, 5, "W"))
        
        # 2. Out of bounds (to_point)
        self.assertFalse(self.board.is_valid_move(10, 24, "W"))
        
        # 3. Bar piece present (Covers `if self.bar[color] > 0:` branch)
        self.board.bar["W"] = 1
        self.assertFalse(self.board.is_valid_move(10, 12, "W"))
        self.board.bar["W"] = 0 
        
        # 4. Moving from empty point (Covers `if not self.points[from_point]:`)
        self.assertFalse(self.board.is_valid_move(1, 3, "W"))
        
        # 5. Moving opponent's piece (Covers `or self.points[from_point][0] != color:`)
        self.assertFalse(self.board.is_valid_move(15, 17, "W"))
        
        # 6. Target blocked by opponent (prime) (Covers `len(points[to]) >= 2 and != color:`)
        self.board.points[12] = ["B", "B"]
        self.assertFalse(self.board.is_valid_move(10, 12, "W"))
        
        # 7. Valid move (Simple move)
        self.assertTrue(self.board.is_valid_move(10, 11, "W"))
        
        # 8. Valid move (Hitting single opponent)
        self.assertTrue(self.board.is_valid_move(10, 15, "W"))

    # --- Move Execution Tests (move_checker) ---

    def test_move_checker_hit(self):
        """Test moving and hitting a single opponent checker."""
        self.board.points = [[] for _ in range(24)]
        self.board.points[10] = ["W"]
        self.board.points[15] = ["B"] # Hittable target
        self.board.bar["B"] = 0 
        
        self.assertTrue(self.board.move_checker(10, 15, "W"))
        self.assertEqual(self.board.points[15], ["W"])
        self.assertEqual(self.board.points[10], [])
        self.assertEqual(self.board.bar["B"], 1) # Opponent checker should be on the bar

    def test_move_checker_stack(self):
        """Test moving onto an existing stack of own color (covers stacking logic)."""
        self.board.points = [[] for _ in range(24)]
        self.board.points[5] = ["W", "W", "W"] # Existing stack
        self.board.points[10] = ["W"] # Moving checker
        
        self.assertTrue(self.board.move_checker(10, 5, "W"))
        self.assertEqual(len(self.board.points[5]), 4)
        self.assertEqual(self.board.points[5], ["W", "W", "W", "W"]) # Check consistency (list of identical strings)

    def test_move_checker_invalid_move(self):
        """Test attempting an invalid move (covers initial failure branch)."""
        # White tries to move Black's piece (invalid)
        self.assertFalse(self.board.move_checker(0, 1, "W"))

    # --- Bar Entry Tests (can_enter_from_bar, move_checker_from_bar) ---
    
    def test_can_enter_from_bar_comprehensive(self):
        """Covers all branches in can_enter_from_bar."""
        # FIX: Clear the board points to ensure test conditions start clean.
        self.board.points = [[] for _ in range(24)]
        
        # Setup point 19
        self.board.set_point(19, ["B"])
        
        # 1. Invalid point
        self.assertFalse(self.board.can_enter_from_bar("W", 24))
        
        # 2. Empty point (Success)
        self.assertTrue(self.board.can_enter_from_bar("W", 18))
        
        # 3. Hittable opponent (Success)
        self.assertTrue(self.board.can_enter_from_bar("W", 19))
        
        # 4. Blocked opponent (Failure)
        self.board.set_point(20, ["B", "B"])
        self.assertFalse(self.board.can_enter_from_bar("W", 20))
        
        # 5. Own checker (Success - stacking)
        self.board.set_point(21, ["W"])
        self.assertTrue(self.board.can_enter_from_bar("W", 21))

    def test_move_checker_from_bar_comprehensive(self):
        """Covers all failure and success branches in move_checker_from_bar."""
        self.board.bar = {"W": 1, "B": 1}
        
        # 1. White trying to enter Black's home board (18-23 vs 0-5)
        self.assertFalse(self.board.move_checker_from_bar(5, "W"))
        
        # 2. Black trying to enter White's home board
        self.assertFalse(self.board.move_checker_from_bar(18, "B"))
        
        # 3. Bar entry blocked by opponent prime
        self.board.set_point(20, ["B", "B"])
        self.assertFalse(self.board.move_checker_from_bar(20, "W"))
        self.board.set_point(20, [])

        # 4. Successful White bar entry (empty point)
        self.assertTrue(self.board.move_checker_from_bar(22, "W"))
        self.assertEqual(self.board.bar["W"], 0)
        self.assertEqual(self.board.points[22], ["W"])

        # 5. Successful Black bar entry (hit opponent)
        self.board.bar["B"] = 1 # Restore black bar count
        self.board.set_point(1, ["W"]) # Hittable target
        self.assertTrue(self.board.move_checker_from_bar(1, "B"))
        self.assertEqual(self.board.bar["B"], 0)
        self.assertEqual(self.board.bar["W"], 1) # White hit counter increased
        self.assertEqual(self.board.points[1], ["B"])

    def test_move_checker_from_bar_no_pieces(self):
        """Covers `if self.bar[color] == 0:` branch."""
        self.board.bar = {"W": 0, "B": 0}
        self.assertFalse(self.board.move_checker_from_bar(22, "W"))

    # --- Bear Off Tests (can_bear_off, bear_off) ---

    def test_can_bear_off_comprehensive(self):
        """Covers all branches in can_bear_off."""
        # 1. Cannot bear off if piece on bar (Covers `if self.bar[color] > 0:` branch)
        self.board.bar["W"] = 1
        self.assertFalse(self.board.can_bear_off("W"))
        self.board.bar["W"] = 0
        
        # 2. Cannot bear off White if piece is outside home board (Covers `if any(checker == color for checker in self.points[i])` branch)
        # White home: 18-23. Outside: 0-17.
        self.board.points = [[] for _ in range(24)]
        self.board.points[17] = ["W"] # Piece outside home
        self.assertFalse(self.board.can_bear_off("W"))
        
        # 3. Cannot bear off Black if piece is outside home board
        # Black home: 0-5. Outside: 6-23.
        self.board.points = [[] for _ in range(24)]
        self.board.points[6] = ["B"] # Piece outside home
        self.assertFalse(self.board.can_bear_off("B"))
        
        # 4. Can bear off White (All pieces in home)
        self.board.points = [[] for _ in range(24)]
        self.board.points[18] = ["W"] * 15 # All 15 pieces in home
        self.assertTrue(self.board.can_bear_off("W"))
        
        # 5. Can bear off Black (All pieces in home)
        self.board.points = [[] for _ in range(24)]
        self.board.points[5] = ["B"] * 15 
        self.assertTrue(self.board.can_bear_off("B"))

    def test_bear_off_comprehensive(self):
        """Covers all failure and success branches in bear_off."""
        # Setup for successful bear off
        self.board.points = [[] for _ in range(24)]
        self.board.points[18] = ["W"]
        self.board.points[5] = ["B"]
        
        # 1. Cannot bear off (due to piece outside home)
        self.board.points[17] = ["W"] 
        self.assertFalse(self.board.bear_off("W", 18))
        self.board.points[17] = [] # Clear piece outside
        
        # 2. Bear off from empty point (Covers `if not self.points[point]`)
        self.assertFalse(self.board.bear_off("W", 19))
        
        # 3. Bear off opponent's piece (Covers `or self.points[point][0] != color`)
        self.assertFalse(self.board.bear_off("W", 5))

        # 4. Successful White bear off
        self.assertTrue(self.board.bear_off("W", 18))
        self.assertEqual(self.board.borne_off["W"], 1)
        self.assertEqual(len(self.board.points[18]), 0)

        # 5. Successful Black bear off (All pieces are now in Black home after setup change)
        self.assertTrue(self.board.can_bear_off("B")) # Verify it's possible
        self.assertTrue(self.board.bear_off("B", 5))
        self.assertEqual(self.board.borne_off["B"], 1)
        self.assertEqual(len(self.board.points[5]), 0)


if __name__ == "__main__":
    unittest.main()
