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
    notification = Notification()
    
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
    max_moves_this_turn = 2  # Track max moves for this turn (2 or 4 for doubles)
    
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
                        # Set max moves based on if it's doubles
                        max_moves_this_turn = len(dice)  # Will be 4 for doubles, 2 otherwise
                        print(f"{backgammon_board.current_player} rolled: {dice}")
                    else:
                        print("Already rolled! Make your moves or press N for next turn")()
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
                    max_moves_this_turn = 2
                    selected_point = None
                    print(f"Turn ended. Now playing: {backgammon_board.current_player}")
                
                # Press R to reset board
                elif event.key == pygame.K_r:
                    backgammon_board.reset()
                    selected_point = None
                    dice_rolled = False
                    moves_made = 0
                    max_moves_this_turn = 2
                    print("Board reset!")
            
            # Handle board interactions (clicks)
            interaction_result = board_interaction.handle_event(event)
            if interaction_result:
                if interaction_result['type'] == 'point_click':
                    point = interaction_result['point']
                    
                    # Must roll dice first
                    if not dice_rolled:
                        notification.add_message("Roll dice first!", "warning")
                        print("Roll dice first! (Press SPACE or click Roll Dice)")
                        continue
                    
                    # Check if all moves used
                    if moves_made >= max_moves_this_turn:
                        notification.add_message("All moves used! Press N", "warning")
                        print("All moves used! Press N to end turn")
                        continue
                    
                    print(f"Clicked on point {point}")
                    
                    # Simple move logic: select first, then move
                    if selected_point is None:
                        # First click - select a point (must have current player's pieces)
                        if backgammon_board.board.points[point] and \
                           backgammon_board.board.points[point][0] == backgammon_board.current_player:
                            selected_point = point
                            notification.add_message(f"Selected point {point}", "info")
                            print(f"Selected point {point}")
                        else:
                            player_name = "White" if backgammon_board.current_player == "W" else "Black"
                            notification.add_message(f"No {player_name} pieces here!", "error")
                            print(f"Point {point} has no {backgammon_board.current_player} pieces")
                    else:
                        # Second click - try to move
                        distance = abs(point - selected_point)
                        
                        # Validate point is in range (0-23)
                        if not (0 <= point <= 23):
                            notification.add_message("Out of range!", "error")
                            print(f"Point {point} is out of range!")
                            selected_point = None
                            continue
                        
                        # Check if distance matches one of the available dice
                        if distance in backgammon_board.dice_values:
                            try:
                                success = backgammon_board.move_checker(selected_point, point)
                                if success:
                                    notification.add_message(f"Moved: {selected_point} → {point}", "success")
                                    print(f"Moved from {selected_point} to {point}")
                                    # Remove used die
                                    backgammon_board.dice_values.remove(distance)
                                    moves_made += 1
                                    
                                    # Check if all moves used
                                    if not backgammon_board.dice_values:
                                        notification.add_message("All dice used!", "info")
                                        print("All dice used! Press N to end turn")
                                else:
                                    notification.add_message("Invalid move!", "error")
                                    print(f"Invalid move from {selected_point} to {point}")
                            except Exception as e:
                                notification.add_message(f"Error: {str(e)}", "error")
                                print(f"Error moving: {e}")
                        else:
                            notification.add_message(f"Need dice: {distance}, have: {backgammon_board.dice_values}", "error")
                            print(f"Distance {distance} doesn't match dice: {backgammon_board.dice_values}")
                        
                        selected_point = None
            
            # Handle button clicks
            if roll_button.handle_event(event):
                if not dice_rolled:
                    dice = backgammon_board.roll_dice()
                    dice_rolled = True
                    moves_made = 0
                    max_moves_this_turn = len(dice)  # Will be 4 for doubles, 2 otherwise
                    player_name = "White" if backgammon_board.current_player == "W" else "Black"
                    # Show just the first two values for display
                    if len(dice) >= 2:
                        notification.add_message(f"{player_name} rolled: {dice[0]}, {dice[1]}", "success")
                    print(f"{backgammon_board.current_player} rolled: {dice}")
                else:
                    notification.add_message("Already rolled!", "warning")
                    print("Already rolled! Make your moves or press N for next turn")
            
            if reset_button.handle_event(event):
                backgammon_board.reset()
                selected_point = None
                dice_rolled = False
                moves_made = 0
                max_moves_this_turn = 2
                notification.add_message("Board reset!", "info")
                print("Board reset!")
            
            if next_turn_button.handle_event(event):
                backgammon_board.switch_player()
                dice_rolled = False
                moves_made = 0
                max_moves_this_turn = 2
                selected_point = None
                player_name = "White" if backgammon_board.current_player == "W" else "Black"
                notification.add_message(f"{player_name}'s turn", "info")
                print(f"Turn ended. Now playing: {backgammon_board.current_player}")
        
        # Update game state
        backgammon_board.update()
        
        # Fill the screen with a color to wipe away anything from last frame
        screen.fill(Config.DARK_BROWN)
        
        # RENDER YOUR GAME HERE
        backgammon_board.render(screen)
        
        # Draw notifications on top of everything
        notification.draw(screen)
        
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