"""
Pruebas unitarias para pygame_ui/backgammon_board.py
"""

import unittest
import pygame
from unittest.mock import patch, Mock, MagicMock

# Importar la clase que queremos probar
from pygame_ui.backgammon_board import BackgammonBoard

# Importar las clases que vamos a simular (para 'autospec')
from core.board import Board as CoreBoard
from core.Dice import Dice as CoreDice
from pygame_ui.board_renderer import BoardRenderer
from pygame_ui.checker_renderer import CheckerRenderer
from pygame_ui.dice_renderer import DiceRenderer


class TestBackgammonBoard(unittest.TestCase):
    """Pruebas para la clase coordinadora BackgammonBoard."""

    def setUp(self):
        """
        Configura el entorno de prueba.
        Simulamos (patch) todas las dependencias que BackgammonBoard importa
        y crea en su __init__.
        """
        
        # 1. Definir los patchers para cada dependencia
        # Usamos 'autospec=True' para que los mocks tengan la misma firma
        # que las clases reales.
        self.patcher_board = patch(
            'pygame_ui.backgammon_board.Board', autospec=True
        )
        self.patcher_dice = patch(
            'pygame_ui.backgammon_board.Dice', autospec=True
        )
        self.patcher_board_renderer = patch(
            'pygame_ui.backgammon_board.BoardRenderer', autospec=True
        )
        self.patcher_checker_renderer = patch(
            'pygame_ui.backgammon_board.CheckerRenderer', autospec=True
        )
        self.patcher_dice_renderer = patch(
            'pygame_ui.backgammon_board.DiceRenderer', autospec=True
        )

        # 2. Iniciar los patchers
        self.MockBoard = self.patcher_board.start()
        self.MockDice = self.patcher_dice.start()
        self.MockBoardRenderer = self.patcher_board_renderer.start()
        self.MockCheckerRenderer = self.patcher_checker_renderer.start()
        self.MockDiceRenderer = self.patcher_dice_renderer.start()

        # 3. Registrar la limpieza para detener los patchers después de cada prueba
        self.addCleanup(self.patcher_board.stop)
        self.addCleanup(self.patcher_dice.stop)
        self.addCleanup(self.patcher_board_renderer.stop)
        self.addCleanup(self.patcher_checker_renderer.stop)
        self.addCleanup(self.patcher_dice_renderer.stop)

        # 4. Guardar las *instancias* que __init__ creará
        self.mock_board_inst = self.MockBoard.return_value
        self.mock_dice_inst = self.MockDice.return_value
        self.mock_board_renderer_inst = self.MockBoardRenderer.return_value
        self.mock_checker_renderer_inst = self.MockCheckerRenderer.return_value
        self.mock_dice_renderer_inst = self.MockDiceRenderer.return_value
        
        # 5. Crear la instancia de la clase bajo prueba
        # Su __init__ ahora usará nuestras clases Mock
        self.game_board = BackgammonBoard()

        # 6. Crear una superficie de pygame simulada
        self.mock_surface = MagicMock(spec=pygame.Surface)

    def test_init_and_properties(self):
        """
        Prueba la inicialización y las propiedades.
        Cubre la propiedad 'dice_values' (línea 78).
        """
        # Verificar que todos los constructores de dependencias fueron llamados
        self.MockBoard.assert_called_once()
        self.MockDice.assert_called_once()
        self.MockBoardRenderer.assert_called_once()
        self.MockCheckerRenderer.assert_called_once()
        self.MockDiceRenderer.assert_called_once()

        # Verificar el estado inicial
        self.assertEqual(self.game_board.current_player, "W")
        self.assertEqual(self.game_board.dice_values, [])
        self.assertIs(self.game_board.board, self.mock_board_inst)

    def test_render_no_dice(self):
        """
        Prueba el renderizado cuando no hay dados que mostrar.
        Cubre la rama 'False' de la condición 'if self.__dice_values__' (línea 99).
        """
        self.game_board.render(self.mock_surface)

        # Debe dibujar el tablero y las fichas
        self.mock_board_renderer_inst.draw.assert_called_once_with(
            self.mock_surface
        )
        self.mock_checker_renderer_inst.draw.assert_called_once_with(
            self.mock_surface, self.mock_board_inst
        )
        
        # No debe dibujar los dados
        self.mock_dice_renderer_inst.draw.assert_not_called()

    def test_render_with_dice(self):
        """
        Prueba el renderizado cuando SÍ hay dados.
        Cubre las líneas 99-102.
        """
        # Forzamos el estado para tener valores de dados
        self.game_board.__dict__['__dice_values__'] = [5, 2] # Acceso directo para la prueba

        self.game_board.render(self.mock_surface)

        # Debe dibujar todo
        self.mock_board_renderer_inst.draw.assert_called_once_with(
            self.mock_surface
        )
        self.mock_checker_renderer_inst.draw.assert_called_once_with(
            self.mock_surface, self.mock_board_inst
        )
        
        # Debe dibujar los dados con los valores correctos
        self.mock_dice_renderer_inst.draw.assert_called_once_with(
            self.mock_surface, [5, 2]
        )

    def test_render_with_doubles_dice(self):
        """
        Prueba que el renderizado solo muestra 2 dados incluso si hay 4 (dobles).
        Confirma la lógica de 'display_values' (línea 101).
        """
        self.game_board.__dict__['__dice_values__'] = [3, 3, 3, 3]

        self.game_board.render(self.mock_surface)
        
        # Debe dibujar los dados, pero solo los dos primeros
        self.mock_dice_renderer_inst.draw.assert_called_once_with(
            self.mock_surface, [3, 3] # Solo los dos primeros
        )

    def test_update(self):
        """
        Prueba el método 'update'.
        Cubre la línea 116 ('pass').
        """
        # Simplemente llamamos al método para cubrirlo
        try:
            self.game_board.update()
        except Exception as e:
            self.fail(f"update() generó una excepción inesperada: {e}")
        # No se espera ninguna acción

    def test_reset(self):
        """Prueba que el reseteo llama a sus dependencias y reinicia el estado."""
        # Cambiamos el estado
        self.game_board.__dict__['__current_player__'] = "B"
        self.game_board.__dict__['__dice_values__'] = [1, 2]

        # Ejecutamos el reseteo
        self.game_board.reset()

        # Verificar que los métodos de reseteo de las dependencias fueron llamados
        self.mock_board_inst.reset.assert_called_once()
        self.mock_dice_inst.reset.assert_called_once()

        # Verificar que el estado interno se reinició
        self.assertEqual(self.game_board.current_player, "W")
        self.assertEqual(self.game_board.dice_values, [])

    def test_roll_dice(self):
        """Prueba que 'roll_dice' usa la clase Dice y actualiza el estado."""
        expected_moves = [4, 6]
        self.mock_dice_inst.get_moves.return_value = expected_moves
        
        moves = self.game_board.roll_dice()

        # Verificar que se usó la dependencia
        self.mock_dice_inst.roll.assert_called_once()
        self.mock_dice_inst.get_moves.assert_called_once()
        
        # Verificar que el estado y el valor de retorno son correctos
        self.assertEqual(moves, expected_moves)
        self.assertEqual(self.game_board.dice_values, expected_moves)

    def test_move_checker(self):
        """
        Prueba que 'move_checker' delega la llamada al Board.
        Cubre las líneas 148-150.
        """
        self.mock_board_inst.move_checker.return_value = True
        
        # El jugador actual es 'W'
        result = self.game_board.move_checker(from_point=10, to_point=15)

        # Verificar que se llamó al tablero con los argumentos correctos
        self.mock_board_inst.move_checker.assert_called_once_with(
            10, 15, "W" # Asegurarse de que pasa al jugador actual
        )
        self.assertTrue(result)

    def test_switch_player(self):
        """
        Prueba el cambio de jugador.
        Cubre la línea 165 (limpiar 'dice_values').
        """
        # Estado inicial: W, con dados
        self.game_board.__dict__['__dice_values__'] = [5, 5]
        self.assertEqual(self.game_board.current_player, "W")

        # Primer cambio
        self.game_board.switch_player()
        self.assertEqual(self.game_board.current_player, "B")
        self.assertEqual(self.game_board.dice_values, [], "Los dados no se limpiaron")

        # Segundo cambio
        self.game_board.switch_player()
        self.assertEqual(self.game_board.current_player, "W")
        self.assertEqual(self.game_board.dice_values, [])


if __name__ == "__main__":
    # Necesario para inicializar pygame si se usa spec=pygame.Surface
    pygame.init()
    unittest.main()