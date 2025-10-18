"""
Board renderer that draws the empty backgammon board structure.
Handles drawing the board, points, bar, and right panel.
"""
import pygame
from config import Config


class BoardRenderer:
    """
    Renders the backgammon board structure without game pieces.
    Responsible for drawing the board, triangular points, bar, and side panel.
    """
    
    def __init__(self):
        """Initialize the board renderer."""
        self.inner_left = Config.BOARD_X + Config.BORDER_THICKNESS
        self.inner_right = Config.BOARD_X + Config.BOARD_WIDTH - Config.BORDER_THICKNESS
        self.inner_top = Config.BOARD_Y + Config.BORDER_THICKNESS
        self.inner_bottom = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
    
    def draw(self, surface):
        """
        Draw the complete backgammon board structure.
        
        Args:
            surface: Pygame surface to draw on
        """
        self._draw_border(surface)
        self._draw_board_background(surface)
        self._draw_points(surface)
        self._draw_bar(surface)
        self._draw_right_panel(surface)
    
    def _draw_border(self, surface):
        """Draw the dark brown border frame."""
        outer_rect = pygame.Rect(
            Config.BOARD_X,
            Config.BOARD_Y,
            Config.BOARD_WIDTH,
            Config.BOARD_HEIGHT
        )
        pygame.draw.rect(surface, Config.DARK_BROWN, outer_rect)
    
    def _draw_board_background(self, surface):
        """Draw the main wooden board background."""
        board_rect = pygame.Rect(
            self.inner_left,
            self.inner_top,
            self.inner_right - self.inner_left,
            self.inner_bottom - self.inner_top
        )
        pygame.draw.rect(surface, Config.WOOD_BROWN, board_rect)
    
    def _draw_points(self, surface):
        """Draw all 24 triangular points."""
        for i in range(12):
            x_pos = self._calculate_point_x(i)
            color = Config.LIGHT_TAN if i % 2 == 0 else Config.DARK_POINT
            
            # Top point (pointing down)
            top_points = [
                (x_pos, self.inner_top),
                (x_pos + Config.POINT_WIDTH, self.inner_top),
                (x_pos + Config.POINT_WIDTH / 2, self.inner_top + Config.POINT_HEIGHT)
            ]
            pygame.draw.polygon(surface, color, top_points)
            
            # Bottom point (pointing up)
            bottom_points = [
                (x_pos, self.inner_bottom),
                (x_pos + Config.POINT_WIDTH, self.inner_bottom),
                (x_pos + Config.POINT_WIDTH / 2, self.inner_bottom - Config.POINT_HEIGHT)
            ]
            pygame.draw.polygon(surface, color, bottom_points)
    
    def _calculate_point_x(self, index):
        """
        Calculate x position for a point based on its index (0-11).
        Points 0-5 are on the right side, 6-11 on the left side.
        """
        if index < 6:
            # Right side points (0-5)
            right_section_start = Config.BAR_X + Config.BAR_WIDTH
            return right_section_start + (5 - index) * Config.POINT_WIDTH
        else:
            # Left side points (6-11)
            return self.inner_left + (11 - index) * Config.POINT_WIDTH
    
    def _draw_bar(self, surface):
        """Draw the central green bar with brass hinges."""
        bar_height = self.inner_bottom - self.inner_top
        
        # Draw green bar background
        bar_rect = pygame.Rect(
            Config.BAR_X,
            self.inner_top,
            Config.BAR_WIDTH,
            bar_height
        )
        pygame.draw.rect(surface, Config.GREEN_BAR, bar_rect)
        
        # Add texture lines
        for i in range(8):
            y_pos = self.inner_top + (i + 1) * bar_height // 9
            pygame.draw.line(
                surface,
                (30, 70, 50),
                (Config.BAR_X, y_pos),
                (Config.BAR_X + Config.BAR_WIDTH, y_pos),
                1
            )
        
        # Draw hinges
        hinge_x = Config.BAR_X + (Config.BAR_WIDTH - Config.HINGE_WIDTH) // 2
        
        # Top hinge
        top_hinge = pygame.Rect(
            hinge_x,
            self.inner_top + 20,
            Config.HINGE_WIDTH,
            Config.HINGE_HEIGHT
        )
        pygame.draw.rect(surface, Config.BRASS, top_hinge)
        pygame.draw.rect(surface, (140, 100, 0), top_hinge, 2)
        
        # Bottom hinge
        bottom_hinge = pygame.Rect(
            hinge_x,
            self.inner_bottom - 35,
            Config.HINGE_WIDTH,
            Config.HINGE_HEIGHT
        )
        pygame.draw.rect(surface, Config.BRASS, bottom_hinge)
        pygame.draw.rect(surface, (140, 100, 0), bottom_hinge, 2)
    
    def _draw_right_panel(self, surface):
        """Draw the right side panel with diagonal stripes."""
        panel_height = self.inner_bottom - self.inner_top
        section_height = panel_height // 3
        
        # Top striped section
        self._draw_stripes(
            surface,
            Config.RIGHT_PANEL_X,
            self.inner_top,
            Config.RIGHT_PANEL_WIDTH,
            section_height
        )
        
        # Middle wood section
        middle_rect = pygame.Rect(
            Config.RIGHT_PANEL_X,
            self.inner_top + section_height,
            Config.RIGHT_PANEL_WIDTH,
            section_height
        )
        pygame.draw.rect(surface, Config.WOOD_BROWN, middle_rect)
        
        # Bottom striped section
        self._draw_stripes(
            surface,
            Config.RIGHT_PANEL_X,
            self.inner_top + 2 * section_height,
            Config.RIGHT_PANEL_WIDTH,
            section_height
        )
    
    def _draw_stripes(self, surface, x, y, width, height):
        """Draw diagonal green/yellow stripes."""
        stripe_width = 15
        num_stripes = (width + height) // stripe_width + 2
        
        for i in range(num_stripes):
            color = Config.STRIPE_GREEN if i % 2 == 0 else Config.STRIPE_YELLOW
            start_x = x + i * stripe_width
            end_y = y + i * stripe_width
            
            if start_x < x + width and end_y < y + height:
                points = [
                    (max(x, start_x), y),
                    (min(x + width, start_x + stripe_width), y),
                    (x, min(y + height, end_y + stripe_width)),
                    (x, max(y, end_y))
                ]
                pygame.draw.polygon(surface, color, points)