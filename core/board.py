class Board:
    """A Backgammon board."""

    def __init__(self):
        """Initialize empty board."""
        self.points = [0] * 24  # 24 points (positive for white, negative for black)
        self.bar = {'white': 0, 'black': 0}
        self.borne_off = {'white': 0, 'black': 0}
        self.reset()

    def reset(self):
        """Reset board to starting position."""
        self.points = [0] * 24
        # Set starting pieces
        self.points[0] = -2  # 2 Black pieces on 0 peak
        self.points[5] = 5   # 5 White pieces on peak 5
        self.points[7] = 3   # 3 White pieces on peak 7
        self.points[11] = 5  # White pieces
        self.points[12] = -5 # Black pieces
        self.points[16] = -3 # Black pieces
        self.points[18] = -5 # Black pieces
        self.points[23] = 2  # White pieces
        self.bar = {'white': 0, 'black': 0}
        self.borne_off = {'white': 0, 'black': 0}

    def move_checker(self, from_point: int, to_point: int, color: str) -> bool:
        """Move a checker if valid."""
        # Check if move is valid
        if not (0 <= from_point < 24 and 0 <= to_point < 24):
            return False
        if self.bar[color] > 0:
            return False
        if color == 'white' and self.points[from_point] <= 0:
            return False
        if color == 'black' and self.points[from_point] >= 0:
            return False
        if color == 'white' and self.points[to_point] < -1:
            return False
        if color == 'black' and self.points[to_point] > 1:
            return False

        # Handle hits
        sign = 1 if color == 'white' else -1
        if (color == 'white' and self.points[to_point] == -1) or \
           (color == 'black' and self.points[to_point] == 1):
            self.points[to_point] = 0
            self.bar['black' if color == 'white' else 'white'] += 1

        # Move piece
        self.points[from_point] -= sign
        self.points[to_point] += sign
        return True

    def bear_off(self, point: int, color: str) -> bool:
        """Remove piece from board if allowed."""
        # Check if bearing off is allowed
        start = 18 if color == 'white' else 0
        end = 24 if color == 'white' else 6
        
        # All pieces must be in home board
        for i in range(24):
            if color == 'white' and i < 18 and self.points[i] > 0:
                return False
            if color == 'black' and i > 5 and self.points[i] < 0:
                return False

        # Remove piece
        if color == 'white' and self.points[point] > 0:
            self.points[point] -= 1
            self.borne_off['white'] += 1
            return True
        if color == 'black' and self.points[point] < 0:
            self.points[point] += 1  
            self.borne_off['black'] += 1
            return True
            
        return False