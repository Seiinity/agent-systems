from dataclasses import dataclass


@dataclass(frozen=True)
class World:
    """
    Represents the world.

    Attributes
    ----------
    nodes : list[str]
        A list of available nodes.
    connections : list[tuple[str, str]]
        A list of tuples representing the connections between nodes.
    locked_connections : list[tuple[str, str]]
        A list of tuples representing which connections are locked.
    key : str | None
        The name of the node which contains the key.
    """

    nodes: list[str]
    connections: list[tuple[str, str]]
    locked_connections: list[tuple[str, str]]
    key: str | None
