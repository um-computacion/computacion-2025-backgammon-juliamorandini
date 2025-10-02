import unittest
from unittest.mock import patch
from core.Dice import Dice


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

    @patch("random.randint", side_effect=[5, 2])
    def test_roll_different_values(self, _):
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
        if hasattr(self.dice, "reset"):
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

    def test_mock_rolls(self):
        """Test that mock rolls work correctly."""
        mock_values = [(3, 4), (6, 6), (1, 2)]
        self.dice.set_mock_rolls(mock_values)

        for expected in mock_values:
            result = self.dice.roll()
            self.assertEqual(result, expected)

    def test_clear_mock(self):
        """Test clearing mock values."""
        self.dice.set_mock_rolls([(1, 1)])
        self.dice.clear_mock()
        # Should now use random values
        for _ in range(10):
            v1, v2 = self.dice.roll()
            self.assertTrue(1 <= v1 <= 6)
            self.assertTrue(1 <= v2 <= 6)

    def test_mock_exhaustion(self):
        """Test behavior when mock values are exhausted."""
        self.dice.set_mock_rolls([(1, 1)])
        self.dice.roll()  # Use the mock value
        # Should now use random values
        for _ in range(10):
            v1, v2 = self.dice.roll()
            self.assertTrue(1 <= v1 <= 6)
            self.assertTrue(1 <= v2 <= 6)

    def test_reset_clears_mock(self):
        """Test that reset clears mock values."""
        self.dice.set_mock_rolls([(6, 6)])
        self.dice.reset()
        self.assertEqual(self.dice.get_values(), (1, 1))
        # Should use random values after reset
        v1, v2 = self.dice.roll()
        self.assertTrue(1 <= v1 <= 6)
        self.assertTrue(1 <= v2 <= 6)

    def test_invalid_mock_values(self):
        """Test setting invalid mock values."""
        with self.assertRaises(ValueError):
            self.dice.set_mock_rolls([(7, 1)])
        with self.assertRaises(ValueError):
            self.dice.set_mock_rolls([(1, 0)])

    def test_die_type_validation(self):
        """Test that die values must be integers."""
        with self.assertRaises(TypeError):
            self.dice.die1 = 1.5
        with self.assertRaises(TypeError):
            self.dice.die2 = "3"

    def test_empty_mock_values(self):
        """Test that empty mock values list raises error."""
        with self.assertRaises(ValueError):
            self.dice.set_mock_rolls([])

    def test_none_mock_values(self):
        """Test setting None as mock values."""
        with self.assertRaises(ValueError):
            self.dice.set_mock_rolls(None)

    def test_mock_invalid_tuple_size(self):
        """Test mock values with wrong tuple size."""
        with self.assertRaises(ValueError):
            self.dice.set_mock_rolls([(1,)])
        with self.assertRaises(ValueError):
            self.dice.set_mock_rolls([(1, 2, 3)])

    def test_property_getters(self):
        """Test die property getters."""
        self.dice.die1 = 3
        self.dice.die2 = 4
        self.assertEqual(self.dice.die1, 3)
        self.assertEqual(self.dice.die2, 4)

    def test_consecutive_rolls(self):
        """Test multiple consecutive rolls."""
        prev_values = self.dice.get_values()
        found_different = False

        for _ in range(10):
            current_values = self.dice.roll()
            if current_values != prev_values:
                found_different = True
                break
            prev_values = current_values

        self.assertTrue(found_different, "Consecutive rolls should eventually differ")


if __name__ == "__main__":
    unittest.main()
