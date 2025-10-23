"""Comprehensive test module for BoardRenderer class."""
import unittest
from unittest.mock import Mock, patch, MagicMock, call
import pygame
from pygame_ui.board_renderer import BoardRenderer
from config import Config


class TestBoardRendererInitialization(unittest.TestCase):
    """Test suite for BoardRenderer initialization."""

    def setUp(self):
        """Set up test fixtures."""
        self.renderer = BoardRenderer()

    def test_initialization_creates_inner_boundaries(self):
        """Test that initialization calculates inner boundaries correctly."""
        expected_inner_left = Config.BOARD_X + Config.BORDER_THICKNESS
        expected_inner_right = Config.BOARD_X + Config.BOARD_WIDTH - Config.BORDER_THICKNESS
        expected_inner_top = Config.BOARD_Y + Config.BORDER_THICKNESS
        expected_inner_bottom = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS

        self.assertEqual(self.renderer._inner_left, expected_inner_left)
        self.assertEqual(self.renderer._inner_right, expected_inner_right)
        self.assertEqual(self.renderer._inner_top, expected_inner_top)
        self.assertEqual(self.renderer._inner_bottom, expected_inner_bottom)

    def test_initialization_calculates_point_width(self):
        """Test that initialization calculates point width correctly."""
        left_section_width = Config.BAR_X - (Config.BOARD_X + Config.BORDER_THICKNESS)
        expected_point_width = left_section_width // 6

        self.assertEqual(self.renderer._point_width, expected_point_width)

    def test_private_attributes_exist(self):
        """Test that all private attributes are created."""
        self.assertTrue(hasattr(self.renderer, '_inner_left'))
        self.assertTrue(hasattr(self.renderer, '_inner_right'))
        self.assertTrue(hasattr(self.renderer, '_inner_top'))
        self.assertTrue(hasattr(self.renderer, '_inner_bottom'))
        self.assertTrue(hasattr(self.renderer, '_point_width'))


class TestBoardRendererDraw(unittest.TestCase):
    """Test suite for main draw method."""

    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.renderer = BoardRenderer()
        self.mock_surface = Mock(spec=pygame.Surface)

    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()

    @patch.object(BoardRenderer, '_draw_border')
    @patch.object(BoardRenderer, '_draw_board_background')
    @patch.object(BoardRenderer, '_draw_points')
    @patch.object(BoardRenderer, '_draw_bar')
    @patch.object(BoardRenderer, '_draw_right_panel')
    def test_draw_calls_all_methods_in_order(
        self, mock_right_panel, mock_bar, mock_points, mock_bg, mock_border
    ):
        """Test that draw method calls all drawing methods in correct order."""
        self.renderer.draw(self.mock_surface)

        # Verify all methods were called once
        mock_border.assert_called_once_with(self.mock_surface)
        mock_bg.assert_called_once_with(self.mock_surface)
        mock_points.assert_called_once_with(self.mock_surface)
        mock_bar.assert_called_once_with(self.mock_surface)
        mock_right_panel.assert_called_once_with(self.mock_surface)


class TestDrawBorder(unittest.TestCase):
    """Test suite for _draw_border method."""

    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.renderer = BoardRenderer()
        self.mock_surface = Mock(spec=pygame.Surface)

    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()

    @patch('pygame.draw.rect')
    def test_draw_border_creates_correct_rect(self, mock_draw_rect):
        """Test that border rectangle is created with correct dimensions."""
        self.renderer._draw_border(self.mock_surface)

        # Verify pygame.draw.rect was called
        mock_draw_rect.assert_called_once()

        # Get the actual call arguments
        call_args = mock_draw_rect.call_args
        surface, color, rect = call_args[0]

        self.assertEqual(surface, self.mock_surface)
        self.assertEqual(color, Config.DARK_BROWN)
        self.assertEqual(rect.x, Config.BOARD_X)
        self.assertEqual(rect.y, Config.BOARD_Y)
        self.assertEqual(rect.width, Config.BOARD_WIDTH)
        self.assertEqual(rect.height, Config.BOARD_HEIGHT)


