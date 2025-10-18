"""Panel component for bearing off area."""

import pygame
from typing import Tuple
from ..constants import WOOD_COLOR

class Panel:
    """Right panel for bearing off in Backgammon."""

    def __init__(self, x: int, y: int, width: int, height: int):
        """Initialize panel properties.
        
        Args:
            x: X coordinate
            y: Y coordinate
            width: Panel width
            height: Panel height
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, surface: pygame.Surface) -> None:
        """Draw panel with sections.
        
        Args:
            surface: Pygame surface to draw on
        """
        # Draw background
        pygame.draw.rect(surface, WOOD_COLOR,
                        (self.x, self.y, self.width, self.height))
        
        # Draw sections
        section_height = self._get_section_height()
        self._draw_sections(surface, section_height)

    def _get_section_height(self) -> int:
        """Calculate height of each section.
        
        Returns:
            int: Height of one section
        """
        return self.height // 3

    def _draw_sections(self, surface: pygame.Surface, section_height: int) -> None:
        """Draw panel sections.
        
        Args:
            surface: Pygame surface to draw on
            section_height: Height of each section
        """
        # Middle section is already drawn with background
        # Top section stripes
        self._draw_stripes(surface, self.y, section_height)
        # Bottom section stripes
        self._draw_stripes(surface, self.y + 2 * section_height, section_height)

    def _draw_stripes(self, surface: pygame.Surface, start_y: int, height: int) -> None:
        """Draw diagonal stripes in a section.
        
        Args:
            surface: Pygame surface to draw on
            start_y: Starting Y coordinate
            height: Section height
        """
        stripe_width = 10
        for i in range(0, self.width + height, stripe_width * 2):
            points = [
                (self.x + i, start_y),
                (self.x + i + stripe_width, start_y),
                (self.x + i - height, start_y + height),
                (self.x + i - height - stripe_width, start_y + height)
            ]
            pygame.draw.polygon(surface, (53, 101, 77), points)