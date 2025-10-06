"""Command Line Interface module for Backgammon game."""

from typing import Optional, Tuple
from core.BackgammonGame import Game
from abc import ABC, abstractmethod


class CommandInterface(ABC):
    """Interface for CLI commands following Interface Segregation Principle."""
    
    @abstractmethod
    def execute(self, *args):
        """Execute the command."""
        pass


class MoveCommand(CommandInterface):
    """Command for moving pieces."""
    
    def execute(self, game: Game, from_point: int, to_point: int) -> bool:
        """Execute move command.
        
        Args:
            game: Game instance
            from_point: Starting point
            to_point: Target point
            
        Returns:
            bool: True if move was successful
        """
        return game.make_move(from_point, to_point)


class RollCommand(CommandInterface):
    """Command for rolling dice."""
    
    def execute(self, game: Game) -> Tuple[int, int]:
        """Execute roll command.
        
        Args:
            game: Game instance
            
        Returns:
            Tuple[int, int]: Dice values
        """
        return game.dice.roll()


class BackgammonCLI:
    """Command Line Interface for Backgammon game."""

    def __init__(self):
        """Initialize CLI with new game."""
        self.game = Game()
        self.commands = {
            'move': MoveCommand(),
            'roll': RollCommand(),
            'help': self.show_help,
            'quit': self.quit_game
        }
        self.is_running = True

    def display_board(self) -> None:
        """Display current board state."""
        board = self.game.get_board()
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

    def run(self) -> None:
        """Main game loop."""
        print("Welcome to Backgammon!")
        self.show_help()
        
        while self.is_running:
            self.display_board()
            print(f"\nCurrent player: {self.game.current_player}")
            
            command = input("\nEnter command: ").lower().strip()
            
            if command == "quit":
                self.commands["quit"]()
            elif command == "help":
                self.commands["help"]()
            elif command == "roll":
                values = self.commands["roll"].execute(self.game)
                print(f"Rolled: {values}")
            elif command == "move":
                move = self.get_move_input()
                if move:
                    from_point, to_point = move
                    if self.commands["move"].execute(self.game, from_point, to_point):
                        print("Move successful!")
                    else:
                        print("Invalid move!")
            else:
                print("Unknown command. Type 'help' for commands.")

            if self.game.check_winner():
                print(f"\n{self.game.current_player} wins!")
                self.is_running = False


if __name__ == "__main__":
    cli = BackgammonCLI()
    cli.run()


#python -m core.cli