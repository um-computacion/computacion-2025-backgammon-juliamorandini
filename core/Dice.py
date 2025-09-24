from typing import Tuple, List, Optional
import random

class Dice:
    """Simple dice class for Backgammon."""

    def __init__(self):
        """Initialize with two dice set to 1."""
        self._die1 = 1
        self._die2 = 1
        self._mock_values: Optional[List[Tuple[int, int]]] = None
        self._mock_index = 0

    def roll(self) -> Tuple[int, int]:
        """Roll both dice or return next mock value if set."""
        if self._mock_values and self._mock_index < len(self._mock_values):
            self.die1, self.die2 = self._mock_values[self._mock_index]
            self._mock_index += 1
        else:
            self.die1 = random.randint(1, 6)
            self.die2 = random.randint(1, 6)
        return self.get_values()

    def get_values(self) -> Tuple[int, int]:
        """Get current dice values."""
        return (self.die1, self.die2)

    def is_double(self) -> bool:
        """Check if dice show same value."""
        return self.die1 == self.die2

    def get_moves(self) -> List[int]:
        """Get available moves based on dice values."""
        if self.is_double():
            return [self.die1] * 4
        return [self.die1, self.die2]

    @property
    def die1(self) -> int:
        """Get value of first die."""
        return self._die1

    @die1.setter
    def die1(self, value: int) -> None:
        """Set value of first die with validation."""
        if not isinstance(value, int):
            raise TypeError("Die value must be an integer")
        if not 1 <= value <= 6:
            raise ValueError("Die value must be between 1 and 6")
        self._die1 = value

    @property
    def die2(self) -> int:
        """Get value of second die."""
        return self._die2

    @die2.setter
    def die2(self, value: int) -> None:
        """Set value of second die with validation."""
        if not isinstance(value, int):
            raise TypeError("Die value must be an integer")
        if not 1 <= value <= 6:
            raise ValueError("Die value must be between 1 and 6")
        self._die2 = value

    def set_mock_rolls(self, values: Optional[List[Tuple[int, int]]]) -> None:
        """Set predetermined roll values for testing.
        
        Args:
            values: List of tuples containing dice values
            
        Raises:
            ValueError: If values is None, empty, or contains invalid dice values
        """
        if values is None:
            raise ValueError("Mock values cannot be None")
        if not values:
            raise ValueError("Mock values list cannot be empty")
            
        for value in values:
            if not isinstance(value, tuple) or len(value) != 2:
                raise ValueError("Mock values must be tuples of length 2")
            v1, v2 = value
            if not (1 <= v1 <= 6 and 1 <= v2 <= 6):
                raise ValueError("Die values must be between 1 and 6")
                
        self._mock_values = values
        self._mock_index = 0

    def clear_mock(self) -> None:
        """Clear mock values and return to random rolling."""
        self._mock_values = None
        self._mock_index = 0

    def reset(self) -> None:
        """Reset dice to initial state."""
        self.die1 = 1
        self.die2 = 1
        self.clear_mock()