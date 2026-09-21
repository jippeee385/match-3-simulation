import numpy as np
import pytest

from match3.game.board import EMPTY, Board


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


def test_board_has_expected_shape():
    board = make_board()

    assert board.grid.shape == (8, 8)


def test_random_board_has_no_initial_matches():
    rng = np.random.default_rng(42)

    board = Board.random(rng=rng)

    assert board.find_matches() == set()


def test_horizontal_match_is_detected():
    board = make_board()

    board.grid[0, 2:5] = 0

    matches = board.find_matches()

    assert matches == {
        (0, 2),
        (0, 3),
        (0, 4),
    }


def test_vertical_match_is_detected():
    board = make_board()

    board.grid[1:4, 2] = 0

    matches = board.find_matches()

    assert matches == {
        (1, 2),
        (2, 2),
        (3, 2),
    }


def test_four_candy_match_is_detected():
    board = make_board()

    board.grid[0, 2:6] = 0

    matches = board.find_matches()

    assert matches == {
        (0, 2),
        (0, 3),
        (0, 4),
        (0, 5),
    }


def test_no_match_returns_empty_set():
    board = make_board()

    assert board.find_matches() == set()


def test_adjacent_cells_can_swap():
    board = make_board()

    original_first = board.grid[0, 0]
    original_second = board.grid[0, 1]

    board.swap((0, 0), (0, 1))

    assert board.grid[0, 0] == original_second
    assert board.grid[0, 1] == original_first


def test_diagonal_swap_is_rejected():
    board = make_board()

    with pytest.raises(ValueError):
        board.swap((0, 0), (1, 1))

def test_swap_creates_match():
    board = make_board()

    board.grid[0] = [0, 0, 1, 0, 4, 5, 1, 2]

    assert board.can_swap((0, 2), (0, 3))

def test_swap_that_does_not_create_match_is_invalid():
    board = make_board()

    assert not board.can_swap((0, 0), (0, 1))

def test_non_adjacent_swap_is_invalid():
    board = make_board()

    assert not board.can_swap((0, 0), (1, 1))


def test_can_swap_does_not_modify_board():
    board = make_board()

    original = board.grid.copy()

    board.can_swap((0, 0), (0, 1))

    np.testing.assert_array_equal(board.grid, original)

def test_swap_outside_board_is_rejected():
    board = make_board()

    with pytest.raises(ValueError):
        board.swap((0, 0), (8, 0))


def test_remove_matches():
    board = make_board()

    board.grid[0, 1] = 2
    board.grid[0, 2] = 2
    board.grid[0, 3] = 2

    matches = board.find_matches()

    board.remove_matches(matches)

    assert board.grid[0, 1] == EMPTY
    assert board.grid[0, 2] == EMPTY
    assert board.grid[0, 3] == EMPTY

def test_remove_matches_preserves_unmatched_cells():
    board = make_board()

    original_value = board.grid[0, 0]

    board.grid[0, 1] = 2
    board.grid[0, 2] = 2
    board.grid[0, 3] = 2

    matches = board.find_matches()

    board.remove_matches(matches)

    assert board.grid[0, 0] == original_value

def test_apply_gravity():
    board = make_board()

    board.grid[:, 0] = np.array(
        [0, EMPTY, 1, EMPTY, 2, 3, EMPTY, 4]
    )

    board.apply_gravity()

    expected = np.array(
        [EMPTY, EMPTY, EMPTY, 0, 1, 2, 3, 4]
    )

    assert np.array_equal(board.grid[:, 0], expected)

def test_apply_gravity_does_not_change_full_column():
    board = make_board()

    original = board.grid[:, 0].copy()

    board.apply_gravity()

    assert np.array_equal(board.grid[:, 0], original)

def test_apply_gravity_applies_to_all_columns():
    board = make_board()

    board.grid[:, 0] = np.array(
        [0, EMPTY, 1, EMPTY, 2, 3, EMPTY, 4]
    )
    board.grid[:, 1] = np.array(
        [EMPTY, 5, EMPTY, 4, EMPTY, 3, 2, 1]
    )

    board.apply_gravity()

    expected_col_0 = np.array(
        [EMPTY, EMPTY, EMPTY, 0, 1, 2, 3, 4]
    )
    expected_col_1 = np.array(
        [EMPTY, EMPTY, EMPTY, 5, 4, 3, 2, 1]
    )

    assert np.array_equal(board.grid[:, 0], expected_col_0)
    assert np.array_equal(board.grid[:, 1], expected_col_1)

def test_refill_fills_empty_cells():
    board = make_board()

    board.grid[0, 0] = EMPTY
    board.grid[1, 1] = EMPTY
    board.grid[2, 2] = EMPTY

    rng = np.random.default_rng(42)

    board.refill(rng)

    assert not np.any(board.grid == EMPTY)

def test_refill_generates_valid_candy_types():
    board = make_board()

    board.grid[0, 0] = EMPTY
    board.grid[1, 1] = EMPTY
    board.grid[2, 2] = EMPTY

    rng = np.random.default_rng(42)

    board.refill(rng)

    assert np.all(board.grid >= 0)
    assert np.all(board.grid < board.candy_types)

def test_refill_preserves_existing_candies():
    board = make_board()

    original_value = board.grid[0, 1]

    board.grid[0, 0] = EMPTY

    rng = np.random.default_rng(42)

    board.refill(rng)

    assert board.grid[0, 1] == original_value

def test_get_swap_matches_does_not_modify_board():
    board = make_board()

    original = board.grid.copy()

    board.get_swap_matches((0, 0), (0, 1))

    np.testing.assert_array_equal(
        board.grid,
        original,
    )

def test_get_swap_matches_rejects_non_adjacent_cells():

    board = make_board()
    
    with pytest.raises(ValueError):
        board.get_swap_matches((0, 0), (0, 2))