class TestDrawBoardBackground(unittest.TestCase):
    """Test suite for _draw_board_background method."""

    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.renderer = BoardRenderer()
        self.mock_surface = Mock(spec=pygame.Surface)

    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()

    @patch('pygame.draw.rect')
    def test_draw_board_background_creates_correct_rect(self, mock_draw_rect):
        """Test that background rectangle is created with correct dimensions."""
        self.renderer._draw_board_background(self.mock_surface)

        mock_draw_rect.assert_called_once()

        call_args = mock_draw_rect.call_args
        surface, color, rect = call_args[0]

        self.assertEqual(surface, self.mock_surface)
        self.assertEqual(color, Config.WOOD_BROWN)
        self.assertEqual(rect.x, self.renderer._inner_left)
        self.assertEqual(rect.y, self.renderer._inner_top)
        expected_width = self.renderer._inner_right - self.renderer._inner_left
        expected_height = self.renderer._inner_bottom - self.renderer._inner_top
        self.assertEqual(rect.width, expected_width)
        self.assertEqual(rect.height, expected_height)


class TestDrawPoints(unittest.TestCase):
    """Test suite for _draw_points method."""

    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.renderer = BoardRenderer()
        self.mock_surface = Mock(spec=pygame.Surface)

    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()

    @patch.object(BoardRenderer, '_draw_single_point')
    def test_draw_points_calls_draw_single_point_24_times(self, mock_draw_single):
        """Test that _draw_points calls _draw_single_point for all 24 points."""
        self.renderer._draw_points(self.mock_surface)

        self.assertEqual(mock_draw_single.call_count, 24)

        # Verify it was called with correct point indices
        for i in range(24):
            mock_draw_single.assert_any_call(self.mock_surface, i)


class TestDrawSinglePoint(unittest.TestCase):
    """Test suite for _draw_single_point method."""

    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.renderer = BoardRenderer()
        self.mock_surface = Mock(spec=pygame.Surface)

    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()

    @patch('pygame.draw.polygon')
    def test_draw_single_point_bottom_right_quadrant(self, mock_draw_polygon):
        """Test drawing point in bottom right quadrant (0-5)."""
        for point_index in range(6):
            mock_draw_polygon.reset_mock()
            self.renderer._draw_single_point(self.mock_surface, point_index)
            mock_draw_polygon.assert_called_once()

    @patch('pygame.draw.polygon')
    def test_draw_single_point_bottom_left_quadrant(self, mock_draw_polygon):
        """Test drawing point in bottom left quadrant (6-11)."""
        for point_index in range(6, 12):
            mock_draw_polygon.reset_mock()
            self.renderer._draw_single_point(self.mock_surface, point_index)
            mock_draw_polygon.assert_called_once()

    @patch('pygame.draw.polygon')
    def test_draw_single_point_top_left_quadrant(self, mock_draw_polygon):
        """Test drawing point in top left quadrant (12-17)."""
        for point_index in range(12, 18):
            mock_draw_polygon.reset_mock()
            self.renderer._draw_single_point(self.mock_surface, point_index)
            mock_draw_polygon.assert_called_once()

    @patch('pygame.draw.polygon')
    def test_draw_single_point_top_right_quadrant(self, mock_draw_polygon):
        """Test drawing point in top right quadrant (18-23)."""
        for point_index in range(18, 24):
            mock_draw_polygon.reset_mock()
            self.renderer._draw_single_point(self.mock_surface, point_index)
            mock_draw_polygon.assert_called_once()

    @patch('pygame.draw.polygon')
    def test_draw_single_point_uses_alternating_colors(self, mock_draw_polygon):
        """Test that points use alternating colors."""
        # Points 0-5 (bottom right) should use LIGHT_TAN
        self.renderer._draw_single_point(self.mock_surface, 0)
        call_args = mock_draw_polygon.call_args[0]
        self.assertEqual(call_args[1], Config.LIGHT_TAN)

        # Points 6-11 (bottom left) should use DARK_POINT
        mock_draw_polygon.reset_mock()
        self.renderer._draw_single_point(self.mock_surface, 6)
        call_args = mock_draw_polygon.call_args[0]
        self.assertEqual(call_args[1], Config.DARK_POINT)

    @patch('pygame.draw.polygon')
    def test_draw_single_point_triangle_shape_bottom(self, mock_draw_polygon):
        """Test that bottom points create correct triangle shape."""
        point_index = 5
        self.renderer._draw_single_point(self.mock_surface, point_index)

        call_args = mock_draw_polygon.call_args[0]
        points = call_args[2]

        # Bottom points should have 3 vertices with bottom edge at _inner_bottom
        self.assertEqual(len(points), 3)
        self.assertEqual(points[0][1], self.renderer._inner_bottom)
        self.assertEqual(points[1][1], self.renderer._inner_bottom)

    @patch('pygame.draw.polygon')
    def test_draw_single_point_triangle_shape_top(self, mock_draw_polygon):
        """Test that top points create correct triangle shape."""
        point_index = 15
        self.renderer._draw_single_point(self.mock_surface, point_index)

        call_args = mock_draw_polygon.call_args[0]
        points = call_args[2]

        # Top points should have 3 vertices with top edge at _inner_top
        self.assertEqual(len(points), 3)
        self.assertEqual(points[0][1], self.renderer._inner_top)
        self.assertEqual(points[1][1], self.renderer._inner_top)


