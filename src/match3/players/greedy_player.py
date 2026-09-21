from __future__ import annotations

import numpy as np

from match3.game.game import Game
from match3.game.moves import Move

from .base import Player


class GreedyPlayer(Player):
    def __init__(
        self,
        objective_weight: float = 1.0,
        score_weight: float = 1.0,
        rng: np.random.Generator | None = None,
    ):
        self.objective_weight = objective_weight
        self.score_weight = score_weight
        self.rng = rng or np.random.default_rng()

    def _calculate_reward(
        self,
        game: Game,
        matched_values: list[int],
    ) -> float:
        # Combine immediate objective progress and score.
        objective_progress = (
            game.calculate_objective_progress_from_values(
                matched_values
            )
        )
        score = game.calculate_score_from_values(matched_values)

        return (
            self.objective_weight * objective_progress
            + self.score_weight * score
        )

    def choose_move(self, game: Game) -> Move | None:
        board = game.state.board

        # Track all moves tied for the highest reward.
        best_reward = float("-inf")
        best_moves: list[Move] = []

        rows, cols = board.grid.shape

        for row in range(rows):
            for col in range(cols):
                # Evaluate the horizontal swap.
                if col < cols - 1:
                    move = Move(
                        first=(row, col),
                        second=(row, col + 1),
                    )

                    if game.check_move(move):
                        # Evaluate only the immediate result of the swap.
                        matched_values = board.get_swap_match_values(
                            move.first,
                            move.second,
                        )

                        reward = self._calculate_reward(
                            game,
                            matched_values,
                        )

                        if reward > best_reward:
                            best_reward = reward
                            best_moves = [move]

                        elif reward == best_reward:
                            best_moves.append(move)

                # Evaluate the vertical swap.
                if row < rows - 1:
                    move = Move(
                        first=(row, col),
                        second=(row + 1, col),
                    )

                    if game.check_move(move):
                        # Evaluate only the immediate result of the swap.
                        matched_values = board.get_swap_match_values(
                            move.first,
                            move.second,
                        )

                        reward = self._calculate_reward(
                            game,
                            matched_values,
                        )

                        if reward > best_reward:
                            best_reward = reward
                            best_moves = [move]

                        elif reward == best_reward:
                            best_moves.append(move)

        # No valid moves means the player cannot continue.
        if not best_moves:
            return None

        # Randomly break ties between equally good moves.
        index = self.rng.integers(len(best_moves))
        return best_moves[index]