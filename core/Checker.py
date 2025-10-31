"""Module containing the Checker class for Backgammon pieces."""

from typing import Union, Dict, List, Optional


class Checker:
    """Represents a single checker piece in Backgammon."""

    def __init__(self, color: str, position: Union[int, str]) -> None:
        """Initialize a checker piece.

        Args:
            color: Color of the checker ('white' or 'black')
            position: Starting position (0-23, 'bar', or 'off')

        Raises:
            ValueError: If color is invalid
        """
        if color not in ["white", "black"]:
            raise ValueError("Color must be 'white' or 'black'")

        self.color = color
        self.position = position
        self.is_on_bar = position == "bar"
        self.is_borne_off = position == "off"

    def move_to(self, new_position: int) -> bool:
        """Move checker to new position on board.

        Args:
            new_position: Target position (0-23)

        Returns:
            bool: True if move was valid, False otherwise
        """
        if 0 <= new_position <= 23:
            self.position = new_position
            self.is_on_bar = False
            self.is_borne_off = False
            return True
        return False

    def send_to_bar(self) -> None:
        """Send checker to the bar."""
        self.position = "bar"
        self.is_on_bar = True
        self.is_borne_off = False

    def bear_off(self) -> None:
        """Bear off the checker from the board."""
        self.position = "off"
        self.is_borne_off = True
        self.is_on_bar = False

    def can_bear_off(self, all_home: bool) -> bool:
        """Check if checker can be borne off.

        Args:
            all_home: Whether all checkers are in home quadrant

        Returns:
            bool: True if checker can be borne off
        """
        if not all_home:
            return False
        if not isinstance(self.position, int):
            return False
        if self.color == "white":
            return self.position >= 18
        return self.position <= 5

    def is_point_blocked(self, point: int, board: Dict[int, List["Checker"]]) -> bool:
        """Check if a point is blocked by opponent.

        Args:
            point: Point to check
            board: Current board state

        Returns:
            bool: True if point is blocked
        """
        if point not in board or not board[point]:
            return False

        opponent_color = "black" if self.color == "white" else "white"
        opponent_checkers = [c for c in board[point] if c.color == opponent_color]

        return len(opponent_checkers) >= 2

    def can_move_to(self, point: int, board: Dict[int, List["Checker"]]) -> bool:
        """Check if checker can move to point.

        Args:
            point: Target point
            board: Current board state

        Returns:
            bool: True if move is valid
        """
        if not (0 <= point < 24):
            return False
        return not self.is_point_blocked(point, board)

    def move(self, point: int, board: Dict[int, List["Checker"]]) -> bool:
        """Move checker to new point.

        Args:
            point: Target point
            board: Current board state

        Returns:
            bool: True if move was successful
        """
        if self.can_move_to(point, board):
            old_position = self.position
            self.position = point
            self.is_on_bar = False

            if isinstance(old_position, int):
                board[old_position] = [c for c in board[old_position] if c != self]

            if point not in board:
                board[point] = []
            board[point].append(self)

            return True
        return False