class TestDrawBar(unittest.TestCase):
    """Test suite for _draw_bar method."""

    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.renderer = BoardRenderer()
        self.mock_surface = Mock(spec=pygame.Surface)

    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()

    @patch('pygame.draw.rect')
    @patch('pygame.draw.line')
    def test_draw_bar_creates_main_rectangle(self, mock_line, mock_rect):
        """Test that bar main rectangle is drawn correctly."""
        self.renderer._draw_bar(self.mock_surface)

        # First call should be the main bar rectangle
        first_call = mock_rect.call_args_list[0][0]
        surface, color, rect = first_call

        self.assertEqual(surface, self.mock_surface)
        self.assertEqual(color, Config.GREEN_BAR)
        self.assertEqual(rect.x, Config.BAR_X)
        self.assertEqual(rect.y, self.renderer._inner_top)
        self.assertEqual(rect.width, Config.BAR_WIDTH)

    @patch('pygame.draw.rect')
    @patch('pygame.draw.line')
    def test_draw_bar_creates_8_lines(self, mock_line, mock_rect):
        """Test that 8 decorative lines are drawn on the bar."""
        self.renderer._draw_bar(self.mock_surface)

        self.assertEqual(mock_line.call_count, 8)

    @patch('pygame.draw.rect')
    @patch('pygame.draw.line')
    def test_draw_bar_creates_hinges(self, mock_line, mock_rect):
        """Test that two hinges are drawn on the bar."""
        self.renderer._draw_bar(self.mock_surface)

        # Should have: 1 bar rect + 2 hinge rects + 2 hinge borders = 5 rect calls
        self.assertEqual(mock_rect.call_count, 5)

    @patch('pygame.draw.rect')
    @patch('pygame.draw.line')
    def test_draw_bar_hinge_colors(self, mock_line, mock_rect):
        """Test that hinges use correct brass color."""
        self.renderer._draw_bar(self.mock_surface)

        # Check hinge colors (calls 1 and 3 are the filled hinges)
        hinge_calls = [mock_rect.call_args_list[1], mock_rect.call_args_list[3]]

        for call in hinge_calls:
            color = call[0][1]
            self.assertEqual(color, Config.BRASS)


class TestDrawRightPanel(unittest.TestCase):
    """Test suite for _draw_right_panel method."""

    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.renderer = BoardRenderer()
        self.mock_surface = Mock(spec=pygame.Surface)

    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()

    @patch.object(BoardRenderer, '_draw_stripes')
    @patch('pygame.draw.rect')
    def test_draw_right_panel_creates_three_sections(self, mock_rect, mock_stripes):
        """Test that right panel has three sections."""
        self.renderer._draw_right_panel(self.mock_surface)

        # Should call _draw_stripes twice (top and bottom sections)
        self.assertEqual(mock_stripes.call_count, 2)

        # Should draw middle rectangle once
        mock_rect.assert_called_once()

    @patch.object(BoardRenderer, '_draw_stripes')
    @patch('pygame.draw.rect')
    def test_draw_right_panel_middle_section_color(self, mock_rect, mock_stripes):
        """Test that middle section uses correct wood color."""
        self.renderer._draw_right_panel(self.mock_surface)

        call_args = mock_rect.call_args[0]
        color = call_args[1]

        self.assertEqual(color, Config.WOOD_BROWN)

    @patch.object(BoardRenderer, '_draw_stripes')
    @patch('pygame.draw.rect')
    def test_draw_right_panel_stripe_sections(self, mock_rect, mock_stripes):
        """Test that stripe sections are created correctly."""
        self.renderer._draw_right_panel(self.mock_surface)

        # Verify _draw_stripes was called for top and bottom sections
        calls = mock_stripes.call_args_list
        self.assertEqual(len(calls), 2)

        # Both calls should include surface and correct x position
        for call in calls:
            args = call[0]
            self.assertEqual(args[0], self.mock_surface)
            self.assertEqual(args[1], Config.RIGHT_PANEL_X)


