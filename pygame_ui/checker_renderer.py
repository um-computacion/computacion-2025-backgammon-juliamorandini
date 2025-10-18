"""
Checker renderer for drawing backgammon game pieces on the board.
"""
import pygame
from config import Config
from core.board import Board


class CheckerRenderer:
    """
    Renders checker pieces (game pieces) on the board.
    Reads the board state and draws checkers at appropriate positions.
    """
    
    def __init__(self):
        """Initialize the checker renderer."""
        self.inner_left = Config.BOARD_X + Config.BORDER_THICKNESS
        self.inner_top = Config.BOARD_Y + Config.BORDER_THICKNESS
        self.inner_bottom = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
    
    def draw(self, surface, board: Board):
        """
        Draw all checkers on the board based on board state.
        
        Args:
            surface: Pygame surface to draw on
            board: Board object containing game state
        """
        # Draw checkers on all 24 points
        for point_index in range(24):
            checkers = board.points[point_index]
            if checkers:
                self._draw_point_checkers(surface, point_index, checkers)
        
        # Draw checkers on the bar (if any)
        self._draw_bar_checkers(surface, board.bar)
        
        # Draw borne off checkers
        self._draw_borne_off_checkers(surface, board.borne_off)
    
    def _draw_point_checkers(self, surface, point_index, checkers):
        """
        Draw all checkers at a specific point.
        
        Args:
            surface: Pygame surface to draw on
            point_index: Point number (0-23)
            checkers: List of checker colors at this point
        """
        x_pos = self._get_point_x_center(point_index)
        
        # Determine if this is a top or bottom point
        is_top = point_index <= 11
        
        for i, color in enumerate(checkers):
            if is_top:
                # Top points - stack downward
                y_pos = self.inner_top + Config.POINT_HEIGHT - (i * Config.CHECKER_SPACING) - Config.CHECKER_RADIUS
            else:
                # Bottom points - stack upward
                y_pos = self.inner_bottom - Config.POINT_HEIGHT + (i * Config.CHECKER_SPACING) + Config.CHECKER_RADIUS
            
            self._draw_single_checker(surface, x_pos, y_pos, color)
    
    def _draw_bar_checkers(self, surface, bar_dict):
        """
        Draw checkers on the bar (captured pieces).
        
        Args:
            surface: Pygame surface to draw on
            bar_dict: Dictionary with bar counts {'W': count, 'B': count}
        """
        bar_center_x = Config.BAR_X + Config.BAR_WIDTH // 2
        
        # Draw white checkers on bar (top half)
        if bar_dict['W'] > 0:
            for i in range(bar_dict['W']):
                y_pos = self.inner_top + 50 + (i * Config.CHECKER_SPACING)
                self._draw_single_checker(surface, bar_center_x, y_pos, 'W')
        
        # Draw black checkers on bar (bottom half)
        if bar_dict['B'] > 0:
            for i in range(bar_dict['B']):
                y_pos = self.inner_bottom - 50 - (i * Config.CHECKER_SPACING)
                self._draw_single_checker(surface, bar_center_x, y_pos, 'B')
    
    def _draw_borne_off_checkers(self, surface, borne_off_dict):
        """
        Draw borne off checkers in the right panel.
        
        Args:
            surface: Pygame surface to draw on
            borne_off_dict: Dictionary with borne off counts {'W': count, 'B': count}
        """
        panel_center_x = Config.RIGHT_PANEL_X + Config.RIGHT_PANEL_WIDTH // 2
        
        # Draw white borne off pieces (bottom section)
        if borne_off_dict['W'] > 0:
            for i in range(min(borne_off_dict['W'], 15)):  # Max display 15
                row = i // 5
                col = i % 5
                x_pos = panel_center_x
                y_pos = self.inner_bottom - 100 - (row * Config.CHECKER_SPACING)
                self._draw_single_checker(surface, x_pos, y_pos, 'W')
        
        # Draw black borne off pieces (top section)
        if borne_off_dict['B'] > 0:
            for i in range(min(borne_off_dict['B'], 15)):  # Max display 15
                row = i // 5
                col = i % 5
                x_pos = panel_center_x
                y_pos = self.inner_top + 100 + (row * Config.CHECKER_SPACING)
                self._draw_single_checker(surface, x_pos, y_pos, 'B')
    
    def _draw_single_checker(self, surface, x, y, color):
        """
        Draw a single checker at the specified position.
        
        Args:
            surface: Pygame surface to draw on
            x: X coordinate of checker center
            y: Y coordinate of checker center
            color: 'W' for white or 'B' for black
        """
        # Choose colors based on checker color
        if color == 'W':
            main_color = Config.WHITE_CHECKER
            highlight_color = Config.CHECKER_HIGHLIGHT_WHITE
        else:
            main_color = Config.BLACK_CHECKER
            highlight_color = Config.CHECKER_HIGHLIGHT_BLACK
        
        # Draw main checker circle
        pygame.draw.circle(
            surface,
            main_color,
            (int(x), int(y)),
            Config.CHECKER_RADIUS
        )
        
        # Draw outline
        pygame.draw.circle(
            surface,
            Config.CHECKER_OUTLINE,
            (int(x), int(y)),
            Config.CHECKER_RADIUS,
            2
        )
        
        # Add inner highlight for 3D effect
        pygame.draw.circle(
            surface,
            highlight_color,
            (int(x - 5), int(y - 5)),
            Config.CHECKER_RADIUS // 3
        )
    
    def _get_point_x_center(self, point_index):
        """
        Get the X coordinate of the center of a point.
        
        Args:
            point_index: Point number (0-23)
            
        Returns:
            X coordinate of point center
        """
        # Convert point index to visual index (0-11)
        if point_index < 6:
            visual_index = 5 - point_index
        elif point_index < 12:
            visual_index = point_index - 6
        elif point_index < 18:
            visual_index = 23 - point_index
        else:
            visual_index = point_index - 12
        
        # Calculate x position
        if visual_index < 6:
            # Right side
            section_start = Config.BAR_X + Config.BAR_WIDTH
            x = section_start + (5 - visual_index) * Config.POINT_WIDTH
        else:
            # Left side
            x = self.inner_left + (11 - visual_index) * Config.POINT_WIDTH
        
        return x + Config.POINT_WIDTH // 2