"""Bar component for Backgammon board."""

import pygame
from typing import Tuple
from ..constants import BAR_COLOR, HINGE_COLOR

class Bar:
    """Central bar dividing the Backgammon board."""

    def __init__(self, x: int, y: int, width: int, height: int):
        """Initialize bar properties.
        
        Args:
            x: X coordinate
            y: Y coordinate
            width: Bar width
            height: Bar height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, surface: pygame.Surface) -> None:
        """Draw bar and hinges on surface.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw main bar
        pygame.draw.rect(surface, BAR_COLOR, 
                        (self.x, self.y, self.width, self.height))

        # Draw hinges
        self._draw_hinges(surface)

    def _draw_hinges(self, surface: pygame.Surface) -> None:
        """Draw decorative hinges on bar.
        
        Args:
            surface: Pygame surface to draw on
        """
        hinge_width = self.width * 1.5
        hinge_height = 20

        # Top hinge
        pygame.draw.ellipse(surface, HINGE_COLOR,
                          (self.x - hinge_width//4, self.y,
                           hinge_width, hinge_height))

        # Bottom hinge
        pygame.draw.ellipse(surface, HINGE_COLOR,
                          (self.x - hinge_width//4,
                           self.y + self.height - hinge_height,
                           hinge_width, hinge_height))