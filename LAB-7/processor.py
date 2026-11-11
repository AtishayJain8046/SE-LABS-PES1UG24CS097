"""Elevator dispatch with explicit validation at each public entry point."""

import math


def _require_floor(value, label):
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValueError(f"{label} must be an integer floor")


def next_direction(current, direction, requests):
    """Continue in the current direction when possible, or choose a new one."""
    _require_floor(current, "current")
    if not isinstance(direction, str) or direction not in ("up", "down", "idle"):
        raise ValueError("direction must be 'up', 'down', or 'idle'")
    if not isinstance(requests, (list, tuple)):
        raise ValueError("requests must be a list or tuple of floors")
    for floor in requests:
        _require_floor(floor, "request")

    above = [floor for floor in requests if floor > current]
    below = [floor for floor in requests if floor < current]
    if direction == "down" and below:
        return "down"
    if above:
        return "up"
    if below:
        return "down"
    return "idle"


def door_action(load_kg, blocked, emergency):
    """Choose a door action for a valid load and sensor state."""
    if isinstance(load_kg, bool) or not isinstance(load_kg, (int, float)):
        raise ValueError("load_kg must be a finite nonnegative number")
    if load_kg < 0 or (isinstance(load_kg, float) and not math.isfinite(load_kg)):
        raise ValueError("load_kg must be a finite nonnegative number")
    if not isinstance(blocked, bool):
        raise ValueError("blocked must be a boolean")
    if not isinstance(emergency, bool):
        raise ValueError("emergency must be a boolean")

    if emergency:
        return "hold_open"
    if load_kg > 630:
        return "overload"
    if blocked:
        return "reopen"
    return "close"


def pick_elevator(cars, floor):
    """Return the first car with the lowest adjusted distance, or None."""
    _require_floor(floor, "floor")
    if not isinstance(cars, (list, tuple)):
        raise ValueError("cars must be a list or tuple of car records")

    best = None
    best_gap = None
    for record in cars:
        if not isinstance(record, (list, tuple)) or len(record) != 3:
            raise ValueError("car record must contain name, position, and is_idle")
        name, position, is_idle = record
        if not isinstance(name, str) or not name:
            raise ValueError("car name must be a nonempty string")
        _require_floor(position, "car position")
        if not isinstance(is_idle, bool):
            raise ValueError("car is_idle must be a boolean")

        gap = abs(position - floor)
        if not is_idle:
            gap += 5
        if best_gap is None or gap < best_gap:
            best = name
            best_gap = gap
    return best
