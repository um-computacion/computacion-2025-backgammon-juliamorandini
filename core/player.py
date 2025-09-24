class Player:
    """Player in Backgammon game."""
    
    def __init__(self, name: str, color: str):
        """Create new player.
        
        Args:
            name: Player's name
            color: Player's color (white/black)
        """
        def __init__(self, name: str, color: str):
            self.name = name
            self.color = color
            self.points = 0
            self.pieces_in_home_board = 15
            self.pieces_on_bar = 0
            self.current_position = 0
            self.pieces_at_point = 2
            self.pieces = [1] * 15  # Create list with 15 pieces
            self.pieces_removed = 0  

    def is_valid_move(self, dice_roll: int) -> bool:
        """Check if moving by dice_roll from current position is valid.
        
        Args:
            dice_roll: The number of points to move (1-6)
            
        Returns:
            bool: True if move is within board boundaries, False otherwise
        """
        # Board has points 1-24, movement must stay within bounds
        new_position = self.current_position + dice_roll
        return 1 <= new_position <= 24

    def can_reenter_from_bar(self, entry_point: int) -> bool:
        """Check if player can reenter from the bar at given entry point.
        
        Args:
            entry_point: The point number where reentry is attempted
            
        Returns:
            bool: True if reentry is possible, False otherwise
        """
        # Reentry is possible if player has pieces on bar and entry point is valid
        return self.pieces_on_bar > 0 and 1 <= entry_point <= 24

    def can_bear_off(self) -> bool:
        """Check if player can bear off."""
        return self.pieces_in_home_board == 15
        

    def is_point_blocked(self, point: int, opponent: 'Player') -> bool:
        """Check if point is blocked by opponent.
        
        Args:
            point: Point number to check
            opponent: Opponent player object
            
        Returns:
            bool: True if point is blocked, False otherwise
        """
        return opponent.current_position == point and opponent.pieces_at_point >= 2

    def can_hit_opponent(self, opponent: 'Player') -> bool:
        """Check if can hit opponent's piece.
        
        Args:
            opponent: Opponent player object
            
        Returns:
            bool: True if can hit opponent, False otherwise
        """
        same_pos = opponent.current_position == self.current_position
        return same_pos and opponent.pieces_at_point == 1

    def is_point_secure(self) -> bool:
        """Check if current point is secure (2+ pieces).
        
        Returns:
            bool: True if point is secure, False otherwise
        """
        return self.pieces_at_point >= 2
    
    def has_won(self) -> bool:
        """Check if player has won by bearing off all pieces."""
        return self.pieces_removed == 15