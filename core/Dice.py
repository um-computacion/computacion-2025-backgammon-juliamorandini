from typing import Tuple, List
import random

class Dice:
    """Simple dice class for Backgammon."""

    def __init__(self):
        """Initialize with two dice set to 1."""
        self.die1 = 1
        self.die2 = 1

    def roll(self):
        """Roll both dice."""
        self.die1 = random.randint(1, 6)
        self.die2 = random.randint(1, 6)
        return (self.die1, self.die2)

    def get_values(self):
        """Get current dice values."""
        return (self.die1, self.die2)

    def is_double(self):
        """Check if dice show same value."""
        return self.die1 == self.die2

    def get_moves(self):
        """Get available moves based on dice values."""
        if self.is_double():
            return [self.die1] * 4
        return [self.die1, self.die2]

    @property
    def die1(self):
        return self._die1

    @die1.setter
    def die1(self, value):
        if not 1 <= value <= 6:
            raise ValueError("Die value must be between 1 and 6")
        self._die1 = value

    @property
    def die2(self):
        return self._die2

    @die2.setter
    def die2(self, value):
        if not 1 <= value <= 6:
            raise ValueError("Die value must be between 1 and 6")
        self._die2 = value