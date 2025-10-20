"""
Main entry point for the Backgammon game.
This is the file you run to start the game.

IMPORTANT: Run this file from the project root directory:
    python main.py
"""
import pygame
from typing import Optional

from config import Config
from pygame_ui.backgammon_board import BackgammonBoard
from pygame_ui.board_interaction import BoardInteraction
from pygame_ui.button import Button


def is_valid_direction(from_point: int, to_point: int, player: str) -> bool:
    """
    Check if the move is in the correct direction for the player.
    
    White moves counter-clockwise (from higher numbers to lower: 23 -> 0)
    Black moves clockwise (from lower numbers to higher: 0 -> 23)
    
    Args:
        from_point: Starting point (0-23)
        to_point: Destination point (0-23)
        player: 'W' for White or 'B' for Black
        
    Returns:
        True if move is in correct direction, False otherwise
    """
    if player == "W":
        # White moves counter-clockwise: from high to low (23 -> 0)
        return to_point < from_point
    else:  # player == "B"
        # Black moves clockwise: from low to high (0 -> 23)
        return to_point > from_point


def main() -> None:
    """
    Main game function with game loop.
    
    This function initializes pygame, creates game components,
    and runs the main game loop handling events, updates, and rendering.
    
    Returns:
        None
    """
    # Pygame setup
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode(
        (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
    )
    pygame.display.set_caption("Backgammon Game")
    clock: pygame.time.Clock = pygame.time.Clock()
    
    # Create game components
    backgammon_board: BackgammonBoard = BackgammonBoard()
    board_interaction: BoardInteraction = BoardInteraction()
    
    # Create UI buttons
    roll_button: Button = Button(
        50, 650, 150, 50, "Roll Dice",
        color=(70, 130, 180),
        hover_color=(100, 160, 210)
    )
    reset_button: Button = Button(
        220, 650, 150, 50, "Reset",
        color=(180, 70, 70),
        hover_color=(210, 100, 100)
    )
    next_turn_button: Button = Button(
        390, 650, 150, 50, "Next Turn",
        color=(70, 180, 70),
        hover_color=(100, 210, 100)
    )
    
    # Game state variables
    selected_point: Optional[int] = None  # Track which point is selected
    dice_rolled: bool = False  # Track if dice have been rolled this turn
    moves_made: int = 0  # Track number of moves made this turn
    max_moves_this_turn: int = 0  # Track maximum moves for current turn
    
    # Game loop
    running: bool = True
    
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
                        # Calculate max moves based on whether it's doubles
                        max_moves_this_turn = 4 if len(dice) == 4 else 2
                        print(f"{backgammon_board.current_player} rolled: {dice}")
                    else:
                        print("Already rolled! Make your moves or press N for next turn")
                
                # Press N to end turn (next player)
                elif event.key == pygame.K_n:
                    backgammon_board.switch_player()
                    dice_rolled = False
                    moves_made = 0
                    max_moves_this_turn = 0
                    selected_point = None
                    print(f"Turn ended. Now playing: {backgammon_board.current_player}")
                
                # Press R to reset board
                elif event.key == pygame.K_r:
                    backgammon_board.reset()
                    selected_point = None
                    dice_rolled = False
                    moves_made = 0
                    max_moves_this_turn = 0
                    print("Board reset!")
            
            # Handle board interactions (clicks)
            interaction_result = board_interaction.handle_event(event)
            if interaction_result:
                if interaction_result['type'] == 'point_click':
                    point: int = interaction_result['point']
                    
                    # Must roll dice first
                    if not dice_rolled:
                        print("Roll dice first! (Press SPACE or click Roll Dice)")
                        continue
                    
                    # Check if all moves used
                    if not backgammon_board.dice_values:
                        print("All moves used! Press N to end turn")
                        continue
                    
                    if moves_made >= max_moves_this_turn:
                        print("All moves used! Press N to end turn")
                        continue
                    
                    print(f"Clicked on point {point}")
                    
                    # Simple move logic: select first, then move
                    if selected_point is None:
                        # First click - select a point (must have current player's pieces)
                        if (backgammon_board.board.points[point] and
                            backgammon_board.board.points[point][0] == backgammon_board.current_player):
                            selected_point = point
                            print(f"Selected point {point}")
                        else:
                            print(f"Point {point} has no {backgammon_board.current_player} pieces")
                    else:
                        # Second click - try to move
                        distance: int = abs(point - selected_point)
                        
                        # Check if move is in correct direction
                        if not is_valid_direction(selected_point, point, backgammon_board.current_player):
                            player_name: str = "White" if backgammon_board.current_player == "W" else "Black"
                            direction: str = "counter-clockwise (towards 0)" if backgammon_board.current_player == "W" else "clockwise (towards 23)"
                            print(f"Invalid direction! {player_name} must move {direction}")
                            selected_point = None
                            continue
                        
                        # Check if distance matches one of the available dice
                        if distance in backgammon_board.dice_values:
                            success: bool = backgammon_board.move_checker(selected_point, point)
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
                print(f"DEBUG: Roll button click detected at {pygame.mouse.get_pos()}")
                if not dice_rolled:
                    print("DEBUG: Rolling dice...")
                    dice = backgammon_board.roll_dice()
                    dice_rolled = True
                    moves_made = 0
                    max_moves_this_turn = 4 if len(dice) == 4 else 2
                    print(f"{backgammon_board.current_player} rolled: {dice}")
                else:
                    print("Already rolled! Make your moves or press N for next turn")
            
            if reset_button.handle_event(event):
                backgammon_board.reset()
                selected_point = None
                dice_rolled = False
                moves_made = 0
                max_moves_this_turn = 0
                print("Board reset!")
            
            if next_turn_button.handle_event(event):
                backgammon_board.switch_player()
                dice_rolled = False
                moves_made = 0
                max_moves_this_turn = 0
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
        
        # Draw current player indicator (moved right to avoid collision)
        font: pygame.font.Font = pygame.font.Font(None, 36)
        player_color: str = "White" if backgammon_board.current_player == "W" else "Black"
        player_text: str = f"Current Player: {player_color}"
        text_surface: pygame.Surface = font.render(player_text, True, (255, 255, 255))
        screen.blit(text_surface, (750, 660))
        
        # Draw dice values if rolled (moved right to align with player indicator)
        if backgammon_board.dice_values:
            dice_text: str = f"Dice: {backgammon_board.dice_values}"
            dice_surface: pygame.Surface = font.render(dice_text, True, (255, 255, 255))
            screen.blit(dice_surface, (750, 700))
        else:
            if dice_rolled:
                all_used: pygame.Surface = font.render("All dice used!", True, (255, 255, 0))
                screen.blit(all_used, (750, 700))
        
        # Draw selected point indicator (moved right)
        if selected_point is not None:
            selected_text: str = f"Selected: Point {selected_point}"
            selected_surface: pygame.Surface = font.render(selected_text, True, (255, 255, 0))
            screen.blit(selected_surface, (1000, 660))
        
        # flip() the display to put your work on screen
        pygame.display.flip()
        
        # Limits FPS to 60
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()