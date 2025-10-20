"""
Notification system for displaying messages to the player.
cada vez que se hacia un movimiento fuera de rango el programa se cerraba y se tenia que reiniciar partida
"""
import pygame
from config import Config


class Notification:
    """
    Displays temporary messages on screen.
    Shows errors, warnings, and info messages to the player.
    """
    
    def __init__(self):
        """Initialize the notification system."""
        self.messages = []  # List of (text, color, time_remaining)
        self.font = pygame.font.Font(None, 40)
        self.display_time = 3000  # 3 seconds in milliseconds
    
    def add_message(self, text, message_type="info"):
        """
        Add a new message to display.
        
        Args:
            text: Message text to display
            message_type: Type of message - "error", "warning", "info", "success"
        """
        # Choose color based on message type
        colors = {
            "error": (255, 50, 50),      # Red
            "warning": (255, 200, 50),   # Yellow
            "info": (100, 150, 255),     # Blue
            "success": (50, 255, 100)    # Green
        }
        
        color = colors.get(message_type, colors["info"])
        self.messages.append({
            "text": text,
            "color": color,
            "time": pygame.time.get_ticks(),
            "duration": self.display_time
        })
        
        # Keep only last 3 messages
        if len(self.messages) > 3:
            self.messages.pop(0)
    
    def update(self):
        """Update and remove expired messages."""
        current_time = pygame.time.get_ticks()
        self.messages = [
            msg for msg in self.messages
            if current_time - msg["time"] < msg["duration"]
        ]
    
    def draw(self, surface):
        """
        Draw all active messages on screen.
        
        Args:
            surface: Pygame surface to draw on
        """
        self.update()
        
        # Draw messages from top to bottom
        y_offset = 20
        for i, msg in enumerate(self.messages):
            # Calculate fade effect based on time remaining
            current_time = pygame.time.get_ticks()
            time_passed = current_time - msg["time"]
            time_remaining = msg["duration"] - time_passed
            
            # Fade out in last 500ms
            if time_remaining < 500:
                alpha = int(255 * (time_remaining / 500))
            else:
                alpha = 255
            
            # Render text with background
            text_surface = self.font.render(msg["text"], True, msg["color"])
            text_rect = text_surface.get_rect(center=(Config.SCREEN_WIDTH // 2, y_offset + i * 50))
            
            # Draw semi-transparent background
            bg_rect = text_rect.inflate(20, 10)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(min(200, alpha))
            bg_surface.fill((40, 40, 40))
            surface.blit(bg_surface, bg_rect)
            
            # Draw text
            text_surface.set_alpha(alpha)
            surface.blit(text_surface, text_rect)