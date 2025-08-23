import unittest

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