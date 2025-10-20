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
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = pygame.font.Font(None, font_size)
        self.is_hovered = False
        print(f"Button '{text}' created at {self.rect}")  # Debug print

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the button on the given surface."""
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2)  # Border

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

        if self.is_hovered:  # Debug visual feedback
            pygame.draw.rect(surface, (255, 255, 0), self.rect, 1)

    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events and return True if clicked."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Get the current mouse position
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                print(f"Button '{self.text}' clicked at {mouse_pos}")  # Debug print
                return True
            else:
                print(f"Click at {mouse_pos} missed button at {self.rect}")  # Debug print
        return False