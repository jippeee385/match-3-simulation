import numpy as np
import pytest

from match3.game.level import Level, Objective, ObjectiveType
from match3.players.random_player import RandomPlayer
from match3.simulation.simulator import (
    SimulationResult,
    simulate_game,
    simulate_games,
)


def make_level() -> Level:
    return Level(
        name="Test Level",
        moves=25,
        objective=Objective(
            type=ObjectiveType.COLLECT,
            target=10,
            candy_type=0,
        ),
    )


def test_simulate_game_returns_result():
    level = make_level()

    rng = np.random.default_rng(42)
    player = RandomPlayer(rng)

    result = simulate_game(
        level,
        player,
        rng=rng,
    )

    assert isinstance(result, SimulationResult)
    assert isinstance(result.won, bool)
    assert result.moves_used >= 0
    assert result.moves_remaining >= 0
    assert result.objective_progress >= 0
    assert result.cascade_count >= 0


def test_simulate_game_is_reproducible():
    level = make_level()

    rng_1 = np.random.default_rng(42)
    player_1 = RandomPlayer(rng_1)

    result_1 = simulate_game(
        level,
        player_1,
        rng=rng_1,
    )

    rng_2 = np.random.default_rng(42)
    player_2 = RandomPlayer(rng_2)

    result_2 = simulate_game(
        level,
        player_2,
        rng=rng_2,
    )

    assert result_1 == result_2

def test_simulate_games_returns_requested_number_of_results():
    level = make_level()

    rng = np.random.default_rng(42)
    player = RandomPlayer(rng)

    results = simulate_games(
        level,
        player,
        n_games=10,
        rng=rng,
    )

    assert len(results) == 10
    assert all(
        isinstance(result, SimulationResult)
        for result in results
    )

def test_simulate_games_rejects_non_positive_number_of_games():
    level = make_level()

    rng = np.random.default_rng(42)
    player = RandomPlayer(rng)

    with pytest.raises(ValueError, match="n_games"):
        simulate_games(
            level,
            player,
            n_games=0,
            rng=rng,
        )