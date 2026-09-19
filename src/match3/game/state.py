from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .board import Board


class GameStatus(Enum):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


@dataclass
class GameState:
    board: Board
    moves_remaining: int
    objective_progress: int = 0
    score: int = 0
    cascade_count: int = 0
    status: GameStatus = GameStatus.PLAYING