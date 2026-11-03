# L6_L7_38 — Elevator Dispatch

Lab 6: Code and Branch Coverage

## About

A small Python module that chooses elevator travel direction, door actions and which car to send to a call.

## Files

| File | Description |
|------|-------------|
| `elevator_dispatch.py` | The module under test |
| `test_elevator_dispatch.py` | Starter test file |
| `CodeCoverageTest_elevator_dispatch.py` | Tests for line/code coverage |
| `BranchCoverageTest_elevator_dispatch.py` | Tests for decision/branch coverage |
| `screenshots/code_coverage_result.png` | Terminal evidence for line coverage |
| `screenshots/branch_coverage_result.png` | Terminal evidence for branch coverage |

## Setup

From the repository root:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cd lab6
```

## Run the code-coverage suite

```bash
../.venv/bin/coverage erase
../.venv/bin/coverage run --source=elevator_dispatch -m pytest CodeCoverageTest_elevator_dispatch.py
../.venv/bin/coverage report -m
```

Result: **100% line coverage** (39 statements, 0 missed).

## Run the branch-coverage suite

```bash
../.venv/bin/coverage erase
../.venv/bin/coverage run --branch --source=elevator_dispatch -m pytest BranchCoverageTest_elevator_dispatch.py
../.venv/bin/coverage report -m
```

Result: **100% branch coverage** (39 statements and 28 branches, 0 missed or partial).

## Coverage analysis

The code-coverage suite executes every statement and return path in the three functions. The
branch-coverage suite additionally checks both outcomes of every decision, including direction
changes, equal-floor requests, emergency precedence, the 630 kg load boundary, idle/busy car
penalties, replacement of the current best car, ties, and an empty car list.
