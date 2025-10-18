"""
Main coordinator class for the backgammon board UI.
Manages the board structure and coordinates rendering.
"""
from core.board import Board
from pygame_ui.board_renderer import BoardRenderer
from pygame_ui.checker_renderer import CheckerRenderer
from pygame_ui.dice_renderer import DiceRenderer


class BackgammonBoard:
    """
    Main coordinator class that manages the board structure and rendering.
    Bridges the game logic (Board class) with the visual representation.
    """
    
    def __init__(self):
        """Initialize the board with game logic and renderers."""
        # Game logic
        self.board = Board()
        
        # Renderers
        self.board_renderer = BoardRenderer()
        self.checker_renderer = CheckerRenderer()
        self.dice_renderer = DiceRenderer()
        
        # Game state
        self.current_player = "W"  # W for White, B for Black
        self.dice_values = []
    
    def render(self, surface):
        """
        Render the complete board with all pieces.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw board structure
        self.board_renderer.draw(surface)
        
        # Draw checkers based on board state
        self.checker_renderer.draw(surface, self.board)
        
        # Draw dice if rolled
        if self.dice_values:
            self.dice_renderer.draw(surface, self.dice_values)
    
    def update(self):
        """
        Update board state (placeholder for future game logic).
        This will handle animations, timers, etc.
        """
        pass
    
    def reset(self):
        """Reset the board to starting position."""
        self.board.reset()
        self.current_player = "W"
        self.dice_values = []
    
    def roll_dice(self):
        """Roll dice for current player."""
        import random
        self.dice_values = [random.randint(1, 6), random.randint(1, 6)]
        return self.dice_values
    
    def move_checker(self, from_point, to_point):
        """
        Attempt to move a checker.
        
        Args:
            from_point: Starting point (0-23)
            to_point: Destination point (0-23)
            
        Returns:
            bool: True if move was successful
        """
        return self.board.move_checker(from_point, to_point, self.current_player)
    
    def switch_player(self):
        """Switch to the other player."""
        self.current_player = "B" if self.current_player == "W" else "W"
        self.dice_values = []