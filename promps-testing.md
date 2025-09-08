## test_board.py
# promp: haz test para la clase board que determine las reglas del tablero de backgammon con unittest (es github copilot con gpt 4.1)
# respuesta:

import unittest
from src.board import Board

class TestBackgammonBoard(unittest.TestCase):

    def setUp(self):
        # Suponemos que tienes una clase Board con un método reset() para inicializar el tablero 
        self.board = Board()
        self.board.reset()

    def test_board_has_24_points(self):
        self.assertEqual(len(self.board.points), 24, "El tablero debe tener 24 puntos.")

    def test_initial_setup(self):
        # Suponemos que cada punto es una lista de fichas, y que las fichas son 'W' (blanco) o 'B' (negro)
        expected_setup = {
            0:  ['W', 'W'],
            5:  ['B']*5,
            7:  ['B']*3,
            11: ['W']*5,
            12: ['B']*5,
            16: ['W']*3,
            18: ['W']*5,
            23: ['B', 'B']
        }
        for point, checkers in expected_setup.items():
            self.assertEqual(self.board.points[point], checkers, f"El punto {point+1} debe tener {checkers} fichas.")
        # Los demás puntos deben estar vacíos
        for i in range(24):
            if i not in expected_setup:
                self.assertEqual(self.board.points[i], [], f"El punto {i+1} debe estar vacío.")

    def test_no_mixed_checkers_on_point(self):
        # Intentar poner fichas de ambos colores en un punto debe fallar
        self.board.points[0] = ['W', 'B']
        self.assertFalse(self.board.is_valid(), "No puede haber fichas de ambos colores en el mismo punto.")

    def test_move_checker(self):
        # Suponemos que hay un método move_checker(from_point, to_point, color)
        self.board.move_checker(0, 1, 'W')
        self.assertEqual(self.board.points[0], ['W'])
        self.assertEqual(self.board.points[1], ['W'])

    def test_capture_checker(self):
        # Simula una captura: un punto con una sola ficha del oponente
        self.board.points[5] = ['B']
        self.board.points[4] = ['W']
        self.board.move_checker(4, 5, 'W')
        self.assertEqual(self.board.bar['B'], 1, "La ficha negra debe estar en la barra tras ser capturada.")
        self.assertEqual(self.board.points[5], ['W'])

    def test_illegal_move(self):
        # No se puede mover a un punto con 2 o más fichas del oponente
        self.board.points[5] = ['B', 'B']
        self.assertFalse(self.board.is_legal_move(4, 5, 'W'), "No se puede mover a un punto bloqueado.")



    def test_cannot_move_from_empty_point(self):
        # No se puede mover ficha desde un punto vacío
        self.board.points[10] = []
        self.assertFalse(self.board.is_legal_move(10, 12, 'W'), "No se puede mover desde un punto vacío.")

    def test_cannot_move_opponent_checker(self):
        # No se puede mover ficha del oponente
        self.board.points[8] = ['B']
        self.assertFalse(self.board.is_legal_move(8, 10, 'W'), "No se puede mover ficha del oponente.")

    def test_bar_priority(self):
        # Si hay fichas en la barra, deben entrar antes de mover otras fichas
        self.board.bar['W'] = 1
        self.assertFalse(self.board.is_legal_move(0, 2, 'W'), "Debe ingresar ficha desde la barra antes de mover otras.")

    def test_bear_off_only_when_all_in_home(self):
        # Solo se puede sacar fichas si todas están en el home
        self.board.points = [[] for _ in range(24)]
        self.board.points[18] = ['W'] * 15  # Todas en home
        self.assertTrue(self.board.can_bear_off('W'), "Debe poder sacar fichas si todas están en el home.")
        self.board.points[10] = ['W']  # Una fuera del home
        self.assertFalse(self.board.can_bear_off('W'), "No debe poder sacar fichas si alguna está fuera del home.")

    def test_bear_off(self):
        # Simula sacar una ficha
        self.board.points = [[] for _ in range(24)]
        self.board.points[18] = ['W']
        self.board.bear_off('W', 18)
        self.assertEqual(self.board.points[18], [], "La ficha debe ser removida del punto.")
        self.assertEqual(self.board.borne_off['W'], 1, "La ficha debe estar en la zona de borne.")

    def test_blocked_entry_from_bar(self):
        # No puede entrar desde la barra si el punto está bloqueado
        self.board.bar['W'] = 1
        self.board.points[0] = ['B', 'B']
        self.assertFalse(self.board.can_enter_from_bar('W', 0), "No puede entrar si el punto está bloqueado.")

