import unittest
from core.Dice import Dice
from unittest.mock import patch

class TestDice(unittest.TestCase):
    """Test cases for the Dice class in Backgammon game.
    
    This class contains unit tests that verify:
    - Dice roll values are within valid range (1-6)
    - Double rolls are correctly identified
    - Move generation for both regular and double rolls
    - Initial state of dice
    - Independence of dice rolls
    """

    def setUp(self):
        """Set up a new Dice instance before each test."""
        self.dice = Dice()

    @patch('random.randint', side_effect=[5, 2])
    def test_roll_different_values(self, mock_randint):
        """Test that rolling dice produces the expected mock values."""
        result = self.dice.roll()
        self.assertEqual(result, (5, 2))

    def test_roll_values_in_range(self):
        """Test that all rolled values are between 1 and 6."""
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
        """Test move generation for non-double rolls."""
        self.dice.die1 = 3
        self.dice.die2 = 5
        self.assertEqual(self.dice.get_moves(), [3, 5])

    def test_get_moves_double(self):
        """Test move generation for double rolls."""
        self.dice.die1 = 6
        self.dice.die2 = 6
        self.assertEqual(self.dice.get_moves(), [6, 6, 6, 6])

    def test_initial_values(self):
        # Al crear el dado, los valores iniciales deben ser 1, 1
        self.assertEqual(self.dice.get_values(), (1, 1))

    def test_get_moves_returns_list(self):
        """Test that get_moves always returns a list of integers."""
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
        """Test that dice can show different values."""
        found_diff = False
        for _ in range(50):
            self.dice.roll()
            if self.dice.die1 != self.dice.die2:
                found_diff = True
                break
        self.assertTrue(found_diff, "Los dados deben poder mostrar valores distintos.")

    def test_invalid_dice_values(self):
        """Test that dice values cannot be set to invalid numbers."""
        with self.assertRaises(ValueError):
            self.dice.die1 = 7
        with self.assertRaises(ValueError):
            self.dice.die2 = 0

if __name__ == '__main__':
    unittest.main()