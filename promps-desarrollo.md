observacion general: tiendo a dejar todos los comentarios y explicacion que el modelo escribe. Aunque se vea mas "sucio" el codigo siento que es util para poder enternder lo que se hace en esa fucnion es especifico
model: github copilot con claude sonnet 3.5

promp: 
haz la clase dice basandote en los test de la clase, respetando un 90% de coverage
respuesta: 
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


promp: haz la clase player basandote en los test de la clase, respetando un 90% de coverage, de forma simple y concisa
observacion: el codigo que escribia era muy complejo y dificil de enternder x lo que tuve que pedir que se simplificara 
respuesta: 
class Player:
    """A player in the Backgammon game."""

    def __init__(self, name: str, color: str) -> None:
        """Initialize a player with name and color.
        
        Args:
            name: Player's name
            color: Player's color ('white' or 'black')
        """
        if color not in ['white', 'black']:
            raise ValueError("Color must be 'white' or 'black'")
        
        self.name = name
        self.color = color
        self.pieces_in_home = 0
        self.pieces_on_bar = 0
        self.pieces_removed = 0
        self.current_position = 0
        self.pieces_at_point = 0

    def is_valid_move(self, dice_roll: int) -> bool:
        """Check if a move is valid based on dice roll."""
        new_position = self.current_position + dice_roll
        return 0 <= new_position <= 23

    def can_hit_opponent(self, opponent) -> bool:
        """Check if can hit opponent's single piece."""
        return (opponent.current_position == self.current_position and 
                opponent.pieces_at_point == 1)

    def can_bear_off(self) -> bool:
        """Check if player can start bearing off pieces."""
        return self.pieces_in_home == 15

    def is_point_blocked(self, point: int, opponent) -> bool:
        """Check if point is blocked by opponent."""
        return (opponent.pieces_at_point >= 2 and 
                opponent.current_position == point)

    def has_won(self) -> bool:
        """Check if player has won."""
        return self.pieces_removed == 15

    def can_reenter_from_bar(self, entry_point: int) -> bool:
        """Check if piece can reenter from bar."""
        return self.pieces_on_bar > 0 and 0 <= entry_point <= 23




promp:
haz la clase checker basandote en los test de la clase, respetando un 90% de coverage, de forma simple y concisa
respuesta:
class Checker:
    """A checker piece in Backgammon."""

    def __init__(self, color: str, position: int) -> None:
        """Create a new checker.
        
        Args:
            color: 'white' or 'black'
            position: Starting position (0-23)
        """
        if color not in ['white', 'black']:
            raise ValueError("Color must be 'white' or 'black'")

        self.color = color
        self.position = position
        self.is_on_bar = False
        self.is_borne_off = False

    def move_to(self, new_position: int) -> bool:
        """Move checker to a new position."""
        if 0 <= new_position <= 23:
            self.position = new_position
            return True
        return False

    def send_to_bar(self) -> None:
        """Send checker to the bar."""
        self.position = 'bar'
        self.is_on_bar = True

    def bear_off(self) -> None:
        """Bear off (remove) the checker from board."""
        self.position = 'off'
        self.is_borne_off = True

    def can_bear_off(self, all_home: bool) -> bool:
        """Check if checker can be borne off."""
        if not all_home:
            return False
            
        if not isinstance(self.position, int):
            return False

        if self.color == 'white':
            return self.position >= 18
        return self.position <= 5


pregunta: haz la clase board basandote en los test de la clase, respetando un 90% de coverage, de forma simple y concisa
respuesta:
class Board:
    """A Backgammon board."""

    def __init__(self):
        """Initialize empty board."""
        self.points = [0] * 24  # 24 points (positive for white, negative for black)
        self.bar = {'white': 0, 'black': 0}
        self.borne_off = {'white': 0, 'black': 0}
        self.reset()

    def reset(self):
        """Reset board to starting position."""
        self.points = [0] * 24
        # Set starting pieces
        self.points[0] = -2  # Black pieces
        self.points[5] = 5   # White pieces
        self.points[7] = 3   # White pieces
        self.points[11] = 5  # White pieces
        self.points[12] = -5 # Black pieces
        self.points[16] = -3 # Black pieces
        self.points[18] = -5 # Black pieces
        self.points[23] = 2  # White pieces
        self.bar = {'white': 0, 'black': 0}
        self.borne_off = {'white': 0, 'black': 0}

    def move_checker(self, from_point: int, to_point: int, color: str) -> bool:
        """Move a checker if valid."""
        # Check if move is valid
        if not (0 <= from_point < 24 and 0 <= to_point < 24):
            return False
        if self.bar[color] > 0:
            return False
        if color == 'white' and self.points[from_point] <= 0:
            return False
        if color == 'black' and self.points[from_point] >= 0:
            return False
        if color == 'white' and self.points[to_point] < -1:
            return False
        if color == 'black' and self.points[to_point] > 1:
            return False

        # Handle hits
        sign = 1 if color == 'white' else -1
        if (color == 'white' and self.points[to_point] == -1) or \
           (color == 'black' and self.points[to_point] == 1):
            self.points[to_point] = 0
            self.bar['black' if color == 'white' else 'white'] += 1

        # Move piece
        self.points[from_point] -= sign
        self.points[to_point] += sign
        return True

    def bear_off(self, point: int, color: str) -> bool:
        """Remove piece from board if allowed."""
        # Check if bearing off is allowed
        start = 18 if color == 'white' else 0
        end = 24 if color == 'white' else 6
        
        # All pieces must be in home board
        for i in range(24):
            if color == 'white' and i < 18 and self.points[i] > 0:
                return False
            if color == 'black' and i > 5 and self.points[i] < 0:
                return False

        # Remove piece
        if color == 'white' and self.points[point] > 0:
            self.points[point] -= 1
            self.borne_off['white'] += 1
            return True
        if color == 'black' and self.points[point] < 0:
            self.points[point] += 1  
            self.borne_off['black'] += 1
            return True
            
        return False


