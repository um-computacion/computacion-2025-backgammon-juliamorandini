"""
Button UI component for creating interactive buttons.
"""
import pygame


class Button:
    """
    A clickable button component.
    Handles rendering and click detection.
    """
    
    def __init__(self, x, y, width, height, text, 
                 color=(100, 100, 100), 
                 hover_color=(150, 150, 150), 
                 text_color=(255, 255, 255)):
        """
        Initialize a button.
        
        Args:
            x: X position of button
            y: Y position of button
            width: Button width
            height: Button height
            text: Text to display on button
            color: Default button color
            hover_color: Color when mouse hovers over button
            text_color: Color of button text
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
        self.font = pygame.font.Font(None, 32)
    
    def draw(self, surface):
        """
        Draw the button on the surface.
        
        Args:
            surface: Pygame
            """