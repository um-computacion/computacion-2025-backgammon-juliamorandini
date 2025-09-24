from core.board import Board
from core.player import Player
from core.Dice import Dice

class Game:
    """A Backgammon game."""

    def __init__(self):
        """Initialize game components."""
        self.board = Board()
        self.dice = Dice()
        self.current_player = 'white'
        self.players = {
            'white': Player("Player 1", "white"),
            'black': Player("Player 2", "black")
        }

    def get_board(self) -> list:
        """Get current board state."""
        return self.board.points

    def make_move(self, from_point: int, to_point: int) -> bool:
        """Make a move if valid."""
        return self.board.move_checker(from_point, to_point, 'W' if self.current_player == 'white' else 'B')

    def set_dice(self, values: list) -> None:
        """Set dice values for testing."""
        self.dice.die1 = values[0]
        self.dice.die2 = values[1]

    def get_available_moves(self) -> list:
        """Get available moves based on dice."""
        return self.dice.get_moves()

    def set_piece(self, point: int, count: int) -> None:
        """Set pieces at point for testing."""
        self.board.points[point] = ['W' if count > 0 else 'B'] * abs(count)

    def add_to_bar(self) -> None:
        """Add current player's piece to bar."""
        color = 'W' if self.current_player == 'white' else 'B'
        self.board.bar[color] += 1

    def must_move_from_bar(self) -> bool:
        """Check if player must move from bar."""
        color = 'W' if self.current_player == 'white' else 'B'
        return self.board.bar[color] > 0

    def get_bar_pieces(self) -> int:
        """Get number of pieces on bar for current player."""
        color = 'W' if self.current_player == 'white' else 'B'
        return self.board.bar[color]

    def bear_off(self, point: int) -> bool:
        """Bear off a piece if possible."""
        color = 'W' if self.current_player == 'white' else 'B'
        return self.board.bear_off(color, point)

    def setup_bearing_off_scenario(self) -> None:
        """Setup board for bearing off test."""
        self.board.points = [[] for _ in range(24)]
        self.set_piece(18, 1)

    def setup_winning_scenario(self) -> None:
        """Setup board for win condition test."""
        color = 'W' if self.current_player == 'white' else 'B'
        self.board.borne_off[color] = 15

    def check_winner(self) -> bool:
        """Check if current player has won."""
        color = 'W' if self.current_player == 'white' else 'B'
        return self.board.borne_off[color] == 15

    
    def get_valid_moves(self) -> list:
        """Get valid moves based on current dice values."""
        dice_values = [self.dice.die1, self.dice.die2]
        return [v for v in dice_values if v <= 6]