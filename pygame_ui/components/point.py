"""Point component for Backgammon board."""

from typing import Tuple
import pygame
from ..constants import LIGHT_POINT, DARK_POINT

class Point:
    """A triangular point on the board."""

    def __init__(self, x: int, y: int, width: int, height: int, 
                 is_light: bool = True, points_up: bool = True):
        """Initialize point properties."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = LIGHT_POINT if is_light else DARK_POINT
        self.points_up = points_up

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the point on given surface."""
        points = self._calculate_points()
        pygame.draw.polygon(surface, self.color, points)

    def _calculate_points(self) -> list[Tuple[int, int]]:
        """Calculate triangle vertices."""
        if self.points_up:
            return [
                (self.x, self.y + self.height),
                (self.x + self.width//2, self.y),
                (self.x + self.width, self.y + self.height)
            ]
        return [
            (self.x, self.y),
            (self.x + self.width//2, self.y + self.height),
            (self.x + self.width, self.y)
        ]