promp: haz la clase game basandote en los test de la clase, respetando un 90% de coverage, de forma simple y concisa y use las clases checker dice player y board
respuesta:
from core.board import Board
from core.player import Player
from core.Dice import Dice

class Game:
    """A Backgammon game."""

    def __init__(self):
        """Create new game with board, players and dice."""
        # Create game components
        self.board = Board()
        self.dice = Dice()
        self.players = {
            'white': Player("Player 1", "white"),
            'black': Player("Player 2", "black")
        }
        self.current_player = 'white'
        self.game_over = False

    def roll_dice(self):
        """Roll dice and return values."""
        return self.dice.roll()

    def move_checker(self, from_point: int, to_point: int) -> bool:
        """Move a checker if valid."""
        # Get current player
        player = self.players[self.current_player]
        
        # Check if move is valid
        if not player.is_valid_move(to_point - from_point):
            return False
            
        # Try to move checker
        if self.board.move_checker(from_point, to_point, self.current_player):
            return True
        return False

    def can_bear_off(self) -> bool:
        """Check if current player can bear off."""
        return self.board.can_bear_off(self.current_player)

    def bear_off(self, point: int) -> bool:
        """Try to bear off a checker."""
        if not self.can_bear_off():
            return False
        return self.board.bear_off(point, self.current_player)

    def switch_turn(self):
        """Switch to other player's turn."""
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def check_winner(self) -> str:
        """Check if there's a winner."""
        # Check if any player has won
        for color, player in self.players.items():
            if player.has_won():
                self.game_over = True
                return color
        return None

    def get_valid_moves(self, dice_values) -> list:
        """Get list of valid moves for current roll."""
        valid_moves = []
        
        # Check each possible move
        for die in dice_values:
            for from_point in range(24):
                to_point = from_point + die
                if to_point < 24:
                    if self.board.move_checker(from_point, to_point, self.current_player):
                        valid_moves.append((from_point, to_point))
                        # Undo move to keep checking
                        self.board.move_checker(to_point, from_point, self.current_player)
                        
        return valid_moves


promp: haz una clase cli para el juego backgammon basado en los test del cli
respuesta:
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

promp: want to create a backgammon board using Pygame. Please create the visual board layout based on this reference image. Here are the specific characteristics I need: Board Structure:

The board should be divided into two halves (left and right sides) separated by a central bar The board has a wooden texture background with a brown/orange color scheme There's a darker brown border/frame around the entire board

Triangular Points:

24 triangular points total (12 on each side of the board) Points alternate in color between two shades: a lighter tan/beige and a darker brown 6 points on the top of each half, 6 points on the bottom of each half The triangles should point inward (top triangles point down, bottom triangles point up) The triangles should be evenly spaced and properly sized

Central Bar:

A vertical green bar divides the board into left and right sections The bar has a wooden texture or pattern with brass-colored hinges (top and bottom) The bar should be proportional to the board size

Right Side Panel:

There's a panel on the far right side of the board This panel has a striped green/yellow diagonal pattern in its upper and lower sections The middle section matches the wooden board texture This appears to be the checker collection/bearing off area

Color Scheme:

Main board: Wood texture in orange/tan tones Dark border: Deep brown Alternating points: Light tan and dark brown Central bar: Green with brass hinges Right panel: Green/yellow diagonal stripes

Important: For now, do NOT include dice or checker pieces. I only want the empty board layout rendered properly use SOLID principies, modular files, Each class has a single responsibility , Easy to maintain and test.

can you help me do it step by step and in different comits, remembering that im a junior. can you also specify when i should make a new folder or file and where i should put all the things that you are givving me

promp: is there any way to make it so if someone want to put a checker out of range it can show a sign saying "out of range" instead of closing the program?
respuesta:
"""
Notification system for displaying messages to the player.
"""
import pygame
from config import Config


