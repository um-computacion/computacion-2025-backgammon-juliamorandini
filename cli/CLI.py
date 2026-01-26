"""
Command Line Interface module for Backgammon game,
refactored for SOLID principles with proper game flow.
"""

from typing import Optional, Tuple, List, Union
from core.BackgammonGame import Game


class BoardRenderer:
    """Handles only board display logic."""

    def render_board(self, game: Game) -> str:
        """Create a string representation of the current board state."""
        lines = []
        lines.append("\nCurrent Board:")
        lines.append("Points:  13 14 15 16 17 18   19 20 21 22 23 24")
        lines.append("       +------------------+------------------+")

        # Top row (points 12 to 23)
        top_row = "       "
        for i in range(12, 24):
            count = len(game.board.points[i])
            if count:
                color = "W" if game.board.points[i][0] == "W" else "B"
                top_row += f"{color}{count:2} "
            else:
                top_row += " .  "
            if i == 17:  # Add bar separator
                top_row += " "
        lines.append(top_row)

        # Bottom row (points 11 down to 0)
        bottom_row = "       "
        for i in range(11, -1, -1):
            count = len(game.board.points[i])
            if count:
                color = "W" if game.board.points[i][0] == "W" else "B"
                bottom_row += f"{color}{count:2} "
            else:
                bottom_row += " .  "
            if i == 6:  # Add bar separator
                bottom_row += " "
        lines.append(bottom_row)
        lines.append("       +------------------+------------------+")
        lines.append("Points:  12 11 10  9  8  7    6  5  4  3  2  1")

        # Bar and Borne off
        lines.append(
            f"\nBar - White: {game.board.bar['W']} Black: {game.board.bar['B']}"
        )
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
        self.display_message("=" * 50)
        self.display_message("Welcome to Backgammon!")
        self.display_message("=" * 50)

    def display_help(self) -> None:
        """Prints the help text."""
        self.display_message(
            """
Commands:
- roll: Roll the dice to start your turn
- move <from> <to>: Move a checker (e.g., 'move 24 20')
  * Use 'bar' for moving from the bar (e.g., 'move bar 20')
  * Use 'off' to bear off (e.g., 'move 3 off')
- skip: Skip turn if no moves available
- help: Show this help
- quit: Exit game

Game Rules:
- White moves from 24→1 (counterclockwise)
- Black moves from 1→24 (clockwise)
- You must roll before making moves
- Use all dice rolls if possible
- If you have pieces on the bar, you must enter them first
"""
        )

    def display_goodbye(self) -> None:
        """Prints the exit message."""
        self.display_message("\nThanks for playing!")

    def display_turn(self, player: str) -> None:
        """Displays the current player's turn."""
        color = "●" if player == "black" else "○"
        self.display_message(f"\n{'=' * 50}")
        self.display_message(f"{color} Current player: {player.upper()}")
        self.display_message(f"{'=' * 50}")

    def display_roll(self, values: Union[List[int], Tuple[int, ...]]) -> None:
        """Displays the dice roll results."""
        if len(values) == 2:
            self.display_message(f"\n🎲 Rolled: {values[0]} and {values[1]}")
        else:
            # Doubles
            self.display_message(
                f"\n🎲 Rolled DOUBLES: {values[0]} and {values[0]} (4 moves!)"
            )
        self.display_message(f"📋 Available moves: {list(values)}")

    def display_move_success(self, from_point: str, to_point: str) -> None:
        """Notifies user of a successful move."""
        self.display_message(f"✓ Moved from {from_point} to {to_point}")

    def display_move_failure(self, reason: str = "Invalid move") -> None:
        """Notifies user of an invalid move."""
        self.display_message(f"✗ {reason}")

    def display_winner(self, player: str) -> None:
        """Displays the game winner."""
        self.display_message("\n" + "=" * 50)
        self.display_message(f"🎉 {player.upper()} WINS! 🎉")
        self.display_message("=" * 50)

    def display_error(self, message: str) -> None:
        """Displays an error message."""
        self.display_message(f"⚠ Error: {message}")

    def display_must_roll(self) -> None:
        """Reminds player to roll first."""
        self.display_message("⚠ You must roll the dice first! Type 'roll'")

    def display_remaining_dice(self, remaining: List[int]) -> None:
        """Display remaining dice."""
        if remaining:
            self.display_message(f"📋 Remaining moves: {remaining}")
        else:
            self.display_message("✓ All dice used! Turn complete.")

    def display_must_move_from_bar(self) -> None:
        """Notify that player must move from bar."""
        self.display_message("⚠ You have pieces on the bar! You must enter them first.")
        self.display_message("   Use: move bar <point>")


