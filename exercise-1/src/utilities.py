import sys

import config

from enum import Enum
from pygame import Vector2, Surface, Color, Rect
from pygame.font import Font
from pathlib import Path


class Utilities:

    """
    Contains utility methods.
    """

    @staticmethod
    def manhattan_distance(pos1: Vector2, pos2: Vector2) -> int:

        """
        Calculates the Manhattan distance between two points.

        Parameters
        ----------
        pos1 : Vector2
            The first point's X and Y coordinates.
        pos2 : Vector2
            The second point's X and Y coordinates.

        Returns
        -------
        int
            The Manhattan distance between both points.
        """

        return int(abs(pos1.x - pos2.x) + abs(pos1.y - pos2.y))

    @staticmethod
    def draw_outlined_text(
            screen: Surface,
            text: str,
            pos: Vector2,
            text_colour: Color = config.COLOUR_TEXT,
            outline_colour: Color = config.COLOUR_EMPTY,
            outline_thickness: int = 2,
            font_size: int = 10,
            align: str = "centre"
    ) -> None:

        """
        Draws text with an outline at a given position.

        Parameters
        ----------
        screen : Surface
            The surface to draw on.
        text : str
            The text to draw.
        pos : Vector2
            The centre position to draw the text at.
        text_colour : Color, optional
            The main text colour.
        outline_colour : Color, optional
            The outline colour.
        outline_thickness : int, optional
            Thickness of the outline in pixels.
        font_size : int, optional
            Font size to use.
        align : str, optional
            The alignment of the text.
        """

        # Default font.
        font_path: Path = Utilities.resource_path("fonts/petty_5x5.otf")
        font: Font = Font(str(font_path), font_size)

        # Renders the surfaces.
        outline_surf: Surface = font.render(text, True, outline_colour)
        text_surf: Surface = font.render(text, True, text_colour)

        # Defines a get_rect function based on alignment.
        def get_rect(surf: Surface, position: tuple[int, int]) -> Rect:
            if align == "left":
                return surf.get_rect(topleft=position)
            return surf.get_rect(center=position)

        # Draws the outline in 8 directions.
        for dx in [-outline_thickness, 0, outline_thickness]:
            for dy in [-outline_thickness, 0, outline_thickness]:
                if dx != 0 or dy != 0:
                    screen.blit(outline_surf, get_rect(outline_surf, (int(pos.x) + dx, int(pos.y) + dy)))

        # Draws the main text.
        screen.blit(text_surf, get_rect(text_surf, (int(pos.x), int(pos.y))))

    @staticmethod
    def resource_path(relative_path: str) -> Path:

        """
        Gets the absolute path to a resource.
        """

        try:
            # PyInstaller stores temp folder path here
            base_path = Path(sys._MEIPASS)
        except AttributeError:
            # Running in normal Python
            base_path = Path(__file__).resolve().parent.parent
        return base_path / relative_path


class Direction(Enum):

    """
    Stores direction tuples.
    """

    UP = (-1, 0)
    DOWN = (1, 0)
    LEFT = (0, -1)
    RIGHT = (0, 1)

    def __init__(self, dx: int, dy: int) -> None:

        self.dx = dx
        self.dy = dy