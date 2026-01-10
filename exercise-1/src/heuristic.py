import config

from enum import Enum
from utilities import Utilities
from world import World
from pygame import Vector2


class Features:

    """
    Stores the features required for the heuristic.
    """

    def __init__(
        self,
        player_dist: int,
        powerup_time: float,
        powerup_dist: int
    ):

        self.player_dist = player_dist
        self.powerup_time = powerup_time
        self.powerup_dist = powerup_dist

        self._normalise()

    def _normalise(self) -> None:

        """
        Normalises the features to a range of [0, 1].
        """

        self.player_dist = self.player_dist / config.MAX_MANHATTAN
        self.powerup_time = min(self.powerup_time, config.MAX_POWERUP_TIME) / config.MAX_POWERUP_TIME
        self.powerup_dist = self.powerup_dist / config.MAX_MANHATTAN


class Decision(Enum):

    CHASE = 0
    FLEE = 1


class ChaseFleeHeuristic:

    """
    Heuristic for deciding whether the agent should chase the player
    or flee from them.
    """

    def __init__(self, world: World):

        self._world = world

    def _calculate(
            self,
            position: Vector2,
            player_position: Vector2,
            powerup_timer: float
    ) -> float:

        """
        Calculates the heuristic value.

        Parameters
        ----------
        position : Vector2
            The position of the agent.
        player_position : Vector2
            The position of the player.
        powerup_timer : float
            The time remaining on the player's powerup.

        Returns
        -------
        float
            The heuristic value.
        """

        # Extracts raw features.
        player_dist: int = Utilities.manhattan_distance(position, player_position)
        powerup_dist: int = self._world.get_distance_to_nearest_powerup(player_position)

        print(player_dist, powerup_dist)

        # Normalises the features.
        features: Features = Features(
            player_dist,
            powerup_timer,
            powerup_dist
        )




        bias: float = -0.05
        print(f"({config.WEIGHT_POWERUP_DIST} * {features.powerup_dist:.2f}) + ({config.WEIGHT_PLAYER_DIST} * {features.player_dist:.2f}) -({config.WEIGHT_TIME} * {features.powerup_time:.2f}) + {bias}")

        # Calculates the heuristic.
        value: float = (
            + config.WEIGHT_POWERUP_DIST * features.powerup_dist
            + config.WEIGHT_PLAYER_DIST * features.player_dist
            - config.WEIGHT_TIME * features.powerup_time
            + bias
        )

        print(value)

        return value

    def decide(
        self,
        position: Vector2,
        player_position: Vector2,
        powerup_timer: float
    ) -> tuple[Decision, float]:

        """
        Makes a decision based on the heuristic value.

        Parameters
        ----------
        position : Vector2
            The position of the agent.
        player_position : Vector2
            The position of the player.
        powerup_timer : float
            The time remaining on the player's powerup.

        Returns
        -------
        Decision
            The decision to take.

        """

        value: float = self._calculate(position, player_position, powerup_timer)

        if value > 0.0:
            return Decision.CHASE, value
        else:
            return Decision.FLEE, value
