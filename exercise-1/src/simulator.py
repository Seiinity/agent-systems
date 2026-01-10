import sys
import pygame
import config

from pygame import Surface, Vector2
from pygame.time import Clock
from heuristic import Decision, ChaseFleeHeuristic
from utilities import Utilities
from world import World
from entity import Entity


class Simulator:

    """
    Interactive simulator for the chase/flee heuristic.
    """

    def __init__(self) -> None:

        # Initiates the Pygame process.
        pygame.init()
        pygame.display.set_caption("Chase/Flee Heuristic Simulator")
        self._screen: Surface = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self._clock: Clock = Clock()

        # Creates the world.
        self._world: World = World()

        # Creates the player.
        self._player: Entity = Entity(config.START_PLAYER, config.COLOUR_PLAYER, "PLY", self._world)
        self._has_powerup: bool = False
        self._powerup_timer: float = 0

        # Creates the agent.
        self._agent: Entity = Entity(config.START_AGENT, config.COLOUR_AGENT, "AGT", self._world)
        self._heuristic: ChaseFleeHeuristic = ChaseFleeHeuristic(self._world)
        self._h_value: float = 0.0
        self._decision: Decision = Decision.CHASE

        # UI state.
        self._dragging: bool = False
        self._running: bool = True
        self._dragging_entity: Entity | None = None

        # Calculates the heuristic initially.
        self._calculate_heuristic()

    def _calculate_heuristic(self) -> None:

        self._decision, self._h_value = self._heuristic.decide(
            self._agent.position, self._player.position, self._powerup_timer
        )

    def _handle_input(self) -> None:

        """
        Handles user input.
        """

        for event in pygame.event.get():

            # Quits the simulator with the X.
            if event.type == pygame.QUIT:
                self._running = False

            # Handles keyboard events.
            elif event.type == pygame.KEYDOWN:

                # Quits the simulator with Esc.
                if event.key == pygame.K_ESCAPE:
                    self._running = False

                # Toggles player power-up.
                elif event.key == pygame.K_SPACE:

                    self._has_powerup = not self._has_powerup
                    self._powerup_timer = config.MAX_POWERUP_TIME if self._has_powerup else 0
                    self._calculate_heuristic()

                # Increases power-up time.
                elif event.key == pygame.K_UP and self._has_powerup:

                    self._powerup_timer = min(config.MAX_POWERUP_TIME, self._powerup_timer + 0.25)
                    self._calculate_heuristic()

                # Decreases power-up time.
                elif event.key == pygame.K_DOWN and self._has_powerup:

                    self._powerup_timer = max(0.0, self._powerup_timer - 0.25)
                    self._calculate_heuristic()

                # Resets the simulator.
                elif event.key == pygame.K_r:

                    self._player.position = config.START_PLAYER
                    self._agent.position = config.START_AGENT
                    self._has_powerup = False
                    self._powerup_timer = config.MAX_POWERUP_TIME
                    self._calculate_heuristic()

            # Handles mouse down events.
            elif event.type == pygame.MOUSEBUTTONDOWN:

                # Start drag.
                if event.button == 1:

                    mouse_pos: Vector2 = Vector2(pygame.mouse.get_pos())

                    if self._player.contains_point(mouse_pos):
                        self._dragging_entity = self._player
                        self._player.dragging = True

                    elif self._agent.contains_point(mouse_pos):
                        self._dragging_entity = self._agent
                        self._agent.dragging = True

            # Handles mouse up events.
            elif event.type == pygame.MOUSEBUTTONUP:

                # Stop drag.
                if event.button == 1 and self._dragging_entity:
                    self._dragging_entity.dragging = False
                    self._dragging_entity = None

            # Handles mouse movement.
            elif event.type == pygame.MOUSEMOTION:

                mouse_pos: Vector2 = Vector2(pygame.mouse.get_pos())

                # Updates hover states.
                self._player.hover = self._player.contains_point(mouse_pos)
                self._agent.hover = self._agent.contains_point(mouse_pos)

                # Handles dragging.
                if self._dragging_entity:
                    self._dragging_entity.set_position_from_screen(mouse_pos)
                    self._calculate_heuristic()

    def draw_ui(self):

        """
        Draws the UI panel.
        """

        ui_x = config.GRID_SIZE * config.CELL_SIZE + 150
        ui_y = 55

        # Background.
        pygame.draw.rect(self._screen, config.COLOUR_UI_BG,
                         (config.GRID_SIZE * config.CELL_SIZE, 0,
                          200, config.SCREEN_HEIGHT))

        # Agent decision.
        Utilities.draw_outlined_text(self._screen, f"Decision: {str(self._decision).split(".")[1]}", Vector2(ui_x, ui_y))
        ui_y += 25

        # Heuristic value.
        Utilities.draw_outlined_text(self._screen, f"H = {self._h_value:+.4f}", Vector2(ui_x, ui_y))
        ui_y += 45

        # Power-up status.
        power_status = "ON" if self._has_powerup else "OFF"
        Utilities.draw_outlined_text(self._screen, f"Power-up: {power_status}", Vector2(ui_x, ui_y))
        ui_y += 45

        features = [
            f"Distance: {Utilities.manhattan_distance(self._agent.position, self._player.position)}",
            f"Time: {self._powerup_timer:.2f}s" if self._has_powerup else "Time: 0.00s",
            f"To Powerup: {self._world.get_distance_to_nearest_powerup(self._player.position)}"
        ]

        for feature in features:
            Utilities.draw_outlined_text(self._screen, feature, Vector2(ui_x, ui_y))
            ui_y += 25

        ui_y += 55

        # Controls.
        Utilities.draw_outlined_text(self._screen, "====== Controls ======", Vector2(ui_x, ui_y))
        ui_y += 35

        controls = [
            "Drag: Move entities",
            "Space: Toggle power-up",
            "Up/Down: Adjust time",
            "R: Reset",
            "ESC: Quit"
        ]

        for control in controls:
            Utilities.draw_outlined_text(self._screen, control, Vector2(ui_x, ui_y))
            ui_y += 22

    def _draw(self):
        """
        Draws the world, entities, and UI.
        """
        self._screen.fill((255, 255, 255))

        self._world.draw(self._screen)
        self._player.draw(self._screen)
        self._agent.draw(self._screen)
        self.draw_ui()

        pygame.display.flip()

    def run(self):

        """
        Main simulation loop.
        """

        while self._running:

            self._clock.tick(config.FPS)
            self._handle_input()
            self._draw()

        pygame.quit()
        sys.exit()