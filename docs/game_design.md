# Match-3 Game — Mechanics Design

## Board

* **Size:** 8 × 8
* **Candy types:** 6
* Each cell contains one normal candy, a special candy, or a blocker.
* The board is populated randomly at the start of a game.
* Initial boards must contain **no pre-existing matches**.

## Moves

* A move consists of swapping two horizontally or vertically adjacent cells.
* A swap is valid only if it produces at least one match.
* Each valid swap consumes one move.
* Invalid swaps are rejected and do not consume a move.

## Matches

* A match consists of **3 or more identical candies** in a horizontal or vertical line.
* All candies in a match are removed.
* Matches of 4+ generate special candies.

### Special candies

| Match | Result           |
| ----- | ---------------- |
| 3     | Normal clear     |
| 4     | Line-clear candy |
| 5+    | Colour bomb      |

Special-candy interactions will initially be limited to simple activation; more complex combinations may be added later if useful.

## Cascades

After candies are removed:

1. Candies fall under gravity.
2. Empty cells are refilled with randomly generated candies.
3. New matches are detected.
4. Steps 1–3 repeat until the board is stable.

A single player move may therefore produce multiple cascades.

## Blockers

* Levels may contain blockers occupying individual cells.
* A blocker is removed when the candy beneath it participates in a match.
* Blockers do not move independently.
* Blocker count and placement are configurable level parameters.

## Objectives

Initial objective types:

* **Collect:** collect a specified number of a particular candy type.
* **Clear blockers:** remove a specified number of blockers.
* **Score:** reach a specified score.

A level is completed when its objective is satisfied.

## Level Completion

A game ends when either:

**Win**

* The level objective is completed.

**Loss**

* The player has no moves remaining before completing the objective.

## Level Parameters

Each level is defined by configurable parameters:

* Board size
* Number of candy types
* Move limit
* Objective type and target
* Blocker count
* Blocker placement
* Special-candy generation rules

These parameters form the experimental space for the difficulty-balancing analysis.

## Design Principle

The game should be **simple enough to simulate at scale but sufficiently rich to create meaningful differences in difficulty between player types and level configurations**.
