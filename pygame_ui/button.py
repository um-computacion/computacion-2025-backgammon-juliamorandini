"""Button component for Pygame UI."""

import pygame
from typing import Tuple


class Button:
    """A clickable button with hover effect."""

    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        color: Tuple[int, int, int] = (70, 130, 180),
        hover_color: Tuple[int, int, int] = (100, 160, 210),
        text_color: Tuple[int, int, int] = (255, 255, 255),
        font_size: int = 24,
    ) -> None:
        """Initialize button properties."""
        # Create rect in screen coordinates
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button on the given surface."""
        # Get screen-space mouse position
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

        # Draw button
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)

        # Draw centered text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events and return True if clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # FIX: Use event.pos instead of pygame.mouse.get_pos()
            return self.rect.collidepoint(event.pos)
        return False
