from __future__ import annotations

from abc import ABC, abstractmethod

from match3.game.game import Game
from match3.game.moves import Move


class Player(ABC):
    @abstractmethod
    def choose_move(self, game: Game) -> Move | None:
        """Choose the next move to play."""
        ...