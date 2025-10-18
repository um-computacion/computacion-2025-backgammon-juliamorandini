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
            surface: Pygame surface to draw on
        """
        # Choose color based on hover state
        current_color = self.hover_color if self.is_hovered else self.color
        
        # Draw button rectangle with rounded corners effect
        pygame.draw.rect(surface, current_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2, border_radius=8)
        
        # Draw text centered on button
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        """
        Handle mouse events for the button.
        
        Args:
            event: Pygame event
            
        Returns:
            True if button was clicked, False otherwise
        """
        if event.type == pygame.MOUSEMOTION:
            # Update hover state based on mouse position
            self.is_hovered = self.rect.collidepoint(event.pos)
            return False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if button was clicked
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        
        return False
    