import pygame
from typing import List, Tuple
from config import Config


class BoardRenderer:
    def __init__(self) -> None:
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
        self._draw_border(surface)
        self._draw_board_background(surface)
        self._draw_points(surface)
        self._draw_bar(surface)
        self._draw_right_panel(surface)

    def _draw_border(self, surface: pygame.Surface) -> None:
        outer_rect = pygame.Rect(
            Config.BOARD_X, Config.BOARD_Y, Config.BOARD_WIDTH, Config.BOARD_HEIGHT
        )
        pygame.draw.rect(surface, Config.DARK_BROWN, outer_rect)

    def _draw_board_background(self, surface: pygame.Surface) -> None:
        board_rect = pygame.Rect(
            self._inner_left,
            self._inner_top,
            self._inner_right - self._inner_left,
            self._inner_bottom - self._inner_top,
        )
        pygame.draw.rect(surface, Config.WOOD_BROWN, board_rect)

    def _draw_points(self, surface: pygame.Surface) -> None:
        for point_index in range(24):
            self._draw_single_point(surface, point_index)

    def _draw_single_point(self, surface: pygame.Surface, point_index: int) -> None:
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

    # ... rest of the methods remain the same for bar and right panel
    def _draw_bar(self, surface: pygame.Surface) -> None:
        bar_height = self._inner_bottom - self._inner_top

        bar_rect = pygame.Rect(
            Config.BAR_X, self._inner_top, Config.BAR_WIDTH, bar_height
        )
        pygame.draw.rect(surface, Config.GREEN_BAR, bar_rect)

        for i in range(8):
            y_pos = self._inner_top + (i + 1) * bar_height // 9
            pygame.draw.line(
                surface,
                (30, 70, 50),
                (Config.BAR_X, y_pos),
                (Config.BAR_X + Config.BAR_WIDTH, y_pos),
                1,
            )

        hinge_x = Config.BAR_X + (Config.BAR_WIDTH - Config.HINGE_WIDTH) // 2

        top_hinge = pygame.Rect(
            hinge_x, self._inner_top + 20, Config.HINGE_WIDTH, Config.HINGE_HEIGHT
        )
        pygame.draw.rect(surface, Config.BRASS, top_hinge)
        pygame.draw.rect(surface, (140, 100, 0), top_hinge, 2)

        bottom_hinge = pygame.Rect(
            hinge_x, self._inner_bottom - 35, Config.HINGE_WIDTH, Config.HINGE_HEIGHT
        )
        pygame.draw.rect(surface, Config.BRASS, bottom_hinge)
        pygame.draw.rect(surface, (140, 100, 0), bottom_hinge, 2)

    def _draw_right_panel(self, surface: pygame.Surface) -> None:
        panel_height = self._inner_bottom - self._inner_top
        section_height = panel_height // 3

        self._draw_stripes(
            surface,
            Config.RIGHT_PANEL_X,
            self._inner_top,
            Config.RIGHT_PANEL_WIDTH,
            section_height,
        )

        middle_rect = pygame.Rect(
            Config.RIGHT_PANEL_X,
            self._inner_top + section_height,
            Config.RIGHT_PANEL_WIDTH,
            section_height,
        )
        pygame.draw.rect(surface, Config.WOOD_BROWN, middle_rect)

        self._draw_stripes(
            surface,
            Config.RIGHT_PANEL_X,
            self._inner_top + 2 * section_height,
            Config.RIGHT_PANEL_WIDTH,
            section_height,
        )

    def _draw_stripes(
        self, surface: pygame.Surface, x: int, y: int, width: int, height: int
    ) -> None:
        stripe_width = 15

        clip_rect = pygame.Rect(x, y, width, height)
        surface.set_clip(clip_rect)

        pygame.draw.rect(surface, Config.STRIPE_GREEN, clip_rect)

        max_coverage = width + height

        for i in range(-height, max_coverage, stripe_width * 2):
            p1 = (x + i, y)
            p2 = (x + i + stripe_width, y)
            p3 = (x + i + stripe_width + height, y + height)
            p4 = (x + i + height, y + height)

            points = [p1, p2, p3, p4]

            pygame.draw.polygon(surface, Config.STRIPE_YELLOW, points)

        surface.set_clip(None)
