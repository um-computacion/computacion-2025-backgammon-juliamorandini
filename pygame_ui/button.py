"""
Button UI component for creating interactive buttons.
"""
import pygame
from typing import Tuple


class Button:
    """
    A clickable button component.
    
    Handles rendering and click detection for UI buttons.
    This class follows Single Responsibility Principle by only
    managing button appearance and interaction.
    """
   
    def __init__(self, x: int, y: int, width: int, height: int, text: str,
                 color: Tuple[int, int, int] = (100, 100, 100),
                 hover_color: Tuple[int, int, int] = (150, 150, 150),
                 text_color: Tuple[int, int, int] = (255, 255, 255)) -> None:
        """
        Initialize a button.
        
        Creates a button with the specified position, size, and appearance.
       
        Args:
            x: X position of button top-left corner
            y: Y position of button top-left corner
            width: Button width in pixels
            height: Button height in pixels
            text: Text to display on button
            color: Default button background color (R, G, B)
            hover_color: Color when mouse hovers over button (R, G, B)
            text_color: Color of button text (R, G, B)
            
        Returns:
            None
        """
        self.__rect__: pygame.Rect = pygame.Rect(x, y, width, height)
        self.__text__: str = text
        self.__color__: Tuple[int, int, int] = color
        self.__hover_color__: Tuple[int, int, int] = hover_color
        self.__text_color__: Tuple[int, int, int] = text_color
        self.__is_hovered__: bool = False
        self.__font__: pygame.font.Font = pygame.font.Font(None, 32)
   
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the button on the surface.
        
        Renders the button with appropriate color based on hover state
        and centers the text on the button.
       
        Args:
            surface: Pygame surface to draw on
            
        Returns:
            None
        """
        # Choose color based on hover state
        current_color: Tuple[int, int, int] = (
            self.__hover_color__ if self.__is_hovered__ else self.__color__
        )
       
        # Draw button rectangle with rounded corners effect
        pygame.draw.rect(surface, current_color, self.__rect__, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.__rect__, 2, border_radius=8)
       
        # Draw text centered on button
        text_surface: pygame.Surface = self.__font__.render(
            self.__text__, True, self.__text_color__
        )
        text_rect: pygame.Rect = text_surface.get_rect(center=self.__rect__.center)
        surface.blit(text_surface, text_rect)
   
    def handle_event(self, event: pygame.event.Event) -> bool:
        """
        Handle mouse events for the button.
        
        Updates hover state on mouse motion and detects clicks.
       
        Args:
            event: Pygame event object
           
        Returns:
            True if button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            # Update hover state based on mouse position
            self.__is_hovered__ = self.__rect__.collidepoint(event.pos)
            return False
       
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if button was clicked
            if event.button == 1 and self.__rect__.collidepoint(event.pos):
                return True
       
        return False