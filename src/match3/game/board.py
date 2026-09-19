from __future__ import annotations

from dataclasses import dataclass

import numpy as np

EMPTY = -1
DEFAULT_BOARD_SIZE = (8, 8)
DEFAULT_CANDY_TYPES = 6


@dataclass
class Board:
    """Represents the current candy board."""

    grid: np.ndarray
    candy_types: int = DEFAULT_CANDY_TYPES

    def __post_init__(self) -> None:
        if self.grid.ndim != 2:
            raise ValueError("Board grid must be a 2D NumPy array.")

        if self.grid.shape != DEFAULT_BOARD_SIZE:
            raise ValueError(
                f"Board must be {DEFAULT_BOARD_SIZE[0]}x{DEFAULT_BOARD_SIZE[1]}."
            )

        if np.any(self.grid < EMPTY):
            raise ValueError("Board contains invalid candy values.")

        if np.any(self.grid >= self.candy_types):
            raise ValueError("Board contains an invalid candy type.")

    @classmethod
    def random(
        cls,
        size: tuple[int, int] = DEFAULT_BOARD_SIZE,
        candy_types: int = DEFAULT_CANDY_TYPES,
        rng: np.random.Generator | None = None,
    ) -> Board:
        """Create a random board with no initial matches."""
        if size != DEFAULT_BOARD_SIZE:
            raise ValueError(
                f"Only {DEFAULT_BOARD_SIZE[0]}x{DEFAULT_BOARD_SIZE[1]} "
                "boards are currently supported."
            )

        if candy_types < 3:
            raise ValueError("At least 3 candy types are required.")

        rng = rng or np.random.default_rng()

        while True:
            grid = rng.integers(
                0,
                candy_types,
                size=size,
            )

            board = cls(grid=grid, candy_types=candy_types)

            if not board.find_matches():
                return board

    def swap(
        self,
        first: tuple[int, int],
        second: tuple[int, int],
    ) -> None:
        """Swap two adjacent cells in-place."""
        self._validate_position(first)
        self._validate_position(second)

        if not self._are_adjacent(first, second):
            raise ValueError(
                "Only horizontally or vertically adjacent cells can swap."
            )

        self.grid[first], self.grid[second] = (
            self.grid[second],
            self.grid[first],
        )

    def find_matches(self) -> set[tuple[int, int]]:
        """Return all cells belonging to horizontal or vertical matches."""
        matches: set[tuple[int, int]] = set()

        rows, cols = self.grid.shape

        # Horizontal matches
        for row in range(rows):
            start = 0

            while start < cols:
                value = self.grid[row, start]

                if value == EMPTY:
                    start += 1
                    continue

                end = start + 1

                while end < cols and self.grid[row, end] == value:
                    end += 1

                if end - start >= 3:
                    matches.update(
                        (row, col)
                        for col in range(start, end)
                    )

                start = end

        # Vertical matches
        for col in range(cols):
            start = 0

            while start < rows:
                value = self.grid[start, col]

                if value == EMPTY:
                    start += 1
                    continue

                end = start + 1

                while end < rows and self.grid[end, col] == value:
                    end += 1

                if end - start >= 3:
                    matches.update(
                        (row, col)
                        for row in range(start, end)
                    )

                start = end

        return matches

    def _validate_position(self, position: tuple[int, int]) -> None:
        """Validate that a position exists on the board."""
        row, col = position
        rows, cols = self.grid.shape

        if not (0 <= row < rows and 0 <= col < cols):
            raise ValueError(f"Position {position} is outside the board.")

    def can_swap(
        self,
        first: tuple[int, int],
        second: tuple[int, int],
    ) -> bool:
        """Return True if swapping two adjacent cells creates a match."""
        if not self._are_adjacent(first, second):
            return False

        self.swap(first, second)

        has_match = (
            self._cell_has_match(first)
            or self._cell_has_match(second)
        )

        self.swap(first, second)

        return has_match

    def remove_matches(self, matches: set[tuple[int, int]]) -> None:
        """Remove matched candies from the board."""
        for row, col in matches:
            self.grid[row, col] = EMPTY

    def apply_gravity(self) -> None:
        """Move non-empty candies down each column."""
        rows, cols = self.grid.shape

        for col in range(cols):
            non_empty = self.grid[:, col][self.grid[:, col] != EMPTY]

            empty_count = rows - len(non_empty)

            self.grid[:, col] = np.concatenate(
                [
                    np.full(empty_count, EMPTY),
                    non_empty,
                ]
            )

    def refill(self, rng: np.random.Generator | None = None) -> None:
        """Fill empty cells with randomly generated candies."""
        rng = rng or np.random.default_rng()

        empty_positions = np.argwhere(self.grid == EMPTY)

        for row, col in empty_positions:
            self.grid[row, col] = rng.integers(
                0,
                self.candy_types,
            )

    def _cell_has_match(self, position: tuple[int, int]) -> bool:
        """Return True if the candy at a position is part of a match."""
        row, col = position
        value = self.grid[row, col]

        if value == EMPTY:
            return False

        rows, cols = self.grid.shape

        # Horizontal run
        horizontal_count = 1

        current_col = col - 1
        while current_col >= 0 and self.grid[row, current_col] == value:
            horizontal_count += 1
            current_col -= 1

        current_col = col + 1
        while current_col < cols and self.grid[row, current_col] == value:
            horizontal_count += 1
            current_col += 1

        if horizontal_count >= 3:
            return True

        # Vertical run
        vertical_count = 1

        current_row = row - 1
        while current_row >= 0 and self.grid[current_row, col] == value:
            vertical_count += 1
            current_row -= 1

        current_row = row + 1
        while current_row < rows and self.grid[current_row, col] == value:
            vertical_count += 1
            current_row += 1

        return vertical_count >= 3

    @staticmethod
    def _are_adjacent(
        first: tuple[int, int],
        second: tuple[int, int],
    ) -> bool:
        row_difference = abs(first[0] - second[0])
        col_difference = abs(first[1] - second[1])

        return row_difference + col_difference == 1