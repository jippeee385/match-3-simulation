
import numpy as np

from match3.game.board import Board
from match3.game.state import GameState, GameStatus


def make_board() -> Board:
    grid = np.array(
        [
            [0, 1, 2, 3, 4, 5, 1, 2],
            [1, 2, 3, 4, 5, 1, 2, 3],
            [2, 3, 4, 5, 1, 2, 3, 4],
            [3, 4, 5, 1, 2, 3, 4, 5],
            [4, 5, 1, 2, 3, 4, 5, 1],
            [5, 1, 2, 3, 4, 5, 1, 2],
            [1, 2, 3, 4, 5, 1, 2, 3],
            [2, 3, 4, 5, 1, 2, 3, 4],
        ]
    )
    return Board(grid)


def test_game_state_initialises_with_defaults():
    board = make_board()

    state = GameState(
        board=board,
        moves_remaining=25,
    )

    assert state.board is board
    assert state.moves_remaining == 25
    assert state.objective_progress == 0
    assert state.score == 0
    assert state.cascade_count == 0
    assert state.status == GameStatus.PLAYING


def test_game_state_can_be_updated():
    state = GameState(
        board=make_board(),
        moves_remaining=25,
    )

    state.moves_remaining -= 1
    state.objective_progress += 3
    state.score += 100
    state.cascade_count += 1

    assert state.moves_remaining == 24
    assert state.objective_progress == 3
    assert state.score == 100
    assert state.cascade_count == 1


def test_game_state_status_can_change():
    state = GameState(
        board=make_board(),
        moves_remaining=25,
    )

    state.status = GameStatus.WON

    assert state.status == GameStatus.WON


def test_game_status_values():
    assert GameStatus.PLAYING.value == "playing"
    assert GameStatus.WON.value == "won"
    assert GameStatus.LOST.value == "lost"