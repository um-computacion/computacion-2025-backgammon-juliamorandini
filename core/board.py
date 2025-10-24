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
        self.points[0] = ["B", "B"]
        self.points[5] = ["W"] * 5
        self.points[7] = ["W"] * 3
        self.points[11] = ["W"] * 5
        self.points[12] = ["B"] * 5
        self.points[16] = ["B"] * 3
        self.points[18] = ["B"] * 5
        self.points[23] = ["W", "W"]
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

        if (
            self.points[to_point]
            and len(self.points[to_point]) == 1
            and self.points[to_point][0] != color
        ):
            hit_color = self.points[to_point][0]
            self.bar[hit_color] += 1
            self.points[to_point] = []

        checker = self.points[from_point].pop()
        self.points[to_point].append(checker)

        if len(self.points[to_point]) > 1:
            # Re-ensure all elements are the same color string for consistency
            # (Though popping and appending maintains color if is_valid is true)
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

        # Define ranges based on color
        if color == "W":
            outside_range = range(0, 18)  # Points 0-17
        else:
            outside_range = range(6, 24)  # Points 6-23

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
        if self.bar[color] == 0:
            return False

        # Check if the target point is in the correct home board range
        if color == "W" and not (18 <= to_point <= 23):
            return False
        if color == "B" and not (0 <= to_point <= 5):
            return False

        if not self.can_enter_from_bar(color, to_point):
            return False

        # Hit logic (only hits if it's a single opponent piece)
        if (
            self.points[to_point]
            and len(self.points[to_point]) == 1
            and self.points[to_point][0] != color
        ):
            hit_color = self.points[to_point][0]
            self.bar[hit_color] += 1
            self.points[to_point] = []

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
