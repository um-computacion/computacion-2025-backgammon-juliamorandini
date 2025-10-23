"""
Pruebas unitarias para pygame_ui/checker_renderer.py
(Versión corregida 2)
"""

import unittest
import pygame
from unittest.mock import Mock, patch, call
from typing import List, Dict, Tuple

# --- Dependencias simuladas ---

class Board: #! CORRECCIÓN: Renombrado de 'test_Board' a 'Board'
    """Clase 'Board' simulada para pruebas."""
    points: List[List[str]]
    bar: Dict[str, int]
    borne_off: Dict[str, int]

    def __init__(self) -> None:
        self.points = [[] for _ in range(24)]
        self.bar = {"W": 0, "B": 0}
        self.borne_off = {"W": 0, "B": 0}

# --- Clase bajo prueba ---
try:
    from pygame_ui.checker_renderer import CheckerRenderer
except ImportError:
    print("ADVERTENCIA: No se pudo importar CheckerRenderer. Usando versión local simulada.")
    pass 

# --- Pruebas ---

#! 1. ELIMINAR EL DECORADOR @patch DE LA CLASE
class TestCheckerRenderer(unittest.TestCase):
    """Pruebas unitarias para la clase CheckerRenderer."""

    #! 2. CAMBIAR LA FIRMA DE 'setUp'
    def setUp(self) -> None:
        """Configura el entorno de prueba antes de cada test."""
        
        #! 3. INICIAR EL PATCH MANUALMENTE
        self.patcher = patch('pygame_ui.checker_renderer.Config')
        mock_config = self.patcher.start()
        
        # Esto asegura que self.patcher.stop() se llame automáticamente
        # después de cada prueba, incluso si falla.
        self.addCleanup(self.patcher.stop)

        #! 4. CONFIGURAMOS EL MOCK (igual que antes)
        mock_config.BOARD_X = 10
        mock_config.BOARD_Y = 10
        mock_config.BORDER_THICKNESS = 5
        mock_config.BOARD_HEIGHT = 600
        mock_config.BAR_X = 400
        mock_config.BAR_WIDTH = 50
        mock_config.CHECKER_RADIUS = 20
        mock_config.CHECKER_SPACING = 45
        mock_config.RIGHT_PANEL_X = 800
        mock_config.RIGHT_PANEL_WIDTH = 100
        mock_config.WHITE_CHECKER = (255, 255, 255)
        mock_config.BLACK_CHECKER = (0, 0, 0)
        mock_config.CHECKER_HIGHLIGHT_WHITE = (200, 200, 200)
        mock_config.CHECKER_HIGHLIGHT_BLACK = (50, 50, 50)
        mock_config.CHECKER_OUTLINE = (10, 10, 10)

        pygame.init()
        self.surface = pygame.Surface((1000, 800))
        
        # Ahora, cuando se llame a CheckerRenderer(), usará el mock_config
        # que acabamos de configurar.
        self.renderer = CheckerRenderer() 
        
        # Usa la clase 'Board' corregida para el 'spec'
        self.mock_board = Mock(spec=Board) 
        self.mock_board.points = [[] for _ in range(24)]
        self.mock_board.bar = {"W": 0, "B": 0}
        self.mock_board.borne_off = {"W": 0, "B": 0}

        # Guardamos el mock para usarlo en las aserciones
        self.mock_config = mock_config

    def tearDown(self) -> None:
        """Limpia después de cada prueba."""
        pygame.quit()
        # No es necesario llamar a self.patcher.stop() aquí,
        # self.addCleanup() ya se encarga de eso.

    #! 5. TODOS LOS MÉTODOS DE PRUEBA PERMANECEN EXACTAMENTE IGUAL
    # Ya no necesitan recibir 'mock_config' como argumento,
    # ya que acceden a él a través de 'self.mock_config' guardado en setUp.

    def test_init_calculates_dimensions_correctly(self) -> None:
        """Prueba que __init__ calcula las dimensiones internas correctamente."""
        self.assertEqual(self.renderer._inner_left, 15)
        self.assertEqual(self.renderer._inner_top, 15)
        self.assertEqual(self.renderer._inner_bottom, 605)
        self.assertEqual(self.renderer._point_width, 64)

    def test_get_point_x_center_all_quadrants(self) -> None:
        """Prueba _get_point_x_center para los cuatro cuadrantes."""
        self.assertEqual(self.renderer._get_point_x_center(2), 674)
        self.assertEqual(self.renderer._get_point_x_center(7), 303)
        self.assertEqual(self.renderer._get_point_x_center(15), 239)
        self.assertEqual(self.renderer._get_point_x_center(20), 610)

    @patch("pygame_ui.checker_renderer.pygame.draw.circle")
    def test_draw_single_checker_white(self, mock_draw_circle: Mock) -> None:
        """Prueba que _draw_single_checker dibuja una ficha blanca."""
        self.renderer._draw_single_checker(self.surface, 100, 150, "W")

        self.assertEqual(mock_draw_circle.call_count, 3)
        
        mock_draw_circle.assert_any_call(
            self.surface, 
            self.mock_config.WHITE_CHECKER, 
            (100, 150), 
            self.mock_config.CHECKER_RADIUS
        )
        mock_draw_circle.assert_any_call(
            self.surface, 
            self.mock_config.CHECKER_OUTLINE, 
            (100, 150), 
            self.mock_config.CHECKER_RADIUS, 
            2
        )
        mock_draw_circle.assert_any_call(
            self.surface,
            self.mock_config.CHECKER_HIGHLIGHT_WHITE,
            (95, 145),
            self.mock_config.CHECKER_RADIUS // 3,
        )

    @patch("pygame_ui.checker_renderer.pygame.draw.circle")
    def test_draw_single_checker_black(self, mock_draw_circle: Mock) -> None:
        """Prueba que _draw_single_checker dibuja una ficha negra."""
        self.renderer._draw_single_checker(self.surface, 200, 250, "B")

        self.assertEqual(mock_draw_circle.call_count, 3)
        
        mock_draw_circle.assert_any_call(
            self.surface, 
            self.mock_config.BLACK_CHECKER, 
            (200, 250), 
            self.mock_config.CHECKER_RADIUS
        )
        mock_draw_circle.assert_any_call(
            self.surface, 
            self.mock_config.CHECKER_OUTLINE, 
            (200, 250), 
            self.mock_config.CHECKER_RADIUS, 
            2
        )
        mock_draw_circle.assert_any_call(
            self.surface,
            self.mock_config.CHECKER_HIGHLIGHT_BLACK,
            (195, 245),
            self.mock_config.CHECKER_RADIUS // 3,
        )

    # ... (El resto de tus métodos de prueba van aquí sin cambios) ...

    @patch.object(CheckerRenderer, "_draw_single_checker")
    def test_draw_point_checkers_bottom_row(self, mock_draw_single: Mock) -> None:
        """Prueba el dibujo de fichas en la fila inferior (0-11)."""
        point_index = 5
        checkers = ["W", "W"]
        checker_positions = []

        with patch.object(self.renderer, "_get_point_x_center", return_value=500.0) as mock_get_x:
            self.renderer._draw_point_checkers(
                self.surface, point_index, checkers, checker_positions
            )

        mock_get_x.assert_called_with(5)
        self.assertEqual(mock_draw_single.call_count, 2)
        
        mock_draw_single.assert_has_calls([
            call(self.surface, 500.0, 585, "W"),
            call(self.surface, 500.0, 540, "W")
        ])

        expected_positions = [
            (500, 585, self.mock_config.CHECKER_RADIUS, 5, "W"),
            (500, 540, self.mock_config.CHECKER_RADIUS, 5, "W"),
        ]
        self.assertEqual(checker_positions, expected_positions)

    @patch.object(CheckerRenderer, "_draw_single_checker")
    def test_draw_point_checkers_top_row(self, mock_draw_single: Mock) -> None:
        """Prueba el dibujo de fichas en la fila superior (12-23)."""
        point_index = 15
        checkers = ["B", "B"]
        checker_positions = []

        with patch.object(self.renderer, "_get_point_x_center", return_value=300.0) as mock_get_x:
            self.renderer._draw_point_checkers(
                self.surface, point_index, checkers, checker_positions
            )
        
        mock_get_x.assert_called_with(15)
        self.assertEqual(mock_draw_single.call_count, 2)
        
        mock_draw_single.assert_has_calls([
            call(self.surface, 300.0, 35, "B"),
            call(self.surface, 300.0, 80, "B")
        ])

        expected_positions = [
            (300, 35, self.mock_config.CHECKER_RADIUS, 15, "B"),
            (300, 80, self.mock_config.CHECKER_RADIUS, 15, "B"),
        ]
        self.assertEqual(checker_positions, expected_positions)

    @patch.object(CheckerRenderer, "_draw_single_checker")
    def test_draw_bar_checkers(self, mock_draw_single: Mock) -> None:
        """Prueba el dibujo de fichas en la barra para ambos jugadores."""
        bar_dict = {"W": 2, "B": 1}
        self.renderer._draw_bar_checkers(self.surface, bar_dict)

        self.assertEqual(mock_draw_single.call_count, 3)
        
        mock_draw_single.assert_has_calls([
            call(self.surface, 425, 65, "W"),
            call(self.surface, 425, 110, "W"),
            call(self.surface, 425, 555, "B")
        ], any_order=True)

    @patch.object(CheckerRenderer, "_draw_single_checker")
    def test_draw_bar_checkers_empty(self, mock_draw_single: Mock) -> None:
        """Prueba que no se dibuja nada si la barra está vacía."""
        bar_dict = {"W": 0, "B": 0}
        self.renderer._draw_bar_checkers(self.surface, bar_dict)
        mock_draw_single.assert_not_called()

    @patch.object(CheckerRenderer, "_draw_single_checker")
    def test_draw_borne_off_checkers(self, mock_draw_single: Mock) -> None:
        """Prueba el dibujo de fichas sacadas, con varias filas."""
        borne_off_dict = {"W": 6, "B": 2}
        self.renderer._draw_borne_off_checkers(self.surface, borne_off_dict)

        self.assertEqual(mock_draw_single.call_count, 8)
        
        w_calls = [
            call(self.surface, 850, 505, 'W'),
            call(self.surface, 850, 460, 'W')
        ]
        b_calls = [
            call(self.surface, 850, 115, 'B')
        ]
        
        mock_draw_single.assert_has_calls(w_calls, any_order=True)
        self.assertEqual(
            [c[0][1] for c in mock_draw_single.call_args_list if c[0][3] == "W"].count(850), 6
        )
        self.assertEqual(
            [c[0][2] for c in mock_draw_single.call_args_list if c[0][3] == "W"].count(505), 5
        )
        self.assertEqual(
            [c[0][2] for c in mock_draw_single.call_args_list if c[0][3] == "W"].count(460), 1
        )
        mock_draw_single.assert_has_calls(b_calls, any_order=True)
        self.assertEqual(
            [c[0][2] for c in mock_draw_single.call_args_list if c[0][3] == "B"].count(115), 2
        )


    @patch.object(CheckerRenderer, "_draw_single_checker")
    def test_draw_borne_off_checkers_exceeds_15(self, mock_draw_single: Mock) -> None:
        """Prueba que solo se dibujan 15 fichas como máximo."""
        borne_off_dict = {"W": 20, "B": 0}
        self.renderer._draw_borne_off_checkers(self.surface, borne_off_dict)
        self.assertEqual(mock_draw_single.call_count, 15)

    @patch.object(CheckerRenderer, "_draw_single_checker")
    def test_draw_borne_off_checkers_empty(self, mock_draw_single: Mock) -> None:
        """Prueba que no se dibuja nada si borne_off está vacío."""
        borne_off_dict = {"W": 0, "B": 0}
        self.renderer._draw_borne_off_checkers(self.surface, borne_off_dict)
        mock_draw_single.assert_not_called()

    @patch.object(CheckerRenderer, "_draw_point_checkers")
    @patch.object(CheckerRenderer, "_draw_bar_checkers")
    @patch.object(CheckerRenderer, "_draw_borne_off_checkers")
    def test_draw_main_orchestration(
        self,
        mock_draw_borne_off: Mock,
        mock_draw_bar: Mock,
        mock_draw_point: Mock,
    ) -> None:
        """Prueba que el método `draw` llama a sus submétodos correctamente."""
        self.mock_board.points[1] = ["W"]
        self.mock_board.points[15] = ["B", "B"]
        self.mock_board.bar = {"W": 1, "B": 0}
        self.mock_board.borne_off = {"W": 0, "B": 3}

        checker_positions = self.renderer.draw(self.surface, self.mock_board)

        self.assertEqual(mock_draw_point.call_count, 2)
        mock_draw_point.assert_any_call(
            self.surface, 1, ["W"], checker_positions
        )
        mock_draw_point.assert_any_call(
            self.surface, 15, ["B", "B"], checker_positions
        )
        mock_draw_bar.assert_called_once_with(self.surface, {"W": 1, "B": 0})
        mock_draw_borne_off.assert_called_once_with(self.surface, {"W": 0, "B": 3})
    
    @patch.object(CheckerRenderer, "_draw_point_checkers")
    @patch.object(CheckerRenderer, "_draw_bar_checkers")
    @patch.object(CheckerRenderer, "_draw_borne_off_checkers")
    def test_draw_main_orchestration_empty_board(
        self,
        mock_draw_borne_off: Mock,
        mock_draw_bar: Mock,
        mock_draw_point: Mock,
    ) -> None:
        """Prueba que `draw` funciona en un tablero completamente vacío."""
        checker_positions = self.renderer.draw(self.surface, self.mock_board)

        mock_draw_point.assert_not_called()
        mock_draw_bar.assert_called_once_with(self.surface, {"W": 0, "B": 0})
        mock_draw_borne_off.assert_called_once_with(self.surface, {"W": 0, "B": 0})
        self.assertEqual(checker_positions, [])


if __name__ == "__main__":
    unittest.main()