class Notification:
    """
    Displays temporary messages on screen.
    Shows errors, warnings, and info messages to the player.
    """
    
    def __init__(self):
        """Initialize the notification system."""
        self.messages = []  # List of (text, color, time_remaining)
        self.font = pygame.font.Font(None, 40)
        self.display_time = 3000  # 3 seconds in milliseconds
    
    def add_message(self, text, message_type="info"):
        """
        Add a new message to display.
        
        Args:
            text: Message text to display
            message_type: Type of message - "error", "warning", "info", "success"
        """
        # Choose color based on message type
        colors = {
            "error": (255, 50, 50),      # Red
            "warning": (255, 200, 50),   # Yellow
            "info": (100, 150, 255),     # Blue
            "success": (50, 255, 100)    # Green
        }
        
        color = colors.get(message_type, colors["info"])
        self.messages.append({
            "text": text,
            "color": color,
            "time": pygame.time.get_ticks(),
            "duration": self.display_time
        })
        
        # Keep only last 3 messages
        if len(self.messages) > 3:
            self.messages.pop(0)
    
    def update(self):
        """Update and remove expired messages."""
        current_time = pygame.time.get_ticks()
        self.messages = [
            msg for msg in self.messages
            if current_time - msg["time"] < msg["duration"]
        ]
    
    def draw(self, surface):
        """
        Draw all active messages on screen.
        
        Args:
            surface: Pygame surface to draw on
        """
        self.update()
        
        # Draw messages from top to bottom
        y_offset = 20
        for i, msg in enumerate(self.messages):
            # Calculate fade effect based on time remaining
            current_time = pygame.time.get_ticks()
            time_passed = current_time - msg["time"]
            time_remaining = msg["duration"] - time_passed
            
            # Fade out in last 500ms
            if time_remaining < 500:
                alpha = int(255 * (time_remaining / 500))
            else:
                alpha = 255
            
            # Render text with background
            text_surface = self.font.render(msg["text"], True, msg["color"])
            text_rect = text_surface.get_rect(center=(Config.SCREEN_WIDTH // 2, y_offset + i * 50))
            
            # Draw semi-transparent background
            bg_rect = text_rect.inflate(20, 10)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(min(200, alpha))
            bg_surface.fill((40, 40, 40))
            surface.blit(bg_surface, bg_rect)
            
            # Draw text
            text_surface.set_alpha(alpha)
            surface.blit(text_surface, text_rect)

y para pygame ui
"""
Main entry point for the Backgammon game.
This is the file you run to start the game.
"""
import pygame
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config
from pygame_ui.backgammon_board import BackgammonBoard
from pygame_ui.board_interaction import BoardInteraction
from pygame_ui.button import Button


def main():
    """Main game function with game loop."""
    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("Backgammon Game")
    clock = pygame.time.Clock()
    
    # Create game components
    backgammon_board = BackgammonBoard()
    board_interaction = BoardInteraction()
    
    # Create UI buttons
    roll_button = Button(50, 650, 150, 50, "Roll Dice", 
                        color=(70, 130, 180), 
                        hover_color=(100, 160, 210))
    reset_button = Button(220, 650, 150, 50, "Reset", 
                         color=(180, 70, 70), 
                         hover_color=(210, 100, 100))
    next_turn_button = Button(390, 650, 150, 50, "Next Turn", 
                             color=(70, 180, 70), 
                             hover_color=(100, 210, 100))
    
    # Game loop
    running = True
    selected_point = None  # Track which point is selected
    dice_rolled = False  # Track if dice have been rolled this turn
    moves_made = 0  # Track number of moves made this turn
    
    while running:
        # Poll for events
        for event in pygame.event.get():
            # pygame.QUIT event means the user clicked X to close window
            if event.type == pygame.QUIT:
                running = False
            
            # Handle ESC key to quit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                # Press SPACE to roll dice
                elif event.key == pygame.K_SPACE:
                    if not dice_rolled:
                        dice = backgammon_board.roll_dice()
                        dice_rolled = True
                        moves_made = 0
                        print(f"{backgammon_board.current_player} rolled: {dice}")
                    else:
                        print("Already rolled! Make your moves or press N for next turn")
                
                # Press N to end turn (next player)
                elif event.key == pygame.K_n:
                    backgammon_board.switch_player()
                    dice_rolled = False
                    moves_made = 0
                    selected_point = None
                    print(f"Turn ended. Now playing: {backgammon_board.current_player}")
                
                # Press R to reset board
                elif event.key == pygame.K_r:
                    backgammon_board.reset()
                    selected_point = None
                    dice_rolled = False
                    moves_made = 0
                    print("Board reset!")
            
            # Handle board interactions (clicks)
            interaction_result = board_interaction.handle_event(event)
            if interaction_result:
                if interaction_result['type'] == 'point_click':
                    point = interaction_result['point']
                    
                    # Must roll dice first
                    if not dice_rolled:
                        print("Roll dice first! (Press SPACE or click Roll Dice)")
                        continue
                    
                    # Check if all moves used
                    max_moves = 4 if backgammon_board.dice_values[0] == backgammon_board.dice_values[1] else 2
                    if moves_made >= max_moves:
                        print("All moves used! Press N to end turn")
                        continue
                    
                    print(f"Clicked on point {point}")
                    
                    # Simple move logic: select first, then move
                    if selected_point is None:
                        # First click - select a point (must have current player's pieces)
                        if backgammon_board.board.points[point] and \
                           backgammon_board.board.points[point][0] == backgammon_board.current_player:
                            selected_point = point
                            print(f"Selected point {point}")
                        else:
                            print(f"Point {point} has no {backgammon_board.current_player} pieces")
                    else:
                        # Second click - try to move
                        distance = abs(point - selected_point)
                        
                        # Check if distance matches one of the available dice
                        if distance in backgammon_board.dice_values:
                            success = backgammon_board.move_checker(selected_point, point)
                            if success:
                                print(f"Moved from {selected_point} to {point}")
                                # Remove used die
                                backgammon_board.dice_values.remove(distance)
                                moves_made += 1
                                
                                # Check if all moves used
                                if not backgammon_board.dice_values:
                                    print("All dice used! Press N to end turn")
                            else:
                                print(f"Invalid move from {selected_point} to {point}")
                        else:
                            print(f"Distance {distance} doesn't match dice: {backgammon_board.dice_values}")
                        
                        selected_point = None
            
            # Handle button clicks
            if roll_button.handle_event(event):
                if not dice_rolled:
                    dice = backgammon_board.roll_dice()
                    dice_rolled = True
                    moves_made = 0
                    print(f"{backgammon_board.current_player} rolled: {dice}")
                else:
                    print("Already rolled! Make your moves or press N for next turn")
            
            if reset_button.handle_event(event):
                backgammon_board.reset()
                selected_point = None
                dice_rolled = False
                moves_made = 0
                print("Board reset!")
            
            if next_turn_button.handle_event(event):
                backgammon_board.switch_player()
                dice_rolled = False
                moves_made = 0
                selected_point = None
                print(f"Turn ended. Now playing: {backgammon_board.current_player}")
        
        # Update game state
        backgammon_board.update()
        
        # Fill the screen with a color to wipe away anything from last frame
        screen.fill(Config.DARK_BROWN)
        
        # RENDER YOUR GAME HERE
        backgammon_board.render(screen)
        
        # Draw UI buttons
        roll_button.draw(screen)
        reset_button.draw(screen)
        next_turn_button.draw(screen)
        
        # Draw current player indicator
        font = pygame.font.Font(None, 36)
        player_color = "White" if backgammon_board.current_player == "W" else "Black"
        player_text = f"Current Player: {player_color}"
        text_surface = font.render(player_text, True, (255, 255, 255))
        screen.blit(text_surface, (600, 660))
        
        # Draw dice values if rolled
        if backgammon_board.dice_values:
            dice_text = f"Dice: {backgammon_board.dice_values}"
            dice_surface = font.render(dice_text, True, (255, 255, 255))
            screen.blit(dice_surface, (600, 700))
        else:
            if dice_rolled:
                all_used = font.render("All dice used!", True, (255, 255, 0))
                screen.blit(all_used, (600, 700))
        
        # Draw selected point indicator
        if selected_point is not None:
            selected_text = f"Selected: Point {selected_point}"
            selected_surface = font.render(selected_text, True, (255, 255, 0))
            screen.blit(selected_surface, (900, 660))
        
        # flip() the display to put your work on screen
        pygame.display.flip()
        
        # Limits FPS to 60
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()


comente en un commit que amenace a github copilot con claude sonnet 3.5 asi que quiero mostrar las promps que solucionaron un problemas de 2 dias y 4 commits

i will shoot you disconect your servers I AM NOT PLAYING CHECK ALL THE CODE AND SEE WHY IF I CLICK THE PART OF THE BUTTON THATS OUTSIDE THE BOARD IT WORKS AND THE INSIDE DOESNT

respuesta:
takes deep breath I see the critical issue now. The problem is in the BoardInteraction class that's handling clicks - it's intercepting clicks on the board area before they reach the buttons.

Let's fix this in two steps:

First, modify the BoardInteraction class:
Then fix the event handling in PygameUI.py:
The key fix is:

Check button clicks BEFORE board interaction
Skip board interaction if a button was clicked
Limit board interaction area to above the buttons
This should make the buttons work consistently regardless of where you click them.

observacion: tuve que cambiar demasiado el codigo el proceso de arreglar la hitbox de los botones y pase por un total de 4 IAs (githubcopilot con sonnet 3.5, claude 4.5, deepseek y gemini) y tuve que estar una tarde arreglando los botones y los carteles porque estaban mal(yo pensaba que estaba mal y queria poner que se podian tocar estas cosas en el teclado), tuve que hacer como 3 rondas de debug pero salio. todo esto lo comento porque me olvide de poner commits en el medio asi que no esta documentado la totalidad de la odisea que fue esto. 


promp:also can you take off that red and yellow box on the right and move the new boxes far far right (gemini pro 2.5)
respuesta:
import pygame
from typing import Optional, List, Tuple

from config import Config
from pygame_ui.backgammon_board import BackgammonBoard
from pygame_ui.button import Button
from pygame_ui.board_interaction import BoardInteraction

CheckerPos = Tuple[int, int, int, int, str]


def is_valid_direction(from_point: int, to_point: int, player: str) -> bool:
    """Checks if the move direction is valid for the player."""
    if player == "W":
        return to_point < from_point
    else:
        return to_point > from_point


def get_entry_point_for_dice(dice_value: int, player: str) -> int:
    """Get the entry point corresponding to a dice value.

    Args:
        dice_value: The dice value (1-6)
        player: 'W' for White or 'B' for Black

    Returns:
        The entry point (0-23)
    """
    if player == "W":
        # White enters at 24 - dice_value (1→23, 2→22, ..., 6→18)
        return 24 - dice_value
    else:
        # Black enters at dice_value - 1 (1→0, 2→1, ..., 6→5)
        return dice_value - 1


class Game:
    """
    Encapsulates the main game logic, state, and rendering.
    """

    def __init__(self):
        """Initializes the game, Pygame, and all game state variables."""
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode(
            (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Backgammon Game")
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.backgammon_board: BackgammonBoard = BackgammonBoard()
        self.board_interaction = BoardInteraction()

        # --- UI Elements ---
        self.roll_button: Button = Button(
            50, 730, 150, 50, "Roll Dice", color=(70, 130, 180), hover_color=(100, 160, 210)
        )
        self.reset_button: Button = Button(
            220, 730, 150, 50, "Reset", color=(180, 70, 70), hover_color=(210, 100, 100)
        )
        self.next_turn_button: Button = Button(
            390, 730, 150, 50, "Next Turn", color=(70, 180, 70), hover_color=(100, 210, 100)
        )
        self.font: pygame.font.Font = pygame.font.Font(None, 36)

        # --- Game State Variables ---
        self.selected_point: Optional[int] = None
        self.bar_selected: bool = False
        self.dice_rolled: bool = False
        self.moves_made: int = 0
        self.max_moves_this_turn: int = 0
        self.running: bool = True


        self.bear_off_area_width: int = 80 # Width of the bear-off area
        # Calculate x position to be on the far right, with a small margin
        self.bear_off_area_x: int = Config.SCREEN_WIDTH - self.bear_off_area_width - Config.BORDER_THICKNESS 
        
        # Black's Bear-Off Rect (Top-Right)
        self.bear_off_rect_b: pygame.Rect = pygame.Rect(
            self.bear_off_area_x, Config.BOARD_Y + Config.BORDER_THICKNESS, 
            self.bear_off_area_width, Config.BOARD_HEIGHT // 2 - Config.BORDER_THICKNESS * 1.5 
        )
        # White's Bear-Off Rect (Bottom-Right)
        self.bear_off_rect_w: pygame.Rect = pygame.Rect(
            self.bear_off_area_x, Config.BOARD_Y + Config.BOARD_HEIGHT // 2 + Config.BORDER_THICKNESS * 0.5, 
            self.bear_off_area_width, Config.BOARD_HEIGHT // 2 - Config.BORDER_THICKNESS * 1.5
        )

        self.checker_radius: int = Config.CHECKER_RADIUS
        self.checker_color_w: Tuple[int, int, int] = Config.WHITE_CHECKER
        self.checker_color_b: Tuple[int, int, int] = Config.BLACK_CHECKER
        self.checker_outline: Tuple[int, int, int] = Config.CHECKER_OUTLINE
        # Assuming a color from Config or just hardcoding
        self.bear_off_bg_color: Tuple[int, int, int] = Config.WOOD_BROWN # Use a board-like color


    def run(self):
        """Starts and runs the main game loop."""
        while self.running:
            # --- Event Handling ---
            for event in pygame.event.get():
                self.handle_event(event)

            # --- Game Logic Update ---
            self.update()

            # --- Rendering ---
            self.render()

            self.clock.tick(60)

        pygame.quit()

    def handle_event(self, event: pygame.event.Event):
        """Handles a single Pygame event."""
        if event.type == pygame.QUIT:
            self.running = False
            return

        if event.type == pygame.KEYDOWN:
            self.handle_keydown(event.key)
            return

        # --- Button Events ---
        if self.roll_button.handle_event(event):
            self.do_roll_dice()
            return

        if self.reset_button.handle_event(event):
            self.do_reset()
            return

        if self.next_turn_button.handle_event(event):
            self.do_next_turn()
            return

        # --- Mouse Click on Board ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_click(event.pos)
            return

    def handle_keydown(self, key: int):
        """Handles keyboard press events."""
        if key == pygame.K_ESCAPE:
            self.running = False
        elif key == pygame.K_SPACE:
            self.do_roll_dice()
        elif key == pygame.K_n:
            self.do_next_turn()
        elif key == pygame.K_r:
            self.do_reset()

    def do_roll_dice(self):
        """Action for rolling the dice."""
        if not self.dice_rolled:
            dice = self.backgammon_board.roll_dice()
            self.dice_rolled = True
            self.moves_made = 0
            self.max_moves_this_turn = 4 if len(dice) == 4 else 2
            print(f"{self.backgammon_board.current_player} rolled: {dice}")
        else:
            print("Already rolled! Make your moves or press N for next turn")

    def do_reset(self):
        """Action for resetting the game."""
        self.backgammon_board.reset()
        self.selected_point = None
        self.bar_selected = False
        self.dice_rolled = False
        self.moves_made = 0
        self.max_moves_this_turn = 0
        print("Board reset!")

    def do_next_turn(self):
        """Action for switching to the next turn."""
        self.backgammon_board.switch_player()
        self.dice_rolled = False
        self.moves_made = 0
        self.max_moves_this_turn = 0
        self.selected_point = None
        self.bar_selected = False
        print(f"Turn ended. Now playing: {self.backgammon_board.current_player}")

    def handle_mouse_click(self, mouse_pos: Tuple[int, int]):
        """Handles logic for all mouse clicks on the board/bar."""
        if not self.dice_rolled:
            print("Roll dice first!")
            return

        # CHECK IF PLAYER HAS PIECES ON BAR
        has_bar_pieces = (
            self.backgammon_board.board.bar[self.backgammon_board.current_player] > 0
        )

        if has_bar_pieces:
            self.handle_bar_move(mouse_pos)
        else:
            self.handle_normal_move(mouse_pos)

    def handle_bar_move(self, mouse_pos: Tuple[int, int]):
        """Handles a move attempt when the player has pieces on the bar."""
        # Check if clicking on bar area
        bar_x = Config.BAR_X
        bar_y_top = Config.BOARD_Y + Config.BORDER_THICKNESS
        bar_y_bottom = (
            Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
        )
        bar_width = Config.BAR_WIDTH

        if (
            bar_x <= mouse_pos[0] <= bar_x + bar_width
            and bar_y_top <= mouse_pos[1] <= bar_y_bottom
        ):
            # Clicked on bar
            self.bar_selected = True
            bar_pieces = self.backgammon_board.board.bar[
                self.backgammon_board.current_player
            ]
            print(f"\n✓ Selected checker from bar! ({bar_pieces} pieces on bar)")
            print(f"Valid entry points with current dice:")
            for dice_val in self.backgammon_board.dice_values:
                entry_pt = get_entry_point_for_dice(
                    dice_val, self.backgammon_board.current_player
                )
                print(f" 	Dice {dice_val} → Point {entry_pt}")
            return

        # Clicked on board (attempting to enter)
        clicked_point = self.board_interaction.get_clicked_point(mouse_pos)

        if clicked_point is not None:
            if not self.bar_selected:
                print("Click the BAR first to select a checker!")
                return

            # Get valid entry points
            valid_entry_points = {}
            for dice_val in self.backgammon_board.dice_values:
                entry_pt = get_entry_point_for_dice(
                    dice_val, self.backgammon_board.current_player
                )
                valid_entry_points[dice_val] = entry_pt

            # Check if clicked point is valid
            matching_dice = None
            for dice_val, entry_pt in valid_entry_points.items():
                if entry_pt == clicked_point:
                    matching_dice = dice_val
                    break

            if matching_dice is None:
                print(
                    f"Cannot enter at point {clicked_point}. Valid: {list(valid_entry_points.values())}"
                )
                return

            # Attempt to enter from bar
            if self.backgammon_board.board.move_checker_from_bar(
                clicked_point, self.backgammon_board.current_player
            ):
                print(
                    f"Entered from bar at point {clicked_point} using dice {matching_dice}"
                )
                self.backgammon_board.dice_values.remove(matching_dice)
                self.moves_made += 1
                self.bar_selected = False

                if (
                    self.moves_made >= self.max_moves_this_turn
                    or not self.backgammon_board.dice_values
                ):
                    print("✓ Turn complete!")
                    self.do_next_turn()
            else:
                print(f"Cannot enter at point {clicked_point} (blocked)")

    def handle_normal_move(self, mouse_pos: Tuple[int, int]):
        """Handles a move attempt when the player has no pieces on the bar."""
        clicked_point = self.board_interaction.get_clicked_point(mouse_pos)
        player = self.backgammon_board.current_player

        if self.selected_point is None:
            # --- Select a point ---
            if clicked_point is None:
                print("Clicked outside points.")
                return 
                
            point_pieces = self.backgammon_board.board.points[clicked_point]
            if (
                point_pieces
                and point_pieces[0] == player
            ):
                self.selected_point = clicked_point
                print(f"Selected point {clicked_point}")
            else:
                print(
                    f"No {player} pieces at point {clicked_point}"
                )
        else:
            # --- Move to destination ---
            is_bear_off_click = False
            distance = 0
            is_bearing_off = self.backgammon_board.board.can_bear_off(player)

            if clicked_point is not None:
                # Clicked on a point
                if clicked_point == self.selected_point:
                    self.selected_point = None
                    print("Point deselected")
                    return
                # This is a regular move, calculate distance
                distance = abs(clicked_point - self.selected_point)
            
            else:
                # Clicked off-point. Check if it's a valid bear-off click.
                if player == "W" and self.bear_off_rect_w.collidepoint(mouse_pos):
                    is_bear_off_click = True
                    distance = self.selected_point + 1 # e.g., point 0 -> distance 1
                elif player == "B" and self.bear_off_rect_b.collidepoint(mouse_pos):
                    is_bear_off_click = True
                    distance = 24 - self.selected_point # e.g., point 23 -> distance 1
                else:
                    # Clicked somewhere invalid (not a point, not correct bear-off)
                    print("Invalid destination click.")
                    self.selected_point = None # Deselect
                    return
            
            # --- Process the move (Bear off or Regular) ---

            if is_bearing_off and is_bear_off_click:
                # --- Handle Bear Off Attempt ---
                
                # Check if exact dice value exists
                if distance in self.backgammon_board.dice_values:
                    if self.backgammon_board.board.bear_off(player, self.selected_point):
                        print(f"Bore off from point {self.selected_point}!")
                        self.backgammon_board.dice_values.remove(distance)
                        self.moves_made += 1
                    else:
                        print("Cannot bear off from that point (logic error)!")
                
                # Check if a higher dice value can be used (if no exact match and this is the furthest checker)
                elif all(d > distance for d in self.backgammon_board.dice_values):
                        # Check if this is the furthest checker
                    is_furthest = True
                    if player == 'W':
                        for p in range(self.selected_point + 1, 6):
                            if self.backgammon_board.board.points[p] and self.backgammon_board.board.points[p][0] == 'W':
                                is_furthest = False
                                break
                    else: # Player 'B'
                        for p in range(self.selected_point - 1, 17, -1): # 17 is 18-1
                            if self.backgammon_board.board.points[p] and self.backgammon_board.board.points[p][0] == 'B':
                                is_furthest = False
                                break
                    
                    if is_furthest:
                        if self.backgammon_board.board.bear_off(player, self.selected_point):
                            print(f"Bore off from point {self.selected_point} (using higher dice)!")
                            # Use the smallest dice that is larger than the distance
                            used_dice = min(d for d in self.backgammon_board.dice_values if d > distance)
                            self.backgammon_board.dice_values.remove(used_dice)
                            self.moves_made += 1
                        else:
                            print("Cannot bear off from that point (logic error)!")
                    else:
                        print(f"No dice value matches for bearing off (must move furthest checker first)")

                else:
                    print(f"No dice value matches for bearing off ({distance})")
            
            elif clicked_point is None:
                # This was a bear-off click, but 'is_bearing_off' was False
                print("You cannot bear off yet (all pieces not in home).")

            # --- Handle Regular Move ---
            elif distance in self.backgammon_board.dice_values:
                if is_valid_direction(
                    self.selected_point,
                    clicked_point,
                    self.backgammon_board.current_player,
                ):
                    if self.backgammon_board.move_checker(
                        self.selected_point, clicked_point
                    ):
                        print(
                            f"Moved from {self.selected_point} to {clicked_point}"
                        )
                        self.backgammon_board.dice_values.remove(distance)
                        self.moves_made += 1
                    else:
                        print(f"Invalid move!")
                else:
                    print(
                        f"Wrong direction for {self.backgammon_board.current_player}"
                    )
            else:
                print(f"No dice value matches distance {distance}")

            # --- Reset selection and check for turn end ---
            self.selected_point = None
            if (
                self.moves_made >= self.max_moves_this_turn
                or not self.backgammon_board.dice_values
            ):
                # Check for win condition
                if self.backgammon_board.board.borne_off[player] == 15:
                    print(f"🎉 PLAYER {player} WINS! 🎉")
                    self.do_reset() # Reset board after win
                else:
                    print("Turn complete!")
                    self.do_next_turn()

    def update(self):
        """Updates game state logic (e.g., animations)."""
        self.backgammon_board.update()

    def render(self):
        """Draws the entire game screen."""
        self.screen.fill(Config.DARK_BROWN)

        # Draw board and pieces
        self.backgammon_board.render(self.screen)

        # --- REMOVED: Old right panel drawing (stripes) ---
        # No specific code was drawing a "red and yellow box" directly from config in the previous render.
        # It's likely an internal part of BackgammonBoard or BoardInteraction.
        # If there's still a striped area, it's coming from those files.
        # For now, I'm assuming the changes here will handle the visible elements.


        # Draw buttons
        self.roll_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        self.next_turn_button.draw(self.screen)

        # --- Draw Text Info ---
        player_color: str = (
            "White" if self.backgammon_board.current_player == "W" else "Black"
        )
        player_text: str = f"Current Player: {player_color}"
        text_surface: pygame.Surface = self.font.render(player_text, True, (255, 255, 255))
        self.screen.blit(text_surface, (self.bear_off_area_x, 660)) 

        # Display bar pieces if any
        bar_pieces = self.backgammon_board.board.bar[self.backgammon_board.current_player]
        if bar_pieces > 0:
            bar_text: str = f"On Bar: {bar_pieces}"
            bar_surface: pygame.Surface = self.font.render(bar_text, True, (255, 100, 100))
            self.screen.blit(bar_surface, (self.bear_off_area_x, 620))
        
        borne_off_w = self.backgammon_board.board.borne_off["W"]
        borne_off_b = self.backgammon_board.board.borne_off["B"]

        # Draw Black's container
        pygame.draw.rect(self.screen, self.bear_off_bg_color, self.bear_off_rect_b, 0, 8)
        pygame.draw.rect(self.screen, (255, 255, 255), self.bear_off_rect_b, 2, 8)
        
        # Draw White's container
        pygame.draw.rect(self.screen, self.bear_off_bg_color, self.bear_off_rect_w, 0, 8)
        pygame.draw.rect(self.screen, (255, 255, 255), self.bear_off_rect_w, 2, 8)

        # Draw Black's borne-off checkers (stacked from bottom up)
        for i in range(borne_off_b):
            x = self.bear_off_rect_b.centerx
            # Stack with a 1.5x overlap
            y = self.bear_off_rect_b.bottom - (i * self.checker_radius // 1.5) - self.checker_radius - 5
            if y < self.bear_off_rect_b.top + self.checker_radius: break # Stop if full
            pygame.draw.circle(self.screen, self.checker_color_b, (x, y), self.checker_radius)
            pygame.draw.circle(self.screen, self.checker_outline, (x, y), self.checker_radius, 2)

        # Draw White's borne-off checkers (stacked from top down)
        for i in range(borne_off_w):
            x = self.bear_off_rect_w.centerx
            y = self.bear_off_rect_w.top + (i * self.checker_radius // 1.5) + self.checker_radius + 5
            if y > self.bear_off_rect_w.bottom - self.checker_radius: break # Stop if full
            pygame.draw.circle(self.screen, self.checker_color_w, (x, y), self.checker_radius)
            pygame.draw.circle(self.screen, self.checker_outline, (x, y), self.checker_radius, 2)
        
        # Draw text labels for borne-off
        borne_off_text_w: str = f"White Off: {borne_off_w}"
        borne_off_text_b: str = f"Black Off: {borne_off_b}"
        borne_off_surf_w: pygame.Surface = self.font.render(borne_off_text_w, True, (200, 200, 200))
        borne_off_surf_b: pygame.Surface = self.font.render(borne_off_text_b, True, (200, 200, 200))
        # Place text relative to the new rects
        self.screen.blit(borne_off_surf_b, (self.bear_off_rect_b.x, self.bear_off_rect_b.y - 40))
        self.screen.blit(borne_off_surf_w, (self.bear_off_rect_w.x, self.bear_off_rect_w.y - 40))



        # Display dice info
        if self.backgammon_board.dice_values:
            dice_text: str = f"Dice: {self.backgammon_board.dice_values}"
            dice_surface: pygame.Surface = self.font.render(dice_text, True, (255, 255, 255))
            self.screen.blit(dice_surface, (self.bear_off_rect_w.x, 700)) # Moved text
        else:
            if self.dice_rolled:
                all_used: pygame.Surface = self.font.render(
                    "All dice used!", True, (255, 255, 0)
                )
                self.screen.blit(all_used, (self.bear_off_rect_w.x, 700)) # Moved text

        pygame.display.flip()


def main() -> None:
    """
    Main function to create and run the game.
    """
    game = Game()
    game.run()


if __name__ == "__main__":
    main()





promp: [pedi arreglos de cli porque no funcionaba], no tengo la promp exacta
respuesta
"""
Command Line Interface module for Backgammon game,
refactored for SOLID principles with proper game flow.
"""

from typing import Optional, Tuple, List
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
        # FIX 1: Match the test assertion exactly
        self.display_message("\nThanks for playing!")

    def display_turn(self, player: str) -> None:
        """Displays the current player's turn."""
        color = "●" if player == "black" else "○"
        self.display_message(f"\n{'=' * 50}")
        self.display_message(f"{color} Current player: {player.upper()}")
        self.display_message(f"{'=' * 50}")

    def display_roll(self, values: List[int]) -> None:
        """Displays the dice roll results."""
        if len(values) == 2:
            self.display_message(f"\n🎲 Rolled: {values[0]} and {values[1]}")
        else:
            # Doubles
            self.display_message(
                f"\n🎲 Rolled DOUBLES: {values[0]} and {values[0]} (4 moves!)"
            )
        self.display_message(f"📋 Available moves: {values}")

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
        
        # This was part of my previous fix, and it's correct.
        # The original code returned strings, but the tests need ints.
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
        
        # REMOVED HACK FROM HERE.
        # The hack in __init__ breaks the 'roll' tests.

    # FIX 2: Renamed 'start_turn' to 'set_roll'
    def set_roll(self, values: List[int]) -> None:
        """Sets the dice roll values for the turn."""
        self.original_roll = values.copy()
        self.remaining_dice = values.copy()
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
            # Display current state
            board_string = self.renderer.render_board(self.game)
            self.ui.display_message(board_string)
            self.ui.display_turn(self.game.current_player)

            # Check for winner first
            if self.game.check_winner():
                self.ui.display_winner(self.game.current_player)
                self.is_running = False
                break

            # Get and process command
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
        
        # This check is correct, but the tests fail it.
        if not self.state_manager.has_rolled:
            self.ui.display_must_roll()
            return

        if not self.state_manager.remaining_dice:
            self.ui.display_error("No dice remaining. Type 'skip' to end turn.")
            return

        # Keep original strings for UI messages
        from_str = args[0].lower() if args else "?"
        to_str = args[1].lower() if len(args) > 1 else "?"

        move_points_ints = self.validator.validate_move(args)
        if not move_points_ints:
            self.ui.display_error("Invalid move format. Use: move <from> <to>")
            return

        from_point, to_point = move_points_ints # These are ints (-1 for bar/off)

        # Handle bar move (from_point == -1)
        if from_point == -1:
            if not self.game.must_move_from_bar():
                self.ui.display_move_failure("No pieces on the bar")
                return

            if to_point == -1:  # "move bar off" - invalid
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

        # Handle bearing off (to_point == -1)
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

        # Normal move
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
            # This message needs to match the test
            self.ui.display_move_failure("Invalid move!") 

    # FIX 3: Refactored handle_roll
    def handle_roll(self) -> None:
        """Handle roll command."""
        if self.state_manager.has_rolled:
            self.ui.display_error(
                "You've already rolled! Make your moves or type 'skip' to end turn."
            )
            return

        # Call roll on self.game (which is the mock in tests)
        # The test expects game.dice.roll() and returns a tuple.
        values_tuple = self.game.dice.roll()
        values_list = list(values_tuple)

        # Pass the values to the state manager to update state
        self.state_manager.set_roll(values_list)
        self.ui.display_roll(values_list)

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


hecho otra vez:
"""Module containing the main Backgammon game logic."""

from core.board import Board
from core.player import Player
from core.Dice import Dice


class Game:
    """A Backgammon game."""

    def __init__(self):
        """Initialize game components."""
        self.board = Board()
        self.dice = Dice()
        self.current_player = "white"
        self.players = {
            "white": Player("Player 1", "white"),
            "black": Player("Player 2", "black"),
        }

    def get_board(self) -> list:
        """Get current board state as point counts."""
        board_state = []
        for point in self.board.points:
            if not point:
                board_state.append(0)
            else:
                count = len(point)
                if point[0] == "B":
                    board_state.append(-count)
                else:
                    board_state.append(count)
        return board_state

    def make_move(self, from_point: int, to_point: int) -> bool:
        """Make a move if valid."""
        color = "W" if self.current_player == "white" else "B"

        if self.board.bar[color] > 0:
            return False

        return self.board.move_checker(from_point, to_point, color)

    def make_bar_move(self, to_point: int) -> bool:
        """Move a checker from the bar to a valid entry point."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.move_checker_from_bar(to_point, color)

    def get_entry_point_for_dice(self, dice_value: int) -> int:
        """Get the entry point corresponding to a dice value."""
        color = "W" if self.current_player == "white" else "B"

        if color == "W":
            return 24 - dice_value
        else:
            return dice_value - 1

    def set_dice(self, values: list) -> None:
        """Set dice values for testing."""
        self.dice.die1 = values[0]
        self.dice.die2 = values[1]

    def get_available_moves(self) -> list:
        """Get available moves based on dice."""
        return self.dice.get_moves()

    def set_piece(self, point: int, count: int, color: str = None) -> None:
        """Set pieces at point for testing."""
        if color is None:
            color = "W" if self.current_player == "white" else "B"
        self.board.points[point] = [color] * abs(count)

    def add_to_bar(self, color: str = None) -> None:
        """Add current player's piece to bar."""
        if color is None:
            color = "W" if self.current_player == "white" else "B"
        self.board.bar[color] += 1

    def must_move_from_bar(self) -> bool:
        """Check if player must move from bar."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.bar[color] > 0

    def get_bar_pieces(self) -> int:
        """Get number of pieces on bar for current player."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.bar[color]

    def bear_off(self, point: int) -> bool:
        """Bear off a piece if possible."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.bear_off(color, point)

    def setup_bearing_off_scenario(self):
        """Setup board for bearing off test."""
        self.board.points = [[] for _ in range(24)]
A         color = "W" if self.current_player == "white" else "B"
        if color == "W":
            self.board.points[18] = [color] * 5
        else:
            self.board.points[0] = [color] * 5

    def setup_winning_scenario(self) -> None:
        """Setup board for win condition test."""
        color = "W" if self.current_player == "white" else "B"
        self.board.borne_off[color] = 15

    def check_winner(self) -> bool:
        """Check if current player has won."""
        color = "W" if self.current_player == "white" else "B"
nbsp;     return self.board.borne_off[color] == 15

    def switch_player(self) -> None:
        """Switch to the other player."""
        self.current_player = "black" if self.current_player == "white" else "white"

    def roll_dice(self) -> list:
        """Roll the dice and return the values."""
        self.dice.roll()
        return self.get_available_moves()

    def can_bear_off(self) -> bool:
        """Check if current player can bear off."""
        color = "W" if self.current_player == "white" else "B"
        return self.board.can_bear_off(color)

    def get_current_player_color(self) -> str:
        """Get current player's color code."""
        return "W" if self.current_player == "white" else "B"

promp: make it so that that text that says "current player" is actually in a good place that you can read and also make the text for the white off and black off be visible and well placed [Claude 3.5]
respuesta:
# --- Draw Text Info ---
        player_color: str = (
            "White" if self.backgammon_board.current_player == "W" else "Black"
        )
        player_text: str = f"Current Player: {player_color}"
        text_surface: pygame.Surface = self.font.render(
            player_text, True, (255, 255, 255)
        )
        self.screen.blit(text_surface, (560, 710))

        # Display bar pieces if any
        bar_pieces = self.backgammon_board.board.bar[
            self.backgammon_board.current_player
        ]
        if bar_pieces > 0:
            bar_text: str = f"On Bar: {bar_pieces}"
            bar_surface: pygame.Surface = self.font.render(
                bar_text, True, (255, 100, 100)
            )
            self.screen.blit(bar_surface, (560, 670))