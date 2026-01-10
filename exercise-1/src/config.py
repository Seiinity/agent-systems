import numpy as np

from numpy.typing import NDArray
from pygame import Vector2, Color


# Display settings.
CELL_SIZE: int      = 60
GRID_SIZE: int      = 8
SCREEN_WIDTH: int   = GRID_SIZE * CELL_SIZE + 300
SCREEN_HEIGHT: int  = GRID_SIZE * CELL_SIZE
FPS: int            = 10

# Colours.
COLOUR_EMPTY: Color        = Color(240, 240, 240)
COLOUR_WALL: Color         = Color(40, 40, 40)
COLOUR_POWERUP: Color      = Color(255, 215, 0)
COLOUR_PLAYER: Color       = Color(0, 120, 255)
COLOUR_AGENT: Color  = Color(255, 60, 60)
COLOUR_GRID: Color         = Color(180, 180, 180)
COLOUR_TEXT: Color         = Color(40, 40, 40)
COLOUR_UI_BG: Color        = Color(250, 250, 250)

# Game parameters.
MAX_POWERUP_TIME: float    = 10
MAX_MANHATTAN: int         = 14

# World config.
WORLD_MAP: NDArray[np.int_] = np.array([
    [0, 0, 0, 0, 0, 2, 0, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 1, 2, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 1, 0, 0, 2],
    [0, 0, 0, 1, 1, 0, 0, 0],
    [0, 1, 0, 0, 0, 2, 1, 0],
    [0, 1, 1, 0, 0, 1, 1, 0],
    [0, 2, 0, 0, 0, 0, 0, 0],
])

START_PLAYER: Vector2  = Vector2(0, 0)
START_AGENT: Vector2   = Vector2(7, 7)

# Heuristic weights.
WEIGHT_TIME: float          = 0.55
WEIGHT_POWERUP_DIST: float  = 0.40
WEIGHT_PLAYER_DIST: float   = 0.05