if __name__ == '__main__':
    unittest.main()

## observaciones: esta bien de momento, pense en cambiar de w a B para blanco envés de white y B a N para negro pero creo que esta bien y no va a afectar mucho., lo mismo con el resto de las funciones que estan en ingles
agregue un import src.board para que lo detectara en el test




promp:haz test para la clase game que determine las reglas de los de backgammon con unittest
respuestas:
import unittest
from game import Game  # Asumiendo que la clase Game está en un archivo game.py

class TestBackgammonGame(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada test"""
        self.game = Game()

    def test_initial_board_setup(self):
        """Test para verificar la configuración inicial del tablero"""
        board = self.game.get_board()
        # Verificar posiciones iniciales de las fichas
        self.assertEqual(board[0], (-2))  # 2 fichas negras en posición 0
        self.assertEqual(board[23], (2))  # 2 fichas blancas en posición 23
        self.assertEqual(board[11], (5))  # 5 fichas blancas en posición 11
        self.assertEqual(board[12], (-5)) # 5 fichas negras en posición 12

    def test_valid_move(self):
        """Test para verificar movimientos válidos"""
        # Simular un movimiento válido
        result = self.game.make_move(1, 3) # mover desde posición 1 a 3
        self.assertTrue(result)

    def test_invalid_move(self):
        """Test para verificar movimientos inválidos"""
        # Simular un movimiento inválido
        result = self.game.make_move(1, 8) # movimiento demasiado largo
        self.assertFalse(result)

    def test_hitting_blot(self):
        """Test para verificar la captura de fichas solitarias"""
        # Configurar situación de blot
        self.game.set_piece(5, 1) # Una ficha solitaria en posición 5
        # Realizar movimiento de captura
        self.game.make_move(3, 5)
        # Verificar que la ficha fue capturada
        self.assertEqual(self.game.get_bar_pieces(), 1)

    def test_bearing_off(self):
        """Test para verificar las reglas de salida de fichas"""
        # Configurar situación de bearing off
        self.game.setup_bearing_off_scenario()
        # Intentar sacar una ficha
        result = self.game.bear_off(23)
        self.assertTrue(result)

    def test_double_dice(self):
        """Test para verificar el manejo de dados dobles"""
        self.game.set_dice([6, 6])
        # Verificar que se permiten 4 movimientos
        moves_allowed = self.game.get_available_moves()
        self.assertEqual(len(moves_allowed), 4)

    def test_blocked_position(self):
        """Test para verificar posiciones bloqueadas"""
        # Crear un bloqueo (más de 2 fichas del oponente)
        self.game.set_piece(10, -3)
        # Intentar mover a una posición bloqueada
        result = self.game.make_move(8, 10)
        self.assertFalse(result)

    def test_winner_detection(self):
        """Test para verificar la detección del ganador"""
        # Configurar un escenario de victoria
        self.game.setup_winning_scenario()
        # Verificar si hay un ganador
        self.assertTrue(self.game.check_winner())

    def test_valid_dice_moves(self):
        """Test para verificar movimientos según los dados"""
        self.game.set_dice([3, 4])
        # Verificar que solo se permiten movimientos de 3 y 4 espacios
        valid_moves = self.game.get_valid_moves()
        self.assertTrue(all(move in [3, 4] for move in valid_moves))

    def test_bar_piece_movement(self):
        """Test para verificar el movimiento obligatorio de fichas en la barra"""
        # Poner una ficha en la barra
        self.game.add_to_bar()
        # Verificar que solo se permiten movimientos desde la barra
        self.assertTrue(self.game.must_move_from_bar())
        
if __name__ == '__main__':
    unittest.main()

observaciones y cambios: cambie nombres de clases, ademas agregue las especificaciones que me dio en la conversacion para tener como referencia para el creado de la clase