class Checker:
    """A checker piece in Backgammon."""

    def __init__(self, color: str, position: int) -> None:
        """Create a new checker.
        
        Args:
            color: 'white' or 'black'
            position: Starting position (0-23)
        """
        if color not in ['white', 'black']:
            raise ValueError("Color must be 'white' or 'black'")

        self.color = color
        self.position = position
        self.is_on_bar = False
        self.is_borne_off = False

    def move_to(self, new_position: int) -> bool:
        """Move checker to a new position."""
        if 0 <= new_position <= 23:
            self.position = new_position
            return True
        return False

    def send_to_bar(self) -> None:
        """Send checker to the bar."""
        self.position = 'bar'
        self.is_on_bar = True

    def bear_off(self) -> None:
        """Bear off (remove) the checker from board."""
        self.position = 'off'
        self.is_borne_off = True

    def can_bear_off(self, all_home: bool) -> bool:
        """Check if checker can be borne off."""
        if not all_home:
            return False
            
        if not isinstance(self.position, int):
            return False

        if self.color == 'white':
            return self.position >= 18
        return self.position <= 5