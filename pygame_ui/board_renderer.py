"""
Board renderer that draws the empty backgammon board structure.
Handles drawing the board, points, bar, and right panel.
"""
import pygame
from typing import List, Tuple

from config import Config


class BoardRenderer:
    """
    Renders the backgammon board structure without game pieces.
    
    Responsible for drawing the board, triangular points, bar, and side panel.
    This class follows Single Responsibility Principle by only handling
    the visual rendering of the board structure.
    """
    
    def __init__(self) -> None:
        """
        Initialize the board renderer.
        
        Calculates and stores the inner boundaries of the board
        based on the configuration settings.
        
        Args:
            None
            
        Returns:
            None
        """
        self.__inner_left__: int = Config.BOARD_X + Config.BORDER_THICKNESS
        self.__inner_right__: int = Config.BOARD_X + Config.BOARD_WIDTH - Config.BORDER_THICKNESS
        self.__inner_top__: int = Config.BOARD_Y + Config.BORDER_THICKNESS
        self.__inner_bottom__: int = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
    
    def draw(self, surface: pygame.Surface) -> None:
        """
        Draw the complete backgammon board structure.
        
        Renders all board elements in the correct order: border, background,
        points, bar, and right panel.
        
        Args:
            surface: Pygame surface to draw on
            
        Returns:
            None
        """
        self._draw_border(surface)
        self._draw_board_background(surface)
        self._draw_points(surface)
        self._draw_bar(surface)
        self._draw_right_panel(surface)
    
    def _draw_border(self, surface: pygame.Surface) -> None:
        """
        Draw the dark brown border frame.
        
        Creates the outer frame that surrounds the entire board.
        
        Args:
            surface: Pygame surface to draw on
            
        Returns:
            None
        """
        outer_rect: pygame.Rect = pygame.Rect(
            Config.BOARD_X,
            Config.BOARD_Y,
            Config.BOARD_WIDTH,
            Config.BOARD_HEIGHT
        )
        pygame.draw.rect(surface, Config.DARK_BROWN, outer_rect)
    
    def _draw_board_background(self, surface: pygame.Surface) -> None:
        """
        Draw the main wooden board background.
        
        Fills the inner area of the board with the wood texture color.
        
        Args:
            surface: Pygame surface to draw on
            
        Returns:
            None
        """
        board_rect: pygame.Rect = pygame.Rect(
            self.__inner_left__,
            self.__inner_top__,
            self.__inner_right__ - self.__inner_left__,
            self.__inner_bottom__ - self.__inner_top__
        )
        pygame.draw.rect(surface, Config.WOOD_BROWN, board_rect)
    
    def _draw_points(self, surface: pygame.Surface) -> None:
        """
        Draw all 24 triangular points.
        
        Creates the triangular playing points that alternate in color.
        Points are drawn in pairs (top and bottom) for each column.
        
        Args:
            surface: Pygame surface to draw on
            
        Returns:
            None
        """
        for i in range(12):
            x_pos: float = self._calculate_point_x(i)
            color: Tuple[int, int, int] = Config.LIGHT_TAN if i % 2 == 0 else Config.DARK_POINT
            
            # Top point (pointing down)
            top_points: List[Tuple[float, float]] = [
                (x_pos, self.__inner_top__),
                (x_pos + Config.POINT_WIDTH, self.__inner_top__),
                (x_pos + Config.POINT_WIDTH / 2, self.__inner_top__ + Config.POINT_HEIGHT)
            ]
            pygame.draw.polygon(surface, color, top_points)
            
            # Bottom point (pointing up)
            bottom_points: List[Tuple[float, float]] = [
                (x_pos, self.__inner_bottom__),
                (x_pos + Config.POINT_WIDTH, self.__inner_bottom__),
                (x_pos + Config.POINT_WIDTH / 2, self.__inner_bottom__ - Config.POINT_HEIGHT)
            ]
            pygame.draw.polygon(surface, color, bottom_points)
    
    def _calculate_point_x(self, index: int) -> float:
        """
        Calculate x position for a point based on its index (0-11).
        
        Points 0-5 are on the right side, 6-11 on the left side.
        The bar separates the two sections.
        
        Args:
            index: Point visual index (0-11)
            
        Returns:
            X coordinate for the left edge of the point
        """
        if index < 6:
            # Right side points (0-5)
            right_section_start: float = Config.BAR_X + Config.BAR_WIDTH
            return right_section_start + (5 - index) * Config.POINT_WIDTH
        else:
            # Left side points (6-11)
            return self.__inner_left__ + (11 - index) * Config.POINT_WIDTH
    
    def _draw_bar(self, surface: pygame.Surface) -> None:
        """
        Draw the central green bar with brass hinges.
        
        Creates the middle bar that separates the two halves of the board
        and adds decorative texture lines and metal hinges.
        
        Args:
            surface: Pygame surface to draw on
            
        Returns:
            None
        """
        bar_height: int = self.__inner_bottom__ - self.__inner_top__
        
        # Draw green bar background
        bar_rect: pygame.Rect = pygame.Rect(
            Config.BAR_X,
            self.__inner_top__,
            Config.BAR_WIDTH,
            bar_height
        )
        pygame.draw.rect(surface, Config.GREEN_BAR, bar_rect)
        
        # Add texture lines
        for i in range(8):
            y_pos: int = self.__inner_top__ + (i + 1) * bar_height // 9
            pygame.draw.line(
                surface,
                (30, 70, 50),
                (Config.BAR_X, y_pos),
                (Config.BAR_X + Config.BAR_WIDTH, y_pos),
                1
            )
        
        # Draw hinges
        hinge_x: int = Config.BAR_X + (Config.BAR_WIDTH - Config.HINGE_WIDTH) // 2
        
        # Top hinge
        top_hinge: pygame.Rect = pygame.Rect(
            hinge_x,
            self.__inner_top__ + 20,
            Config.HINGE_WIDTH,
            Config.HINGE_HEIGHT
        )
        pygame.draw.rect(surface, Config.BRASS, top_hinge)
        pygame.draw.rect(surface, (140, 100, 0), top_hinge, 2)
        
        # Bottom hinge
        bottom_hinge: pygame.Rect = pygame.Rect(
            hinge_x,
            self.__inner_bottom__ - 35,
            Config.HINGE_WIDTH,
            Config.HINGE_HEIGHT
        )
        pygame.draw.rect(surface, Config.BRASS, bottom_hinge)
        pygame.draw.rect(surface, (140, 100, 0), bottom_hinge, 2)
    
    def _draw_right_panel(self, surface: pygame.Surface) -> None:
        """
        Draw the right side panel with diagonal stripes.
        
        Creates a decorative panel on the right side with alternating
        striped sections and a wooden middle section.
        
        Args:
            surface: Pygame surface to draw on
            
        Returns:
            None
        """
        panel_height: int = self.__inner_bottom__ - self.__inner_top__
        section_height: int = panel_height // 3
        
        # Top striped section
        self._draw_stripes(
            surface,
            Config.RIGHT_PANEL_X,
            self.__inner_top__,
            Config.RIGHT_PANEL_WIDTH,
            section_height
        )
        
        # Middle wood section
        middle_rect: pygame.Rect = pygame.Rect(
            Config.RIGHT_PANEL_X,
            self.__inner_top__ + section_height,
            Config.RIGHT_PANEL_WIDTH,
            section_height
        )
        pygame.draw.rect(surface, Config.WOOD_BROWN, middle_rect)
        
        # Bottom striped section
        self._draw_stripes(
            surface,
            Config.RIGHT_PANEL_X,
            self.__inner_top__ + 2 * section_height,
            Config.RIGHT_PANEL_WIDTH,
            section_height
        )
    
    def _draw_stripes(self, surface: pygame.Surface, x: int, y: int, 
                      width: int, height: int) -> None:
        """
        Draw diagonal green/yellow stripes.
        
        Creates an alternating diagonal stripe pattern for the side panel.
        
        Args:
            surface: Pygame surface to draw on
            x: Left edge X coordinate
            y: Top edge Y coordinate
            width: Width of striped area
            height: Height of striped area
            
        Returns:
            None
        """
        stripe_width: int = 15
        num_stripes: int = (width + height) // stripe_width + 2
        
        for i in range(num_stripes):
            color: Tuple[int, int, int] = (
                Config.STRIPE_GREEN if i % 2 == 0 else Config.STRIPE_YELLOW
            )
            start_x: int = x + i * stripe_width
            end_y: int = y + i * stripe_width
            
            if start_x < x + width and end_y < y + height:
                points: List[Tuple[int, int]] = [
                    (max(x, start_x), y),
                    (min(x + width, start_x + stripe_width), y),
                    (x, min(y + height, end_y + stripe_width)),
                    (x, max(y, end_y))
                ]
                pygame.draw.polygon(surface, color, points)