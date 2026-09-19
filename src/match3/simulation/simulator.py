from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from match3.game.game import Game
from match3.game.level import Level
from match3.game.state import GameStatus
from match3.players.base import Player


@dataclass(frozen=True)
class SimulationResult:
    won: bool
    moves_used: int
    moves_remaining: int
    objective_progress: int
    cascade_count: int


def simulate_game(
    level: Level,
    player: Player,
    rng: np.random.Generator | None = None,
) -> SimulationResult:
    """Simulate one game using the provided player."""
    rng = rng or np.random.default_rng()

    game = Game(level, rng=rng)

    while game.state.status == GameStatus.PLAYING:
        move = player.choose_move(game)

        if move is None:
            game.state.status = GameStatus.LOST
            break

        game.apply_move(move)

    return SimulationResult(
        won=game.state.status == GameStatus.WON,
        moves_used=level.moves - game.state.moves_remaining,
        moves_remaining=game.state.moves_remaining,
        objective_progress=game.state.objective_progress,
        cascade_count=game.state.cascade_count,
    )

def simulate_games(
    level: Level,
    player: Player,
    n_games: int = 1000,
    rng: np.random.Generator | None = None,
) -> list[SimulationResult]:
    """Simulate multiple games using the provided player."""
    if n_games <= 0:
        raise ValueError("n_games must be greater than zero.")

    rng = rng or np.random.default_rng()

    results: list[SimulationResult] = []

    for _ in range(n_games):
        result = simulate_game(
            level,
            player,
            rng=rng,
        )
        results.append(result)

    return results