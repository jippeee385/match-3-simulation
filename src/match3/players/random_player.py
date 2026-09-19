from __future__ import annotations

import numpy as np

from match3.game.game import Game
from match3.game.moves import Move
from match3.players.base import Player


class RandomPlayer(Player):
    def __init__(self, rng: np.random.Generator | None = None):
        self.rng = rng or np.random.default_rng()

    def choose_move(self, game: Game) -> Move | None:
        """Choose a random valid move."""
        rows, cols = game.state.board.grid.shape

        valid_moves: list[Move] = []

        for row in range(rows):
            for col in range(cols):
                if col + 1 < cols:
                    move = Move(
                        first=(row, col),
                        second=(row, col + 1),
                    )
                    if game.check_move(move):
                        valid_moves.append(move)

                if row + 1 < rows:
                    move = Move(
                        first=(row, col),
                        second=(row + 1, col),
                    )
                    if game.check_move(move):
                        valid_moves.append(move)

        if not valid_moves:
            return None

        index = self.rng.integers(0, len(valid_moves))

        return valid_moves[index]