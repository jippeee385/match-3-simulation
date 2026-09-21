from __future__ import annotations

import numpy as np

from .board import Board
from .level import Level, ObjectiveType
from .moves import Move
from .state import GameState, GameStatus


class Game:
    def __init__(
        self,
        level: Level,
        rng: np.random.Generator | None = None,
    ):
        self.level = level
        self.rng = rng or np.random.default_rng()

        self.state = GameState(
            board=Board.random(
                size=level.board_size,
                candy_types=level.candy_types,
                rng=self.rng,
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

        self.resolve_board(self.rng)

        self.update_status()

    def calculate_score(
        self,
        matches: set[tuple[int, int]],
    ) -> int:
        """Calculate score gained from matched cells."""
        return len(matches)

    def calculate_score_from_values(
        self,
        values: list[int],
    ) -> int:
        """Calculate score from matched candy values."""
        return len(values)

    def update_score(
        self,
        matches: set[tuple[int, int]],
    ) -> None:
        """Update the game score based on matched cells."""
        self.state.score += self.calculate_score(matches)

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
            # update the objective progress and score based on the matches
            self.update_score(matches)

            self.state.board.remove_matches(matches)
            self.state.board.apply_gravity()
            self.state.board.refill(rng)

            self.state.cascade_count += 1

    def calculate_objective_progress(
        self,
        matches: set[tuple[int, int]],
    ) -> int:
        """Calculate objective progress from matched cells."""
        objective = self.level.objective

        if objective.type == ObjectiveType.COLLECT:
            return sum(
                self.state.board.grid[row, col] == objective.candy_type
                for row, col in matches
            )

        return 0

    def calculate_objective_progress_from_values(
        self,
        values: list[int],
    ) -> int:
        """Calculate objective progress from matched candy values."""
        objective = self.level.objective

        if objective.type == ObjectiveType.COLLECT:
            return sum(
                value == objective.candy_type
                for value in values
            )

        return 0

    def update_objective_progress(
        self,
        matches: set[tuple[int, int]],
    ) -> None:
        """Update objective progress based on matched cells."""
        self.state.objective_progress += (
            self.calculate_objective_progress(matches)
        )

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