class InputValidator:
    """Handles only input validation logic."""

    def parse_point(self, point_str: str) -> Optional[int]:
        """
        Convert point string to integer.
        Special cases: 'bar' -> -1, 'off' -> -1
        """
        point_str = point_str.lower()
        if point_str == "bar":
            return -1
        if point_str == "off":
            return -1
        try:
            point = int(point_str)
            if 0 <= point <= 24:
                return point
            return None
        except ValueError:
            return None

    def validate_move(self, args: List[str]) -> Optional[Tuple[int, int]]:
        """
        Validates if the move arguments are valid.
        Returns:
            A tuple of (from_point, to_point) as integers, or None if invalid.
        """
        if len(args) != 2:
            return None

        from_p = self.parse_point(args[0])
        to_p = self.parse_point(args[1])

        if from_p is None or to_p is None:
            return None

        return (from_p, to_p)


class CommandParser:
    """Handles only command parsing and routing."""

    def __init__(self):
        self.known_commands = {"move", "roll", "help", "quit", "skip"}

    def parse_command(self, raw_input: str) -> Tuple[str, List[str]]:
        """
        Parses raw user input into a command and its arguments.
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


class GameStateManager:
    """Manages game state and turn logic."""

    def __init__(self, game: Game):
        self.game = game
        self.has_rolled = False
        self.remaining_dice = []
        self.original_roll = []

    def set_roll(self, values: Union[List[int], Tuple[int, ...]]) -> None:
        """Sets the dice roll values for the turn."""
        values_list = list(values)
        self.original_roll = values_list.copy()
        self.remaining_dice = values_list.copy()
        self.has_rolled = True

    def can_move(self) -> bool:
        """Check if player can make a move."""
        return self.has_rolled and len(self.remaining_dice) > 0

    def use_die(self, value: int) -> bool:
        """Remove a die value from remaining dice."""
        if value in self.remaining_dice:
            self.remaining_dice.remove(value)
            return True
        return False

    def end_turn(self):
        """End current turn and switch players."""
        self.has_rolled = False
        self.remaining_dice = []
        self.original_roll = []
        self.game.switch_player()

    def get_remaining(self) -> List[int]:
        """Get remaining dice values."""
        return self.remaining_dice.copy()


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
        self.state_manager = GameStateManager(self.game)
        self.is_running = True

    def run(self) -> None:
        """Main game loop."""
        self.ui.display_welcome()
        self.ui.display_help()

        while self.is_running:
            board_string = self.renderer.render_board(self.game)
            self.ui.display_message(board_string)
            self.ui.display_turn(self.game.current_player)

            if self.game.check_winner():
                self.ui.display_winner(self.game.current_player)
                self.is_running = False
                break

            command_raw = self.ui.get_input("\n> ")
            self.process_input(command_raw)

    def process_input(self, command_raw: str) -> None:
        """
        Parse and route the user's command to the correct handler.
        """
        command, args = self.parser.parse_command(command_raw)

        if command == "move":
            self.handle_move(args)
        elif command == "roll":
            self.handle_roll()
        elif command == "skip":
            self.handle_skip()
        elif command == "help":
            self.ui.display_help()
        elif command == "quit":
            self.handle_quit()
        else:
            self.ui.display_error("Unknown command. Type 'help' for commands.")

    def handle_move(self, args: List[str]) -> None:
        """Handle move command."""
        if not self.state_manager.has_rolled:
            self.ui.display_must_roll()
            return

        if not self.state_manager.remaining_dice:
            self.ui.display_error("No dice remaining. Type 'skip' to end turn.")
            return

        from_str = args[0].lower() if args else "?"
        to_str = args[1].lower() if len(args) > 1 else "?"

        move_points_ints = self.validator.validate_move(args)
        if not move_points_ints:
            self.ui.display_error("Invalid move format. Use: move <from> <to>")
            return

        from_point, to_point = move_points_ints

        if from_point == -1:
            if not self.game.must_move_from_bar():
                self.ui.display_move_failure("No pieces on the bar")
                return

            if to_point == -1:
                self.ui.display_error("Invalid point for entering from bar")
                return

            color = self.game.get_current_player_color()
            if color == "W":
                required_die = 25 - to_point
            else:
                required_die = to_point + 1

            if required_die not in self.state_manager.remaining_dice:
                self.ui.display_move_failure(
                    f"No die with value {required_die} to enter at point {to_point}"
                )
                return

            if self.game.make_bar_move(to_point):
                self.state_manager.use_die(required_die)
                self.ui.display_move_success(from_str, to_str)
                self.ui.display_remaining_dice(self.state_manager.get_remaining())

                if not self.state_manager.remaining_dice:
                    self.state_manager.end_turn()
            else:
                self.ui.display_move_failure(
                    "Cannot enter at that point (occupied by opponent)"
                )
            return

        if to_point == -1:
            if from_point == -1:
                self.ui.display_error("Invalid move")
                return

            if not self.game.can_bear_off():
                self.ui.display_move_failure(
                    "You cannot bear off yet (not all pieces in home board)"
                )
                return

            color = self.game.get_current_player_color()
            if color == "W":
                required_die = from_point
            else:
                required_die = 25 - from_point

            if required_die not in self.state_manager.remaining_dice:
                self.ui.display_move_failure(f"No die with value {required_die}")
                return

            if self.game.bear_off(from_point):
                self.state_manager.use_die(required_die)
                self.ui.display_move_success(from_str, to_str)
                self.ui.display_remaining_dice(self.state_manager.get_remaining())

                if not self.state_manager.remaining_dice:
                    self.state_manager.end_turn()
            else:
                self.ui.display_move_failure("Cannot bear off from that point")
            return

        if self.game.must_move_from_bar():
            self.ui.display_must_move_from_bar()
            return

        distance = abs(from_point - to_point)

        if distance not in self.state_manager.remaining_dice:
            self.ui.display_move_failure(
                f"No die with value {distance}. Available: {self.state_manager.remaining_dice}"
            )
            return

        if self.game.make_move(from_point, to_point):
            self.state_manager.use_die(distance)
            self.ui.display_move_success(from_str, to_str)
            self.ui.display_remaining_dice(self.state_manager.get_remaining())

            if not self.state_manager.remaining_dice:
                self.state_manager.end_turn()
        else:
            self.ui.display_move_failure("Invalid move!")

    def handle_roll(self) -> None:
        """Handle roll command."""
        if self.state_manager.has_rolled:
            self.ui.display_error(
                "You've already rolled! Make your moves or type 'skip' to end turn."
            )
            return

        values_tuple = self.game.dice.roll()

        self.state_manager.set_roll(values_tuple)
        self.ui.display_roll(values_tuple)

    def handle_skip(self) -> None:
        """Handle skip turn command."""
        if not self.state_manager.has_rolled:
            self.ui.display_error("You must roll first before skipping!")
            return

        remaining = self.state_manager.get_remaining()
        if remaining:
            self.ui.display_message(
                f"Skipping turn with {len(remaining)} unused dice: {remaining}"
            )

        self.state_manager.end_turn()
        self.ui.display_message("Turn ended. Next player's turn.")

    def handle_quit(self) -> None:
        """Exit the game."""
        self.is_running = False
        self.ui.display_goodbye()


if __name__ == "__main__":
    cli = BackgammonCLI()
    cli.run()
