import pygame
from typing import Optional, Tuple
from config import Config


class BoardInteraction:
    def __init__(self) -> None:
        self._selected_point: Optional[int] = None
        self._mouse_pos: Tuple[int, int] = (0, 0)
    
    def handle_event(self, event: pygame.event.Event) -> Optional[dict]:
        if event.type == pygame.MOUSEMOTION:
            self._mouse_pos = event.pos
            return None
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if mouse_pos[1] < 600:  # Don't handle clicks in button area
                point = self.get_clicked_point(mouse_pos)
                if point is not None:
                    return {'type': 'point_click', 'point': point}
        return None

    @staticmethod
    def get_clicked_point(pos: Tuple[int, int]) -> Optional[int]:
        x, y = pos
        
        # Board boundaries
        inner_left = Config.BOARD_X + Config.BORDER_THICKNESS
        inner_right = Config.BOARD_X + Config.BOARD_WIDTH - Config.BORDER_THICKNESS
        inner_top = Config.BOARD_Y + Config.BORDER_THICKNESS
        inner_bottom = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
        
        # Check if click is within board area
        if not (inner_left <= x <= inner_right and inner_top <= y <= inner_bottom):
            return None
        
        # Calculate section widths
        left_section_width = Config.BAR_X - inner_left
        right_section_width = inner_right - (Config.BAR_X + Config.BAR_WIDTH)
        point_width = left_section_width // 6
        
        is_top = y < (Config.BOARD_Y + Config.BOARD_HEIGHT) // 2
        
        # Check left section (points 6-11 bottom, 12-17 top)
        if x < Config.BAR_X:
            x_relative = x - inner_left
            point_in_quadrant = x_relative // point_width
            
            if 0 <= point_in_quadrant <= 5:
                if is_top:
                    return 12 + point_in_quadrant  # Points 12-17
                else:
                    return 11 - point_in_quadrant  # Points 11-6
        
        # Check right section (points 0-5 bottom, 18-23 top)  
        elif x > Config.BAR_X + Config.BAR_WIDTH:
            x_relative = x - (Config.BAR_X + Config.BAR_WIDTH)
            point_in_quadrant = x_relative // point_width
            
            if 0 <= point_in_quadrant <= 5:
                if is_top:
                    return 18 + point_in_quadrant  # Points 18-23
                else:
                    return 5 - point_in_quadrant   # Points 5-0
        
        return None

    def get_point_coords(self, point: int) -> Optional[Tuple[int, int]]:
        """Get screen coordinates for a given point number."""
        if not (0 <= point <= 23):
            return None

        inner_left = Config.BOARD_X + Config.BORDER_THICKNESS
        inner_right = Config.BOARD_X + Config.BOARD_WIDTH - Config.BORDER_THICKNESS
        inner_top = Config.BOARD_Y + Config.BORDER_THICKNESS
        inner_bottom = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
        
        left_section_width = Config.BAR_X - inner_left
        point_width = left_section_width // 6
        
        # Calculate x coordinate based on point number
        if 0 <= point <= 5:  # Bottom right
            point_in_quadrant = 5 - point
            x = (Config.BAR_X + Config.BAR_WIDTH) + (point_in_quadrant * point_width)
        elif 6 <= point <= 11:  # Bottom left
            point_in_quadrant = 11 - point
            x = inner_left + (point_in_quadrant * point_width)
        elif 12 <= point <= 17:  # Top left
            point_in_quadrant = point - 12
            x = inner_left + (point_in_quadrant * point_width)
        else:  # Top right (18-23)
            point_in_quadrant = point - 18
            x = (Config.BAR_X + Config.BAR_WIDTH) + (point_in_quadrant * point_width)
        
        # Calculate y coordinate
        if point >= 12:  # Top half
            y = inner_top + (Config.POINT_HEIGHT // 2)
        else:  # Bottom half
            y = inner_bottom - (Config.POINT_HEIGHT // 2)
        
        # Center in the point width
        x += point_width // 2
        
        return (int(x), int(y))