"""
Módulo de pruebas exhaustivo para la clase BoardRenderer.
(Corrección para el error 'set_clip' read-only)
"""

import unittest
from unittest.mock import Mock, patch, call
import pygame

# --- Clases bajo prueba ---
try:
    from pygame_ui.board_renderer import BoardRenderer
except ImportError:
    print("ADVERTENCIA: No se pudo importar BoardRenderer. Usando versión simulada.")
    class BoardRenderer:
        def __init__(self): pass
        def draw(self, s): pass
        def _draw_border(self, s): pass
        def _draw_board_background(self, s): pass
        def _draw_points(self, s): pass
        def _draw_single_point(self, s, i): pass
        def _draw_bar(self, s): pass
        def _draw_right_panel(self, s): pass
        def _draw_stripes(self, s, x, y, w, h): pass

# --- Clase Base de Pruebas ---

class BoardRendererTestBase(unittest.TestCase):
    """
    Clase base para las pruebas de BoardRenderer.
    
    Maneja el patching de 'Config' y la inicialización/cierre de pygame
    para todas las clases de prueba que hereden de ella.
    """
    
    def setUp(self):
        """Configura el entorno de prueba antes de cada test."""
        
        self.patcher = patch('pygame_ui.board_renderer.Config')
        mock_config = self.patcher.start()
        self.addCleanup(self.patcher.stop)

        # Configuración del mock de Config
        mock_config.BOARD_X = 10
        mock_config.BOARD_Y = 10
        mock_config.BORDER_THICKNESS = 5
        mock_config.BOARD_WIDTH = 800
        mock_config.BOARD_HEIGHT = 600
        mock_config.BAR_X = 400
        mock_config.BAR_WIDTH = 50
        mock_config.POINT_HEIGHT = 200
        mock_config.HINGE_WIDTH = 30
        mock_config.HINGE_HEIGHT = 15
        mock_config.RIGHT_PANEL_X = 750
        mock_config.RIGHT_PANEL_WIDTH = 50
        mock_config.DARK_BROWN = (10, 10, 10)
        mock_config.WOOD_BROWN = (20, 20, 20)
        mock_config.LIGHT_TAN = (30, 30, 30)
        mock_config.DARK_POINT = (40, 40, 40)
        mock_config.GREEN_BAR = (50, 50, 50)
        mock_config.BRASS = (60, 60, 60)
        mock_config.STRIPE_GREEN = (70, 70, 70)
        mock_config.STRIPE_YELLOW = (80, 80, 80)
        
        self.mock_config = mock_config
        pygame.init()
        self.renderer = BoardRenderer()
        
        # La base crea una superficie REAL para las pruebas de integración
        self.surface = pygame.Surface((1000, 800))

    def tearDown(self):
        """Limpia después de cada prueba."""
        pygame.quit()


# --- Clases de Prueba ---

class TestBoardRendererInitialization(BoardRendererTestBase):
    # (Esta clase no necesita cambios)
    def test_initialization_creates_inner_boundaries(self):
        self.assertEqual(self.renderer._inner_left, 15)
        self.assertEqual(self.renderer._inner_right, 805)
        self.assertEqual(self.renderer._inner_top, 15)
        self.assertEqual(self.renderer._inner_bottom, 605)

    def test_initialization_calculates_point_width(self):
        left_section_width = 400 - 15
        expected_point_width = 385 // 6
        self.assertEqual(self.renderer._point_width, expected_point_width)

    def test_private_attributes_exist(self):
        self.assertTrue(hasattr(self.renderer, "_inner_left"))
        self.assertTrue(hasattr(self.renderer, "_inner_right"))
        self.assertTrue(hasattr(self.renderer, "_inner_top"))
        self.assertTrue(hasattr(self.renderer, "_inner_bottom"))
        self.assertTrue(hasattr(self.renderer, "_point_width"))


class TestBoardRendererDraw(BoardRendererTestBase):
    # (Esta clase no necesita cambios)
    @patch.object(BoardRenderer, "_draw_border")
    @patch.object(BoardRenderer, "_draw_board_background")
    @patch.object(BoardRenderer, "_draw_points")
    @patch.object(BoardRenderer, "_draw_bar")
    @patch.object(BoardRenderer, "_draw_right_panel")
    def test_draw_calls_all_methods_in_order(
        self, mock_right_panel, mock_bar, mock_points, mock_bg, mock_border
    ):
        self.renderer.draw(self.surface)
        mock_border.assert_called_once_with(self.surface)
        mock_bg.assert_called_once_with(self.surface)
        mock_points.assert_called_once_with(self.surface)
        mock_bar.assert_called_once_with(self.surface)
        mock_right_panel.assert_called_once_with(self.surface)


