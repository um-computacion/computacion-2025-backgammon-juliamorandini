"""Module containing the Board class for Backgammon game."""

from typing import List, Dict


class Board:
    """Backgammon board representation."""

    def __init__(self):
        """Initialize empty board."""
        self.points: List[List[str]] = [[] for _ in range(24)]
        self.bar: Dict[str, int] = {"W": 0, "B": 0}
        self.borne_off: Dict[str, int] = {"W": 0, "B": 0}
        self.reset()

    def reset(self) -> None:
        """Reset board to initial position."""
        self.points = [[] for _ in range(24)]
        # Initial setup
        self.points[0] = ["B", "B"]  # 2 black pieces at point 0
        self.points[5] = ["W"] * 5  # 5 white pieces at point 5
        self.points[7] = ["W"] * 3  # 3 white pieces at point 7
        self.points[11] = ["W"] * 5  # 5 white pieces at point 11
        self.points[12] = ["B"] * 5  # 5 black pieces at point 12
        self.points[16] = ["B"] * 3  # 3 black pieces at point 16
        self.points[18] = ["B"] * 5  # 5 black pieces at point 18
        self.points[23] = ["W", "W"]  # 2 white pieces at point 23
        self.bar = {"W": 0, "B": 0}
        self.borne_off = {"W": 0, "B": 0}

    def is_valid_move(self, from_point: int, to_point: int, color: str) -> bool:
        """Check if move is valid.

        Args:
            from_point: Starting point (0-23)
            to_point: Target point (0-23)
            color: Color of moving piece ('W' or 'B')

        Returns:
            bool: True if move is valid
        """
        if not 0 <= from_point < 24 or not 0 <= to_point < 24:
            return False

        if self.bar[color] > 0:
            return False

        if not self.points[from_point] or self.points[from_point][0] != color:
            return False

        if (
            self.points[to_point]
            and len(self.points[to_point]) >= 2
            and self.points[to_point][0] != color
        ):
            return False

        return True

    def move_checker(self, from_point: int, to_point: int, color: str) -> bool:
        """Move checker if valid.

        Args:
            from_point: Starting point
            to_point: Target point
            color: Color of moving piece

        Returns:
            bool: True if move was successful
        """
        if not self.is_valid_move(from_point, to_point, color):
            return False

        # Handle hitting opponent's blot
        if (
            self.points[to_point]
            and len(self.points[to_point]) == 1
            and self.points[to_point][0] != color
        ):
            hit_color = self.points[to_point][0]
            self.bar[hit_color] += 1
            self.points[to_point] = []

        # Move checker
        if self.points[from_point]:
            checker = self.points[from_point].pop()
            self.points[to_point].append(checker)
            return True

        return False

    def bear_off(self, color: str, point: int) -> bool:
        """Remove piece from board.

        Args:
            color: Color of piece to bear off
            point: Point to bear off from

        Returns:
            bool: True if piece was borne off
        """
        if not self.can_bear_off(color):
            return False
        if not self.points[point] or self.points[point][0] != color:
            return False
        self.points[point].pop()
        self.borne_off[color] += 1
        return True

    def can_enter_from_bar(self, color: str, point: int) -> bool:
        """Check if piece can enter from bar.

        Args:
            color: Color of piece
            point: Target point

        Returns:
            bool: True if piece can enter
        """
        if not self.points[point]:
            return True
        if len(self.points[point]) < 2:
            return True
        return self.points[point][0] == color

    def can_bear_off(self, color: str) -> bool:
        """Check if player can bear off pieces.

        Args:
            color: Color to check

        Returns:
            bool: True if all pieces are in home board
        """
        if self.bar[color] > 0:
            return False

        start = 18 if color == "W" else 0

        # Check no pieces outside home board
        for i in range(0, start):
            if any(c == color for c in self.points[i]):
                return False
        return True

    def is_valid(self) -> bool:
        """Check if board state is valid.

        Returns:
            bool: True if no points have mixed colors
        """
        return all(
            not point or all(c == point[0] for c in point) for point in self.points
        )

    def move_checker_from_bar(self, to_point: int, color: str) -> bool:
        """Move checker from bar to home board.

        Args:
            to_point: Target point (must be 0-5 for Black, 18-23 for White)
            color: Color of moving piece ('W' or 'B')

        Returns:
            bool: True if move was successful
        """
        # Check if player has pieces on bar
        if self.bar[color] == 0:
            return False

        # White enters at points 18-23, Black enters at points 0-5
        if color == "W" and not (18 <= to_point <= 23):
            return False
        if color == "B" and not (0 <= to_point <= 5):
            return False

        # Check if point is available
        if not self.can_enter_from_bar(color, to_point):
            return False

        # Handle hitting opponent's blot
        if (
            self.points[to_point]
            and len(self.points[to_point]) == 1
            and self.points[to_point][0] != color
        ):
            hit_color = self.points[to_point][0]
            self.bar[hit_color] += 1
            self.points[to_point] = []

        # Move checker from bar
        self.bar[color] -= 1
        self.points[to_point].append(color)
        return True
