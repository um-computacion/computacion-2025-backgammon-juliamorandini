"""Board component that integrates all Backgammon pieces."""

import pygame
from typing import List
from ..constants import (WINDOW_WIDTH, WINDOW_HEIGHT, BORDER_WIDTH,
                        WOOD_COLOR, BORDER_COLOR)
from .point import Point
from .bar import Bar
from .panel import Panel

class Board:
    """Main Backgammon board that contains all components."""

    def __init__(self):
        """Initialize board and all its components."""
        self.surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.border_width = BORDER_WIDTH
        self.points: List[Point] = []
        self._setup_points()
        
        # Create bar in center
        bar_x = (WINDOW_WIDTH - 40) // 2  # 40 is bar width
        self.bar = Bar(bar_x, BORDER_WIDTH, 40, 
                      WINDOW_HEIGHT - 2 * BORDER_WIDTH)
        
        # Create right panel
        panel_x = WINDOW_WIDTH - 100 - BORDER_WIDTH  # 100 is panel width
        self.panel = Panel(panel_x, BORDER_WIDTH, 100,
                          WINDOW_HEIGHT - 2 * BORDER_WIDTH)

    def _setup_points(self) -> None:
        """Create and position all board points."""
        point_width = 50
        point_height = (WINDOW_HEIGHT - 2 * BORDER_WIDTH) // 2
        points_per_quadrant = 6
        
        # Calculate spacing between points
        available_width = (WINDOW_WIDTH - 2 * BORDER_WIDTH - 40) // 2  # 40 is bar width
        point_spacing = available_width // points_per_quadrant
        
        # Create points for both halves
        for i in range(24):
            x = BORDER_WIDTH + (i % 12) * point_spacing
            if i >= 12:  # Right half
                x += 40  # Add bar width
            
            y = BORDER_WIDTH if i < 12 else WINDOW_HEIGHT // 2
            is_light = i % 2 == 0
            points_up = i >= 12
            
            self.points.append(Point(x, y, point_width, point_height,
                                   is_light, points_up))

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the complete board with all components.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Draw wooden background
        self.surface.fill(WOOD_COLOR)
        
        # Draw border
        pygame.draw.rect(self.surface, BORDER_COLOR,
                        (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT),
                        self.border_width)
        
        # Draw all components
        for point in self.points:
            point.draw(self.surface)
        self.bar.draw(self.surface)
        self.panel.draw(self.surface)
        
        # Draw to screen
        screen.blit(self.surface, (0, 0))