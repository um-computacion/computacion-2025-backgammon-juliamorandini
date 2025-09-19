import random
from typing import Tuple, List

class Dice:
    """Class representing dice in Backgammon game."""

    def __init__(self) -> None:
        """Initialize dice with value 1."""
        self._values = [1, 1]

    def roll(self) -> Tuple[int, int]:
        """Roll both dice and return their values."""
        self._values = [random.randint(1, 6) for _ in range(2)]
        return tuple(self._values)

    def get_values(self) -> Tuple[int, int]:
        """Return current dice values."""
        return tuple(self._values)

    def is_double(self) -> bool:
        """Check if dice show same value."""
        return self._values[0] == self._values[1]

    def get_moves(self) -> List[int]:
        """Return available moves based on dice values."""
        return self._values * 2 if self.is_double() else self._values