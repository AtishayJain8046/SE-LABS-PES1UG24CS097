# Lab 7 - Fuzz Testing for Input Validation

This lab uses the [Lab 6 elevator dispatcher](../LAB-6/elevator_dispatch/lab6/elevator_dispatch.py) as its baseline. The Hypothesis suite checks expected dispatch behavior and generates malformed inputs for all three functions.

## Run the tests

From `LAB-7`:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -q --hypothesis-show-statistics
```

## Input contract and findings

| Function | Accepted inputs | Counterexample on the Lab 6 implementation |
| --- | --- | --- |
| `next_direction` | Integer current/request floors, a list or tuple of requests, and `up`, `down`, or `idle` | An empty direction string was treated as idle. |
| `door_action` | Finite nonnegative integer or float load and two boolean flags | A load of `-1` was accepted and returned `close`. |
| `pick_elevator` | Integer target floor and a list or tuple of three-field car records with a nonempty name, integer position, and boolean idle flag | A car with `is_idle=None` was treated as busy and could be selected. |

Malformed arguments now raise `ValueError` with a field-specific message. Booleans are rejected as floors and loads. Valid empty collections, below-ground floors, the 630 kg threshold, the five-floor busy-car penalty, and first-car tie breaking are covered by the tests.

The same suite produced **10 failures and 3 passes** on the Lab 6 implementation, then **13 passes** on the corrected implementation. To reproduce the baseline, copy the Lab 6 source into a temporary folder as `processor.py`, copy `test_processor.py` next to it, and run pytest from that folder.
