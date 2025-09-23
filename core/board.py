class Board:
    """Backgammon board representation."""

    def __init__(self):
        """Initialize empty board."""
        self.points = [[] for _ in range(24)]
        self.bar = {'W': 0, 'B': 0}
        self.borne_off = {'W': 0, 'B': 0}
        self.reset()

    def reset(self):
        """Reset board to initial position."""
        self.points = [[] for _ in range(24)]
        # Initial setup with W/B notation
        self.points[0] = ['B', 'B']
        self.points[5] = ['W'] * 5
        self.points[7] = ['W'] * 3
        self.points[11] = ['W'] * 5
        self.points[12] = ['B'] * 5
        self.points[16] = ['B'] * 3
        self.points[18] = ['B'] * 5
        self.points[23] = ['W', 'W']
        self.bar = {'W': 0, 'B': 0}
        self.borne_off = {'W': 0, 'B': 0}

    def is_valid_move(self, from_point: int, to_point: int, color: str) -> bool:
        """Check if move is valid."""
        if not 0 <= from_point < 24 or not 0 <= to_point < 24:
            return False
        if self.bar[color] > 0:
            return False
        if not self.points[from_point] or self.points[from_point][0] != color:
            return False
        if len(self.points[to_point]) >= 2 and self.points[to_point][0] != color:
            return False
        return True

    def move_checker(self, from_point: int, to_point: int, color: str) -> bool:
        """Move checker if valid."""
        if not self.is_valid_move(from_point, to_point, color):
            return False

        # Handle hitting opponent's blot
        if self.points[to_point] and self.points[to_point][0] != color:
            hit_color = self.points[to_point][0]
            self.bar[hit_color] += 1
            self.points[to_point] = []

        # Move checker
        self.points[from_point].pop()
        self.points[to_point].append(color)
        return True

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