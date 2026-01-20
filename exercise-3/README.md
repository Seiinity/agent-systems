# Exercise 3: Minimax with Static Evaluation

## Overview

Mini-Connect-3 is played on a 3x3 grid where players drop pieces vertically.<br/>
The goal is to connect 3 pieces in a row (horizontal, vertical, or diagonal).

### Proposed Features

| Feature               | Symbol        | Description                                        | Weight       |
|-----------------------|---------------|----------------------------------------------------|--------------|
| **Center Control**    | $\theta_1(s)$ | Pieces in center column.                           | $w_1$ = +3   |
| **Our Threats**       | $\theta_2(s)$ | Our "almost wins" (2 aligned + 1 reachable empty). | $w_2$ = +4   |
| **Opponent Threats**  | $\theta_3(s)$ | The opponent's "almost wins".                      | $w_3$ = -4   |
| **Vertical Pressure** | $\theta_4(s)$ | Two stacked pieces with free cell above.           | $w_4$ = +2   |
| **Terminal State**    | $\theta_5(s)$ | Win/Loss/Draw detection.                           | $w_5$ = ±100 |

### Evaluation Function Formula

$$f(s) = 3 \cdot \theta_1(s) + 4 \cdot \theta_2(s) - 4 \cdot \theta_3(s) + 2 \cdot \theta_4(s) + 100 \cdot \theta_5(s)$$

### Feature Explanations

#### $\theta_1$: Center Control ($w = 3$)
The center column provides the most connectivity options (can contribute to horizontal, vertical, and both diagonals).<br/>
Controlling it gives significant strategic advantage.

```
Good for X:          Bad for X:
+---+---+---+        +---+---+---+
| . | X | . |        | . | O | . |
+---+---+---+        +---+---+---+
```

#### $\theta_2$: Our Threats ($w = 4$)
Having two pieces aligned with one empty cell that could complete a win creates immediate pressure on the opponent.

```
X Threat (horizontal):    X Threat (vertical):
+---+---+---+             +---+---+---+
| X | X | . | ← can win   | . | . | . | ← can win above
+---+---+---+             +---+---+---+
                          | . | . | X |
                          +---+---+---+
                          | . | . | X | 
                          +---+---+---+
```

#### $\theta_3$: Opponent Threats ($w = -4$)
Same as θ₂ but for the opponent. Negative weight because opponent threats are disadvantageous.

#### $\theta_4$: Vertical Pressure ($w = 2$)
Two pieces stacked with a free cell above. This is valuable because:
- It's a direct path to winning vertically;
- The opponent must eventually block or lose.

#### $\theta_5$: Terminal State ($w = ±100$)
- **Win**: +100 (strongly positive);
- **Loss**: -100 (strongly negative);  
- **Draw**: 0 (neutral).

## Tree Enumeration

With $\text{depth}=2$...

![Thumbnail](https://i.imgur.com/CCTpvpe.png)

For this example...

### Evaluation Function Reminder

$$f(s) = 3 \cdot \theta_1 + 4 \cdot \theta_2 - 4 \cdot \theta_3 + 2 \cdot \theta_4$$

Where:
- $\theta_1$: Center control (pieces in column 1);
- $\theta_2$: X's two-in-a-row threats;
- $\theta_3$: O's two-in-a-row threats;  
- $\theta_4$: Vertical pressure.

$\theta_5$ is ignored as there's no terminal condition.

---

### State-by-State Evaluation

#### Branch 1: X plays Left (Column 0)

| State | Board                 | Center (X) | Center (O) | Threats | $f(s)$ |
|-------|-----------------------|------------|------------|---------|--------|
| **1** | O stacked on X (left) | 0          | 0          | None    | **0**  |
| **2** | X left, O center      | 0          | 1          | None    | **-3** |
| **3** | X left, O right       | 0          | 0          | None    | **0**  |

**O chooses State 2** (minimum = -3)

---

#### Branch 2: X plays Center (Column 1)

| State | Board                   | Center (X) | Center (O) | Threats | $f(s)$ |
|-------|-------------------------|------------|------------|---------|--------|
| **4** | X center, O left        | 1          | 0          | None    | **+3** |
| **5** | O stacked on X (center) | 1          | 1          | None    | **0**  |
| **6** | X center, O right       | 1          | 0          | None    | **+3** |

**O chooses State 5** (minimum = 0)

---

#### Branch 3: X plays Right (Column 2)

| State | Board                  | Center (X) | Center (O) | Threats | $f(s)$ |
|-------|------------------------|------------|------------|---------|--------|
| **7** | X right, O left        | 0          | 0          | None    | **0**  |
| **8** | X right, O center      | 0          | 1          | None    | **-3** |
| **9** | O stacked on X (right) | 0          | 0          | None    | **0**  |

**O chooses State 8** (minimum = -3)

---

### Summary Table

| State | Configuration      | θ₁ (center diff) | $f(s)$ |
|-------|--------------------|------------------|--------|
| 1     | X,O stacked left   | 0 - 0 = 0        | **0**  |
| 2     | X left, O center   | 0 - 1 = -1       | **-3** |
| 3     | X left, O right    | 0 - 0 = 0        | **0**  |
| 4     | X center, O left   | 1 - 0 = +1       | **+3** |
| 5     | X,O stacked center | 1 - 1 = 0        | **0**  |
| 6     | X center, O right  | 1 - 0 = +1       | **+3** |
| 7     | X right, O left    | 0 - 0 = 0        | **0**  |
| 8     | X right, O center  | 0 - 1 = -1       | **-3** |
| 9     | X,O stacked right  | 0 - 0 = 0        | **0**  |

---

### Minimax Decision

| X's Move              | MIN's Choice | Worst Outcome |
|-----------------------|--------------|---------------|
| Column 0 (left)       | State 2      | -3            |
| **Column 1 (center)** | **State 5**  | **0**         |
| Column 2 (right)      | State 8      | -3            |

### Best Move:

X should play **CENTER (Column 1)**.<br/>
This gives X the best guaranteed outcome (0) because even when O plays optimally, X maintains a neutral position with center control.

## Is the algorithm capable of winning?

Yes, but with limitations depending on the depth. The deeper the search, the more chances it has of winning.<br/>
With $\text{depth}=2$, it can only look one move ahead, which might trap it in suboptimal solutions long-term.<br/>
An example of this would be moves that create two threats simultaneously, which would need more than the next move to come to fruition.

### How to improve?

Increasing the depth search is the first step in improving this algorithm.<br/>
Next, a timer could be implemented where, instead of a set depth, the algorithm searches as deep as it can within that timer and chooses the best move found.<br/>
Finally, it would be good to implement more complicated features, such as double-threat (fork) detection and how many moves are available to make.