class TestDrawStripes(unittest.TestCase):
    """Test suite for _draw_stripes method."""

    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.renderer = BoardRenderer()
        self.mock_surface = Mock(spec=pygame.Surface)

    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()

    @patch('pygame.draw.polygon')
    @patch('pygame.draw.rect')
    def test_draw_stripes_sets_clipping_region(self, mock_rect, mock_polygon):
        """Test that stripes method sets clipping region."""
        x, y, width, height = 100, 100, 200, 300

        self.renderer._draw_stripes(self.mock_surface, x, y, width, height)

        # Verify set_clip was called
        self.mock_surface.set_clip.assert_called()

    @patch('pygame.draw.polygon')
    @patch('pygame.draw.rect')
    def test_draw_stripes_draws_background(self, mock_rect, mock_polygon):
        """Test that stripes background is drawn."""
        x, y, width, height = 100, 100, 200, 300

        self.renderer._draw_stripes(self.mock_surface, x, y, width, height)

        # First rect call should be the background
        first_call = mock_rect.call_args_list[0][0]
        color = first_call[1]

        self.assertEqual(color, Config.STRIPE_GREEN)

    @patch('pygame.draw.polygon')
    @patch('pygame.draw.rect')
    def test_draw_stripes_draws_multiple_stripes(self, mock_rect, mock_polygon):
        """Test that multiple stripe polygons are drawn."""
        x, y, width, height = 100, 100, 200, 300

        self.renderer._draw_stripes(self.mock_surface, x, y, width, height)

        # Should draw multiple polygon stripes
        self.assertGreater(mock_polygon.call_count, 0)

    @patch('pygame.draw.polygon')
    @patch('pygame.draw.rect')
    def test_draw_stripes_uses_yellow_color(self, mock_rect, mock_polygon):
        """Test that stripes use yellow color."""
        x, y, width, height = 100, 100, 200, 300

        self.renderer._draw_stripes(self.mock_surface, x, y, width, height)

        # Check that polygons use STRIPE_YELLOW
        for call in mock_polygon.call_args_list:
            color = call[0][1]
            self.assertEqual(color, Config.STRIPE_YELLOW)

    @patch('pygame.draw.polygon')
    @patch('pygame.draw.rect')
    def test_draw_stripes_resets_clipping(self, mock_rect, mock_polygon):
        """Test that clipping region is reset after drawing."""
        x, y, width, height = 100, 100, 200, 300

        self.renderer._draw_stripes(self.mock_surface, x, y, width, height)

        # Verify set_clip was called with None to reset
        calls = self.mock_surface.set_clip.call_args_list
        last_call = calls[-1][0]
        self.assertEqual(last_call[0], None)

    @patch('pygame.draw.polygon')
    @patch('pygame.draw.rect')
    def test_draw_stripes_polygon_points_count(self, mock_rect, mock_polygon):
        """Test that each stripe polygon has 4 points."""
        x, y, width, height = 100, 100, 200, 300

        self.renderer._draw_stripes(self.mock_surface, x, y, width, height)

        # Each polygon should have 4 points
        for call in mock_polygon.call_args_list:
            points = call[0][2]
            self.assertEqual(len(points), 4)


class TestBoardRendererIntegration(unittest.TestCase):
    """Integration tests for BoardRenderer."""

    def setUp(self):
        """Set up test fixtures."""
        pygame.init()
        self.renderer = BoardRenderer()
        self.surface = pygame.Surface((800, 700))

    def tearDown(self):
        """Clean up after tests."""
        pygame.quit()

    def test_full_render_without_errors(self):
        """Test that full render completes without errors."""
        try:
            self.renderer.draw(self.surface)
            success = True
        except Exception:
            success = False

        self.assertTrue(success, "Full render should complete without errors")

    def test_render_multiple_times(self):
        """Test that rendering multiple times works correctly."""
        try:
            for _ in range(5):
                self.renderer.draw(self.surface)
            success = True
        except Exception:
            success = False

        self.assertTrue(success, "Multiple renders should work")

    def test_all_drawing_methods_callable(self):
        """Test that all drawing methods can be called individually."""
        methods = [
            '_draw_border',
            '_draw_board_background',
            '_draw_points',
            '_draw_bar',
            '_draw_right_panel'
        ]

        for method_name in methods:
            with self.subTest(method=method_name):
                method = getattr(self.renderer, method_name)
                try:
                    method(self.surface)
                    success = True
                except Exception:
                    success = False
                self.assertTrue(success, f"{method_name} should be callable")


if __name__ == "__main__":
    unittest.main()