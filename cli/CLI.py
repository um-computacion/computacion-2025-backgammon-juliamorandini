"""
Command Line Interface module for Backgammon game,
refactored for SOLID principles.
"""

from typing import Optional, Tuple, List
from core.BackgammonGame import Game


class BoardRenderer:
    """Handles only board display logic."""

    def render_board(self, game: Game) -> str:
        """Create a string representation of the current board state."""
        lines = []
        lines.append("\nCurrent Board:")
        # Note: These labels from the original code are for the bottom row
        lines.append("Points:  12 11 10  9  8  7    6  5  4  3  2  1")
        lines.append("       +------------------+------------------+")

        # Top row (points 23 down to 12)
        top_row = "       "
        for i in range(23, 11, -1):
            count = len(game.board.points[i])
            if count:
                color = "W" if game.board.points[i][0] == "W" else "B"
                top_row += f"{color}{count:2} "
            else:
                top_row += " .  "
        lines.append(top_row)

        # Bottom row (points 0 up to 11)
        bottom_row = "       "
        for i in range(0, 12):
            count = len(game.board.points[i])
            if count:
                color = "W" if game.board.points[i][0] == "W" else "B"
                bottom_row += f"{color}{count:2} "
            else:
                bottom_row += " .  "
        lines.append(bottom_row)
        lines.append("")  # Newline from original code

        # Bar and Borne off
        lines.append(f"Bar - White: {game.board.bar['W']} Black: {game.board.bar['B']}")
        lines.append(
            f"Borne Off - White: {game.board.borne_off['W']} Black: {game.board.borne_off['B']}"
        )

        return "\n".join(lines)


class UserInterface:
    """Handles only user input and output."""

    def display_message(self, message: str) -> None:
        """Prints a message to the console."""
        print(message)

    def get_input(self, prompt: str) -> str:
        """Gets user input from the console."""
        return input(prompt)

    def display_welcome(self) -> None:
        """Prints the welcome message."""
        self.display_message("Welcome to Backgammon!")

    def display_help(self) -> None:
        """Prints the help text."""
        self.display_message(
            """
Commands:
- move <from> <to>: Move a checker (e.g., 'move 5 1')
- roll: Roll the dice
- help: Show this help
- quit: Exit game
"""
        )

    def display_goodbye(self) -> None:
        """Prints the exit message."""
        self.display_message("Thanks for playing!")

    def display_turn(self, player: str) -> None:
        """Displays the current player's turn."""
        self.display_message(f"\nCurrent player: {player}")

    def display_roll(self, values: Tuple[int, int]) -> None:
        """Displays the dice roll results."""
        self.display_message(f"Rolled: {values}")

    def display_move_success(self) -> None:
        """Notifies user of a successful move."""
        self.display_message("Move successful!")

    def display_move_failure(self) -> None:
        """Notifies user of an invalid move."""
        self.display_message("Invalid move!")

    def display_winner(self, player: str) -> None:
        """Displays the game winner."""
        self.display_message(f"\n{player} wins!")

    def display_error(self, message: str) -> None:
        """Displays an error message."""
        self.display_message(f"Error: {message}")


class InputValidator:
    """Handles only input validation logic."""

    def validate_move(self, args: List[str]) -> Optional[Tuple[int, int]]:
        """
        Validates if the move arguments are two valid integers.

        Args:
            args: A list of strings from the user (e.g., ['5', '1']).

        Returns:
            A tuple of (from_point, to_point) as integers, or None if invalid.
        """
        if len(args) != 2:
            return None
        try:
            return (int(args[0]), int(args[1]))
        except ValueError:
            return None


class CommandParser:
    """Handles only command parsing and routing."""

    def __init__(self):
        self.known_commands = {"move", "roll", "help", "quit"}

    def parse_command(self, raw_input: str) -> Tuple[str, List[str]]:
        """
        Parses raw user input into a command and its arguments.

        Args:
            raw_input: The raw string from the user.

        Returns:
            A tuple of (command, args_list).
            Returns ('unknown', []) if the command is not recognized.
        """
        parts = raw_input.lower().strip().split()
        if not parts:
            return "unknown", []

        command = parts[0]
        args = parts[1:]

        if command in self.known_commands:
            return command, args
        else:
            return "unknown", []


class BackgammonCLI:
    """
    Acts as a coordinator, delegating to specialized classes.
    Manages the main game loop and application state.
    """

    def __init__(self):
        """Initialize CLI with new game and specialized components."""
        self.game = Game()
        self.ui = UserInterface()
        self.renderer = BoardRenderer()
        self.parser = CommandParser()
        self.validator = InputValidator()
        self.is_running = True

    def run(self) -> None:
        """Main game loop."""
        self.ui.display_welcome()
        self.ui.display_help()

        while self.is_running:
            # Display current state
            board_string = self.renderer.render_board(self.game)
            self.ui.display_message(board_string)
            self.ui.display_turn(self.game.current_player)

            # Get and process command
            command_raw = self.ui.get_input("\nEnter command: ")
            self.process_input(command_raw)

            # Check for winner
            winner = self.game.check_winner()
            if winner:
                self.ui.display_winner(winner)
                self.is_running = False

    def process_input(self, command_raw: str) -> None:
        """
        Parse and route the user's command to the correct handler.
        """
        command, args = self.parser.parse_command(command_raw)

        if command == "move":
            self.handle_move(args)
        elif command == "roll":
            self.handle_roll()
        elif command == "help":
            self.ui.display_help()
        elif command == "quit":
            self.handle_quit()
        else:
            self.ui.display_error("Unknown command. Type 'help' for commands.")

    def handle_move(self, args: List[str]) -> None:
        """Handle move command."""
        move_points = self.validator.validate_move(args)
        if not move_points:
            self.ui.display_error("Invalid move format. Use: move <from> <to>")
            return

        from_point, to_point = move_points
        if self.game.make_move(from_point, to_point):
            self.ui.display_move_success()
        else:
            self.ui.display_move_failure()

    def handle_roll(self) -> None:
        """Handle roll command."""
        # Note: Game logic should ideally check if a roll is allowed
        values = self.game.dice.roll()
        self.ui.display_roll(values)

    def handle_quit(self) -> None:
        """Exit the game."""
        self.is_running = False
        self.ui.display_goodbye()


if __name__ == "__main__":
    cli = BackgammonCLI()
    cli.run()
