import pygame
from typing import Optional, List, Tuple

from config import Config
from pygame_ui.backgammon_board import BackgammonBoard
from pygame_ui.button import Button
from pygame_ui.board_interaction import BoardInteraction

CheckerPos = Tuple[int, int, int, int, str]

def is_valid_direction(from_point: int, to_point: int, player: str) -> bool:
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


def main() -> None:
    pygame.init()
    screen: pygame.Surface = pygame.display.set_mode(
        (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
    )
    pygame.display.set_caption("Backgammon Game")
    clock: pygame.time.Clock = pygame.time.Clock()
    
    backgammon_board: BackgammonBoard = BackgammonBoard()
    
    roll_button: Button = Button(
        50, 730, 150, 50, "Roll Dice",
        color=(70, 130, 180),
        hover_color=(100, 160, 210)
    )
    reset_button: Button = Button(
        220, 730, 150, 50, "Reset",
        color=(180, 70, 70),
        hover_color=(210, 100, 100)
    )
    next_turn_button: Button = Button(
        390, 730, 150, 50, "Next Turn",
        color=(70, 180, 70),
        hover_color=(100, 210, 100)
    )
    
    selected_point: Optional[int] = None
    dice_rolled: bool = False
    moves_made: int = 0
    max_moves_this_turn: int = 0
    
    board_interaction = BoardInteraction()
    
    running: bool = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                elif event.key == pygame.K_SPACE:
                    if not dice_rolled:
                        dice = backgammon_board.roll_dice()
                        dice_rolled = True
                        moves_made = 0
                        max_moves_this_turn = 4 if len(dice) == 4 else 2
                        print(f"{backgammon_board.current_player} rolled: {dice}")
                    else:
                        print("Already rolled! Make your moves or press N for next turn")
                
                elif event.key == pygame.K_n:
                    backgammon_board.switch_player()
                    dice_rolled = False
                    moves_made = 0
                    max_moves_this_turn = 0
                    selected_point = None
                    print(f"Turn ended. Now playing: {backgammon_board.current_player}")
                
                elif event.key == pygame.K_r:
                    backgammon_board.reset()
                    selected_point = None
                    dice_rolled = False
                    moves_made = 0
                    max_moves_this_turn = 0
                    print("Board reset!")
            
            elif roll_button.handle_event(event):
                if not dice_rolled:
                    dice = backgammon_board.roll_dice()
                    dice_rolled = True
                    moves_made = 0
                    max_moves_this_turn = 4 if len(dice) == 4 else 2
                    print(f"{backgammon_board.current_player} rolled: {dice}")
                else:
                    print("Already rolled! Make your moves or press N for next turn")
            
            elif reset_button.handle_event(event):
                backgammon_board.reset()
                selected_point = None
                dice_rolled = False
                moves_made = 0
                max_moves_this_turn = 0
                print("Board reset!")
            
            elif next_turn_button.handle_event(event):
                backgammon_board.switch_player()
                dice_rolled = False
                moves_made = 0
                max_moves_this_turn = 0
                selected_point = None
                print(f"Turn ended. Now playing: {backgammon_board.current_player}")
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                
                if not dice_rolled:
                    print("Roll dice first!")
                    continue

                # CHECK IF PLAYER HAS PIECES ON BAR
                if backgammon_board.board.bar[backgammon_board.current_player] > 0:
                    # PLAYER MUST ENTER FROM BAR
                    bar_x = Config.BAR_X
                    bar_y_top = Config.BOARD_Y + Config.BORDER_THICKNESS
                    bar_y_bottom = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
                    bar_width = Config.BAR_WIDTH
                    
                    # Check if clicking on bar area
                    if bar_x <= mouse_pos[0] <= bar_x + bar_width and bar_y_top <= mouse_pos[1] <= bar_y_bottom:
                        # Clicked on bar - select it
                        selected_point = "BAR"
                        bar_pieces = backgammon_board.board.bar[backgammon_board.current_player]
                        print(f"Selected checker from bar! ({bar_pieces} pieces on bar)")
                        print(f"Valid entry points with current dice:")
                        for dice_val in backgammon_board.dice_values:
                            entry_pt = get_entry_point_for_dice(dice_val, backgammon_board.current_player)
                            print(f"  Dice {dice_val} → Point {entry_pt}")
                        continue
                    
                    # Not clicking bar, must click valid entry point if bar is selected
                    if selected_point == "BAR":
                        clicked_point = board_interaction.get_clicked_point(mouse_pos)
                        
                        if clicked_point is not None:
                            # Get valid entry points for this player's dice
                            valid_entry_points = {}  # dice_value -> point
                            for dice_val in backgammon_board.dice_values:
                                entry_pt = get_entry_point_for_dice(dice_val, backgammon_board.current_player)
                                valid_entry_points[dice_val] = entry_pt
                            
                            # Check if clicked point matches any valid entry point
                            matching_dice = None
                            for dice_val, entry_pt in valid_entry_points.items():
                                if entry_pt == clicked_point:
                                    matching_dice = dice_val
                                    break
                            
                            if matching_dice is None:
                                print(f"Cannot enter at point {clicked_point}. Valid entry points: {list(valid_entry_points.values())}")
                                selected_point = None
                                continue
                            
                            # Try to enter from bar
                            if backgammon_board.board.move_checker_from_bar(clicked_point, backgammon_board.current_player):
                                print(f"✓ Entered from bar at point {clicked_point} using dice {matching_dice}")
                                backgammon_board.dice_values.remove(matching_dice)
                                moves_made += 1
                                
                                # Check if turn is complete
                                if moves_made >= max_moves_this_turn or not backgammon_board.dice_values:
                                    print("Turn complete!")
                                    backgammon_board.switch_player()
                                    dice_rolled = False
                                    moves_made = 0
                                    max_moves_this_turn = 0
                            else:
                                print(f"Cannot enter at point {clicked_point} (point blocked)")
                            
                            selected_point = None
                        continue
                    else:
                        print("Click the BAR first to select a checker!")
                        continue
                
                # NORMAL MOVE (not from bar)
                clicked_point = board_interaction.get_clicked_point(mouse_pos)
                if clicked_point is None:
                    continue
                    
                    # NORMAL MOVE (not from bar)
                    if selected_point is None:
                        # Selecting a point
                        point_pieces = backgammon_board.board.points[clicked_point]
                        if point_pieces and point_pieces[0] == backgammon_board.current_player:
                            selected_point = clicked_point
                            print(f"Selected point {clicked_point}")
                        else:
                            print(f"No {backgammon_board.current_player} pieces at point {clicked_point}")
                    else:
                        # Making a move
                        if clicked_point == selected_point:
                            # Deselect if clicking same point
                            selected_point = None
                            print("Point deselected")
                            continue
                            
                        distance = abs(clicked_point - selected_point)
                        if distance in backgammon_board.dice_values:
                            if is_valid_direction(selected_point, clicked_point, backgammon_board.current_player):
                                if backgammon_board.move_checker(selected_point, clicked_point):
                                    print(f"Moved from {selected_point} to {clicked_point}")
                                    backgammon_board.dice_values.remove(distance)
                                    moves_made += 1
                                    if moves_made >= max_moves_this_turn or not backgammon_board.dice_values:
                                        print("Turn complete!")
                                        backgammon_board.switch_player()
                                        dice_rolled = False
                                        moves_made = 0
                                        max_moves_this_turn = 0
                                else:
                                    print(f"Invalid move!")
                            else:
                                print(f"Wrong direction for {backgammon_board.current_player}")
                        else:
                            print(f"No dice value matches distance {distance}")
                        selected_point = None

        backgammon_board.update()
        
        screen.fill(Config.DARK_BROWN)
        
        backgammon_board.render(screen)
        
        roll_button.draw(screen)
        reset_button.draw(screen)
        next_turn_button.draw(screen)
        
        font: pygame.font.Font = pygame.font.Font(None, 36)
        player_color: str = "White" if backgammon_board.current_player == "W" else "Black"
        player_text: str = f"Current Player: {player_color}"
        text_surface: pygame.Surface = font.render(player_text, True, (255, 255, 255))
        screen.blit(text_surface, (750, 660))
        
        # Display bar pieces if any
        bar_pieces = backgammon_board.board.bar[backgammon_board.current_player]
        if bar_pieces > 0:
            bar_text: str = f"On Bar: {bar_pieces}"
            bar_surface: pygame.Surface = font.render(bar_text, True, (255, 100, 100))
            screen.blit(bar_surface, (750, 620))
        
        if backgammon_board.dice_values:
            dice_text: str = f"Dice: {backgammon_board.dice_values}"
            dice_surface: pygame.Surface = font.render(dice_text, True, (255, 255, 255))
            screen.blit(dice_surface, (750, 700))
        else:
            if dice_rolled:
                all_used: pygame.Surface = font.render("All dice used!", True, (255, 255, 0))
                screen.blit(all_used, (750, 700))

        pygame.display.flip()
        
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()