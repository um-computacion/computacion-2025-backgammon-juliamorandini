from core.board import Board
from core.player import Player
from core.Dice import Dice

class Game:
    """A Backgammon game."""

    def __init__(self):
        """Create new game with board, players and dice."""
        # Create game components
        self.board = Board()
        self.dice = Dice()
        self.players = {
            'white': Player("Player 1", "white"),
            'black': Player("Player 2", "black")
        }
        self.current_player = 'white'
        self.game_over = False

    def roll_dice(self):
        """Roll dice and return values."""
        return self.dice.roll()

    def move_checker(self, from_point: int, to_point: int) -> bool:
        """Move a checker if valid."""
        # Get current player
        player = self.players[self.current_player]
        
        # Check if move is valid
        if not player.is_valid_move(to_point - from_point):
            return False
            
        # Try to move checker
        if self.board.move_checker(from_point, to_point, self.current_player):
            return True
        return False

    def can_bear_off(self) -> bool:
        """Check if current player can bear off."""
        return self.board.can_bear_off(self.current_player)

    def bear_off(self, point: int) -> bool:
        """Try to bear off a checker."""
        if not self.can_bear_off():
            return False
        return self.board.bear_off(point, self.current_player)

    def switch_turn(self):
        """Switch to other player's turn."""
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def check_winner(self) -> str:
        """Check if there's a winner."""
        # Check if any player has won
        for color, player in self.players.items():
            if player.has_won():
                self.game_over = True
                return color
        return None

    def get_valid_moves(self, dice_values) -> list:
        """Get list of valid moves for current roll."""
        valid_moves = []
        
        # Check each possible move
        for die in dice_values:
            for from_point in range(24):
                to_point = from_point + die
                if to_point < 24:
                    if self.board.move_checker(from_point, to_point, self.current_player):
                        valid_moves.append((from_point, to_point))
                        # Undo move to keep checking
                        self.board.move_checker(to_point, from_point, self.current_player)
                        
        return valid_moves