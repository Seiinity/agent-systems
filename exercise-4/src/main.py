"""
Tic-Tac-Toe + MCTS Skeleton (for students)
------------------------------------------
Goal: Implement Monte Carlo Tree Search inside the MCTS class.

You have everything you need:
- A minimal Tic-Tac-Toe environment (GameState) with helper methods.
- A Node structure to store tree statistics.
- An MCTS class with clearly marked to-do blocks for each MCTS phase:
    1) Selection
    2) Expansion
    3) Simulation (rollout)
    4) Backpropagation
- A simple CLI runner so you can play Human vs. MCTS once you implement it.
- A quick unit test to sanity-check the game logic.

Conventions:
- Players are 1 (X) and -1 (O). Empty = 0.
- Rewards are from the perspective of the root player (the player to move at the root).
  Suggested: win = 1.0, draw = 0.5, loss = 0.0  (feel free to change).
- The "best move" returned by search() is the child with the highest visit count.

Recommended reading order:
- GameState
- Node
- MCTS (fill in the TODOs)
- The runner at the bottom (you can comment it out during development).

"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Dict
import math
import random
import copy

# ----------------------------
# Tic-Tac-Toe Game Definition
# ----------------------------


@dataclass
class GameState:
    """
    A simple Tic-Tac-Toe state.
    Board: 3x3 with values in {1 (X), -1 (O), 0 (empty)}.
    player_to_move: 1 for X, -1 for O.
    """

    board: List[int] = field(default_factory=lambda: [0] * 9)
    player_to_move: int = 1  # 1 = X, -1 = O

    def legal_moves(self) -> List[int]:
        """Return a list of indices (0..8) where a move can be played."""
        return [i for i, v in enumerate(self.board) if v == 0]

    def play(self, move: int) -> "GameState":
        """Return the next state after playing 'move' (0..8)."""
        if self.board[move] != 0:
            raise ValueError(f"Illegal move: {move}")
        next_board = self.board.copy()
        next_board[move] = self.player_to_move
        return GameState(next_board, -self.player_to_move)

    def winner(self) -> Optional[int]:
        """Return 1 if X wins, -1 if O wins, None otherwise (including draw/incomplete)."""
        lines = [
            (0, 1, 2),
            (3, 4, 5),
            (6, 7, 8),  # rows
            (0, 3, 6),
            (1, 4, 7),
            (2, 5, 8),  # cols
            (0, 4, 8),
            (2, 4, 6),  # diagonals
        ]
        for a, b, c in lines:
            s = self.board[a] + self.board[b] + self.board[c]
            if s == 3:
                return 1
            if s == -3:
                return -1
        return None

    def is_terminal(self) -> bool:
        """Return True if the game ended (win or draw)."""
        if self.winner() is not None:
            return True
        return all(v != 0 for v in self.board)

    def result_from_perspective(self, root_player: int) -> float:
        """
        Return a reward from the perspective of 'root_player'.
        Suggested mapping: win=1.0, draw=0.5, loss=0.0.
        """
        w = self.winner()
        if w is None:
            # draw if board is full, otherwise not terminal
            if all(v != 0 for v in self.board):
                return 0.5
            raise ValueError("Called result on non-terminal state")
        if w == root_player:
            return 1.0
        else:
            return 0.0

    def pretty(self) -> str:
        """Human-readable board."""
        symbol = {1: "X", -1: "O", 0: " "}
        rows = []
        for r in range(3):
            row = [symbol[self.board[3 * r + c]] for c in range(3)]
            rows.append(" | ".join(row))
        return "\n---------\n".join(rows)


# ----------------------------
# MCTS Tree Node
# ----------------------------


class Node:
    """
    Node in the MCTS tree.
    Stores statistics for UCB selection and links to children.
    """

    def __init__(
        self,
        state: GameState,
        parent: Optional["Node"] = None,
        move: Optional[int] = None,
    ):
        self.state: GameState = state
        self.parent: Optional[Node] = parent
        self.move: Optional[int] = move  # the move that led from parent -> this node
        self.children: Dict[int, Node] = {}  # move -> Node
        self.untried_moves: List[int] = state.legal_moves()
        self.visits: int = 0
        self.value_sum: float = 0.0  # cumulative value from root player's perspective

    def is_fully_expanded(self) -> bool:
        return len(self.untried_moves) == 0

    def best_child_by_visit(self) -> "Node":
        """Return the child with the highest visit count (final action selection)."""
        if not self.children:
            raise ValueError("No children to choose from.")
        return max(self.children.values(), key=lambda n: n.visits)

    def average_value(self) -> float:
        return 0.0 if self.visits == 0 else self.value_sum / self.visits


# ----------------------------
# MCTS Skeleton (fill the TODOs)
# ----------------------------


class MCTS:
    """
    Monte Carlo Tree Search skeleton.
    Fill in the four phases inside the corresponding methods:
      - _select
      - _expand
      - _simulate
      - _backpropagate

    Usage:
        mcts = MCTS(iterations=500, c=math.sqrt(2))
        best_move = mcts.search(root_state)
    """

    def __init__(self, iterations: int = 500, c: float = math.sqrt(2)):
        self.iterations = iterations
        self.c = c  # exploration constant

    # ---------------
    # Public API
    # ---------------
    def search(self, root_state: GameState) -> int:
        """
        Run MCTS from 'root_state' and return the chosen move.
        Recommended policy: return the child with the highest visit count.
        """
        root = Node(copy.deepcopy(root_state))

        for _ in range(self.iterations):
            node = self._select(root)  # (1) Selection
            leaf = self._expand(node)  # (2) Expansion
            reward = self._simulate(leaf, root_state)  # (3) Simulation (rollout)
            self._backpropagate(leaf, reward, root_state)  # (4) Backpropagation

        # Final action: pick the child with the most visits
        return root.best_child_by_visit().move

    # ---------------
    # (1) Selection
    # ---------------
    def _select(self, node: Node) -> Node:
        """
        Traverse the tree from 'node' down to a leaf by applying UCB1 on fully-expanded nodes.
        Stop when you find a node with untried moves or a terminal state.

        IMPLEMENTATION TIPS:
        - While node is non-terminal and fully expanded, choose child with highest UCB.
        - Calculate UCB of child --> Look at Node Functions and use them
        - IMPORTANT: Make sure to handle zero-visit children safely (though fully expanded implies >0 visits).
        """

        while not node.state.is_terminal() and node.is_fully_expanded():

            # Calculates UCB1 for each child and selects the best.
            best_ucb = -float("inf")
            best_child = None
            for child in node.children.values():

                # Prioritises unvisited children.
                if child.visits == 0:
                    ucb = float("inf")

                # Applies the UCB1 formula.
                else:
                    exploitation = child.average_value()
                    exploration = self.c * math.sqrt(
                        math.log(node.visits) / child.visits
                    )
                    ucb = exploitation + exploration

                if ucb > best_ucb:
                    best_ucb = ucb
                    best_child = child

            node = best_child

        return node

    # ---------------
    # (2) Expansion
    # ---------------
    def _expand(self, node: Node) -> Node:
        """
        If node is terminal, nothing to expand -> return node.
        Else, pop one untried move, create the corresponding child, and return it.

        IMPLEMENTATION TIPS:
        - If node has untried_moves, take one (random choice is fine), create child, attach, and return child.
        - If node is terminal or fully expanded, just return the node itself.
        """

        # If the node is terminal or fully expanded, returns the node itself.
        if node.state.is_terminal() or node.is_fully_expanded():
            return node

        # Picks a random untried move.
        move = random.choice(node.untried_moves)
        node.untried_moves.remove(move)

        # Creates the child state and node.
        child_state = node.state.play(move)
        child_node = Node(child_state, parent=node, move=move)

        # Adds the child to the parent's children dict.
        node.children[move] = child_node

        return child_node

    # ---------------
    # (3) Simulation (Rollout)
    # ---------------
    def _simulate(self, node: Node, root_state: GameState) -> float:
        """
        From 'node', play random moves until a terminal state is reached.
        Return the reward from the perspective of the root player (root_state.player_to_move).

        IMPLEMENTATION TIPS:
        - Copy the state's board to avoid mutating the tree state (use copy.deepcopy(node.state)).
        - While not terminal: choose a random legal move and play.
        - Map terminal outcome to a reward (e.g., win=1, draw=0.5, loss=0).
        - (Optional) implement a simple heuristic instead of random to reduce variance.
        """

        # Copies the state to avoid mutating the tree.
        state = copy.deepcopy(node.state)

        # Plays random moves until the node is terminal.
        while not state.is_terminal():
            move = random.choice(state.legal_moves())
            state = state.play(move)

        # Returns the reward from the root player's perspective.
        root_player = root_state.player_to_move
        return state.result_from_perspective(root_player)

    # ---------------
    # (4) Backpropagation
    # ---------------
    def _backpropagate(self, node: Node, reward: float, root_state: GameState) -> None:
        """
        Propagate 'reward' from the leaf up to the root.
        IMPORTANT: reward is always from the root player's perspective.

        IMPLEMENTATION TIPS:
        - Walk up via parent links until None.
        - At each node: increment vistis and value_sum to update (no sign flip needed if reward already from root).
        - If you choose a different reward convention, adjust here accordingly.
        """

        # Moves up the tree from leaf to root.
        while node is not None:
            node.visits += 1
            node.value_sum += reward
            node = node.parent


# ----------------------------
# Simple Baselines / Helpers
# ----------------------------


def random_agent(state: GameState) -> int:
    """Picks a legal move uniformly at random."""
    return random.choice(state.legal_moves())


def play_game(p1_policy, p2_policy, verbose: bool = False) -> int:
    """
    Play a complete game. Policies are callables(state)->move.
    Returns the winner: 1 (X), -1 (O), or 0 for draw.
    """
    state = GameState()
    while not state.is_terminal():
        if state.player_to_move == 1:
            move = p1_policy(state)
        else:
            move = p2_policy(state)
        state = state.play(move)
        if verbose:
            print(state.pretty(), "\n")

    w = state.winner()
    return 0 if w is None else w


# ----------------------------
# Quick Sanity Tests
# ----------------------------


def _test_environment():
    # Check moves and terminal logic in a quick scenario
    s = GameState()
    assert len(s.legal_moves()) == 9
    s = s.play(0).play(4).play(1).play(8).play(2)  # X:0,1,2 wins on top row
    assert s.is_terminal()
    assert s.winner() == 1


def _quick_self_check():
    # Random vs Random to ensure runner works
    res = play_game(random_agent, random_agent, verbose=True)
    assert res in (-1, 0, 1)


# ----------------------------
# CLI Runner
# ----------------------------


def human_vs_mcts():
    """
    Play in terminal: Human (O) vs MCTS (X).
    Run this AFTER implementing MCTS.search().
    """
    mcts = MCTS(iterations=1000, c=math.sqrt(2))
    state = GameState()
    print("You are O. Enter moves as indices 0..8.")
    print("Index map:\n0 1 2\n3 4 5\n6 7 8\n")

    while not state.is_terminal():
        if state.player_to_move == 1:
            move = mcts.search(state)
            state = state.play(move)
            print(f"\nMCTS plays: {move}")
            print(state.pretty())
        else:
            print("\nYour turn (O). Legal:", state.legal_moves())
            while True:
                try:
                    mv = int(input("Move (0..8): "))
                    if mv in state.legal_moves():
                        break
                except Exception:
                    pass
                print("Invalid move. Try again.")
            state = state.play(mv)
            print(state.pretty())

    w = state.winner()
    if w is None:
        print("\nDraw!")
    elif w == 1:
        print("\nMCTS (X) wins!")
    else:
        print("\nHuman (O) wins!")


if __name__ == "__main__":
    # Run quick checks:
    _test_environment()
    _quick_self_check()
    print("Environment OK. To play: call human_vs_mcts()")
    # Uncomment to play in terminal:
    human_vs_mcts()
