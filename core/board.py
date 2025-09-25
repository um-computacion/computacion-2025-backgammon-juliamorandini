class Board:
    """Backgammon board representation."""

    def __init__(self):
        """Initialize empty board."""
        self.points = [[] for _ in range(24)]
        self.bar = {"W": 0, "B": 0}
        self.borne_off = {"W": 0, "B": 0}
        self.reset()

    def reset(self):
        """Reset board to initial position."""
        self.points = [
            [] for _ in range(24)
        ]  # es como la 8va vez que cambio y reviso esto
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
        """Check if move is valid."""
        if not 0 <= from_point < 24 or not 0 <= to_point < 24:
            return False

        # If player has pieces on bar, must move from bar first
        if self.bar[color] > 0 and from_point != "bar":
            return False

        # Check if from_point has player's pieces
        if not self.points[from_point] or self.points[from_point][0] != color:
            return False

        # Check if to_point is blocked by opponent
        if (
            self.points[to_point]
            and len(self.points[to_point]) >= 2
            and self.points[to_point][0] != color
        ):
            return False

        return True

    def move_checker(self, from_point: int, to_point: int, color: str) -> bool:
        """Move checker if valid."""
        if not self.is_valid_move(from_point, to_point, color):
            return False

        # Handle hitting opponent's blot (CAPTURE LOGIC)
        if (
            self.points[to_point]
            and len(self.points[to_point]) == 1
            and self.points[to_point][0] != color
        ):
            # Capture opponent's single piece
            hit_color = self.points[to_point][0]
            self.bar[hit_color] += 1  # Send to bar
            self.points[to_point] = []  # Clear the point
            print(f"Captured {hit_color} piece at point {to_point}")  # Debug

        # Move checker
        if self.points[from_point]:
            checker = self.points[from_point].pop()
            self.points[to_point].append(checker)
            return True

        return False

    def bear_off(self, color: str, point: int) -> bool:
        """Remove piece from board."""
        if not self.points[point] or self.points[point][0] != color:
            return False
        self.points[point].pop()
        self.borne_off[color] += 1
        return True

    def can_enter_from_bar(self, color: str, point: int) -> bool:
        """Check if piece can enter from bar."""
        if not self.points[point]:
            return True
        if len(self.points[point]) < 2:
            return True
        return self.points[point][0] == color

    def is_legal_move(self, from_point: int, to_point: int, color: str) -> bool:
        """Alias for is_valid_move."""
        return self.is_valid_move(from_point, to_point, color)

    def is_valid(self) -> bool:
        """Check if board state is valid (no mixed checkers on points)."""
        for point in self.points:
            if point:
                first_color = point[0]
                for checker in point:
                    if checker != first_color:
                        return False  # Estado inválido del tablero
        return True
