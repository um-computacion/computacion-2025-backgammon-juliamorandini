"""Module containing the main Backgammon game logic."""
from core.board import Board
from core.player import Player
from core.Dice import Dice

class Game:
    """A Backgammon game."""
    def __init__(self):
        """Initialize game components."""
        self.board = Board()
        self.dice = Dice()
        self.current_player = "white"
        self.players = {
            "white": Player("Player 1", "white"),
            "black": Player("Player 2", "black"),
        }
    
    def get_board(self) -> list:
        """Get current board state as point counts."""
        board_state = []
        for point in self.board.points:
            if not point:  # Empty point
                board_state.append(0)
            else:
                count = len(point)
                # Check what color occupies the point
                if point[0] == "B":  # Black pieces
                    board_state.append(-count)
                else:  # White pieces
                    board_state.append(count)
        return board_state
    
    def make_move(self, from_point: int, to_point: int) -> bool:
        """Make a move if valid."""
        color = "W" if self.current_player == "white" else "B"
        
        # Check if player must move from bar
        if self.board.bar[color] > 0:
            return self.make_bar_move(to_point)
        
        return self.board.move_checker(from_point, to_point, color)
    
    def make_bar_move(self, to_point: int) -> bool:
        """Move a checker from the bar to a valid entry point.
        
        Args:
            to_point: The point to enter at
            
        Returns:
            True if move was successful
        """
        color = "W" if self.current_player == "white" else "B"
        
        # Validate entry point based on color
        if color == "W" and not (18 <= to_point <= 23):
            return False
        if color == "B" and not (0 <= to_point <= 5):
            return False
        
        # Check if the point is available (using existing board method)
        if not self.board.can_enter_from_bar(color, to_point):
            return False
        
        # Handle hitting opponent's blot
        if (
            self.board.points[to_point]
            and len(self.board.points[to_point]) == 1
            and self.board.points[to_point][0] != color
        ):
            hit_color = self.board.points[to_point][0]
            self.board.bar[hit_color] += 1
            self.board.points[to_point] = []
        
        # Move checker from bar
        self.board.bar[color] -= 1
        self.board.points[to_point].append(color)
        return True
    
    def get_entry_point_for_dice(self, dice_value: int) -> int:
        """Get the entry point corresponding to a dice value.
        
        Args:
            dice_value: The dice value (1-6)
            
        Returns:
            The entry point (0-23)
        """
        color = "W" if self.current_player == "white" else "B"
        
        if color == "W":
            # White enters at 24 - dice_value (1→23, 2→22, ..., 6→18)
            return 24 - dice_value
        else:
            # Black enters at dice_value - 1 (1→0, 2→1, ..., 6→5)
            return dice_value - 1
    
    def get_valid_bar_entry_points(self) -> list:
        """Get valid entry points based on current dice for player on bar.
        
        Returns:
            List of entry points that can be used with current dice
        """
        if not self.must_move_from_bar():
            return []
        
        color = "W" if self.current_player == "white" else "B"
        dice_values = self.get_available_moves()
        valid_points = []
        
        for dice_val in dice_values:
            entry_point = self.get_entry_point_for_dice(dice_val)
            
            # Check if point is available
            if self.board.can_enter_from_bar(color, entry_point):
                valid_points.append(entry_point)
        
        return valid_points
    
    def set_dice(self, values: list) -> None:
        """Set dice values for testing."""
        self.dice.die1 = values[0]
        self.dice.die2 = values[1]
    
    def get_available_moves(self) -> list:
        """Get available moves based on dice."""
        return self.dice.get_moves()
    
    def set_piece(self, point: int, count: int, color: str = None) -> None:
        """Set pieces at point for testing."""
        if color is None:
            color = "W" if self.current_player == "white" else "B"
        self.board.points[point] = [color] * abs(count)
    
    def add_to_bar(self) -> None:
        """Add current player's piece to bar."""
        color = "W" if self.current_player == "white" else "B"
        self.board.bar[color] += 1
    
    def must_move_from_bar(self) -> bool:
        """Check if player must move from bar."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.bar[color] > 0
    
    def get_bar_pieces(self) -> int:
        """Get number of pieces on bar for current player."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.bar[color]
    
    def bear_off(self, point: int) -> bool:
        """Bear off a piece if possible."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.bear_off(color, point)
    
    def setup_bearing_off_scenario(self):
        """Setup board for bearing off test."""
        self.board.points = [[] for _ in range(24)]
        self.set_piece(23, 1)  # Place piece at point 23 instead
    
    def setup_winning_scenario(self) -> None:
        """Setup board for win condition test."""
        color = "W" if self.current_player == "white" else "B"
        self.board.borne_off[color] = 15
    
    def check_winner(self) -> bool:
        """Check if current player has won."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.borne_off[color] == 15
    
    def get_valid_moves(self) -> list:
        """Get valid moves based on current dice values."""
        dice_values = [self.dice.die1, self.dice.die2]
        return [v for v in dice_values if v <= 6]
    
    def get_opponent_bar_pieces(self) -> int:
        """Get number of pieces on bar for opponent player."""
        opponent_color = "B" if self.current_player == "white" else "W"
        return self.board.bar[opponent_color]