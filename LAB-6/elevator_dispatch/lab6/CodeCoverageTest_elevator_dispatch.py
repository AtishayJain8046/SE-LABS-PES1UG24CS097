"""Line-coverage tests for the elevator dispatch application."""

import pytest

from elevator_dispatch import door_action, next_direction, pick_elevator


@pytest.mark.parametrize(
    ("current", "direction", "requests", "expected"),
    [
        (3, "up", [5], "up"),
        (3, "up", [1], "down"),
        (3, "up", [], "idle"),
        (3, "down", [1], "down"),
        (3, "down", [5], "up"),
        (3, "down", [], "idle"),
        (3, "idle", [5], "up"),
        (3, "idle", [1], "down"),
        (3, "idle", [], "idle"),
    ],
)
def test_next_direction_return_values(current, direction, requests, expected):
    assert next_direction(current, direction, requests) == expected


@pytest.mark.parametrize(
    ("load_kg", "blocked", "emergency", "expected"),
    [
        (100, False, True, "hold_open"),
        (700, False, False, "overload"),
        (100, True, False, "reopen"),
        (100, False, False, "close"),
    ],
)
def test_door_action_return_values(load_kg, blocked, emergency, expected):
    assert door_action(load_kg, blocked, emergency) == expected


def test_pick_elevator_executes_idle_and_busy_paths():
    cars = [("A", 2, True), ("B", 4, False)]
    assert pick_elevator(cars, 2) == "A"
