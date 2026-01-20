import heapq

from world import World
from state import State


class Simulator:

    def __init__(self) -> None:

        self._world = World(
            nodes=["S", "A", "B", "C", "D", "E", "G"],
            connections=[
                ("S", "A"),
                ("S", "B"),
                ("A", "C"),
                ("B", "C"),
                ("B", "D"),
                ("C", "G"),
                ("C", "D"),
                ("D", "E"),
            ],
            locked_connections=[("C", "G")],
            key="E",
        )

    def _get_neighbours(self, position: str, has_key: bool) -> list[str]:
        """
        Gets all the neighbours of the explorer's current node.

        Parameters
        ----------
        position : str
            The position to get neighbours for.
        has_key : bool
            Whether the explorer has picked up the key.

        Returns
        -------
        list[str]
            A list containing the neighbour nodes.

        Notes
        -----
        Neighbours from locked connections are omitted unless ``has_key``
        is ``True``.
        """

        neighbors = []

        for a, b in self._world.connections:

            if position in (a, b):

                neighbor = b if a == position else a

                # Checks if the edge is locked (bidirectional).
                if not has_key and (
                        (position, neighbor) in self._world.locked_connections or
                        (neighbor, position) in self._world.locked_connections
                ):
                    continue

                neighbors.append(neighbor)

        return sorted(neighbors)

    def _build_tree(self) -> tuple[list[State] | None, int, dict]:
        """
        Builds the search tree using Uniform Cost Search.

        Returns
        -------
        tuple[list[State] | None, int, dict]
            A tuple containing:
            - The path to the goal (list of states) or None if no path found;
            - The total cost of the path;
            - A dictionary with the search tree information for visualization.
        """

        # Creates a priority queue (cost, state, path).
        initial_state: State = State(position="S", has_key=False)
        frontier = [(0, initial_state, [initial_state])]

        # This will store the best cost to reach each state.
        best_cost: dict[State, int] = {initial_state: 0}

        # For tree visualisation...
        tree_info = {
            "nodes": [],  # List of (state, cost, parent_state).
            "goal_state": None,
            "goal_path": None,
            "goal_cost": None,
        }

        # Adds the root node to the tree.
        tree_info["nodes"].append((initial_state, 0, None))

        while frontier:

            current_cost, current_state, path = heapq.heappop(frontier)

            # Skips this if there's a better path to this state already.
            if current_cost > best_cost.get(current_state, float("inf")):
                continue

            # Checks if the adventurer has reached the goal.
            if current_state.position == "G" and current_state.has_key:

                tree_info["goal_state"] = current_state
                tree_info["goal_path"] = path
                tree_info["goal_cost"] = current_cost
                return path, current_cost, tree_info

            # Expands the neighbour nodes.
            neighbors = self._get_neighbours(current_state.position, current_state.has_key)

            for neighbor in neighbors:

                # Determines if the key can be picked up.
                new_has_key = current_state.has_key or (neighbor == self._world.key)

                # Creates a new state.
                new_state = State(position=neighbor, has_key=new_has_key)
                new_cost = current_cost + 1  # Edge cost is always 1.

                # Only adds this path if it costs less than other existing paths.
                if new_cost < best_cost.get(new_state, float("inf")):

                    best_cost[new_state] = new_cost
                    new_path = path + [new_state]
                    heapq.heappush(frontier, (new_cost, new_state, new_path))

                    # Adds to the tree for visualisation.
                    tree_info["nodes"].append((new_state, new_cost, current_state))

        # If there's no path, just returns this.
        return None, -1, tree_info

    def run(self):
        """
        Runs the UCS algorithm and prints the results.
        """

        path, cost, tree_info = self._build_tree()

        if path:

            print(
                f"\nPath: {' -> '.join([f'({s.position}, key={s.has_key})' for s in path])}"
            )
            print(f"Total cost: {cost}")

            print("\n=== Search Tree ===")
            for state, state_cost, parent in tree_info["nodes"]:
                parent_str = (
                    f"({parent.position}, key={parent.has_key})" if parent else "ROOT"
                )
                print(
                    f"State: ({state.position}, key={state.has_key}), Cost: {state_cost}, Parent: {parent_str}"
                )

        else:

            print("No path found...")
