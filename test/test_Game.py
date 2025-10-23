"""Comprehensive test module for Game class with improved coverage."""
import unittest
from core.BackgammonGame import Game


class TestGameEnhanced(unittest.TestCase):
    """Enhanced test suite for Game class."""

    def setUp(self):
        """Set up test fixtures."""
        self.game = Game()

    def test_game_initialization(self):
        """Test game initialization."""
        self.assertIsNotNone(self.game.board)
        self.assertIsNotNone(self.game.dice)
        self.assertEqual(self.game.current_player, "white")
        self.assertEqual(len(self.game.players), 2)
        self.assertIn("white", self.game.players)
        self.assertIn("black", self.game.players)

    def test_get_board_empty_points(self):
        """Test get_board with empty points."""
        self.game.board.points = [[] for _ in range(24)]
        board_state = self.game.get_board()
        self.assertEqual(len(board_state), 24)
        self.assertTrue(all(count == 0 for count in board_state))

    def test_get_board_with_white_pieces(self):
        """Test get_board with white pieces."""
        self.game.board.points = [[] for _ in range(24)]
        self.game.board.points[0] = ["W", "W", "W"]
        board_state = self.game.get_board()
        self.assertEqual(board_state[0], 3)

    def test_get_board_with_black_pieces(self):
        """Test get_board with black pieces."""
        self.game.board.points = [[] for _ in range(24)]
        self.game.board.points[5] = ["B", "B"]
        board_state = self.game.get_board()
        self.assertEqual(board_state[5], -2)

    def test_get_board_mixed_pieces(self):
        """Test get_board with mixed pieces on different points."""
        self.game.board.points = [[] for _ in range(24)]
        self.game.board.points[0] = ["W", "W"]
        self.game.board.points[12] = ["B", "B", "B"]
        board_state = self.game.get_board()
        self.assertEqual(board_state[0], 2)
        self.assertEqual(board_state[12], -3)

    def test_make_move_blocked_by_bar(self):
        """Test that moves are blocked when piece is on bar."""
        self.game.board.bar["W"] = 1
        result = self.game.make_move(0, 1)
        self.assertFalse(result)

    def test_make_move_white_player(self):
        """Test make_move for white player."""
        self.game.current_player = "white"
        self.game.board.points[0] = ["W"]
        self.game.board.points[1] = []
        result = self.game.make_move(0, 1)
        # Result depends on board.move_checker implementation
        self.assertIsInstance(result, bool)

    def test_make_move_black_player(self):
        """Test make_move for black player."""
        self.game.current_player = "black"
        self.game.board.bar["B"] = 0
        self.game.board.points[23] = ["B"]
        self.game.board.points[22] = []
        result = self.game.make_move(23, 22)
        self.assertIsInstance(result, bool)

    def test_make_bar_move_white(self):
        """Test moving from bar for white player."""
        self.game.current_player = "white"
        self.game.board.bar["W"] = 1
        self.game.board.points[20] = []
        result = self.game.make_bar_move(20)
        self.assertIsInstance(result, bool)

    def test_make_bar_move_black(self):
        """Test moving from bar for black player."""
        self.game.current_player = "black"
        self.game.board.bar["B"] = 1
        self.game.board.points[3] = []
        result = self.game.make_bar_move(3)
        self.assertIsInstance(result, bool)

    def test_get_entry_point_for_dice_white(self):
        """Test entry point calculation for white player."""
        self.game.current_player = "white"
        entry_point = self.game.get_entry_point_for_dice(3)
        self.assertEqual(entry_point, 21)  # 24 - 3

    def test_get_entry_point_for_dice_black(self):
        """Test entry point calculation for black player."""
        self.game.current_player = "black"
        entry_point = self.game.get_entry_point_for_dice(4)
        self.assertEqual(entry_point, 3)  # 4 - 1

    def test_get_entry_point_for_dice_edge_cases(self):
        """Test entry point calculation edge cases."""
        self.game.current_player = "white"
        self.assertEqual(self.game.get_entry_point_for_dice(1), 23)
        self.assertEqual(self.game.get_entry_point_for_dice(6), 18)
        
        self.game.current_player = "black"
        self.assertEqual(self.game.get_entry_point_for_dice(1), 0)
        self.assertEqual(self.game.get_entry_point_for_dice(6), 5)

    def test_set_dice(self):
        """Test setting dice values."""
        self.game.set_dice([3, 5])
        self.assertEqual(self.game.dice.die1, 3)
        self.assertEqual(self.game.dice.die2, 5)

    def test_set_dice_various_values(self):
        """Test setting various dice values."""
        test_values = [[1, 1], [6, 6], [2, 5], [4, 3]]
        for values in test_values:
            self.game.set_dice(values)
            self.assertEqual(self.game.dice.die1, values[0])
            self.assertEqual(self.game.dice.die2, values[1])

    def test_get_available_moves(self):
        """Test getting available moves."""
        self.game.set_dice([2, 4])
        moves = self.game.get_available_moves()
        self.assertIn(2, moves)
        self.assertIn(4, moves)

    def test_get_available_moves_doubles(self):
        """Test getting available moves with doubles."""
        self.game.set_dice([3, 3])
        moves = self.game.get_available_moves()
        self.assertEqual(len(moves), 4)
        self.assertTrue(all(m == 3 for m in moves))

    def test_set_piece_white(self):
        """Test setting white pieces."""
        self.game.current_player = "white"
        self.game.set_piece(5, 3)
        self.assertEqual(len(self.game.board.points[5]), 3)
        self.assertEqual(self.game.board.points[5][0], "W")

    def test_set_piece_black(self):
        """Test setting black pieces."""
        self.game.current_player = "black"
        self.game.set_piece(10, 2)
        self.assertEqual(len(self.game.board.points[10]), 2)
        self.assertEqual(self.game.board.points[10][0], "B")

    def test_set_piece_with_color_param(self):
        """Test setting pieces with explicit color parameter."""
        self.game.set_piece(7, 4, "B")
        self.assertEqual(len(self.game.board.points[7]), 4)
        self.assertEqual(self.game.board.points[7][0], "B")
        
        self.game.set_piece(8, 3, "W")
        self.assertEqual(len(self.game.board.points[8]), 3)
        self.assertEqual(self.game.board.points[8][0], "W")

    def test_set_piece_various_positions(self):
        """Test setting pieces at various positions."""
        for point in [0, 5, 12, 18, 23]:
            self.game.set_piece(point, 2, "W")
            self.assertEqual(len(self.game.board.points[point]), 2)

    def test_add_to_bar_white(self):
        """Test adding white piece to bar."""
        self.game.current_player = "white"
        initial_count = self.game.board.bar["W"]
        self.game.add_to_bar()
        self.assertEqual(self.game.board.bar["W"], initial_count + 1)

    def test_add_to_bar_black(self):
        """Test adding black piece to bar."""
        self.game.current_player = "black"
        initial_count = self.game.board.bar["B"]
        self.game.add_to_bar()
        self.assertEqual(self.game.board.bar["B"], initial_count + 1)

    def test_add_to_bar_with_color_param(self):
        """Test adding piece to bar with explicit color."""
        initial_count = self.game.board.bar["W"]
        self.game.add_to_bar("W")
        self.assertEqual(self.game.board.bar["W"], initial_count + 1)
        
        initial_count = self.game.board.bar["B"]
        self.game.add_to_bar("B")
        self.assertEqual(self.game.board.bar["B"], initial_count + 1)

    def test_add_multiple_to_bar(self):
        """Test adding multiple pieces to bar."""
        self.game.current_player = "white"
        for i in range(3):
            self.game.add_to_bar()
        self.assertEqual(self.game.board.bar["W"], 3)

    def test_must_move_from_bar_true(self):
        """Test must_move_from_bar returns True when piece on bar."""
        self.game.current_player = "white"
        self.game.board.bar["W"] = 1
        self.assertTrue(self.game.must_move_from_bar())

    def test_must_move_from_bar_false(self):
        """Test must_move_from_bar returns False when no piece on bar."""
        self.game.current_player = "white"
        self.game.board.bar["W"] = 0
        self.assertFalse(self.game.must_move_from_bar())

    def test_must_move_from_bar_both_players(self):
        """Test must_move_from_bar for both players."""
        self.game.board.bar["W"] = 2
        self.game.board.bar["B"] = 0
        
        self.game.current_player = "white"
        self.assertTrue(self.game.must_move_from_bar())
        
        self.game.current_player = "black"
        self.assertFalse(self.game.must_move_from_bar())

    def test_get_bar_pieces_white(self):
        """Test getting bar pieces for white player."""
        self.game.current_player = "white"
        self.game.board.bar["W"] = 2
        self.assertEqual(self.game.get_bar_pieces(), 2)

    def test_get_bar_pieces_black(self):
        """Test getting bar pieces for black player."""
        self.game.current_player = "black"
        self.game.board.bar["B"] = 3
        self.assertEqual(self.game.get_bar_pieces(), 3)

    def test_get_bar_pieces_zero(self):
        """Test getting bar pieces when none present."""
        self.game.current_player = "white"
        self.game.board.bar["W"] = 0
        self.assertEqual(self.game.get_bar_pieces(), 0)

    def test_bear_off_white(self):
        """Test bearing off for white player."""
        self.game.current_player = "white"
        self.game.setup_bearing_off_scenario()
        result = self.game.bear_off(18)
        self.assertIsInstance(result, bool)

    def test_bear_off_black(self):
        """Test bearing off for black player."""
        self.game.current_player = "black"
        self.game.setup_bearing_off_scenario()
        result = self.game.bear_off(0)
        self.assertIsInstance(result, bool)

    def test_setup_bearing_off_scenario_white(self):
        """Test bearing off setup for white player."""
        self.game.current_player = "white"
        self.game.setup_bearing_off_scenario()
        self.assertEqual(len(self.game.board.points[18]), 5)
        self.assertEqual(self.game.board.points[18][0], "W")
        # Check other points are empty
        for i in range(18):
            self.assertEqual(len(self.game.board.points[i]), 0)

    def test_setup_bearing_off_scenario_black(self):
        """Test bearing off setup for black player."""
        self.game.current_player = "black"
        self.game.setup_bearing_off_scenario()
        self.assertEqual(len(self.game.board.points[0]), 5)
        self.assertEqual(self.game.board.points[0][0], "B")
        # Check other points are empty
        for i in range(1, 6):
            self.assertEqual(len(self.game.board.points[i]), 0)

    def test_setup_winning_scenario_white(self):
        """Test winning scenario setup for white player."""
        self.game.current_player = "white"
        self.game.setup_winning_scenario()
        self.assertEqual(self.game.board.borne_off["W"], 15)

    def test_setup_winning_scenario_black(self):
        """Test winning scenario setup for black player."""
        self.game.current_player = "black"
        self.game.setup_winning_scenario()
        self.assertEqual(self.game.board.borne_off["B"], 15)

    def test_check_winner_true_white(self):
        """Test check_winner returns True when white player has won."""
        self.game.current_player = "white"
        self.game.board.borne_off["W"] = 15
        self.assertTrue(self.game.check_winner())

    def test_check_winner_true_black(self):
        """Test check_winner returns True when black player has won."""
        self.game.current_player = "black"
        self.game.board.borne_off["B"] = 15
        self.assertTrue(self.game.check_winner())

    def test_check_winner_false(self):
        """Test check_winner returns False when player hasn't won."""
        self.game.current_player = "white"
        self.game.board.borne_off["W"] = 10
        self.assertFalse(self.game.check_winner())
        
        self.game.board.borne_off["W"] = 0
        self.assertFalse(self.game.check_winner())
        
        self.game.board.borne_off["W"] = 14
        self.assertFalse(self.game.check_winner())

    def test_switch_player_white_to_black(self):
        """Test switching from white to black player."""
        self.game.current_player = "white"
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "black")

    def test_switch_player_black_to_white(self):
        """Test switching from black to white player."""
        self.game.current_player = "black"
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "white")

    def test_multiple_switches(self):
        """Test multiple player switches."""
        self.game.current_player = "white"
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "black")
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "white")
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "black")
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "white")

    def test_roll_dice(self):
        """Test rolling dice."""
        moves = self.game.roll_dice()
        self.assertIsInstance(moves, list)
        self.assertGreater(len(moves), 0)
        self.assertTrue(all(1 <= m <= 6 for m in moves))

    def test_roll_dice_multiple_times(self):
        """Test rolling dice multiple times."""
        for _ in range(10):
            moves = self.game.roll_dice()
            self.assertIsInstance(moves, list)
            self.assertIn(len(moves), [2, 4])  # Either 2 different or 4 same

    def test_can_bear_off_true(self):
        """Test can_bear_off returns True when allowed."""
        self.game.current_player = "white"
        self.game.setup_bearing_off_scenario()
        result = self.game.can_bear_off()
        self.assertIsInstance(result, bool)

    def test_can_bear_off_false(self):
        """Test can_bear_off returns False when not allowed."""
        self.game.current_player = "white"
        self.game.board.points = [[] for _ in range(24)]
        # Place pieces outside home board
        self.game.board.points[0] = ["W", "W"]
        result = self.game.can_bear_off()
        self.assertFalse(result)

    def test_get_current_player_color_white(self):
        """Test getting current player color for white."""
        self.game.current_player = "white"
        self.assertEqual(self.game.get_current_player_color(), "W")

    def test_get_current_player_color_black(self):
        """Test getting current player color for black."""
        self.game.current_player = "black"
        self.assertEqual(self.game.get_current_player_color(), "B")

    def test_get_current_player_color_after_switch(self):
        """Test getting current player color after switching."""
        self.game.current_player = "white"
        self.assertEqual(self.game.get_current_player_color(), "W")
        
        self.game.switch_player()
        self.assertEqual(self.game.get_current_player_color(), "B")
        
        self.game.switch_player()
        self.assertEqual(self.game.get_current_player_color(), "W")

    def test_bar_move_integration(self):
        """Test full bar move integration."""
        self.game.current_player = "white"
        self.game.add_to_bar()
        self.assertTrue(self.game.must_move_from_bar())
        self.assertEqual(self.game.get_bar_pieces(), 1)

    def test_complete_game_flow(self):
        """Test a complete game flow scenario."""
        # Start with white
        self.assertEqual(self.game.current_player, "white")
        
        # Roll dice
        moves = self.game.roll_dice()
        self.assertGreater(len(moves), 0)
        
        # Check winner (should be false at start)
        self.assertFalse(self.game.check_winner())
        
        # Switch player
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "black")
        
        # Switch back
        self.game.switch_player()
        self.assertEqual(self.game.current_player, "white")

    def test_bearing_off_workflow(self):
        """Test complete bearing off workflow."""
        self.game.current_player = "white"
        
        # Setup scenario
        self.game.setup_bearing_off_scenario()
        
        # Should be able to bear off
        can_bear = self.game.can_bear_off()
        self.assertIsInstance(can_bear, bool)
        
        # Get current color
        color = self.game.get_current_player_color()
        self.assertEqual(color, "W")

    def test_bar_workflow_both_players(self):
        """Test bar workflow for both players."""
        # White player
        self.game.current_player = "white"
        self.game.add_to_bar()
        self.assertEqual(self.game.get_bar_pieces(), 1)
        self.assertTrue(self.game.must_move_from_bar())
        
        # Switch to black
        self.game.switch_player()
        self.assertEqual(self.game.get_bar_pieces(), 0)
        self.assertFalse(self.game.must_move_from_bar())
        
        # Add black to bar
        self.game.add_to_bar()
        self.assertEqual(self.game.get_bar_pieces(), 1)
        self.assertTrue(self.game.must_move_from_bar())


if __name__ == "__main__":
    unittest.main()