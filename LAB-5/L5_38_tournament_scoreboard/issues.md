# Issues Found by Static Analysis

Program: `tournament_scoreboard.py`
Tools: Pylint 4.1.3, Bandit 1.9.4, Flake8 7.4.1

Baseline scores (in `reports/before/`):

| Tool | Before |
|------|--------|
| Pylint | 4.75 / 10 |
| Bandit | 1 high, 1 medium, 2 low |
| Flake8 | 4 style violations |

The table is ordered by severity, highest first (Bandit high/medium findings
come first, then the bug, then quality and style issues).

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | Shell command injection (Bandit B605) | Security — High | 71 | `os.system("scp table.json " + server + ":/var/www/")` builds a shell command by string concatenation, so a crafted `server` value is executed by the shell. | Build an argument list and call `subprocess.run()` without a shell; resolve `scp` with `shutil.which()` so no partial path is used. |
| 2 | Insecure temporary file (Bandit B306) | Security — Medium | 66 | `tempfile.mktemp()` returns a predictable, deprecated name and never creates the file, leaving a race where an attacker can pre-create it. | Use `tempfile.mkstemp()`, which creates the file atomically, then close the returned handle. |
| 3 | Mutable default argument (Pylint W0102) | Bug | 11 | `addTeam(teamName, players=[])` shares one single list across every call, so players added to one team leak into all teams. | Default `players` to `None` and create a fresh list inside the function. |
| 4 | Hardcoded password (Bandit B105) | Security — Low | 6 | `REFEREE_PASSWORD = "referee-demo"` embeds a secret directly in the source code. | Read the value from the environment with `os.environ.get("REFEREE_PASSWORD", ...)`. |
| 5 | Insecure pseudo-random generator (Bandit B311) | Security — Low | 61 | `random.choice()` is not suitable for security-sensitive randomness. | Use `secrets.choice()` for the coin toss. |
| 6 | `camelCase` naming (Pylint C0103) | Quality | 11–74 | Function and argument names (`addTeam`, `teamName`, `homeGoals`, ...) violate the PEP 8 `snake_case` style. | Rename to `snake_case` (`add_team`, `team_name`, `home_goals`, ...). |
| 7 | Missing docstrings (Pylint C0114, C0116) | Quality | 1–92 | The module and every function lack a docstring. | Add a module docstring and a short docstring per function. |
| 8 | Unnecessary `elif`/`else` after `return` (Pylint R1705) | Quality | 17–22 | `elif`/`else` after a `return` is redundant and adds nesting. | Use plain `if` statements and a final `return`. |
| 9 | Comparison should use `in` (Pylint R1714) | Quality | 58 | `teamName == table[0] or teamName == table[1]` repeats the same comparison. | `return team_name in (table[0], table[1])`. |
| 10 | Whitespace before `:` (Flake8 E203) | Style | 5 | `{"win" : 3, ...}` has a space before the colon. | Write `{"win": 3, ...}`. |
| 11 | Missing whitespace after `,` (Flake8 E231) | Style | 79 | `recordMatch(..., 2,1)` is missing a space after the comma. | Write `2, 1`. |
| 12 | Wrong number of blank lines (Flake8 E302) | Style | 60 | Only one blank line before `def tossCoin()`. | Separate top-level definitions with two blank lines. |
| 13 | Inline comment spacing (Flake8 E261) | Style | 87 | Only one space before the `# one row per team` comment. | Use at least two spaces before the inline comment. |

## Notes

- Issues 1–5 are the security findings; numbers 1 and 2 are the high/medium
  severity items that the handout asks to prioritise.
- After fixing, the remaining Bandit subprocess review items (B404, B603,
  B607) are inherent to legitimately invoking `scp`; they are handled by
  resolving the executable with `shutil.which()` and documenting the
  verified-safe, non-shell call with a targeted `# nosec` (see issue 1).
- Final results: **Pylint 10.00/10**, **Bandit 0 issues**, **Flake8 0 issues**.
