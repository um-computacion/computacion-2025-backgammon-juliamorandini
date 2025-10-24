"""
Configuration constants for the Backgammon board.
Centralizes all color schemes, dimensions, and layout settings.
"""


class Config:
    """Game configuration settings."""

    # Add debug flag
    DEBUG = True

    # Screen dimensions
    SCREEN_WIDTH = 1200
    SCREEN_HEIGHT = 800

    # Board dimensions
    BOARD_WIDTH = 1000
    BOARD_HEIGHT = 700
    BOARD_X = 100
    BOARD_Y = 50

    # Border dimensions
    BORDER_THICKNESS = 20

    # Point dimensions
    POINT_WIDTH = 60
    POINT_HEIGHT = 200
    POINTS_PER_QUADRANT = 6
    TOTAL_POINTS = 24
    
    # Checker dimensions
    CHECKER_SIZE = 40  # Diameter of checker pieces

    # Bar dimensions
    BAR_WIDTH = 60
    BAR_X = BOARD_X + (BOARD_WIDTH - BAR_WIDTH) // 2

    # Right panel dimensions (COMMENTED OUT, no longer used for striped panel)
    # RIGHT_PANEL_WIDTH = 80
    # RIGHT_PANEL_X = BOARD_X + BOARD_WIDTH - RIGHT_PANEL_WIDTH

    # Colors - Board
    DARK_BROWN = (60, 40, 30)
    WOOD_BROWN = (180, 120, 70)
    LIGHT_TAN = (210, 180, 140)
    DARK_POINT = (100, 70, 50)
    GREEN_BAR = (40, 90, 60)
    BRASS = (184, 134, 11)
    # STRIPE_GREEN = (60, 120, 80) # Removed
    # STRIPE_YELLOW = (220, 200, 100) # Removed

    # Colors - Checkers
    WHITE_CHECKER = (240, 240, 240)
    BLACK_CHECKER = (40, 40, 40)
    CHECKER_OUTLINE = (100, 100, 100)
    CHECKER_HIGHLIGHT_WHITE = (255, 255, 255)
    CHECKER_HIGHLIGHT_BLACK = (80, 80, 80)

    # Colors - Dice
    DICE_WHITE = (255, 255, 255)
    DICE_DOT = (0, 0, 0)

    # Checker dimensions
    CHECKER_RADIUS = 25
    CHECKER_SPACING = 15  # Vertical spacing between stacked checkers

    # Dice dimensions
    DICE_SIZE = 40
    DICE_DOT_RADIUS = 4

    # Hinge dimensions
    HINGE_WIDTH = 50
    HINGE_HEIGHT = 15