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
        # Traditional Backgammon setup:
        self.points[0] = ['W', 'W']      # White at point 1
        self.points[5] = ['B'] * 5       # Black at point 6 (was white)
        self.points[7] = ['B'] * 3       # Black at point 8 (was white)  
        self.points[11] = ['B'] * 5      # Black at point 12 (was white)
        self.points[12] = ['W'] * 5      # White at point 13 (was black)
        self.points[16] = ['W'] * 3      # White at point 17 (was black)
        self.points[18] = ['W'] * 5      # White at point 19 (was black)
        self.points[23] = ['B', 'B']     # Black at point 24
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
    
    def is_valid(self) -> bool:
        """Check if board state is valid (no mixed checkers on points)."""
        for point in self.points:
            if point:
                first_color = point[0]
                for checker in point:
                    if checker != first_color:
                        return False  # Estado inválido del tablero
        return True