import math

import pytest
from hypothesis import example, given, settings
from hypothesis import strategies as st

from processor import door_action, next_direction, pick_elevator


FLOOR = st.integers()
DIRECTION = st.sampled_from(("up", "down", "idle"))
LOAD = st.one_of(st.integers(min_value=0), st.floats(min_value=0, allow_infinity=False))
FLAG = st.booleans()
CAR = st.tuples(st.text(min_size=1), FLOOR, FLAG)
BAD_FLOOR = st.one_of(FLAG, st.none(), st.text(), st.floats())
BAD_LOAD = st.one_of(
    st.integers(max_value=-1), st.floats(max_value=-0.01),
    st.sampled_from((math.nan, math.inf, -math.inf)), FLAG, st.none(), st.text(),
)
BAD_FLAG = st.one_of(st.integers(), st.text(), st.none())


@settings(derandomize=True)
@given(FLOOR, DIRECTION, st.lists(FLOOR))
@example(0, "down", [-1, 0, 1])
def test_direction_matches_available_floors(current, direction, requests):
    available = {"up" if floor > current else "down"
                 for floor in requests if floor != current}
    preference = ("down", "up") if direction == "down" else ("up", "down")
    expected = next((candidate for candidate in preference if candidate in available), "idle")
    assert next_direction(current, direction, tuple(requests)) == expected


@settings(derandomize=True)
@given(st.text().filter(lambda direction: direction not in ("up", "down", "idle")))
def test_direction_rejects_unknown_direction(direction):
    with pytest.raises(ValueError, match="direction"):
        next_direction(0, direction, [1])


@settings(derandomize=True)
@given(BAD_FLOOR)
def test_direction_rejects_invalid_floors(floor):
    with pytest.raises(ValueError, match="current"):
        next_direction(floor, "idle", [])
    with pytest.raises(ValueError, match="request"):
        next_direction(0, "idle", [floor])


@settings(derandomize=True)
@given(st.one_of(st.none(), st.text(), st.dictionaries(FLOOR, FLOOR)))
def test_direction_rejects_invalid_request_collections(requests):
    with pytest.raises(ValueError, match="requests"):
        next_direction(0, "idle", requests)


@settings(derandomize=True)
@given(LOAD, FLAG, FLAG)
@example(630, False, False)
@example(631, True, False)
@example(631, True, True)
def test_door_matches_action_priority(load, blocked, emergency):
    actions = ((emergency, "hold_open"), (load > 630, "overload"), (blocked, "reopen"))
    expected = next((action for enabled, action in actions if enabled), "close")
    assert door_action(load, blocked, emergency) == expected


@settings(derandomize=True)
@given(BAD_LOAD)
def test_door_rejects_invalid_load_even_during_emergency(load):
    with pytest.raises(ValueError, match="load_kg"):
        door_action(load, False, False)
    with pytest.raises(ValueError, match="load_kg"):
        door_action(load, False, True)


@settings(derandomize=True)
@given(BAD_FLAG)
def test_door_rejects_non_boolean_flags(flag):
    with pytest.raises(ValueError, match="blocked"):
        door_action(0, flag, False)
    with pytest.raises(ValueError, match="emergency"):
        door_action(0, False, flag)


@settings(derandomize=True)
@given(st.lists(CAR), FLOOR)
@example([], 0)
@example([("A", 1, True), ("B", -1, True)], 0)
@example([("A", 0, False), ("B", 4, True)], 0)
def test_pick_matches_minimum_adjusted_distance(cars, floor):
    best = min(cars, key=lambda car: abs(car[1] - floor) + (0 if car[2] else 5), default=None)
    assert pick_elevator(tuple(cars), floor) == (None if best is None else best[0])


@settings(derandomize=True)
@given(BAD_FLAG)
def test_pick_rejects_non_boolean_car_status(flag):
    with pytest.raises(ValueError, match="is_idle"):
        pick_elevator([("A", 0, flag)], 0)


@settings(derandomize=True)
@given(BAD_FLOOR)
def test_pick_rejects_invalid_floors(floor):
    with pytest.raises(ValueError, match="floor"):
        pick_elevator([], floor)
    with pytest.raises(ValueError, match="position"):
        pick_elevator([("A", floor, True)], 0)


@settings(derandomize=True)
@given(st.sampled_from(((), ("A", 0), ("A", 0, True, 1), None, "ABC")))
def test_pick_rejects_malformed_car_records(record):
    with pytest.raises(ValueError, match="car record"):
        pick_elevator([record], 0)


@settings(derandomize=True)
@given(st.one_of(st.none(), st.text(), st.dictionaries(FLOOR, FLOOR)))
def test_pick_rejects_invalid_car_collections(cars):
    with pytest.raises(ValueError, match="cars"):
        pick_elevator(cars, 0)


@settings(derandomize=True)
@given(st.one_of(st.just(""), st.none(), FLOOR))
def test_pick_rejects_invalid_car_names(name):
    with pytest.raises(ValueError, match="name"):
        pick_elevator([(name, 0, True)], 0)
