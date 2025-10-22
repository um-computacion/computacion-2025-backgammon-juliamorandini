import pygame
from typing import Optional, List, Tuple

from config import Config
from pygame_ui.backgammon_board import BackgammonBoard
from pygame_ui.button import Button
from pygame_ui.board_interaction import BoardInteraction

CheckerPos = Tuple[int, int, int, int, str]

def get_point_center_coords(point_index: int) -> Tuple[int, int]:
    """Get screen coordinates for the center of a point.
    
    Args:
        point_index: Point number (0-23)
        
    Returns:
        Tuple[int, int]: (x, y) screen coordinates
    """
    # Calculate section widths
    left_section_width = Config.BAR_X - (Config.BOARD_X + Config.BORDER_THICKNESS)
    right_section_width = (Config.BOARD_X + Config.BOARD_WIDTH - Config.BORDER_THICKNESS) - (Config.BAR_X + Config.BAR_WIDTH)
    
    point_width = left_section_width // 6  # Same width for both sections
    
    # Determine x coordinate
    if point_index <= 5:  # Bottom right
        x = (Config.BAR_X + Config.BAR_WIDTH) + (point_index * point_width) + (point_width // 2)
    elif point_index <= 11:  # Bottom left
        x = (Config.BOARD_X + Config.BORDER_THICKNESS) + ((11 - point_index) * point_width) + (point_width // 2)
    elif point_index <= 17:  # Top left
        x = (Config.BOARD_X + Config.BORDER_THICKNESS) + ((point_index - 12) * point_width) + (point_width // 2)
    else:  # Top right (18-23)
        x = (Config.BAR_X + Config.BAR_WIDTH) + ((point_index - 18) * point_width) + (point_width // 2)
    
    # Determine y coordinate
    if point_index >= 12:  # Top half
        y = Config.BOARD_Y + Config.BORDER_THICKNESS + Config.POINT_HEIGHT
    else:  # Bottom half
        y = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS - Config.POINT_HEIGHT
    
    return int(x), int(y)

def is_valid_direction(from_point: int, to_point: int, player: str) -> bool:
    if player == "W":
        return to_point < from_point
    else:
        return to_point > from_point


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
                clicked_point = board_interaction.get_clicked_point(event.pos)
                
                if clicked_point is not None:
                    if not dice_rolled:
                        print("Roll dice first!")
                        continue

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
        
        backgammon_board.render(screen)  # Just render, don't collect positions
        
        roll_button.draw(screen)
        reset_button.draw(screen)
        next_turn_button.draw(screen)
        
        font: pygame.font.Font = pygame.font.Font(None, 36)
        player_color: str = "White" if backgammon_board.current_player == "W" else "Black"
        player_text: str = f"Current Player: {player_color}"
        text_surface: pygame.Surface = font.render(player_text, True, (255, 255, 255))
        screen.blit(text_surface, (750, 660))
        
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