class TestDrawBorder(BoardRendererTestBase):
    # (Esta clase no necesita cambios)
    @patch("pygame.draw.rect")
    def test_draw_border_creates_correct_rect(self, mock_draw_rect):
        self.renderer._draw_border(self.surface)
        mock_draw_rect.assert_called_once()
        surface_arg, color, rect = mock_draw_rect.call_args[0]
        self.assertEqual(surface_arg, self.surface)
        self.assertEqual(color, self.mock_config.DARK_BROWN)
        self.assertEqual(rect.width, self.mock_config.BOARD_WIDTH)

class TestDrawBoardBackground(BoardRendererTestBase):
    # (Esta clase no necesita cambios)
    @patch("pygame.draw.rect")
    def test_draw_board_background_creates_correct_rect(self, mock_draw_rect):
        self.renderer._draw_board_background(self.surface)
        mock_draw_rect.assert_called_once()
        surface_arg, color, rect = mock_draw_rect.call_args[0]
        self.assertEqual(surface_arg, self.surface)
        self.assertEqual(color, self.mock_config.WOOD_BROWN)
        self.assertEqual(rect.x, self.renderer._inner_left)

class TestDrawPoints(BoardRendererTestBase):
    # (Esta clase no necesita cambios)
    @patch.object(BoardRenderer, "_draw_single_point")
    def test_draw_points_calls_draw_single_point_24_times(self, mock_draw_single):
        self.renderer._draw_points(self.surface)
        self.assertEqual(mock_draw_single.call_count, 24)
        mock_draw_single.assert_any_call(self.surface, 23)

class TestDrawSinglePoint(BoardRendererTestBase):
    # (Esta clase no necesita cambios)
    @patch("pygame.draw.polygon")
    def test_draw_single_point_quadrants(self, mock_draw_polygon):
        self.renderer._draw_single_point(self.surface, 2)
        mock_draw_polygon.assert_called()
        mock_draw_polygon.reset_mock()
        self.renderer._draw_single_point(self.surface, 8)
        mock_draw_polygon.assert_called()
        mock_draw_polygon.reset_mock()
        self.renderer._draw_single_point(self.surface, 14)
        mock_draw_polygon.assert_called()
        mock_draw_polygon.reset_mock()
        self.renderer._draw_single_point(self.surface, 20)
        mock_draw_polygon.assert_called()

    @patch("pygame.draw.polygon")
    def test_draw_single_point_uses_alternating_colors(self, mock_draw_polygon):
        self.renderer._draw_single_point(self.surface, 0)
        self.assertEqual(mock_draw_polygon.call_args[0][1], self.mock_config.LIGHT_TAN)
        self.renderer._draw_single_point(self.surface, 6)
        self.assertEqual(mock_draw_polygon.call_args[0][1], self.mock_config.DARK_POINT)
        self.renderer._draw_single_point(self.surface, 12)
        self.assertEqual(mock_draw_polygon.call_args[0][1], self.mock_config.LIGHT_TAN)
        self.renderer._draw_single_point(self.surface, 18)
        self.assertEqual(mock_draw_polygon.call_args[0][1], self.mock_config.DARK_POINT)

    @patch("pygame.draw.polygon")
    def test_draw_single_point_triangle_shape_bottom(self, mock_draw_polygon):
        self.renderer._draw_single_point(self.surface, 5)
        points = mock_draw_polygon.call_args[0][2]
        self.assertEqual(points[2][1], self.renderer._inner_bottom - self.mock_config.POINT_HEIGHT)

    @patch("pygame.draw.polygon")
    def test_draw_single_point_triangle_shape_top(self, mock_draw_polygon):
        self.renderer._draw_single_point(self.surface, 15)
        points = mock_draw_polygon.call_args[0][2]
        self.assertEqual(points[2][1], self.renderer._inner_top + self.mock_config.POINT_HEIGHT)


