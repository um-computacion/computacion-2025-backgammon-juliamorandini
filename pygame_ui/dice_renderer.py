"""
Dice renderer for drawing dice on the board.
"""
import pygame
from config import Config
from typing import List


class DiceRenderer:
    """
    Renders dice on the board.
    Shows the current dice roll values.
    """
    
    def __init__(self):
        """Initialize the dice renderer."""
        # Position dice in the center-right area
        self.dice_x = Config.BOARD_X + Config.BOARD_WIDTH // 2 + 100
        self.dice_y = Config.BOARD_Y + Config.BOARD_HEIGHT // 2 - Config.DICE_SIZE
    
    def draw(self, surface, dice_values: List[int]):
        """
        Draw dice showing the rolled values.
        
        Args:
            surface: Pygame surface to draw on
            dice_values: List of dice values (e.g., [3, 5])
        """
        if not dice_values:
            return
        
        # Draw first die
        if len(dice_values) >= 1:
            self._draw_die(surface, self.dice_x, self.dice_y, dice_values[0])
        
        # Draw second die
        if len(dice_values) >= 2:
            self._draw_die(
                surface,
                self.dice_x,
                self.dice_y + Config.DICE_SIZE + 20,
                dice_values[1]
            )
    
    def _draw_die(self, surface, x, y, value):
        """
        Draw a single die showing the specified value.
        
        Args:
            surface: Pygame surface to draw on
            x: X coordinate of die top-left corner
            y: Y coordinate of die top-left corner
            value: Die value (1-6)
        """
        # Draw die background
        die_rect = pygame.Rect(x, y, Config.DICE_SIZE, Config.DICE_SIZE)
        pygame.draw.rect(surface, Config.DICE_WHITE, die_rect)
        pygame.draw.rect(surface, (0, 0, 0), die_rect, 2)  # Border
        
        # Add rounded corners effect
        pygame.draw.rect(surface, (200, 200, 200), die_rect, 1)
        
        # Calculate center position
        center_x = x + Config.DICE_SIZE // 2
        center_y = y + Config.DICE_SIZE // 2
        offset = Config.DICE_SIZE // 4
        
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
    
    def _draw_dot(self, surface, x, y):
        """
        Draw a single dot on the die.
        
        Args:
            surface: Pygame surface to draw on
            x: X coordinate of dot center
            y: Y coordinate of dot center
        """
        pygame.draw.circle(
            surface,
            Config.DICE_DOT,
            (int(x), int(y)),
            Config.DICE_DOT_RADIUS
        )