"""Command Line Interface module for Backgammon game."""

from typing import Optional, Tuple, Dict, Any, Callable
from core.BackgammonGame import Game


class BackgammonCLI:
    """Command Line Interface for Backgammon game."""

    def __init__(self):
        """Initialize CLI with new game."""
        self.game = Game()
        self.is_running = True
        self.commands: Dict[str, Any] = {
            "move": self.handle_move,
            "roll": self.handle_roll,
            "help": self.show_help,
            "quit": self.quit_game,
        }

    def display_board(self) -> None:
        """Display current board state."""
        print("\nCurrent Board:")
        print("Points:  12 11 10  9  8  7    6  5  4  3  2  1")
        print("      +------------------+------------------+")

        # Display top row (points 13-24)
        print("      ", end="")
        for i in range(23, 11, -1):
            count = len(self.game.board.points[i])
            if count:
                color = "W" if self.game.board.points[i][0] == "W" else "B"
                print(f"{color}{count:2}", end=" ")
            else:
                print(" . ", end=" ")
        print()

        # Display bottom row (points 1-12)
        print("      ", end="")
        for i in range(0, 12):
            count = len(self.game.board.points[i])
            if count:
                color = "W" if self.game.board.points[i][0] == "W" else "B"
                print(f"{color}{count:2}", end=" ")
            else:
                print(" . ", end=" ")
        print("\n")

        # Display bar pieces
        print(f"Bar - White: {self.game.board.bar['W']} Black: {self.game.board.bar['B']}")
        print(f"Borne Off - White: {self.game.board.borne_off['W']} Black: {self.game.board.borne_off['B']}")

    def get_move_input(self) -> Optional[Tuple[int, int]]:
        """Get move input from user.

        Returns:
            Optional[Tuple[int, int]]: From and to points, or None if invalid
        """
        try:
            move = input("Enter move (from to): ").split()
            if len(move) != 2:
                print("Invalid input. Please enter two numbers.")
                return None
            return (int(move[0]), int(move[1]))
        except ValueError:
            print("Invalid input. Please enter numbers.")
            return None

    def show_help(self) -> None:
        """Display help text."""
        print("""
        Commands:
        - move <from> <to>: Move a checker
        - roll: Roll the dice
        - help: Show this help
        - quit: Exit game
        """)

    def quit_game(self) -> None:
        """Exit the game."""
        self.is_running = False
        print("Thanks for playing!")

    def handle_move(self) -> None:
        """Handle move command."""
        move = self.get_move_input()
        if move:
            from_point, to_point = move
            if self.game.make_move(from_point, to_point):
                print("Move successful!")
            else:
                print("Invalid move!")

    def handle_roll(self) -> None:
        """Handle roll command."""
        values = self.game.dice.roll()
        print(f"Rolled: {values}")

    def process_command(self, command: str) -> None:
        """Process user command.
        
        Args:
            command: Command to process
        """
        command = command.lower().strip()
        if command in self.commands:
            self.commands[command]()
        else:
            print("Unknown command. Type 'help' for commands.")

    def run(self) -> None:
        """Main game loop."""
        print("Welcome to Backgammon!")
        self.show_help()

        while self.is_running:
            self.display_board()
            print(f"\nCurrent player: {self.game.current_player}")
            command = input("\nEnter command: ")
            self.process_command(command)

            if self.game.check_winner():
                print(f"\n{self.game.current_player} wins!")
                self.is_running = False


if __name__ == "__main__":
    cli = BackgammonCLI()
    cli.run()


# python -m core.cli
