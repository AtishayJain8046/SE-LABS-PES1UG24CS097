"""Branch-coverage tests for the elevator dispatch application."""

import pytest

from elevator_dispatch import door_action, next_direction, pick_elevator


@pytest.mark.parametrize(
    ("direction", "requests", "expected"),
    [
        ("up", [5, 3, 1], "up"),
        ("up", [3, 1], "down"),
        ("up", [3], "idle"),
        ("down", [5, 3, 1], "down"),
        ("down", [5, 3], "up"),
        ("down", [3], "idle"),
        ("idle", [5, 3], "up"),
        ("idle", [3, 1], "down"),
        ("idle", [3], "idle"),
    ],
)
def test_next_direction_all_decision_outcomes(direction, requests, expected):
    assert next_direction(3, direction, requests) == expected


@pytest.mark.parametrize(
    ("load_kg", "blocked", "emergency", "expected"),
    [
        (700, True, True, "hold_open"),
        (631, False, False, "overload"),
        (630, True, False, "reopen"),
        (630, False, False, "close"),
    ],
)
def test_door_action_precedence_and_weight_boundary(
    load_kg, blocked, emergency, expected
):
    assert door_action(load_kg, blocked, emergency) == expected


@pytest.mark.parametrize(
    ("cars", "floor", "expected"),
    [
        ([], 4, None),
        ([("A", 2, True)], 4, "A"),
        ([("A", 1, True), ("B", 4, True)], 5, "B"),
        ([("A", 4, True), ("B", 6, True)], 5, "A"),
        ([("busy", 5, False), ("idle", 9, True)], 5, "idle"),
        ([("idle", 20, True), ("busy", 5, False)], 5, "busy"),
    ],
)
def test_pick_elevator_all_selection_branches(cars, floor, expected):
    assert pick_elevator(cars, floor) == expected
