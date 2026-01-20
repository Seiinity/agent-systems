from dataclasses import dataclass


@dataclass(frozen=True)
class State:
    """
    Represents a state.

    Attributes
    ----------
    position : str
        The explorer's current room (S, A, B, C, D, E, or G).
    has_key : bool
        Whether the explorer has picked up the key.
    """

    position: str
    has_key: bool

    def __lt__(self, other):
        """For priority queue ordering."""
        return (self.position, self.has_key) < (other.position, other.has_key)
