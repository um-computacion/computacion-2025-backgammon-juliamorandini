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
            if not point:
                board_state.append(0)
            else:
                count = len(point)
                if point[0] == "B":
                    board_state.append(-count)
                else:
                    board_state.append(count)
        return board_state

    def make_move(self, from_point: int, to_point: int) -> bool:
        """Make a move if valid."""
        color = "W" if self.current_player == "white" else "B"

        if self.board.bar[color] > 0:
            return False

        return self.board.move_checker(from_point, to_point, color)

    def make_bar_move(self, to_point: int) -> bool:
        """Move a checker from the bar to a valid entry point."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.move_checker_from_bar(to_point, color)

    def get_entry_point_for_dice(self, dice_value: int) -> int:
        """Get the entry point corresponding to a dice value."""
        color = "W" if self.current_player == "white" else "B"

        if color == "W":
            return 24 - dice_value
        else:
            return dice_value - 1

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

    def add_to_bar(self, color: str = None) -> None:
        """Add current player's piece to bar."""
        if color is None:
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
        color = "W" if self.current_player == "white" else "B"
        if color == "W":
            self.board.points[18] = [color] * 5
        else:
            self.board.points[0] = [color] * 5

    def setup_winning_scenario(self) -> None:
        """Setup board for win condition test."""
        color = "W" if self.current_player == "white" else "B"
        self.board.borne_off[color] = 15

    def check_winner(self) -> bool:
        """Check if current player has won."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.borne_off[color] == 15

    def switch_player(self) -> None:
        """Switch to the other player."""
        self.current_player = "black" if self.current_player == "white" else "white"

    def roll_dice(self) -> list:
        """Roll the dice and return the values."""
        self.dice.roll()
        return self.get_available_moves()

    def can_bear_off(self) -> bool:
        """Check if current player can bear off."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.can_bear_off(color)

    def get_current_player_color(self) -> str:
        """Get current player's color code."""
        return "W" if self.current_player == "white" else "B"
