class Player:
    """Player in Backgammon game."""
    
    def __init__(self, name: str, color: str):
        """Create new player."""
        self.name = name
        self.color = color
        self.points = 0
        self.pieces_in_home = 15
        self.pieces_on_bar = 0
        self.current_position = 0
        self.pieces_at_point = 2

    def can_bear_off(self):
        """Check if player can bear off."""
        return self.pieces_in_home == 15

    def is_point_blocked(self, point: int, opponent) -> bool:
        """Check if point is blocked by opponent."""
        return opponent.current_position == point and opponent.pieces_at_point >= 2

    def can_hit_opponent(self, opponent):
        """Check if can hit opponent's piece."""
        same_pos = opponent.current_position == self.current_position
        return same_pos and opponent.pieces_at_point == 1

    def is_point_secure(self):
        """Check if current point is secure (2+ pieces)."""
        return self.pieces_at_point >= 2