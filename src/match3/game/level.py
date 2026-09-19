from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ObjectiveType(Enum):
    COLLECT = "collect"
    CLEAR_BLOCKERS = "clear_blockers"
    SCORE = "score"


@dataclass(frozen=True)
class Objective:
    """Defines what a player must achieve to complete a level."""

    type: ObjectiveType
    target: int
    candy_type: int | None = None

    def __post_init__(self) -> None:
        if self.target <= 0:
            raise ValueError("Objective target must be greater than zero.")

        if self.type == ObjectiveType.COLLECT and self.candy_type is None:
            raise ValueError(
                "A collect objective requires a candy type."
            )

        if self.type != ObjectiveType.COLLECT and self.candy_type is not None:
            raise ValueError(
                "Candy type is only valid for collect objectives."
            )


@dataclass(frozen=True)
class Level:
    """Configuration for a match-3 level."""

    name: str
    moves: int
    objective: Objective
    board_size: tuple[int, int] = (8, 8)
    candy_types: int = 6
    blocker_positions: tuple[tuple[int, int], ...] = ()

    def __post_init__(self) -> None:
        if self.moves <= 0:
            raise ValueError("Level must have at least one move.")

        rows, cols = self.board_size

        if rows <= 0 or cols <= 0:
            raise ValueError("Board dimensions must be greater than zero.")

        if self.candy_types < 3:
            raise ValueError("At least 3 candy types are required.")

        for position in self.blocker_positions:
            row, col = position

            if not (0 <= row < rows and 0 <= col < cols):
                raise ValueError(
                    f"Blocker position {position} is outside the board."
                )