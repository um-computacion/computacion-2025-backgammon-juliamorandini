"""
Handles mouse interaction with the backgammon board.
Responsible for detecting clicks on points, checkers, and other board elements.
"""
import pygame
from config import Config


class BoardInteraction:
    """
    Manages mouse interactions with the board.
    Detects which point/area the user clicks on.
    """
    
    def __init__(self):
        """Initialize the board interaction handler."""
        self.selected_point = None
        self.mouse_pos = (0, 0)
    
    def handle_event(self, event):
        """
        Handle mouse events on the board.
        
        Args:
            event: Pygame event
            
        Returns:
            Dictionary with interaction info or None
        """
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
            return None
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                return self._handle_click(event.pos)
        
        return None
    
    def _handle_click(self, pos):
        """
        Process a click at the given position.
        
        Args:
            pos: Tuple of (x, y) click coordinates
            
        Returns:
            Dictionary with click information
        """
        point_index = self._get_point_at_position(pos)
        
        if point_index is not None:
            return {
                'type': 'point_click',
                'point': point_index,
                'position': pos
            }
        
        return {
            'type': 'board_click',
            'position': pos
        }
    
    def _get_point_at_position(self, pos):
        """
        Determine which point (0-23) was clicked, if any.
        
        Board layout:
        Top row (left to right):    12 13 14 15 16 17 | BAR | 18 19 20 21 22 23
        Bottom row (left to right):  11 10 9  8  7  6 | BAR | 5  4  3  2  1  0
        
        Args:
            pos: Tuple of (x, y) click coordinates
            
        Returns:
            Point index (0-23) or None if no point was clicked
        """
        x, y = pos
        
        # Calculate board boundaries
        inner_left = Config.BOARD_X + Config.BORDER_THICKNESS
        inner_top = Config.BOARD_Y + Config.BORDER_THICKNESS
        inner_bottom = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
        
        # Check if click is in top or bottom half
        is_top_half = y < (Config.BOARD_Y + Config.BOARD_HEIGHT // 2)
        is_bottom_half = not is_top_half
        
        # Check if in clickable area (near triangles)
        if is_top_half and y > (inner_top + Config.POINT_HEIGHT + 50):
            return None
        if is_bottom_half and y < (inner_bottom - Config.POINT_HEIGHT - 50):
            return None
        
        # Check which horizontal section (left or right of bar)
        if x < Config.BAR_X:
            # Left section
            relative_x = x - inner_left
            if 0 <= relative_x <= Config.POINT_WIDTH * 6:
                point_in_section = int(relative_x // Config.POINT_WIDTH)
                if is_top_half:
                    # Top left: points 12-17
                    return 12 + point_in_section
                else:
                    # Bottom left: points 11,10,9,8,7,6
                    return 11 - point_in_section
        
        elif x > Config.BAR_X + Config.BAR_WIDTH:
            # Right section
            relative_x = x - (Config.BAR_X + Config.BAR_WIDTH)
            if 0 <= relative_x <= Config.POINT_WIDTH * 6:
                point_in_section = int(relative_x // Config.POINT_WIDTH)
                if is_top_half:
                    # Top right: points 18-23
                    return 18 + point_in_section
                else:
                    # Bottom right: points 5,4,3,2,1,0
                    return 5 - point_in_section
        
        return None
    
    def get_hovered_point(self):
        """
        Get the point currently under the mouse cursor.
        
        Returns:
            Point index or None
        """
        return self._get_point_at_position(self.mouse_pos)