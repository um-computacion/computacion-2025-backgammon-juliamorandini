"""
Dice renderer for drawing dice on the board.
"""
import pygame
from typing import List

from config import Config


class DiceRenderer:
    """
    Renders dice on the board.
    
    Shows the current dice roll values with appropriate dot patterns.
    This class follows Single Responsibility Principle by only handling
    the visual rendering of dice.
    """
    
    def __init__(self) -> None:
        """
        Initialize the dice renderer.
        
        Sets up the position where dice will be drawn on the screen.
        Dice are positioned in the center-right area of the board.
        
        Args:
            None
            
        Returns:
            None
        """
        # Position dice in the center-right area
        self.__dice_x__: int = Config.BOARD_X + Config.BOARD_WIDTH // 2 + 100
        self.__dice_y__: int = Config.BOARD_Y + Config.BOARD_HEIGHT // 2 - Config.DICE_SIZE
    
    def draw(self, surface: pygame.Surface, dice_values: List[int]) -> None:
        """
        Draw dice showing the rolled values.
        
        Renders up to two dice with the appropriate dot patterns
        based on the values rolled.
        
        Args:
            surface: Pygame surface to draw on
            dice_values: List of dice values (e.g., [3, 5])
            
        Returns:
            None
        """
        if not dice_values:
            return
        
        # Draw first die
        if len(dice_values) >= 1:
            self._draw_die(surface, self.__dice_x__, self.__dice_y__, dice_values[0])
        
        # Draw second die
        if len(dice_values) >= 2:
            self._draw_die(
                surface,
                self.__dice_x__,
                self.__dice_y__ + Config.DICE_SIZE + 20,
                dice_values[1]
            )
    
    def _draw_die(self, surface: pygame.Surface, x: int, y: int, value: int) -> None:
        """
        Draw a single die showing the specified value.
        
        Creates a square die with rounded corners and appropriate
        dot pattern for the given value (1-6).
        
        Args:
            surface: Pygame surface to draw on
            x: X coordinate of die top-left corner
            y: Y coordinate of die top-left corner
            value: Die value (1-6)
            
        Returns:
            None
        """
        # Draw die background
        die_rect: pygame.Rect = pygame.Rect(x, y, Config.DICE_SIZE, Config.DICE_SIZE)
        pygame.draw.rect(surface, Config.DICE_WHITE, die_rect)
        pygame.draw.rect(surface, (0, 0, 0), die_rect, 2)  # Border
        
        # Add rounded corners effect
        pygame.draw.rect(surface, (200, 200, 200), die_rect, 1)
        
        # Calculate center position
        center_x: int = x + Config.DICE_SIZE // 2
        center_y: int = y + Config.DICE_SIZE // 2
        offset: int = Config.DICE_SIZE // 4
        
        # Draw dots based on value
        if value == 1:
            self._draw_dot(surface, center_x, center_y)
        
        elif value == 2:
            self._draw_dot(surface, center_x - offset, center_y - offset)
            self._draw_dot(surface, center_x + offset, center_y + offset)
        
        elif value == 3:
            self._draw_dot(surface, center_x - offset, center_y - offset)
            self._draw_dot(surface, center_x, center_y)
            self._draw_dot(surface, center_x + offset, center_y + offset)
        
        elif value == 4:
            self._draw_dot(surface, center_x - offset, center_y - offset)
            self._draw_dot(surface, center_x + offset, center_y - offset)
            self._draw_dot(surface, center_x - offset, center_y + offset)
            self._draw_dot(surface, center_x + offset, center_y + offset)
        
        elif value == 5:
            self._draw_dot(surface, center_x - offset, center_y - offset)
            self._draw_dot(surface, center_x + offset, center_y - offset)
            self._draw_dot(surface, center_x, center_y)
            self._draw_dot(surface, center_x - offset, center_y + offset)
            self._draw_dot(surface, center_x + offset, center_y + offset)
        
        elif value == 6:
            self._draw_dot(surface, center_x - offset, center_y - offset)
            self._draw_dot(surface, center_x + offset, center_y - offset)
            self._draw_dot(surface, center_x - offset, center_y)
            self._draw_dot(surface, center_x + offset, center_y)
            self._draw_dot(surface, center_x - offset, center_y + offset)
            self._draw_dot(surface, center_x + offset, center_y + offset)
    
    def _draw_dot(self, surface: pygame.Surface, x: int, y: int) -> None:
        """
        Draw a single dot on the die.
        
        Creates a circular black dot at the specified position.
        
        Args:
            surface: Pygame surface to draw on
            x: X coordinate of dot center
            y: Y coordinate of dot center
            
        Returns:
            None
        """
        pygame.draw.circle(
            surface,
            Config.DICE_DOT,
            (int(x), int(y)),
            Config.DICE_DOT_RADIUS
        )