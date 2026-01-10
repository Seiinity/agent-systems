# Exercise 1 - Chase vs. Flee Heuristic
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/Python-3.13-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pygame](https://img.shields.io/badge/Pygame-2.6.0-5AA816.svg?style=flat)](https://www.pygame.org/news)

## Overview

This project implements a **Chase vs. Flee heuristic** for an agent in a grid-based world. The goal is for the agent to dynamically decide whether it should chase the player or flee, based on the current game state.

The system is deterministic and uses a linear weighted heuristic built from normalised features.

An interactive simulator built with Pygame allows for the testing of the heuristic in real time by moving the player and the agent and toggling power-ups.

![Thumbnail](https://i.imgur.com/M3sFmKK.png)

## Heuristic Design

### Chosen Features

The following are the features chosen to calculate the heuristic:

1. **Time left on power-up:** how much time the player has left on the power-up.
2. **Player's distance to power-up:** the distance of the player to the closest power-up.
3. **Distance to player:** measures how close the agent is to the player.

Together, these features cover immediate threats and future possibilities.

### Feature Normalisation

All features are normalised to $[0, 1]$.

| Feature                       | Normalisation                         |
|-------------------------------|---------------------------------------|
| Time left on power-up         | ``time_remaining / MAX_POWERUP_TIME`` |
| Player's distance to power-up | ``distance / MAX_MANHATTAN``          |
| Distance to player            | ``distance / MAX_MANHATTAN``          |


### Weights

| Feature                       | Weight | Reasoning                                                                                                                                                                                                                                                                                                                                                                                                                 |
|-------------------------------|--------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Time left on power-up         | 0.55   | This is the biggest danger. If the player has a lot of time left on their power-up, the agent should just flee. Otherwise, if the time left is short, there might be situations in which the agent can start chasing the player again.                                                                                                                                                                                    |
| Player's distance to power-up | 0.40   | This is used to predict future risk. The closer the player is to a power-up, the more likely they are to pick it up. In these cases, it might be a good idea for the agent to start fleeing preemptively. It is not as critical as whether the player is actually powered-up or not, but still a big thing to factor in.                                                                                                  |
| Distance to player            | 0.05   | This is the metric used in conjunction with the other two. As such, it has a small weight. If the weight were bigger, it would prevent the agent from ever getting too close to the player, regardless of the situation. However, it is a good idea for the agent to stay away from the player if it is to close to them and the player either has a lot of time remaining on their power-up or are about to collect one. |

### Heuristic Formula

Considering all the above factors, the formula to calculate the cost is simply:

$$C = (0.55 * T)$$

The formula to calculate the reward is:

$$R = (0.40 * D_{powerup}) + (0.05 * D_{player})$$

Additionally, a bias of $-0.05$ is applied in order to better balance the final formula. Therefore, the formula to calculate the heuristic value (desirability) is:

$$H = R - C + b = (0.40 * D_{powerup}) + (0.05 * D_{player}) -(0.55 * T) - 0.05$$

where:

- $T$ is the time remaining on the player's power-up;
- $D_{powerup}$ is the distance from the player to the closest power-up;
- $D_{player}$ is the distance from the agent to the player.

If $H > 0.0$, the agent should chase the player. Otherwise, it should flee.

## Manual Calculation (4 Scenarios)

Below, I manually calculate the heuristic value for four different scenarios.<br/>
For each scenario, the following grid is considered:
```
┌───┬───┬───┬───┬───┬───┬───┬───┐
│   │   │   │   │   │ ● │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │ █ │ █ │   │   │ █ │ █ │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │ █ │ ● │   │   │   │ █ │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │ █ │ █ │   │   │ ● │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │   │   │ █ │ █ │   │   │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │ █ │   │   │   │ ● │ █ │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │ █ │ █ │   │   │ █ │ █ │   │
├───┼───┼───┼───┼───┼───┼───┼───┤
│   │ ● │   │   │   │   │   │   │
└───┴───┴───┴───┴───┴───┴───┴───┘

● = Power-up
█ = Wall
```

In this case:

- ``MAX_MANHATTAN`` is 14.
- ``MAX_POWERUP_TIME`` is 10.

The top-left cell has coordinates $(0, 0)$.
The bottom-right cell has coordinates $(7, 7)$.

### Scenario 1

In this scenario, the player has no power-up and is far from any power-up:

- Player position: $(0, 0)$
- Agent position: $(7, 7)$
- Nearest power-up to player: $(2, 2)$
  - Distance to player: $∣0−2∣+∣0−2∣=4$
- Distance from player to agent: $∣7−0∣+∣7−0∣=14$
- Power-up time left: $0$

Normalised values:

- $D_{powerup} = 4/14 \approx 0.29$
- $D_{player} = 14/14 = 1.0$
- $T = 0/10 = 0$

$$H = R - C + b = (0.40 * D_{powerup}) + (0.05 * D_{player}) -(0.55 * T) - 0.05$$
$$H = (0.40⋅0.29)+(0.05⋅1.0)−(0.55*0)−0.05 \approx 0.116$$

Since $0.116 > 0$, the agent will decide to chase the player.

### Scenario 2

In this scenario, the player has a power-up with 5 seconds remaining and the agent is somewhat close to it:

- Player position: $(0, 0)$
- Agent position: $(4, 2)$
- Nearest power-up to player: $(2, 2)$
  - Distance to player: $∣0−2∣+∣0−2∣=4$
- Distance from player to agent: $∣4−0∣+∣2−0∣=6$
- Power-up time left: $5$

Normalised values:

- $D_{powerup} = 4/14 \approx 0.29$
- $D_{player} = 6/14 \approx 0.43$
- $T = 5/10 = 0.5$

$$H = R - C + b = (0.40 * D_{powerup}) + (0.05 * D_{player}) -(0.55 * T) - 0.05$$
$$H = (0.40⋅0.29)+(0.05⋅0.43)−(0.55*0.5)−0.05 \approx -0.1875$$

Since $-0.1875 \leq 0$, the agent will decide to flee from the player.

### Scenario 3

This scenario is very similar to scenario 2. The difference here is that the player only has 1.5 seconds left on their power-up:

- Player position: $(0, 0)$
- Agent position: $(4, 2)$
- Nearest power-up to player: $(2, 2)$
  - Distance to player: $∣0−2∣+∣0−2∣=4$
- Distance from player to agent: $∣4−0∣+∣2−0∣=6$
- Power-up time left: $1.5$

Normalised values:

- $D_{powerup} = 4/14 \approx 0.29$
- $D_{player} = 6/14 \approx 0.43$
- $T = 1.5/10 = 0.15$

$$H = R - C + b = (0.40 * D_{powerup}) + (0.05 * D_{player}) -(0.55 * T) - 0.05$$
$$H = (0.40⋅0.29)+(0.05⋅0.43)−(0.55*0.15)−0.05 \approx 0.005$$

Since $0.005 > 0$, the agent will decide to chase the player. This shows that it believes that, by the time it reaches the player, the power-up will have run out.

### Scenario 4

In this scenario, the player is close to a power-up and the agent is close to the player:

- Player position: $(4, 0)$
- Agent position: $(0, 1)$
- Nearest power-up to player: $(5, 0)$
  - Distance to player: $∣4−5∣+∣0−0∣=1$
- Distance from player to agent: $∣0−4∣+∣1−0∣=5$
- Power-up time left: $0$

Normalised values:

- $D_{powerup} = 1/14 \approx 0.07$
- $D_{player} = 5/14 \approx 0.36$
- $T = 0/10 = 0$

$$H = R - C + b = (0.40 * D_{powerup}) + (0.05 * D_{player}) -(0.55 * T) - 0.05$$
$$H = (0.40⋅0.07)+(0.05⋅0.36)−(0.55*0)−0.05 \approx -0.004$$

Since $-0.004 \leq 0$, the agent will decide to flee from the player. This shows that it believes that it is too close to the player, and that it needs to start fleeing as the player is about to collect a power-up.

## Considerations

With a linear heuristic, it is impossible to write actual conditional logic. With non-linear heuristics, it might be easier to explicitly tell the agent "if the player has a power-up, it is important to stay away from it, but, if the player does not have a power-up, stay close to it". 

With my implementation, the distance-to-player heuristic always tells the agent "the farther you are from the player the better". The bias and other weights help it chase the player regardless of this when the right conditions are met.

Additionally, in the future, it might be nice to experiment with distances other than the Manhattan distance, and experiment with proper pathfinding (considering walls, for example).

## Simulator

Included is a simulator to simulate these calculations are various positions. A Linux executable is included. For other operating systems, the simulator must be built and run from the source code.

