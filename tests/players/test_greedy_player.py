import numpy as np

from match3.game.board import Board
from match3.game.game import Game
from match3.game.level import Level, Objective, ObjectiveType
from match3.game.moves import Move
from match3.players.greedy_player import GreedyPlayer


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


def make_game(board: Board) -> Game:
    game = Game(make_level())
    game.state.board = board
    return game


def make_greedy_test_board() -> Board:
    grid = np.array(
        [
            [0, 0, 1, 0, 4, 5, 1, 2],
            [1, 1, 2, 1, 5, 1, 2, 3],
            [2, 3, 4, 5, 1, 2, 3, 4],
            [3, 4, 5, 1, 2, 3, 4, 5],
            [4, 5, 1, 2, 3, 4, 5, 1],
            [5, 1, 2, 3, 4, 5, 1, 2],
            [1, 2, 3, 4, 5, 1, 2, 3],
            [2, 3, 4, 5, 1, 2, 3, 4],
        ]
    )

    return Board(grid)


def test_greedy_player_prefers_objective_progress():
    game = make_game(make_greedy_test_board())
    player = GreedyPlayer(rng=np.random.default_rng(42))

    target_move = Move(
        first=(0, 2),
        second=(0, 3),
    )

    non_target_move = Move(
        first=(1, 2),
        second=(1, 3),
    )

    # The starting board should contain no existing matches.
    assert not game.state.board.find_matches()

    # Verify the immediate matches created by each candidate move.
    target_matches = game.state.board.get_swap_matches(
        target_move.first,
        target_move.second,
    )

    non_target_matches = game.state.board.get_swap_matches(
        non_target_move.first,
        non_target_move.second,
    )

    assert target_matches == {
        (0, 0),
        (0, 1),
        (0, 2),
    }

    assert non_target_matches == {
        (1, 0),
        (1, 1),
        (1, 2),
    }

    # Verify the reward components.
    target_values = game.state.board.get_swap_match_values(
        target_move.first,
        target_move.second,
    )

    non_target_values = game.state.board.get_swap_match_values(
        non_target_move.first,
        non_target_move.second,
    )

    assert game.calculate_objective_progress_from_values(target_values) == 3
    assert game.calculate_score_from_values(target_values) == 3

    assert game.calculate_objective_progress_from_values(non_target_values) == 0
    assert game.calculate_score_from_values(non_target_values) == 3

    # The greedy player should choose the higher-reward move.
    chosen_move = player.choose_move(game)

    assert chosen_move == target_move

    # Choosing a move must not modify the board.
    assert not game.state.board.find_matches()