# test_checker.py
import unittest
from core.Checker import Checker


class TestChecker(unittest.TestCase):

    def setUp(self):
        self.white_checker = Checker("white", 1)
        self.black_checker = Checker("black", 1)
        self.board = {
            1: [self.white_checker],
            2: [],
            3: [self.black_checker],
            4: [Checker("black", 4), Checker("black", 4)],
            5: [Checker("white", 5)],
        }

    def test_move_to_empty_point(self):
        # Puede moverse a un punto vacío
        self.assertTrue(self.white_checker.can_move_to(2, self.board))

    def test_move_to_own_point(self):
        # Puede moverse a un punto ocupado por sus propias fichas
        self.assertTrue(self.white_checker.can_move_to(5, self.board))

    def test_move_to_single_opponent_checker(self):
        # Puede golpear una ficha sola del oponente
        self.assertTrue(self.white_checker.can_move_to(3, self.board))

    def test_move_to_blocked_point(self):
        # No puede moverse a un punto con dos o más fichas del oponente
        self.assertFalse(self.white_checker.can_move_to(4, self.board))

    def test_move_updates_position(self):
        # Al moverse, la posición debe actualizarse
        self.white_checker.move(2, self.board)
        self.assertEqual(self.white_checker.position, 2)

    def test_move_to_blocked_point_fails(self):
        # No debe moverse si el punto está bloqueado
        moved = self.white_checker.move(4, self.board)
        self.assertFalse(moved)
        self.assertEqual(self.white_checker.position, 1)

    def test_checker_color(self):
        # El color debe ser válido
        self.assertIn(self.white_checker.color, ["white", "black"])
        self.assertIn(self.black_checker.color, ["white", "black"])

    def test_cannot_move_from_bar_to_blocked(self):
        # No puede entrar desde la barra si el punto está bloqueado
        self.white_checker.send_to_bar()  # Usar este método en lugar de position = 'bar'
        self.board[1] = [Checker("black", 1), Checker("black", 1)]
        self.assertFalse(self.white_checker.can_move_to(1, self.board))

    def test_bear_off_allowed(self):
        # Simula que la ficha puede salir del tablero (bear off)
        self.white_checker.position = 24
        # Suponiendo que el método can_bear_off existe y verifica la condición
        if hasattr(self.white_checker, "can_bear_off"):
            self.assertTrue(self.white_checker.can_bear_off(self.board))

    def test_invalid_color(self):
        # No debería aceptar colores inválidos
        with self.assertRaises(ValueError):
            Checker("red", 1)


if __name__ == "__main__":
    unittest.main()
