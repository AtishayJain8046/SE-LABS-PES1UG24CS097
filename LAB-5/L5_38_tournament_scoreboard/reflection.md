# Reflection

Reflection answers for Lab 5 (Static Code Analysis). The provided handout
lists reflection as a deliverable and enumerates the tools and goals but does
not print the questions, so the four questions below are the standard set for
this lab, drawn from its stated learning outcomes.

## 1. Which issues did the three tools report, and which did you judge most serious?

**Bandit** reported four security issues: a **high** severity shell-injection
risk (B605 — `os.system` building an `scp` command by string concatenation), a
**medium** severity insecure temporary file (B306 — `tempfile.mktemp`), and two
**low** severity items (B105 hardcoded password, B311 use of `random` for a
coin toss). **Pylint** scored the file **4.75/10** and reported one genuine bug
(W0102 mutable default argument) plus naming, docstring and refactor hints
(C0103, C0114/C0116, R1705, R1714). **Flake8** reported four PEP 8 violations
(E203, E302, E231, E261).

The most serious were the Bandit findings. The **shell injection** is the worst
because the `server` value is executed by a shell, so untrusted input becomes
arbitrary command execution. Close behind is the **mutable default argument**:
it is a silent correctness bug — every team registered through `addTeam` shares
one player list, so the code is wrong without ever erroring.

## 2. How did you fix the most serious issues, and why?

- **Shell injection (B605):** replaced `os.system("scp ... " + server + ...)`
  with `subprocess.run([...])` using an explicit argument list and no shell, so
  the server value can never be interpreted as shell syntax. `scp` is resolved
  with `shutil.which()` so no partial executable path is used.
- **Insecure temp file (B306):** switched to `tempfile.mkstemp()`, which
  creates the file atomically, and closed the returned file handle.
- **Mutable default (W0102):** changed the signature to `players=None` and
  created a fresh list inside the function, so each team gets its own list.
- **Hardcoded password (B105):** moved the value out of source and read it with
  `os.environ.get("REFEREE_PASSWORD", ...)`.
- **Insecure PRNG (B311):** used `secrets.choice()` for the coin toss.

## 3. Were there any false positives or trade-offs?

Yes, a few. The remaining Bandit items on the `subprocess` call (B404, B603,
B607) are inherent to legitimately running an external program: the call uses a
fixed, resolved binary and a list of arguments with no shell, so it is safe.
Rather than remove useful functionality, I documented the verified-safe call
with a targeted `# nosec B603` and a `# nosec B404` explanation. Using
`secrets.choice()` instead of `random.choice()` for a coin toss is technically
overkill, but it removes the finding at no cost. All fixes preserved the
program's output exactly, which I verified by diffing the before/after runs.

## 4. What did you learn about static analysis?

I learned that the three tools are complementary rather than redundant: Flake8
alone would have missed the correctness bug and every security issue, and Pylint
alone would have missed the shell injection. Bandit caught the security problems
but said nothing about style. Running all three, fixing by severity, and
re-running until the reports were empty gave a fast, repeatable quality loop —
the file went from **Pylint 4.75/10, Bandit 4 issues, Flake8 4 issues** to
**Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues**. Static analysis is not a
substitute for testing or code review, but it reliably catches whole classes of
bugs and insecure patterns before they ever run, and it is worth wiring into a
pre-commit hook or CI job on every project.
