"""
Renders the static backgammon board, including the border,
background, points (triangles), and the central bar.
"""

import pygame
from config import Config

# pylint: disable=no-member
# 'pygame.draw' methods are dynamically loaded,
# so pylint often reports 'no-member' errors.


class BoardRenderer:
    """Handles all drawing operations for the static game board."""

    def __init__(self) -> None:
        """
        Initializes the renderer.

        Calculates and stores key internal dimensions of the board based on
        Config settings, such as the inner boundaries and the width of a
        single point.
        """
        self._inner_left = Config.BOARD_X + Config.BORDER_THICKNESS
        self._inner_right = (
            Config.BOARD_X + Config.BOARD_WIDTH - Config.BORDER_THICKNESS
        )
        self._inner_top = Config.BOARD_Y + Config.BORDER_THICKNESS
        self._inner_bottom = (
            Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
        )

        # Calculate consistent point width
        left_section_width = Config.BAR_X - self._inner_left
        self._point_width = left_section_width // 6

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the complete static game board onto the given surface.

        This method orchestrates the drawing process by calling the private
        drawing methods for each component in the correct order.
        """
        self._draw_border(surface)
        self._draw_board_background(surface)
        self._draw_points(surface)
        self._draw_bar(surface)
        # self._draw_right_panel(surface) # <--- ¡AQUÍ ESTÁ LA CORRECCIÓN! (Línea comentada)

    def _draw_border(self, surface: pygame.Surface) -> None:
        """Draws the outermost wooden border of the board."""
        outer_rect = pygame.Rect(
            Config.BOARD_X, Config.BOARD_Y, Config.BOARD_WIDTH, Config.BOARD_HEIGHT
        )
        pygame.draw.rect(surface, Config.DARK_BROWN, outer_rect)

    def _draw_board_background(self, surface: pygame.Surface) -> None:
        """Draws the inner background (e.g., wood) inside the border."""
        board_rect = pygame.Rect(
            self._inner_left,
            self._inner_top,
            self._inner_right - self._inner_left,
            self._inner_bottom - self._inner_top,
        )
        pygame.draw.rect(surface, Config.WOOD_BROWN, board_rect)

    def _draw_points(self, surface: pygame.Surface) -> None:
        """Iterates through all 24 points and draws each one."""
        for point_index in range(24):
            self._draw_single_point(surface, point_index)

    def _draw_single_point(self, surface: pygame.Surface, point_index: int) -> None:
        """
        Calculates the geometry and draws a single triangular point.

        This method handles the X-coordinate calculation for all four quadrants,
        determines the correct alternating color, and draws the triangle
        pointing either up (top row) or down (bottom row).
        """
        # Calculate x coordinate (same logic as BoardInteraction)
        if 0 <= point_index <= 5:  # Bottom right
            point_in_quadrant = 5 - point_index
            x = (Config.BAR_X + Config.BAR_WIDTH) + (
                point_in_quadrant * self._point_width
            )
        elif 6 <= point_index <= 11:  # Bottom left
            point_in_quadrant = 11 - point_index
            x = self._inner_left + (point_in_quadrant * self._point_width)
        elif 12 <= point_index <= 17:  # Top left
            point_in_quadrant = point_index - 12
            x = self._inner_left + (point_in_quadrant * self._point_width)
        else:  # Top right (18-23)
            point_in_quadrant = point_index - 18
            x = (Config.BAR_X + Config.BAR_WIDTH) + (
                point_in_quadrant * self._point_width
            )

        # Set color (alternating)
        # Note: The original logic `(point_index // 6) % 2 == 0` creates blocks
        # of 6 light, 6 dark, 6 light, 6 dark.
        # A more traditional alternating pattern would be `point_index % 2 == 0`.
        # Sticking to the original logic provided:
        color = Config.LIGHT_TAN if (point_index // 6) % 2 == 0 else Config.DARK_POINT

        # Draw triangle
        if point_index >= 12:  # Top points
            points = [
                (x, self._inner_top),
                (x + self._point_width, self._inner_top),
                (x + self._point_width // 2, self._inner_top + Config.POINT_HEIGHT),
            ]
        else:  # Bottom points
            points = [
                (x, self._inner_bottom),
                (x + self._point_width, self._inner_bottom),
                (x + self._point_width // 2, self._inner_bottom - Config.POINT_HEIGHT),
            ]

        pygame.draw.polygon(surface, color, points)

    def _draw_bar(self, surface: pygame.Surface) -> None:
        """Draws the central bar, including decorative lines and hinges."""
        bar_height = self._inner_bottom - self._inner_top

        bar_rect = pygame.Rect(
            Config.BAR_X, self._inner_top, Config.BAR_WIDTH, bar_height
        )
        pygame.draw.rect(surface, Config.GREEN_BAR, bar_rect)

        # Draw decorative lines on the bar
        for i in range(8):
            y_pos = self._inner_top + (i + 1) * bar_height // 9
            pygame.draw.line(
                surface,
                (30, 70, 50),  # A slightly darker green for the lines
                (Config.BAR_X, y_pos),
                (Config.BAR_X + Config.BAR_WIDTH, y_pos),
                1,
            )

        # Draw decorative hinges
        hinge_x = Config.BAR_X + (Config.BAR_WIDTH - Config.HINGE_WIDTH) // 2

        top_hinge = pygame.Rect(
            hinge_x, self._inner_top + 20, Config.HINGE_WIDTH, Config.HINGE_HEIGHT
        )
        pygame.draw.rect(surface, Config.BRASS, top_hinge)
        pygame.draw.rect(surface, (140, 100, 0), top_hinge, 2)  # Hinge outline

        bottom_hinge = pygame.Rect(
            hinge_x, self._inner_bottom - 35, Config.HINGE_WIDTH, Config.HINGE_HEIGHT
        )
        pygame.draw.rect(surface, Config.BRASS, bottom_hinge)
        pygame.draw.rect(surface, (140, 100, 0), bottom_hinge, 2)  # Hinge outline
