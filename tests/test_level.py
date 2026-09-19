import pytest

from match3.game.level import Level, Objective, ObjectiveType


def test_create_collect_level():
    objective = Objective(
        type=ObjectiveType.COLLECT,
        target=30,
        candy_type=2,
    )

    level = Level(
        name="level_001",
        moves=25,
        objective=objective,
    )

    assert level.name == "level_001"
    assert level.moves == 25
    assert level.board_size == (8, 8)
    assert level.candy_types == 6
    assert level.objective.type == ObjectiveType.COLLECT
    assert level.objective.target == 30
    assert level.objective.candy_type == 2


def test_create_blocker_level():
    objective = Objective(
        type=ObjectiveType.CLEAR_BLOCKERS,
        target=10,
    )

    level = Level(
        name="level_002",
        moves=20,
        objective=objective,
        blocker_positions=(
            (2, 2),
            (2, 3),
            (3, 2),
        ),
    )

    assert len(level.blocker_positions) == 3


def test_collect_objective_requires_candy_type():
    with pytest.raises(ValueError):
        Objective(
            type=ObjectiveType.COLLECT,
            target=30,
        )


def test_non_collect_objective_cannot_have_candy_type():
    with pytest.raises(ValueError):
        Objective(
            type=ObjectiveType.SCORE,
            target=10_000,
            candy_type=2,
        )


def test_objective_target_must_be_positive():
    with pytest.raises(ValueError):
        Objective(
            type=ObjectiveType.SCORE,
            target=0,
        )


def test_level_requires_positive_moves():
    objective = Objective(
        type=ObjectiveType.SCORE,
        target=10_000,
    )

    with pytest.raises(ValueError):
        Level(
            name="invalid",
            moves=0,
            objective=objective,
        )


def test_blocker_must_be_inside_board():
    objective = Objective(
        type=ObjectiveType.CLEAR_BLOCKERS,
        target=1,
    )

    with pytest.raises(ValueError):
        Level(
            name="invalid",
            moves=20,
            objective=objective,
            blocker_positions=((8, 8),),
        )