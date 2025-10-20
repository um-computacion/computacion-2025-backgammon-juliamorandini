"""
Main coordinator class for the backgammon board UI.
Manages the board structure and coordinates rendering.
"""
from typing import List

from core.board import Board
from core.Dice import Dice
from pygame_ui.board_renderer import BoardRenderer
from pygame_ui.checker_renderer import CheckerRenderer
from pygame_ui.dice_renderer import DiceRenderer


class BackgammonBoard:
    """
    Main coordinator class that manages the board structure and rendering.
    
    Bridges the game logic (Board class) with the visual representation.
    This class follows Single Responsibility Principle by coordinating
    between game logic and UI rendering.
    """
   
    def __init__(self) -> None:
        """
        Initialize the board with game logic and renderers.
        
        Creates the game board, dice, and all necessary renderers
        for displaying the game state.
        
        Args:
            None
            
        Returns:
            None
        """
        # Game logic
        self.__board__: Board = Board()
        self.__dice__: Dice = Dice()
       
        # Renderers
        self.__board_renderer__: BoardRenderer = BoardRenderer()
        self.__checker_renderer__: CheckerRenderer = CheckerRenderer()
        self.__dice_renderer__: DiceRenderer = DiceRenderer()
       
        # Game state
        self.__current_player__: str = "W"  # W for White, B for Black
        self.__dice_values__: List[int] = []
   
    @property
    def board(self) -> Board:
        """
        Get the game board.
        
        Returns:
            Board object containing game state
        """
        return self.__board__
    
    @property
    def current_player(self) -> str:
        """
        Get the current player.
        
        Returns:
            'W' for White or 'B' for Black
        """
        return self.__current_player__
    
    @property
    def dice_values(self) -> List[int]:
        """
        Get the current available dice values.
        
        Returns:
            List of available dice values for moves
        """
        return self.__dice_values__
    
    def render(self, surface) -> None:
        """
        Render the complete board with all pieces.
        
        Draws the board structure, checkers, and dice in the correct order.
       
        Args:
            surface: Pygame surface to draw on
            
        Returns:
            None
        """
        # Draw board structure
        self.__board_renderer__.draw(surface)
       
        # Draw checkers based on board state
        self.__checker_renderer__.draw(surface, self.__board__)
       
        # Draw dice if rolled (and there are dice values available)
        if self.__dice_values__ and len(self.__dice_values__) > 0:
            # Show only the first two dice values for display
            display_values: List[int] = self.__dice_values__[:2]
            self.__dice_renderer__.draw(surface, display_values)
   
    def update(self) -> None:
        """
        Update board state (placeholder for future game logic).
        
        This will handle animations, timers, etc. in future versions.
        
        Args:
            None
            
        Returns:
            None
        """
        pass
   
    def reset(self) -> None:
        """
        Reset the board to starting position.
        
        Resets the board, dice, and game state to initial configuration.
        
        Args:
            None
            
        Returns:
            None
        """
        self.__board__.reset()
        self.__dice__.reset()
        self.__current_player__ = "W"
        self.__dice_values__ = []
   
    def roll_dice(self) -> List[int]:
        """
        Roll dice for current player.
        
        Uses the Dice class to roll two dice. If doubles are rolled,
        the player gets 4 moves of that value. Otherwise, 2 moves.
        
        Args:
            None
            
        Returns:
            List of available move values
        """
        self.__dice__.roll()
        self.__dice_values__ = self.__dice__.get_moves()
        return self.__dice_values__
   
    def move_checker(self, from_point: int, to_point: int) -> bool:
        """
        Attempt to move a checker.
        
        Validates and executes a checker move on the board.
       
        Args:
            from_point: Starting point (0-23)
            to_point: Destination point (0-23)
           
        Returns:
            True if move was successful, False otherwise
        """
        return self.__board__.move_checker(from_point, to_point, self.__current_player__)
   
    def switch_player(self) -> None:
        """
        Switch to the other player.
        
        Toggles between White and Black player and clears dice values.
        
        Args:
            None
            
        Returns:
            None
        """
        self.__current_player__ = "B" if self.__current_player__ == "W" else "W"
        self.__dice_values__ = []