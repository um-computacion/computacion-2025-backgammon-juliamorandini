import unittest
from src.Dice import Dice


class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_roll_values_in_range(self):
        # Lanzar los dados varias veces y comprobar que los valores están en el rango 1-6
        for _ in range(100):
            self.dice.roll()
            die1, die2 = self.dice.get_values()
            self.assertIn(die1, range(1, 7))
            self.assertIn(die2, range(1, 7))

    def test_is_double(self):
        # Forzar dobles y no dobles
        self.dice.die1 = 4
        self.dice.die2 = 4
        self.assertTrue(self.dice.is_double())
        self.dice.die2 = 5
        self.assertFalse(self.dice.is_double())

    def test_get_moves_no_double(self):
        self.dice.die1 = 3
        self.dice.die2 = 5
        self.assertEqual(self.dice.get_moves(), [3, 5])

    def test_get_moves_double(self):
        self.dice.die1 = 6
        self.dice.die2 = 6
        self.assertEqual(self.dice.get_moves(), [6, 6, 6, 6])

    def test_initial_values(self):
        # Al crear el dado, los valores iniciales deben ser 1, 1
        self.assertEqual(self.dice.get_values(), (1, 1))

    def test_get_moves_returns_list(self):
        # get_moves siempre debe devolver una lista de enteros
        self.dice.roll()
        moves = self.dice.get_moves()
        self.assertIsInstance(moves, list)
        for move in moves:
            self.assertIsInstance(move, int)

    def test_reset_dice(self):
        # Si existe un método reset, debe volver a (1, 1)
        if hasattr(self.dice, 'reset'):
            self.dice.roll()
            self.dice.reset()
            self.assertEqual(self.dice.get_values(), (1, 1))

    def test_dice_are_independent(self):
        # Los dos dados pueden tener valores distintos
        found_diff = False
        for _ in range(50):
            self.dice.roll()
            if self.dice.die1 != self.dice.die2:
                found_diff = True
                break
        self.assertTrue(found_diff, "Los dados deben poder mostrar valores distintos.")

if __name__ == '__main__':
    unittest.main()