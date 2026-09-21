import numpy as np
import pytest

from match3.game.board import Board
from match3.game.game import Game
from match3.game.level import Level, Objective, ObjectiveType
from match3.game.moves import Move
from match3.game.state import GameStatus


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


def make_game() -> Game:
    return Game(make_level())


def make_valid_board() -> Board:
    grid = np.array(
        [
            [0, 0, 1, 0, 4, 5, 1, 2],
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


def test_game_initialises_from_level():
    game = make_game()

    assert game.level.name == "Test Level"
    assert game.state.moves_remaining == 25
    assert game.state.status == GameStatus.PLAYING
    assert game.state.board.grid.shape == (8, 8)


def test_valid_move_is_detected():
    game = make_game()
    game.state.board = make_valid_board()

    move = Move(
        first=(0, 2),
        second=(0, 3),
    )

    assert game.check_move(move) is True


def test_invalid_move_is_rejected():
    game = make_game()
    game.state.board = make_valid_board()

    move = Move(
        first=(0, 0),
        second=(0, 1),
    )

    assert game.check_move(move) is False


def test_move_consumes_one_move():
    game = make_game()
    game.state.board = make_valid_board()

    move = Move(
        first=(0, 2),
        second=(0, 3),
    )

    game.apply_move(move)

    assert game.state.moves_remaining == 24


def test_move_resolves_board():
    game = make_game()
    game.state.board = make_valid_board()

    move = Move(
        first=(0, 2),
        second=(0, 3),
    )

    game.apply_move(move)

    assert not game.state.board.find_matches()


def test_invalid_move_raises_error():
    game = make_game()
    game.state.board = make_valid_board()

    move = Move(
        first=(0, 0),
        second=(0, 1),
    )

    with pytest.raises(ValueError, match="Invalid move"):
        game.apply_move(move)


def test_move_is_rejected_after_game_is_over():
    game = make_game()
    game.state.board = make_valid_board()
    game.state.status = GameStatus.WON

    move = Move(
        first=(0, 2),
        second=(0, 3),
    )

    assert game.check_move(move) is False

    with pytest.raises(ValueError, match="Invalid move"):
        game.apply_move(move)

def test_resolve_board_removes_matches():
    game = make_game()

    game.state.board = make_valid_board()

    # Create a horizontal match.
    game.state.board.grid[0] = np.array(
        [0, 0, 1, 0, 4, 5, 1, 2]
    )

    # Make the match explicit:
    game.state.board.grid[0, 1] = 2
    game.state.board.grid[0, 2] = 2
    game.state.board.grid[0, 3] = 2

    rng = np.random.default_rng(42)

    game.resolve_board(rng)

    assert not game.state.board.find_matches()
    assert game.state.cascade_count >= 1

def test_apply_move_resolves_matches():
    game = make_game()
    game.state.board = make_valid_board()

    move = Move(
        first=(0, 2),
        second=(0, 3),
    )

    game.apply_move(move)

    assert not game.state.board.find_matches()
    assert game.state.cascade_count >= 1
    assert game.state.moves_remaining == 24


def test_collect_objective_tracks_matched_candies():
    game = make_game()

    game.state.board = make_valid_board()

    game.state.board.grid[0] = np.array(
        [0, 0, 0, 1, 4, 5, 1, 2]
    )

    matches = game.state.board.find_matches()

    game.update_objective_progress(matches)

    assert game.state.objective_progress == 3

def test_collect_objective_ignores_other_candy_types():
    game = make_game()

    game.state.board = make_valid_board()

    game.state.board.grid[0] = np.array(
        [2, 2, 2, 1, 4, 5, 1, 2]
    )

    matches = game.state.board.find_matches()

    game.update_objective_progress(matches)

    assert game.state.objective_progress == 0

def test_apply_move_updates_objective_progress():
    game = make_game()
    game.state.board = make_valid_board()

    # Objective is to collect candy type 0.
    #
    # Swap positions 0,2 and 0,3:
    #
    # Before: 0 0 1 0
    # After:  0 0 0 1
    #
    # This creates three 0s.

    move = Move(
        first=(0, 2),
        second=(0, 3),
    )

    game.apply_move(move)

    assert game.state.objective_progress >= 3

def test_apply_move_updates_score():
    game = make_game()
    game.state.board = make_valid_board()

    # Swap positions (0,2) and (0,3):
    #
    # Before: 0 0 1 0
    # After:  0 0 0 1
    #
    # This creates three 0s, so the score should increase by 3.

    move = Move(
        first=(0, 2),
        second=(0, 3),
    )

    game.apply_move(move)

    assert game.state.score >= 3

def test_game_wins_when_objective_is_completed():
    game = make_game()

    game.state.objective_progress = 10

    game.update_status()

    assert game.state.status == GameStatus.WON

def test_game_loses_when_moves_run_out():
    game = make_game()

    game.state.moves_remaining = 0

    game.update_status()

    assert game.state.status == GameStatus.LOST

def test_completing_objective_on_last_move_results_in_win():
    game = make_game()

    game.state.objective_progress = 10
    game.state.moves_remaining = 0

    game.update_status()

    assert game.state.status == GameStatus.WON

def test_game_remains_playing_when_objective_incomplete():
    game = make_game()

    game.state.objective_progress = 5
    game.state.moves_remaining = 10

    game.update_status()

    assert game.state.status == GameStatus.PLAYING

def test_calculate_score_three_match():
    level = Level(
        name="Test Level",
        moves=10,
        objective=Objective(
            type=ObjectiveType.COLLECT,
            target=3,
            candy_type=0,
        ),
    )

    game = Game(level)

    matches = {
        (0, 0),
        (0, 1),
        (0, 2),
    }

    assert game.calculate_score(matches) == 3

def test_calculate_score_four_match():
    level = Level(
        name="Test Level",
        moves=10,
        objective=Objective(
            type=ObjectiveType.COLLECT,
            target=3,
            candy_type=0,
        ),
    )

    game = Game(level)

    matches = {
        (0, 0),
        (0, 1),
        (0, 2),
        (0, 3),
    }

    assert game.calculate_score(matches) == 4


def test_calculate_score_counts_all_matched_cells():
    level = Level(
        name="Test Level",
        moves=10,
        objective=Objective(
            type=ObjectiveType.COLLECT,
            target=3,
            candy_type=0,
        ),
    )

    game = Game(level)

    matches = {
        (0, 0),
        (0, 1),
        (0, 2),
        (3, 4),
        (4, 4),
    }

    assert game.calculate_score(matches) == 5

def test_update_score():
    level = Level(
        name="Test Level",
        moves=10,
        objective=Objective(
            type=ObjectiveType.COLLECT,
            target=3,
            candy_type=0,
        ),
    )

    game = Game(level)

    matches = {
        (0, 0),
        (0, 1),
        (0, 2),
    }

    game.update_score(matches)

    assert game.state.score == 3

def test_update_score_accumulates():
    level = Level(
        name="Test Level",
        moves=10,
        objective=Objective(
            type=ObjectiveType.COLLECT,
            target=3,
            candy_type=0,
        ),
    )

    game = Game(level)

    first_matches = {
        (0, 0),
        (0, 1),
        (0, 2),
    }

    second_matches = {
        (1, 0),
        (1, 1),
        (1, 2),
        (1, 3),
    }

    game.update_score(first_matches)
    game.update_score(second_matches)

    assert game.state.score == 7