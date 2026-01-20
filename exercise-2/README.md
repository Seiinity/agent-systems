# Exercise 2 - Uniform Cost Search
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pygame](https://img.shields.io/badge/Pygame-2.6.0-5AA816.svg?style=flat)](https://www.pygame.org/news)

## Overview

An agent (adventurer) must navigate through a dungeon with 7 rooms to reach the goal. The dungeon has the following characteristics:

- **Start:** Room S;
- **Goal:** Room G  ;
- **Key Location:** Room E;
- **Locked Passage:** The passage from C to G requires the key.

![Thumbnail](https://i.imgur.com/w7RScyt.png)

### Graph Structure

**Nodes:** `{S, A, B, C, D, E, G}`

**Connections (bidirectional):**
- S-A, S-B;
- A-C;
- B-C, B-D;
- C-G (locked), C-D;
- D-E.

**Edge Cost:** 1 (all edges)

## State Representation

The state space consists of:

- **State:** `(position, hasKey)`:
  - `position ∈ {S, A, B, C, D, E, G}`;
  - `hasKey ∈ {false, true}`.

- **Initial State:** `(S, false)`;
- **Goal Condition:** `position == G`.

### State Space Size

- 7 positions × 2 key states = **14 possible states**;
- However, not all states are reachable due to the locked door constraint.

## Algorithm: Uniform Cost Search (UCS)

### Rules

1. Start with root node `{S, false}` at cost 0;
2. Expand children in alphabetical neighbor order;
3. Always expand the node with the lowest path cost first;
4. If reaching a state already seen with a higher cost, discard the worst one;
5. Reaching room E flips `hasKey` to `true`.

### Key Constraints

- Cannot traverse C→G without the key;
- The key is automatically picked up when visiting room E;
- Once the key is obtained, it remains in possession.

## Solution

Below is the solution to this problem.<br/>
It is also available in ``tree.pdf``.

![Solution](https://i.imgur.com/Ji8VuLR.png)

## Reflection Questions

### 1. Why is `(pos, hasKey)` enough?

The state `(position, hasKey)` captures all the information needed to determine:
- Where the agent is;
- Whether they can pass through the locked door;
- If they've already collected the key.

**What would happen without `hasKey`?**
Without the `hasKey` component:
- The algorithm would not distinguish between "being at D without key" and "being at D with key";
- The problem becomes unsolvable as, after reaching E, going back to D would be an already existing state with a higher cost.

### 2. Where do conditional edges affect the tree?

The conditional edge C→G affects the search tree by making it so that G is not added as a child when expanding from C without having the key.

### 3. How would a second key change the state space?

With a second key or locked door:
- The state space would become `7 × 2 × 2 = 28` states;
- The state representation would need `(position, hasKey1, hasKey2)`;
- There would be multiple conditional edges to track.

For `n` keys, the state space would be `7 × 2^n` states.

## Simulator

A simulator was included to validate my solution.<br/>
The solution was first hand-crafted and then validated through the simulator, not the other way around.<br/>

Variables in the simulator can be changed to form different graphs.

### Running the Code

```bash
python src/main.py
```

### Expected Output

The program will:
1. Show the search process (nodes expanded with costs);
2. Print the optimal solution path;
3. Display total cost and path length.
