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
        self.points[0] = ["B", "B"]  # 2 black pieces at point 1
        self.points[5] = ["W"] * 5  # 5 white pieces at point 6
        self.points[7] = ["W"] * 3  # 3 white pieces at point 8
        self.points[11] = ["W"] * 5  # 5 white pieces at point 12
        self.points[12] = ["B"] * 5  # 5 black pieces at point 13
        self.points[16] = ["B"] * 3  # 3 black pieces at point 17
        self.points[18] = ["B"] * 5  # 5 black pieces at point 19
        self.points[23] = ["W", "W"]  # 2 white pieces at point 24
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
        # Check point bounds
        if not 0 <= from_point < 24 or not 0 <= to_point < 24:
            return False

        # Check if player has pieces on bar
        if self.bar[color] > 0:
            return False

        # Check if from_point has checkers and they belong to player
        if not self.points[from_point] or self.points[from_point][0] != color:
            return False

        # Check if to_point is not blocked by opponent
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
        checker = self.points[from_point].pop()
        self.points[to_point].append(checker)

        # Ensure point maintains consistent color
        if len(self.points[to_point]) > 1:
            self.points[to_point] = [self.points[to_point][0]] * len(
                self.points[to_point]
            )

        return True

    def bear_off(self, color: str, point: int) -> bool:
        """Remove piece from board.

        Args:
            color: Color of piece to bear off
            point: Point to bear off from

        Returns:
            bool: True if piece was borne off
        """
        # Check if bearing off is allowed
        if not self.can_bear_off(color):
            return False

        # Check if point has checkers and they belong to player
        if not self.points[point] or self.points[point][0] != color:
            return False

        # Remove checker and update borne off count
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
        if not 0 <= point < 24:
            return False

        if not self.points[point]:
            return True

        if len(self.points[point]) == 1 and self.points[point][0] != color:
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

        # Define home board ranges
        if color == "W":
            home_range = range(18, 24)  # Points 19-24
            outside_range = range(0, 18)  # Points 1-18
        else:  # color == "B"
            home_range = range(0, 6)  # Points 1-6
            outside_range = range(6, 24)  # Points 7-24

        # Check if any pieces are outside home board
        for i in outside_range:
            if any(checker == color for checker in self.points[i]):
                return False

        return True

    def is_valid(self) -> bool:
        """Check if board state is valid.

        Returns:
            bool: True if no points have mixed colors
        """
        for point in self.points:
            if point and not all(checker == point[0] for checker in point):
                return False
        return True

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

        # Validate target point based on color
        if color == "W" and not (18 <= to_point <= 23):
            return False
        if color == "B" and not (0 <= to_point <= 5):
            return False

        # Check if point is available for entry
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

        # Move checker from bar to board
        self.bar[color] -= 1
        self.points[to_point].append(color)
        return True

    def get_point(self, point: int) -> List[str]:
        """Get checkers at specific point.

        Args:
            point: Point index (0-23)

        Returns:
            List of checkers at the point
        """
        if 0 <= point < 24:
            return self.points[point]
        return []

    def set_point(self, point: int, checkers: List[str]) -> None:
        """Set checkers at specific point.

        Args:
            point: Point index (0-23)
            checkers: List of checkers to set
        """
        if 0 <= point < 24:
            self.points[point] = checkers
