"""
Handles all drawing operations for the active game pieces (checkers).

This module is responsible for iterating through the board state
and drawing the checkers on their correct points, on the bar,
and in the borne-off area.
"""

from typing import List, Dict, Tuple
import pygame
from config import Config
from core.board import Board

# pylint: disable=no-member
# 'pygame.draw' methods are dynamically loaded,
# so pylint often reports 'no-member' errors.


class CheckerRenderer:
    """Draws all checkers based on the current board state."""

    def __init__(self) -> None:
        """
        Initializes the renderer.

        Calculates and stores key internal dimensions of the board based on
        Config settings, such as the inner boundaries and the width of a
        single point.
        """
        self._inner_left = Config.BOARD_X + Config.BORDER_THICKNESS
        self._inner_top = Config.BOARD_Y + Config.BORDER_THICKNESS
        self._inner_bottom = (
            Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
        )

        # Calculate consistent point width
        left_section_width = Config.BAR_X - self._inner_left
        self._point_width = left_section_width // 6

    def draw(
        self, surface: pygame.Surface, board: Board
    ) -> List[Tuple[int, int, int, int, str]]:
        """
        Draws all checkers on the board, bar, and borne-off area.

        This is the main orchestration method for the renderer.

        Args:
            surface: The pygame.Surface to draw on.
            board: The Board object containing the current game state.

        Returns:
            A list of tuples representing the screen positions and metadata
            of drawn checkers, used for click detection. Each tuple is:
            (x_pos, y_pos, radius, point_index, color)
        """
        checker_positions = []

        # Draw checkers on the 24 points
        for point_index in range(24):
            checkers = board.points[point_index]
            if checkers:
                self._draw_point_checkers(
                    surface, point_index, checkers, checker_positions
                )

        # Draw checkers on the bar and in the borne-off area
        self._draw_bar_checkers(surface, board.bar)
        self._draw_borne_off_checkers(surface, board.borne_off)

        return checker_positions

    def _draw_point_checkers(
        self,
        surface: pygame.Surface,
        point_index: int,
        checkers: List[str],
        checker_positions: List[Tuple[int, int, int, int, str]],
    ) -> None:
        """
        Draws the stack of checkers on a single point.

        Args:
            surface: The pygame.Surface to draw on.
            point_index: The index of the point (0-23).
            checkers: A list of checker colors ("W" or "B") on that point.
            checker_positions: The list to append checker position data to.
        """
        x_pos = self._get_point_x_center(point_index)
        is_top = point_index >= 12
        radius = Config.CHECKER_RADIUS

        for i, color in enumerate(checkers):
            # Calculate Y position, stacking from the edge
            if is_top:
                y_pos = self._inner_top + 20 + (i * Config.CHECKER_SPACING)
            else:
                y_pos = self._inner_bottom - 20 - (i * Config.CHECKER_SPACING)

            # Add to position list for click detection
            checker_positions.append((int(x_pos), y_pos, radius, point_index, color))

            # Draw the checker
            self._draw_single_checker(surface, x_pos, y_pos, color)

    def _draw_bar_checkers(
        self, surface: pygame.Surface, bar_dict: Dict[str, int]
    ) -> None:
        """
        Draws the checkers currently on the bar.

        Args:
            surface: The pygame.Surface to draw on.
            bar_dict: A dictionary mapping player ("W", "B") to the
                      count of checkers on the bar.
        """
        bar_center_x = Config.BAR_X + Config.BAR_WIDTH // 2

        # Draw White's bar checkers, stacking from the top
        if bar_dict["W"] > 0:
            for i in range(bar_dict["W"]):
                y_pos = self._inner_top + 50 + (i * Config.CHECKER_SPACING)
                self._draw_single_checker(surface, bar_center_x, y_pos, "W")

        # Draw Black's bar checkers, stacking from the bottom
        if bar_dict["B"] > 0:
            for i in range(bar_dict["B"]):
                y_pos = self._inner_bottom - 50 - (i * Config.CHECKER_SPACING)
                self._draw_single_checker(surface, bar_center_x, y_pos, "B")

    def _draw_borne_off_checkers(
        self, surface: pygame.Surface, borne_off_dict: Dict[str, int]
    ) -> None:
        """
        Draws checkers that have been borne off, in the right-hand area.

        Args:
            surface: The pygame.Surface to draw on.
            borne_off_dict: A dictionary mapping player ("W", "B") to the
                            count of checkers borne off.
        """
        # Position borne off checkers at the right edge of the board
        panel_center_x = Config.BOARD_WIDTH - Config.CHECKER_SIZE

        # Draw White's borne-off checkers (max 15)
        if borne_off_dict["W"] > 0:
            for i in range(min(borne_off_dict["W"], 15)):
                row = i // 5
                y_pos = self._inner_bottom - 100 - (row * Config.CHECKER_SPACING)
                self._draw_single_checker(surface, panel_center_x, y_pos, "W")

        # Draw Black's borne-off checkers (max 15)
        if borne_off_dict["B"] > 0:
            for i in range(min(borne_off_dict["B"], 15)):
                row = i // 5
                y_pos = self._inner_top + 100 + (row * Config.CHECKER_SPACING)
                self._draw_single_checker(surface, panel_center_x, y_pos, "B")

    def _draw_single_checker(
        self, surface: pygame.Surface, x: float, y: float, color: str
    ) -> None:
        """
        Draws a single checker with outline and highlight.

        Args:
            surface: The pygame.Surface to draw on.
            x: The center x-coordinate.
            y: The center y-coordinate.
            color: The color of the checker ("W" or "B").
        """
        if color == "W":
            main_color = Config.WHITE_CHECKER
            highlight_color = Config.CHECKER_HIGHLIGHT_WHITE
        else:
            main_color = Config.BLACK_CHECKER
            highlight_color = Config.CHECKER_HIGHLIGHT_BLACK

        # Draw main body
        pygame.draw.circle(surface, main_color, (int(x), int(y)), Config.CHECKER_RADIUS)

        # Draw outline
        pygame.draw.circle(
            surface, Config.CHECKER_OUTLINE, (int(x), int(y)), Config.CHECKER_RADIUS, 2
        )

        # Draw simple highlight
        pygame.draw.circle(
            surface,
            highlight_color,
            (int(x - 5), int(y - 5)),
            Config.CHECKER_RADIUS // 3,
        )

    def _get_point_x_center(self, point_index: int) -> float:
        """
        Calculates the center X-coordinate for a given point index.

        Args:
            point_index: The index of the point (0-23).

        Returns:
            The center x-coordinate for that point.
        """
        # Use the same logic as BoardRenderer and BoardInteraction
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

        return x + self._point_width // 2