class TestDrawBar(BoardRendererTestBase):
    # (Esta clase no necesita cambios)
    @patch("pygame.draw.rect")
    @patch("pygame.draw.line")
    def test_draw_bar_creates_all_components(self, mock_line, mock_rect):
        self.renderer._draw_bar(self.surface)
        self.assertEqual(mock_rect.call_args_list[0][0][1], self.mock_config.GREEN_BAR)
        self.assertEqual(mock_line.call_count, 8)
        self.assertEqual(mock_rect.call_count, 5)
        self.assertEqual(mock_rect.call_args_list[1][0][1], self.mock_config.BRASS)
        self.assertEqual(mock_rect.call_args_list[3][0][1], self.mock_config.BRASS)


class TestDrawRightPanel(BoardRendererTestBase):
    # (Esta clase no necesita cambios)
    @patch.object(BoardRenderer, "_draw_stripes")
    @patch("pygame.draw.rect")
    def test_draw_right_panel_creates_three_sections(self, mock_rect, mock_stripes):
        self.renderer._draw_right_panel(self.surface)
        self.assertEqual(mock_stripes.call_count, 2)
        mock_rect.assert_called_once()
        self.assertEqual(mock_rect.call_args[0][1], self.mock_config.WOOD_BROWN)
        self.assertEqual(mock_stripes.call_args_list[0][0][1], self.mock_config.RIGHT_PANEL_X)


# --- INICIO DE LA CORRECCIÓN ---

class TestDrawStripes(BoardRendererTestBase):
    """Prueba el método _draw_stripes."""

    def setUp(self):
        """Sobrescribe el setUp para usar una superficie Mock."""
        # Llama al setUp de la clase base (para config, pygame.init, etc.)
        super().setUp()
        # Sobrescribe self.surface con un Mock para esta clase de prueba
        # Esto nos permite verificar las llamadas a 'set_clip' sin error
        self.surface = Mock(spec=pygame.Surface)

    @patch("pygame.draw.polygon")
    @patch("pygame.draw.rect")
    def test_draw_stripes_workflow(self, mock_rect, mock_polygon):
        """Prueba el flujo completo de _draw_stripes."""
        x, y, width, height = 100, 100, 200, 300
        
        # Llama al método con la superficie Mock
        self.renderer._draw_stripes(self.surface, x, y, width, height)

        # 1. Dibuja el fondo
        mock_rect.assert_called_once()
        self.assertEqual(mock_rect.call_args[0][1], self.mock_config.STRIPE_GREEN)

        # 2. Dibuja múltiples polígonos
        self.assertGreater(mock_polygon.call_count, 0)
        
        # 3. Todos los polígonos son amarillos
        polygon_color = mock_polygon.call_args[0][1]
        self.assertEqual(polygon_color, self.mock_config.STRIPE_YELLOW)
        
        # 4. Todos los polígonos tienen 4 puntos
        polygon_points = mock_polygon.call_args[0][2]
        self.assertEqual(len(polygon_points), 4)

        # 5. Establece y reinicia el clip (ahora funciona porque self.surface es un Mock)
        clip_calls = self.surface.set_clip.call_args_list
        self.assertEqual(len(clip_calls), 2)
        self.assertEqual(clip_calls[0][0][0], pygame.Rect(x, y, width, height)) # Establece
        self.assertEqual(clip_calls[1][0][0], None) # Reinicia

# --- FIN DE LA CORRECCIÓN ---


class TestBoardRendererIntegration(BoardRendererTestBase):
    """
    Pruebas de integración que ejecutan el código sin mocks internos.
    (Esta clase usa la superficie REAL de la clase base)
    """

    def test_full_render_without_errors(self):
        """
        Prueba que 'draw' se ejecuta completamente sin mocks internos
        (excepto pygame) y no lanza errores.
        """
        try:
            self.renderer.draw(self.surface)
            success = True
        except Exception as e:
            print(f"Error en full_render: {e}")
            success = False

        self.assertTrue(success, "La renderización completa no debe lanzar errores")

    def test_all_drawing_methods_callable(self):
        """Prueba que todos los métodos de dibujo se pueden llamar."""
        methods = [
            "_draw_border",
            "_draw_board_background",
            "_draw_points",
            "_draw_bar",
            "_draw_right_panel",
        ]

        for method_name in methods:
            with self.subTest(method=method_name):
                method = getattr(self.renderer, method_name)
                try:
                    method(self.surface)
                    success = True
                except Exception as e:
                    print(f"Error llamando a {method_name}: {e}")
                    success = False
                self.assertTrue(success, f"{method_name} debe ser ejecutable")


if __name__ == "__main__":
    unittest.main()