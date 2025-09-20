class Player:
    """A player in Backgammon game."""
    
    def __init__(self, name, color):
        """Create new player."""
        # Check valid color
        if color not in ['white', 'black']:
            raise ValueError("Color must be 'white' or 'black'")
        
        # Player basic info
        self.name = name
        self.color = color
        
        # Game state
        self.pieces_in_home = 0  # Pieces in home board
        self.pieces_on_bar = 0   # Pieces on bar
        self.pieces_removed = 0  # Pieces taken off
        self.current_position = 0
        self.pieces_at_point = 0 # Pieces at current point

    def is_valid_move(self, dice_roll):
        """Check if move is valid with dice roll."""
        # Calculate new position
        new_pos = self.current_position + dice_roll
        # Check if in board
        return 0 <= new_pos <= 23

    def can_hit_opponent(self, opponent):
        """Check if can hit opponent piece."""
        # Can hit if opponent has single piece
        same_pos = opponent.current_position == self.current_position
        single_piece = opponent.pieces_at_point == 1
        return same_pos and single_piece

    def can_bear_off(self):
        """Check if can bear off pieces."""
        # Need all pieces in home to bear off
        return self.pieces_in_home == 15

    def is_point_blocked(self, point: int, opponent) -> bool:
        """Check if point is blocked by opponent."""
        return (opponent.pieces_at_point >= 2 and 
                opponent.current_position == point)

    def has_won(self) -> bool:
        """Check if player has won."""
        # Win if all pieces removed
        return self.pieces_removed == 15

    def can_reenter_from_bar(self, entry_point: int) -> bool:
        """Check if piece can reenter from bar."""
        return self.pieces_on_bar > 0 and 0 <= entry_point <= 23