import config
import numpy as np
import pygame.draw

from utilities import Utilities, Direction, Color
from pygame import Vector2, Surface
from numpy.typing import NDArray


class World:

    """
    Represents the game world.
    """

    def __init__(self) -> None:

        self._grid: NDArray[np.int_] = config.WORLD_MAP.copy()
        self._powerups: list[Vector2] = self._get_powerup_positions()

    def _get_powerup_positions(self) -> list[Vector2]:

        """
        Returns the positions of all power-ups.

        Returns
        -------
        list[Vector2]
            A list with the positions of all power-ups.
        """

        powerups = []
        for i in range(self._grid.shape[0]):
            for j in range(self._grid.shape[1]):
                if self._grid[i, j] == 2:
                    powerups.append(Vector2(i, j))
        return powerups

    def get_distance_to_nearest_powerup(self, position: Vector2) -> int:

        """
        Finds the distance between the provided position and the power-up
        that is closest to it.

        Arguments
        ---------
        position : Vector2
            The position to calculate the distance from.

        Returns
        -------
        int
            The distance between the provided position and the nearest power-up.
        """

        # Returns the max distance if there are no power-ups left.
        if not self._powerups:
            return config.MAX_MANHATTAN

        # Calculates all the distances.
        distances = [
            Utilities.manhattan_distance(position, powerup)
            for powerup in self._powerups
        ]

        # Returns the smallest distance.
        return min(distances)

    @staticmethod
    def _is_valid_position(position: Vector2) -> bool:

        """
        Checks if a position is within the world bounds.

        Parameters
        ----------
        position : Vector2
            The position to check.

        Returns
        -------
        bool
            ``True`` if the position is within the world bounds,
            ``False`` otherwise.
        """

        row: int = int(position.x)
        col: int = int(position.y)

        return 0 <= row < config.GRID_SIZE and 0 <= col < config.GRID_SIZE

    def is_free(self, position: Vector2) -> bool:

        """
        Checks whether a position is valid and not a wall.

        Parameters
        ----------
        position : Vector2
            The position to check.

        Returns
        -------
        bool
            ``True`` if the position is free, ``False`` otherwise.
        """

        row: int = int(position.x)
        col: int = int(position.y)

        if not self._is_valid_position(position):
            return False

        return self._grid[row, col] != 1

    def draw(self, surface: Surface) -> None:

        """
        Draws the world grid.

        Parameters
        ----------
        surface : Surface
            The Pygame surface to draw the world grid on.
        """

        # Draws the grid itself.
        for row in range(config.GRID_SIZE):

            for col in range(config.GRID_SIZE):

                x: int = col * config.CELL_SIZE
                y: int = row * config.CELL_SIZE

                # Decides on which colour to use.
                colour: Color = config.COLOUR_EMPTY
                if self._grid[row, col] == 1:
                    colour = config.COLOUR_WALL

                pygame.draw.rect(surface, colour, (x, y, config.CELL_SIZE, config.CELL_SIZE))
                pygame.draw.rect(surface, config.COLOUR_GRID, (x, y, config.CELL_SIZE, config.CELL_SIZE), 1)

        # Draws the power-ups.
        for row, col in self._powerups:

            x: int = col * config.CELL_SIZE + config.CELL_SIZE // 2
            y: int = row * config.CELL_SIZE + config.CELL_SIZE // 2
            pygame.draw.circle(surface, config.COLOUR_POWERUP, (x, y), config.CELL_SIZE // 4)