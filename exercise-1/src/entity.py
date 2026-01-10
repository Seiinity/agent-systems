import config
import pygame.draw

from pygame import Vector2, Color, Surface
from world import World
from utilities import Utilities


class Entity:

    """
    Represents a game-world entity, such as the player or the agent.
    """

    def __init__(self, position: Vector2, colour: Color, label: str, world: World) -> None:

        self.position: Vector2 = position

        self._label: str = label
        self._radius: int = 25
        self._colour: Color = colour
        self._world: World = world

        self.is_dragging: bool = False
        self.is_hover: bool = False

    def contains_point(self, point: Vector2) -> bool:

        """
        Checks if a point is within the entity's bounds.

        Parameters
        ----------
        point : Vector2
            The point check.

        Returns
        -------
        bool
            ``True`` if the point is within the entity's bounds,
            ``False`` otherwise.
        """

        # Gets the entity's position on the screen.
        screen_pos: Vector2 = self._get_screen_position()

        # Computes whether the point is inside the circle's bounds.
        dv: Vector2 = point - screen_pos
        return (dv.x * dv.x + dv.y * dv.y) < (self._radius * self._radius)

    def _get_screen_position(self) -> Vector2:

        """
        Converts the entity's grid position to screen coordinates.

        Returns
        -------
        Vector2
            The screen coordinates.
        """

        # Converts units to pixels and adds an offset to be at the centre of the cell.
        x: int = int(self.position.y) * config.CELL_SIZE + config.CELL_SIZE // 2
        y: int = int(self.position.x) * config.CELL_SIZE + config.CELL_SIZE // 2

        return Vector2(x, y)

    def set_position_from_screen(self, screen_pos: Vector2) -> None:

        """
        Sets the entity's position from screen coordinates, snapping
        to the grid.

        Parameters
        ----------
        screen_pos : Vector2
            The screen coordinates to place the entity at.
        """

        # Clamps to grid bounds.
        row: int = max(0, min(config.GRID_SIZE - 1, int(screen_pos.y // config.CELL_SIZE)))
        col: int = max(0, min(config.GRID_SIZE - 1, int(screen_pos.x // config.CELL_SIZE)))

        new_pos: Vector2 = Vector2(row, col)

        # Only moves if the cell is free.
        if self._world.is_free(new_pos):
            self.position = new_pos

    def draw(self, surface: Surface) -> None:

        """
        Draws the entity on the screen.
        """

        screen_pos: Vector2 = self._get_screen_position()

        # Draws the circle.
        pygame.draw.circle(surface, self._colour, screen_pos, self._radius)

        # Draws the label.
        Utilities.draw_outlined_text(surface, self._label, screen_pos)

