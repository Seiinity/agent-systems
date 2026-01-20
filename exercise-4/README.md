# Exercise 4: MCTS
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pygame](https://img.shields.io/badge/Pygame-2.6.0-5AA816.svg?style=flat)](https://www.pygame.org/news)

## Overview

This exercise implements **Monte Carlo Tree Search (MCTS)** for Tic-Tac-Toe.<br/>
The four core MCTS phases were completed to create an AI agent capable of playing optimally.

## Structure

```
main.py
├── GameState      # Tic-Tac-Toe environment with board logic.
├── Node           # Tree node storing visit counts and values.
├── MCTS           # Search algorithm (what I implemented).
└── CLI Runner     # Human vs MCTS gameplay.
```

## MCTS Phases

| Phase               | Method             | Description                                                 |
|---------------------|--------------------|-------------------------------------------------------------|
| **Selection**       | `_select()`        | Traverse tree using UCB1 until reaching an expandable node. |
| **Expansion**       | `_expand()`        | Add a new child node for an untried move.                   |
| **Simulation**      | `_simulate()`      | Random moves to terminal state.                             |
| **Backpropagation** | `_backpropagate()` | Update visits and values from leaf to root.                 |

## Usage

```bash
python main.py
```

The game uses indices 0-8 for moves:
```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

## Mathematical Principle

The UCB1 formula is as follows:

$$u_{i} = \frac{w_i}{n_i} + c \sqrt{\frac{\ln N}{n_{i}}}$$

Where:

- $w_i$ is the accumulated reward for child node $i$;
- $n_i$ is the number of visits to child node $i$;
- $c$ is the exploration constant that controls the trade-off between exploration and exploitation;
- $N$ is the number of visits to the parent node.