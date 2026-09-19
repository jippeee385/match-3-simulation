from __future__ import annotations

import numpy as np

from .board import Board
from .level import Level, ObjectiveType
from .moves import Move
from .state import GameState, GameStatus


class Game:
    def __init__(self, level: Level):
        self.level = level
        self.state = GameState(
            board=Board.random(
                size=level.board_size,
                candy_types=level.candy_types,
            ),
            moves_remaining=level.moves,
        )

    def check_move(self, move: Move) -> bool:
        """Return True if the move is currently valid."""

        if self.state.status != GameStatus.PLAYING:
            return False

        return self.state.board.can_swap(
            move.first,
            move.second,
        )

    def apply_move(self, move: Move) -> None:
        if not self.check_move(move):
            raise ValueError("Invalid move.")

        self.state.board.swap(
            move.first,
            move.second,
        )

        self.state.moves_remaining -= 1

        self.resolve_board()

        self.update_status()

    def resolve_board(
        self,
        rng: np.random.Generator | None = None,
    ) -> None:
        """Resolve all matches and cascades until the board is stable."""
        self.state.cascade_count = 0

        while True:
            matches = self.state.board.find_matches()

            if not matches:
                break


            # update the objective progress based on the matches
            self.update_objective_progress(matches)

            self.state.board.remove_matches(matches)
            self.state.board.apply_gravity()
            self.state.board.refill(rng)

            self.state.cascade_count += 1

    def update_objective_progress(
        self,
        matches: set[tuple[int, int]],
    ) -> None:
        """Update objective progress based on matched cells."""
        objective = self.level.objective

        if objective.type == ObjectiveType.COLLECT:
            collected = sum(
                self.state.board.grid[row, col] == objective.candy_type
                for row, col in matches
            )
            self.state.objective_progress += collected

    def check_win(self) -> bool:
        """Return True if the level objective has been completed."""
        return (
            self.state.objective_progress
            >= self.level.objective.target
        )

    def update_status(self) -> None:
        """Update the game status based on the current state."""
        if self.check_win():
            self.state.status = GameStatus.WON
        elif self.state.moves_remaining <= 0:
            self.state.status = GameStatus.LOST