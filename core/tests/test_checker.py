# test_checker.py
import unittest
from checker import Checker

class TestChecker(unittest.TestCase):

    def setUp(self):
        self.white_checker = Checker('white', 1)
        self.black_checker = Checker('black', 1)
        self.board = {
            1: [self.white_checker],
            2: [],
            3: [self.black_checker],
            4: [Checker('black', 4), Checker('black', 4)],
            5: [Checker('white', 5)],
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

if __name__ == '__main__':
    unittest.main()