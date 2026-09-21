# Agents

This document describes the player agents for testing the simple match 3 game.
## Random Agent

The RandomPlayer provides a simple baseline for player behaviour.

### Behaviour

At each turn, the agent:

1. Identifies all valid swaps on the current board.
2. Selects one of the valid swaps at random.
3. Makes no attempt to evaluate the quality of the move.

The agent therefore has no understanding of the level objective, score, board position, or future consequences of a move.

### Purpose

The random agent provides a useful baseline against which more sophisticated agents can be compared.

## Deterministic Greedy Agent

The GreedyPlayer selects the move with the highest immediate reward.

### Behaviour

At each turn, the agent:

1. Identifies all valid swaps on the current board.
2. Evaluates the immediate reward produced by each swap.
3. Selects a move with the highest reward.
4. Does not consider cascades, future board states, or future rewards.

The immediate reward is defined as:

$$ R(a) = w_o \cdot \text{objective progress}(a) + w_s \cdot \text{immediate score}(a) $$

The initial implementation uses:

objective_weight = 1.0
score_weight = 1.0

The objective determines what constitutes relevant progress. For example, for a COLLECT objective, matching the target candy contributes to objective progress while matching other colours does not.

### Tie-breaking

If multiple moves have the same highest immediate reward, the agent randomly selects between them.

### Purpose

The greedy agent represents a player who is objective-aware and makes locally optimal decisions, but has no ability to anticipate future consequences - it has no ability to estimate future reward.