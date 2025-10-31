import pygame
from typing import Optional, Tuple

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


class GameUI:
    """
    Encapsulates the main game logic, state, and rendering.
    """

    def __init__(self):
        """Initializes the game, Pygame, and all game state variables."""
        pygame.init() # pylint: disable=no-member
        self.screen: pygame.Surface = pygame.display.set_mode(
            (Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
        )
        pygame.display.set_caption("Backgammon Game")
        self.clock: pygame.time.Clock = pygame.time.Clock()

        self.backgammon_board: BackgammonBoard = BackgammonBoard()
        self.board_interaction = BoardInteraction()

        # --- UI Elements ---
        self.roll_button: Button = Button(
            50,
            730,
            150,
            50,
            "Roll Dice",
            color=(70, 130, 180),
            hover_color=(100, 160, 210),
        )
        self.reset_button: Button = Button(
            220, 730, 150, 50, "Reset", color=(180, 70, 70), hover_color=(210, 100, 100)
        )
        self.next_turn_button: Button = Button(
            390,
            730,
            150,
            50,
            "Next Turn",
            color=(70, 180, 70),
            hover_color=(100, 210, 100),
        )
        self.font: pygame.font.Font = pygame.font.Font(None, 36)

        # --- Game State Variables ---
        self.selected_point: Optional[int] = None
        self.bar_selected: bool = False
        self.dice_rolled: bool = False
        self.moves_made: int = 0
        self.max_moves_this_turn: int = 0
        self.running: bool = True

        self.bear_off_area_width: int = 80  # Width of the bear-off area
        # Calculate x position to be on the far right, with a small margin
        self.bear_off_area_x: int = (
            Config.SCREEN_WIDTH - self.bear_off_area_width - Config.BORDER_THICKNESS
        )

        # Black's Bear-Off Rect (Top-Right)
        self.bear_off_rect_b: pygame.Rect = pygame.Rect(
            self.bear_off_area_x,
            Config.BOARD_Y + Config.BORDER_THICKNESS,
            self.bear_off_area_width,
            Config.BOARD_HEIGHT // 2 - Config.BORDER_THICKNESS * 1.5,
        )
        # White's Bear-Off Rect (Bottom-Right)
        self.bear_off_rect_w: pygame.Rect = pygame.Rect(
            self.bear_off_area_x,
            Config.BOARD_Y + Config.BOARD_HEIGHT // 2 + Config.BORDER_THICKNESS * 0.5,
            self.bear_off_area_width,
            Config.BOARD_HEIGHT // 2 - Config.BORDER_THICKNESS * 1.5,
        )

        self.checker_radius: int = Config.CHECKER_RADIUS
        self.checker_color_w: Tuple[int, int, int] = Config.WHITE_CHECKER
        self.checker_color_b: Tuple[int, int, int] = Config.BLACK_CHECKER
        self.checker_outline: Tuple[int, int, int] = Config.CHECKER_OUTLINE
        # Assuming a color from Config or just hardcoding
        self.bear_off_bg_color: Tuple[int, int, int] = (
            Config.WOOD_BROWN
        )  # Use a board-like color

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

        pygame.quit() # pylint: disable=no-member

    def handle_event(self, event: pygame.event.Event):
        """Handles a single Pygame event."""
        if event.type == pygame.QUIT: # pylint: disable=no-member
            self.running = False
            return

        if event.type == pygame.KEYDOWN: # pylint: disable=no-member
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
        if event.type == pygame.MOUSEBUTTONDOWN: # pylint: disable=no-member
            self.handle_mouse_click(event.pos)
            return

    def handle_keydown(self, key: int):
        """Handles keyboard press events."""
        if key == pygame.K_ESCAPE: # pylint: disable=no-member
            self.running = False
        elif key == pygame.K_SPACE: # pylint: disable=no-member
            self.do_roll_dice()
        elif key == pygame.K_n: # pylint: disable=no-member
            self.do_next_turn()
        elif key == pygame.K_r: # pylint: disable=no-member
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
        bar_y_bottom = Config.BOARD_Y + Config.BOARD_HEIGHT - Config.BORDER_THICKNESS
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
            print("Valid entry points with current dice:")
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
            if point_pieces and point_pieces[0] == player:
                self.selected_point = clicked_point
                print(f"Selected point {clicked_point}")
            else:
                print(f"No {player} pieces at point {clicked_point}")
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
                    distance = self.selected_point + 1  # e.g., point 0 -> distance 1
                elif player == "B" and self.bear_off_rect_b.collidepoint(mouse_pos):
                    is_bear_off_click = True
                    distance = 24 - self.selected_point  # e.g., point 23 -> distance 1
                else:
                    # Clicked somewhere invalid (not a point, not correct bear-off)
                    print("Invalid destination click.")
                    self.selected_point = None  # Deselect
                    return

            # --- Process the move (Bear off or Regular) ---

            if is_bearing_off and is_bear_off_click:
                # --- Handle Bear Off Attempt ---

                # Check if exact dice value exists
                if distance in self.backgammon_board.dice_values:
                    if self.backgammon_board.board.bear_off(
                        player, self.selected_point
                    ):
                        print(f"Bore off from point {self.selected_point}!")
                        self.backgammon_board.dice_values.remove(distance)
                        self.moves_made += 1
                    else:
                        print("Cannot bear off from that point (logic error)!")

                # Check if a higher dice value can be used (if no exact match and this is the furthest checker)
                elif all(d > distance for d in self.backgammon_board.dice_values):
                    # Check if this is the furthest checker
                    is_furthest = True
                    if player == "W":
                        for p in range(self.selected_point + 1, 6):
                            if (
                                self.backgammon_board.board.points[p]
                                and self.backgammon_board.board.points[p][0] == "W"
                            ):
                                is_furthest = False
                                break
                    else:  # Player 'B'
                        for p in range(self.selected_point - 1, 17, -1):  # 17 is 18-1
                            if (
                                self.backgammon_board.board.points[p]
                                and self.backgammon_board.board.points[p][0] == "B"
                            ):
                                is_furthest = False
                                break

                    if is_furthest:
                        if self.backgammon_board.board.bear_off(
                            player, self.selected_point
                        ):
                            print(
                                f"Bore off from point {self.selected_point} (using higher dice)!"
                            )
                            # Use the smallest dice that is larger than the distance
                            used_dice = min(
                                d
                                for d in self.backgammon_board.dice_values
                                if d > distance
                            )
                            self.backgammon_board.dice_values.remove(used_dice)
                            self.moves_made += 1
                        else:
                            print("Cannot bear off from that point (logic error)!")
                    else:
                        print(
                            "No dice value matches for bearing off (must move furthest checker first)"
                        )

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
                        print(f"Moved from {self.selected_point} to {clicked_point}")
                        self.backgammon_board.dice_values.remove(distance)
                        self.moves_made += 1
                    else:
                        print("Invalid move!")
                else:
                    print(f"Wrong direction for {self.backgammon_board.current_player}")
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
                    self.do_reset()  # Reset board after win
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

        # Draw buttons
        self.roll_button.draw(self.screen)
        self.reset_button.draw(self.screen)
        self.next_turn_button.draw(self.screen)

        # --- Draw Text Info ---
        player_color: str = (
            "White" if self.backgammon_board.current_player == "W" else "Black"
        )
        player_text: str = f"Current Player: {player_color}"
        text_surface: pygame.Surface = self.font.render(
            player_text, True, (255, 255, 255)
        )
        self.screen.blit(text_surface, (self.bear_off_area_x, 660))

        # Display bar pieces if any
        bar_pieces = self.backgammon_board.board.bar[
            self.backgammon_board.current_player
        ]
        if bar_pieces > 0:
            bar_text: str = f"On Bar: {bar_pieces}"
            bar_surface: pygame.Surface = self.font.render(
                bar_text, True, (255, 100, 100)
            )
            self.screen.blit(bar_surface, (self.bear_off_area_x, 620))

        borne_off_w = self.backgammon_board.board.borne_off["W"]
        borne_off_b = self.backgammon_board.board.borne_off["B"]

        # Draw Black's container
        pygame.draw.rect(
            self.screen, self.bear_off_bg_color, self.bear_off_rect_b, 0, 8
        )
        pygame.draw.rect(self.screen, (255, 255, 255), self.bear_off_rect_b, 2, 8)

        # Draw White's container
        pygame.draw.rect(
            self.screen, self.bear_off_bg_color, self.bear_off_rect_w, 0, 8
        )
        pygame.draw.rect(self.screen, (255, 255, 255), self.bear_off_rect_w, 2, 8)

        # Draw Black's borne-off checkers (stacked from bottom up)
        for i in range(borne_off_b):
            x = self.bear_off_rect_b.centerx
            # Stack with a 1.5x overlap
            y = (
                self.bear_off_rect_b.bottom
                - (i * self.checker_radius // 1.5)
                - self.checker_radius
                - 5
            )
            if y < self.bear_off_rect_b.top + self.checker_radius:
                break  # Stop if full
            pygame.draw.circle(
                self.screen, self.checker_color_b, (x, y), self.checker_radius
            )
            pygame.draw.circle(
                self.screen, self.checker_outline, (x, y), self.checker_radius, 2
            )

        # Draw White's borne-off checkers (stacked from top down)
        for i in range(borne_off_w):
            x = self.bear_off_rect_w.centerx
            y = (
                self.bear_off_rect_w.top
                + (i * self.checker_radius // 1.5)
                + self.checker_radius
                + 5
            )
            if y > self.bear_off_rect_w.bottom - self.checker_radius:
                break  # Stop if full
            pygame.draw.circle(
                self.screen, self.checker_color_w, (x, y), self.checker_radius
            )
            pygame.draw.circle(
                self.screen, self.checker_outline, (x, y), self.checker_radius, 2
            )

        # Draw text labels for borne-off
        borne_off_text_w: str = f"White Off: {borne_off_w}"
        borne_off_text_b: str = f"Black Off: {borne_off_b}"
        borne_off_surf_w: pygame.Surface = self.font.render(
            borne_off_text_w, True, (200, 200, 200)
        )
        borne_off_surf_b: pygame.Surface = self.font.render(
            borne_off_text_b, True, (200, 200, 200)
        )
        # Place text relative to the new rects
        self.screen.blit(
            borne_off_surf_b, (self.bear_off_rect_b.x, self.bear_off_rect_b.y - 40)
        )
        self.screen.blit(
            borne_off_surf_w, (self.bear_off_rect_w.x, self.bear_off_rect_w.y - 40)
        )

        # Display dice info
        if self.backgammon_board.dice_values:
            dice_text: str = f"Dice: {self.backgammon_board.dice_values}"
            dice_surface: pygame.Surface = self.font.render(
                dice_text, True, (255, 255, 255)
            )
            self.screen.blit(dice_surface, (self.bear_off_rect_w.x, 700))  # Moved text
        else:
            if self.dice_rolled:
                all_used: pygame.Surface = self.font.render(
                    "All dice used!", True, (255, 255, 0)
                )
                self.screen.blit(all_used, (self.bear_off_rect_w.x, 700))  # Moved text

        pygame.display.flip()


def main() -> None:
    """
    Main function to create and run the game.
    """
    game = GameUI()
    game.run()


if __name__ == "__main__":
    main()
