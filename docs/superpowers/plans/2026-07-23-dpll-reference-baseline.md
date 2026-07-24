# Deterministic DPLL Reference Baseline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a deterministic DPLL reference solver, permanent DIMACS contract
coverage, and public case-by-case finite-domain agreement evidence against the
existing brute-force solver.

**Architecture:** Keep the existing `Formula` representation and verifier.
Add DPLL privately assisted by clause normalization and deterministic recursive
search, add a separate canonical finite-family generator, and build an
experiment module that records every brute-force/DPLL outcome in JSON. Publish
the reviewed implementation before generating evidence so the report binds to
an exact public commit.

**Tech Stack:** Python 3.11+, standard library only, pytest 8.3–8.x, Markdown,
JSON, Git, GitHub Contents API

## Global Constraints

- Work on branch `dpll-baseline`; branch names must not contain `codex`.
- The repository remains public at `ApacheWang/open-np-hard-research`.
- Use `python -m pytest -q -p no:cacheprovider` for the complete local suite.
- Add no runtime dependency.
- Keep the existing `Formula = tuple[Clause, ...]` representation.
- `dpll_solve` accepts the same well-formed formula contract as
  `satisfies` and `brute_force_solve`; malformed hand-built tuples remain
  outside the runtime contract.
- DPLL applies unit propagation, chooses the lowest remaining variable, and
  branches `False` before `True`.
- A SAT result contains every variable occurring in the original formula and
  must pass `satisfies`.
- Permanent CI differential coverage is exactly the 394 declared-domain cases
  for variable counts 0–3 and at most two canonical clauses.
- Published experiment coverage is exactly the 3,050 declared-domain cases for
  variable counts 0–3 and at most three canonical clauses.
- Repeated literals, tautologies, and duplicate clauses are excluded only from
  the canonical generator; focused solver and parser tests still cover them.
- Finite agreement is never described as a correctness proof, asymptotic
  result, or evidence about \(P\) versus \(NP\).
- A mismatch or invalid model is recorded with the complete formula and both
  solver outcomes before the experiment exits nonzero.
- The evidence `code_commit` must be a 40-hex commit reachable from public
  `origin/main`.
- Use explicit file staging; do not stage unrelated changes.
- Every GitHub file write is sequential and preceded by a fresh blob fetch.
- Publish through the connected GitHub Contents API; do not claim `git push`.
- Source code uses Apache-2.0; original research documentation uses CC BY 4.0.

---

### Task 1: Convert the DIMACS Contract Debt into Permanent Tests

**Files:**
- Create: `tests/test_dimacs_contract.py`
- Read: `foundations/3-sat.md`
- Read: `src/open_np_research/sat3.py`

**Interfaces:**
- Consumes:
  `parse_dimacs_3sat(text: str) -> Formula`,
  `brute_force_solve(formula: Formula) -> dict[int, bool] | None`, and
  `satisfies(formula: Formula, assignment: Mapping[int, bool]) -> bool`.
- Produces: permanent characterization coverage for every accepted or rejected
  DIMACS behavior on which DPLL may rely.

- [ ] **Step 1: Confirm the baseline**

Run:

```powershell
python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

Expected:

```text
...........                                                              [100%]
```

- [ ] **Step 2: Add the complete characterization test file**

Create `tests/test_dimacs_contract.py`:

```python
from __future__ import annotations

import pytest

from open_np_research.sat3 import (
    brute_force_solve,
    parse_dimacs_3sat,
    satisfies,
)


def test_accepts_comments_blanks_spanning_and_multiple_clauses() -> None:
    formula = parse_dimacs_3sat(
        "\n"
        "   c contract example\n"
        "p cnf 5 3\n"
        "1 -1 0 2 2 0\n"
        "-3\n"
        "4 0\n"
        "\n"
    )
    assert formula == ((1, -1), (2, 2), (-3, 4))


def test_accepts_empty_formula_and_unused_declared_variables() -> None:
    empty = parse_dimacs_3sat("p cnf 0 0\n")
    assert empty == ()
    assert brute_force_solve(empty) == {}
    assert satisfies(empty, {})

    unused = parse_dimacs_3sat("p cnf 3 1\n1 0\n")
    assert unused == ((1,),)
    assert brute_force_solve(unused) == {1: True}


def test_accepts_one_two_three_literal_tautological_and_repeated_clauses() -> None:
    formula = parse_dimacs_3sat(
        "p cnf 3 6\n"
        "1 0\n"
        "1 -2 0\n"
        "1 -2 3 0\n"
        "2 2 0\n"
        "3 -3 0\n"
        "1 0\n"
    )
    assert formula == (
        (1,),
        (1, -2),
        (1, -2, 3),
        (2, 2),
        (3, -3),
        (1,),
    )


@pytest.mark.parametrize(
    ("text", "message"),
    (
        ("1 0\n", "missing DIMACS header"),
        ("p cnf 1\n1 0\n", "expected 'p cnf"),
        ("p cnf 1 1\np cnf 1 1\n1 0\n", "exactly one header"),
        ("1 0\np cnf 1 1\n", "before clause data"),
        ("p cnf -1 0\n", "counts must be nonnegative"),
        ("p cnf 1 -1\n", "counts must be nonnegative"),
        ("p cnf 1 1\n1\n", "terminating zero"),
        ("p cnf 1 1\n0\n", "empty clauses"),
        ("p cnf 4 1\n1 2 3 4 0\n", "at most three literals"),
        ("p cnf 1 1\n2 0\n", "exceeds the declared variable count"),
        ("p cnf 1 2\n1 0\n", "clause count"),
    ),
)
def test_rejects_inputs_outside_the_documented_subset(
    text: str,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        parse_dimacs_3sat(text)


def test_rejects_inline_comments() -> None:
    with pytest.raises(ValueError):
        parse_dimacs_3sat("p cnf 1 1\n1 0 c inline comments are excluded\n")


def test_partial_assignment_and_extra_keys_keep_documented_semantics() -> None:
    assert not satisfies(((1,),), {})
    assert satisfies(((1,),), {1: True, 99: False})
```

- [ ] **Step 3: Run the characterization tests**

Run:

```powershell
python -m pytest tests/test_dimacs_contract.py -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

Expected: `16 passed` in the focused file and `27 passed` in the full suite.
These are characterization tests for existing documented behavior, so they are
expected to pass without a production-code change.

- [ ] **Step 4: Commit Task 1**

Run:

```powershell
git add -- tests/test_dimacs_contract.py
git diff --cached --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git diff --cached --name-only
git commit -m "test: lock the DIMACS parser contract"
```

Expected staged path:

```text
tests/test_dimacs_contract.py
```

---

### Task 2: Add the Deterministic DPLL Reference Solver

**Files:**
- Create: `tests/test_dpll.py`
- Modify: `src/open_np_research/sat3.py`
- Modify: `src/open_np_research/__init__.py`
- Modify: `foundations/3-sat.md`

**Interfaces:**
- Consumes: `Clause`, `Formula`, and
  `satisfies(formula: Formula, assignment: Mapping[int, bool]) -> bool`.
- Produces:
  `dpll_solve(formula: Formula) -> dict[int, bool] | None`.

- [ ] **Step 1: Write the failing DPLL tests**

Create `tests/test_dpll.py`:

```python
from __future__ import annotations

from open_np_research.sat3 import dpll_solve, satisfies


def test_dpll_solves_empty_formula() -> None:
    assert dpll_solve(()) == {}


def test_dpll_applies_a_unit_propagation_chain() -> None:
    formula = ((1,), (-1, 2), (-2, 3))
    model = dpll_solve(formula)
    assert model == {1: True, 2: True, 3: True}
    assert satisfies(formula, model)


def test_dpll_detects_conflicting_units() -> None:
    assert dpll_solve(((1,), (-1,))) is None


def test_dpll_backtracks_from_false_to_true() -> None:
    formula = ((1, 2), (1, -2), (-1, 2))
    model = dpll_solve(formula)
    assert model == {1: True, 2: True}
    assert satisfies(formula, model)


def test_dpll_proves_a_two_variable_formula_unsatisfiable() -> None:
    formula = ((1, 2), (1, -2), (-1, 2), (-1, -2))
    assert dpll_solve(formula) is None


def test_dpll_handles_repeated_literals_and_tautologies() -> None:
    formula = ((1, -1), (2, 2))
    model = dpll_solve(formula)
    assert model == {1: False, 2: True}
    assert satisfies(formula, model)


def test_dpll_completes_variables_from_satisfied_clauses() -> None:
    formula = ((1,), (2, -2), (3, -3))
    model = dpll_solve(formula)
    assert model == {1: True, 2: False, 3: False}
    assert satisfies(formula, model)


def test_dpll_uses_a_deterministic_false_first_branch() -> None:
    formula = ((1, 2),)
    expected = {1: False, 2: True}
    assert [dpll_solve(formula) for _ in range(5)] == [expected] * 5
```

- [ ] **Step 2: Verify the intended RED state**

Run:

```powershell
python -m pytest tests/test_dpll.py -q -p no:cacheprovider
```

Expected: collection fails because `dpll_solve` is not exported.

- [ ] **Step 3: Implement the minimal deterministic DPLL search**

Append these private helpers and the public function to
`src/open_np_research/sat3.py`:

```python
def _literal_order(literal: int) -> tuple[int, bool]:
    return (abs(literal), literal < 0)


def _normalize_for_dpll(formula: Formula) -> Formula:
    normalized: list[Clause] = []
    for clause in formula:
        literals = set(clause)
        if any(-literal in literals for literal in literals):
            continue
        normalized.append(tuple(sorted(literals, key=_literal_order)))
    return tuple(normalized)


def _apply_literal(clauses: Formula, literal: int) -> Formula | None:
    false_literal = -literal
    simplified: list[Clause] = []
    for clause in clauses:
        if literal in clause:
            continue
        reduced = tuple(
            candidate for candidate in clause if candidate != false_literal
        )
        if not reduced:
            return None
        simplified.append(reduced)
    return tuple(simplified)


def _dpll_search(
    clauses: Formula,
    assignment: dict[int, bool],
    variables: tuple[int, ...],
) -> dict[int, bool] | None:
    if any(not clause for clause in clauses):
        return None

    while clauses:
        units = sorted(
            (clause[0] for clause in clauses if len(clause) == 1),
            key=_literal_order,
        )
        if not units:
            break

        literal = units[0]
        variable = abs(literal)
        value = literal > 0
        previous = assignment.get(variable)
        if previous is not None and previous != value:
            return None

        simplified = _apply_literal(clauses, literal)
        if simplified is None:
            return None
        assignment = {**assignment, variable: value}
        clauses = simplified

    if not clauses:
        return {
            variable: assignment.get(variable, False)
            for variable in variables
        }

    variable = min(
        abs(literal)
        for clause in clauses
        for literal in clause
        if abs(literal) not in assignment
    )
    for value in (False, True):
        literal = variable if value else -variable
        simplified = _apply_literal(clauses, literal)
        if simplified is None:
            continue
        model = _dpll_search(
            simplified,
            {**assignment, variable: value},
            variables,
        )
        if model is not None:
            return model
    return None


def dpll_solve(formula: Formula) -> dict[int, bool] | None:
    variables = tuple(
        sorted(
            {
                abs(literal)
                for clause in formula
                for literal in clause
            }
        )
    )
    model = _dpll_search(_normalize_for_dpll(formula), {}, variables)
    if model is not None and not satisfies(formula, model):
        raise AssertionError("DPLL returned a model that does not satisfy the formula")
    return model
```

Replace `src/open_np_research/__init__.py` with:

```python
from .sat3 import (
    brute_force_solve,
    dpll_solve,
    parse_dimacs_3sat,
    satisfies,
)

__all__ = [
    "brute_force_solve",
    "dpll_solve",
    "parse_dimacs_3sat",
    "satisfies",
]
```

- [ ] **Step 4: Verify GREEN for the solver**

Run:

```powershell
python -m pytest tests/test_dpll.py -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

Expected: `8 passed` in the focused file and `35 passed` in the full suite.

- [ ] **Step 5: Document the new API and deterministic rules**

In `foundations/3-sat.md`, add `dpll_solve` to the public API block:

```python
parse_dimacs_3sat(text: str) -> Formula
satisfies(formula: Formula, assignment: Mapping[int, bool]) -> bool
brute_force_solve(formula: Formula) -> dict[int, bool] | None
dpll_solve(formula: Formula) -> dict[int, bool] | None
```

After the brute-force semantics, add:

```markdown
`dpll_solve` is a deterministic reference implementation, not a polynomial-time
algorithm. It normalizes repeated literals and tautological clauses only inside
its search, repeatedly applies unit propagation, chooses the lowest-numbered
remaining variable, and tries `False` before `True`. A returned model contains
exactly the variables occurring in the original formula; variables no longer
needed after simplification are completed with `False`. The model is checked
with `satisfies` before it is returned.

Agreement between DPLL and brute force on a finite family is evidence only for
that recorded family. It is not a proof of unrestricted correctness or a
complexity-theoretic conclusion.
```

Add this source under `## Sources`:

```markdown
- Martin Davis, George Logemann, and Donald W. Loveland, “A Machine Program for
  Theorem-Proving,” *Communications of the ACM* 5(7), 394–397, 1962.
  [DOI: 10.1145/368273.368557](https://doi.org/10.1145/368273.368557)
```

- [ ] **Step 6: Run Task 2 verification**

Run:

```powershell
@'
from open_np_research import dpll_solve, satisfies

sat = ((1, 2), (1, -2), (-1, 2))
model = dpll_solve(sat)
assert model == {1: True, 2: True}
assert satisfies(sat, model)

unsat = ((1, 2), (1, -2), (-1, 2), (-1, -2))
assert dpll_solve(unsat) is None
print("PASS: deterministic DPLL contract probe")
'@ | python -
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git diff --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

Expected: the probe passes and the full suite reports `35 passed`.

- [ ] **Step 7: Commit Task 2**

Run:

```powershell
git add -- src/open_np_research/sat3.py src/open_np_research/__init__.py tests/test_dpll.py foundations/3-sat.md
git diff --cached --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git diff --cached --name-only
git commit -m "feat: add deterministic DPLL reference solver"
```

Expected staged paths:

```text
foundations/3-sat.md
src/open_np_research/__init__.py
src/open_np_research/sat3.py
tests/test_dpll.py
```

---

### Task 3: Add the Canonical Family and Agreement Runner

**Files:**
- Create: `src/open_np_research/finite.py`
- Create: `src/open_np_research/agreement.py`
- Create: `tests/test_finite.py`
- Create: `tests/test_agreement.py`

**Interfaces:**
- Consumes:
  `Formula`,
  `brute_force_solve(formula)`,
  `dpll_solve(formula)`, and
  `satisfies(formula, assignment)`.
- Produces:
  `canonical_clauses(variable_count: int) -> tuple[Clause, ...]`,
  `iter_canonical_formulas(variable_count: int, max_clauses: int) -> Iterator[Formula]`,
  `build_agreement_report(*, max_variables: int, max_clauses: int,
  code_commit: str, command: str) -> dict[str, object]`, and
  `python -m open_np_research.agreement`.

- [ ] **Step 1: Write failing canonical-family tests**

Create `tests/test_finite.py`:

```python
from __future__ import annotations

import pytest

from open_np_research.finite import (
    canonical_clauses,
    iter_canonical_formulas,
)


def test_canonical_clause_counts_and_order() -> None:
    assert canonical_clauses(0) == ()
    assert canonical_clauses(1) == ((-1,), (1,))
    assert canonical_clauses(2) == (
        (-1,),
        (1,),
        (-2,),
        (2,),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
    )
    assert len(canonical_clauses(3)) == 26


def test_formula_iteration_uses_distinct_canonical_combinations() -> None:
    assert tuple(iter_canonical_formulas(1, 3)) == (
        (),
        ((-1,),),
        ((1,),),
        ((-1,), (1,)),
    )


@pytest.mark.parametrize(
    ("variable_count", "max_clauses"),
    ((-1, 0), (0, -1)),
)
def test_formula_family_rejects_negative_parameters(
    variable_count: int,
    max_clauses: int,
) -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        tuple(iter_canonical_formulas(variable_count, max_clauses))
```

- [ ] **Step 2: Verify RED for the missing finite module**

Run:

```powershell
python -m pytest tests/test_finite.py -q -p no:cacheprovider
```

Expected: collection fails because `open_np_research.finite` does not exist.

- [ ] **Step 3: Implement the canonical finite family**

Create `src/open_np_research/finite.py`:

```python
from __future__ import annotations

from itertools import combinations, product
from typing import Iterator

from .sat3 import Clause, Formula


def canonical_clauses(variable_count: int) -> tuple[Clause, ...]:
    if variable_count < 0:
        raise ValueError("variable_count must be nonnegative")

    clauses: list[Clause] = []
    variables = range(1, variable_count + 1)
    for width in range(1, min(3, variable_count) + 1):
        for selected in combinations(variables, width):
            for signs in product((-1, 1), repeat=width):
                clauses.append(
                    tuple(
                        variable * sign
                        for variable, sign in zip(
                            selected,
                            signs,
                            strict=True,
                        )
                    )
                )
    return tuple(clauses)


def iter_canonical_formulas(
    variable_count: int,
    max_clauses: int,
) -> Iterator[Formula]:
    if variable_count < 0:
        raise ValueError("variable_count must be nonnegative")
    if max_clauses < 0:
        raise ValueError("max_clauses must be nonnegative")

    clauses = canonical_clauses(variable_count)
    for clause_count in range(0, min(max_clauses, len(clauses)) + 1):
        yield from combinations(clauses, clause_count)
```

- [ ] **Step 4: Verify GREEN for the finite family**

Run:

```powershell
python -m pytest tests/test_finite.py -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

Expected: `4 passed`.

- [ ] **Step 5: Write failing agreement-report tests**

Create `tests/test_agreement.py`:

```python
from __future__ import annotations

import json

import pytest

from open_np_research import agreement


def test_ci_family_has_394_agreeing_raw_cases() -> None:
    report = agreement.build_agreement_report(
        max_variables=3,
        max_clauses=2,
        code_commit="0" * 40,
        command="finite CI contract",
    )

    assert report["formula_count"] == 394
    assert report["mismatch_count"] == 0
    assert report["sat_count"] + report["unsat_count"] == 394
    assert len(report["cases"]) == 394
    assert len(report["input_sha256"]) == 64
    assert len(report["outcome_sha256"]) == 64
    assert all(
        case["brute_force"]["model_valid"] is not False
        and case["dpll"]["model_valid"] is not False
        for case in report["cases"]
    )


def test_agreement_digests_and_case_order_are_deterministic() -> None:
    first = agreement.build_agreement_report(
        max_variables=2,
        max_clauses=2,
        code_commit="1" * 40,
        command="determinism contract",
    )
    second = agreement.build_agreement_report(
        max_variables=2,
        max_clauses=2,
        code_commit="1" * 40,
        command="determinism contract",
    )

    assert first["formula_count"] == 42
    assert first["input_sha256"] == second["input_sha256"]
    assert first["outcome_sha256"] == second["outcome_sha256"]
    assert first["cases"] == second["cases"]


def test_mismatches_preserve_complete_raw_cases(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(agreement, "dpll_solve", lambda formula: None)
    report = agreement.build_agreement_report(
        max_variables=1,
        max_clauses=1,
        code_commit="2" * 40,
        command="forced mismatch contract",
    )

    assert report["formula_count"] == 4
    assert report["mismatch_count"] == 4
    assert report["mismatches"] == report["cases"]
    assert all("formula" in case for case in report["mismatches"])
    assert all("brute_force" in case for case in report["mismatches"])
    assert all("dpll" in case for case in report["mismatches"])


def test_cli_rejects_an_unavailable_public_commit(
    tmp_path,
) -> None:
    output = tmp_path / "results.json"
    exit_code = agreement.main(
        [
            "--max-variables",
            "1",
            "--max-clauses",
            "1",
            "--code-commit",
            "0" * 40,
            "--output",
            str(output),
        ]
    )
    assert exit_code == 2
    assert not output.exists()


def test_report_is_json_serializable() -> None:
    report = agreement.build_agreement_report(
        max_variables=1,
        max_clauses=1,
        code_commit="3" * 40,
        command="serialization contract",
    )
    assert json.loads(json.dumps(report)) == report
```

- [ ] **Step 6: Verify RED for the missing agreement module**

Run:

```powershell
python -m pytest tests/test_agreement.py -q -p no:cacheprovider
```

Expected: collection fails because `open_np_research.agreement` does not exist.

- [ ] **Step 7: Implement the agreement report and CLI**

Create `src/open_np_research/agreement.py`:

```python
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Callable, Sequence

from .finite import iter_canonical_formulas
from .sat3 import (
    Formula,
    brute_force_solve,
    dpll_solve,
    satisfies,
)

Solver = Callable[[Formula], dict[int, bool] | None]
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}")
SCHEMA_VERSION = 1
GENERATOR_VERSION = 1


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )


def _formula_data(formula: Formula) -> list[list[int]]:
    return [list(clause) for clause in formula]


def _model_data(
    model: dict[int, bool] | None,
) -> dict[str, bool] | None:
    if model is None:
        return None
    return {
        str(variable): model[variable]
        for variable in sorted(model)
    }


def _solver_outcome(
    solver: Solver,
    formula: Formula,
) -> dict[str, object]:
    try:
        model = solver(formula)
    except Exception as error:
        return {
            "status": "error",
            "model": None,
            "model_valid": False,
            "error": f"{type(error).__name__}: {error}",
        }

    if model is None:
        return {
            "status": "unsat",
            "model": None,
            "model_valid": None,
            "error": None,
        }
    return {
        "status": "sat",
        "model": _model_data(model),
        "model_valid": satisfies(formula, model),
        "error": None,
    }


def build_agreement_report(
    *,
    max_variables: int,
    max_clauses: int,
    code_commit: str,
    command: str,
) -> dict[str, object]:
    if max_variables < 0 or max_clauses < 0:
        raise ValueError("finite-domain limits must be nonnegative")
    if COMMIT_PATTERN.fullmatch(code_commit) is None:
        raise ValueError("code_commit must be exactly 40 lowercase hex characters")

    input_digest = hashlib.sha256()
    outcome_digest = hashlib.sha256()
    cases: list[dict[str, object]] = []
    mismatches: list[dict[str, object]] = []
    sat_count = 0
    unsat_count = 0

    for variable_count in range(max_variables + 1):
        for formula in iter_canonical_formulas(
            variable_count,
            max_clauses,
        ):
            input_record = {
                "variable_count": variable_count,
                "formula": _formula_data(formula),
            }
            input_line = _canonical_json(input_record)
            input_digest.update((input_line + "\n").encode("utf-8"))

            brute_force = _solver_outcome(brute_force_solve, formula)
            dpll = _solver_outcome(dpll_solve, formula)
            mismatch = (
                brute_force["status"] != dpll["status"]
                or brute_force["model_valid"] is False
                or dpll["model_valid"] is False
            )
            if brute_force["status"] == "sat":
                sat_count += 1
            elif brute_force["status"] == "unsat":
                unsat_count += 1

            case = {
                "case_number": len(cases) + 1,
                "case_id": hashlib.sha256(
                    input_line.encode("utf-8")
                ).hexdigest(),
                **input_record,
                "brute_force": brute_force,
                "dpll": dpll,
                "mismatch": mismatch,
            }
            outcome_digest.update(
                (_canonical_json(case) + "\n").encode("utf-8")
            )
            cases.append(case)
            if mismatch:
                mismatches.append(case)

    return {
        "schema_version": SCHEMA_VERSION,
        "experiment_id": "dpll-agreement-v1",
        "code_commit": code_commit,
        "command": command,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "project_version": version("open-np-research"),
            "runtime_dependencies": [],
        },
        "generator": {
            "version": GENERATOR_VERSION,
            "max_variables": max_variables,
            "max_clauses": max_clauses,
            "clause_widths": [1, 2, 3],
            "distinct_variables_per_clause": True,
            "tautologies": False,
            "duplicate_clauses": False,
        },
        "seed": None,
        "formula_count": len(cases),
        "sat_count": sat_count,
        "unsat_count": unsat_count,
        "mismatch_count": len(mismatches),
        "input_sha256": input_digest.hexdigest(),
        "outcome_sha256": outcome_digest.hexdigest(),
        "finite_domain_statement": (
            "This report covers only the enumerated finite family and does not "
            "prove unrestricted solver correctness or any complexity claim."
        ),
        "performance_claim": None,
        "mismatches": mismatches,
        "cases": cases,
    }


def _require_public_commit(code_commit: str) -> None:
    if COMMIT_PATTERN.fullmatch(code_commit) is None:
        raise ValueError("code_commit must be exactly 40 lowercase hex characters")

    exists = subprocess.run(
        ["git", "cat-file", "-e", f"{code_commit}^{{commit}}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if exists.returncode != 0:
        raise ValueError("code_commit is unavailable in the local repository")

    public = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            code_commit,
            "origin/main",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if public.returncode != 0:
        raise ValueError("code_commit is not reachable from public origin/main")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare deterministic DPLL with brute force on a finite family."
    )
    parser.add_argument("--max-variables", type=int, required=True)
    parser.add_argument("--max-clauses", type=int, required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        _require_public_commit(args.code_commit)
        command = (
            "python -m open_np_research.agreement "
            f"--max-variables {args.max_variables} "
            f"--max-clauses {args.max_clauses} "
            f"--code-commit {args.code_commit} "
            f"--output {args.output.as_posix()}"
        )
        report = build_agreement_report(
            max_variables=args.max_variables,
            max_clauses=args.max_clauses,
            code_commit=args.code_commit,
            command=command,
        )
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        _canonical_json(
            {
                "formula_count": report["formula_count"],
                "mismatch_count": report["mismatch_count"],
                "input_sha256": report["input_sha256"],
                "outcome_sha256": report["outcome_sha256"],
                "output": args.output.as_posix(),
            }
        )
    )
    return 1 if report["mismatch_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 8: Verify GREEN and the exact CI domain**

Run:

```powershell
python -m pytest tests/test_finite.py tests/test_agreement.py -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

Expected: `9 passed` in the two focused files and `44 passed` in the full
suite.

- [ ] **Step 9: Run Task 3 structural probes**

Run:

```powershell
@'
from open_np_research.agreement import build_agreement_report
from open_np_research.finite import canonical_clauses

assert [len(canonical_clauses(n)) for n in range(4)] == [0, 2, 8, 26]
report = build_agreement_report(
    max_variables=3,
    max_clauses=2,
    code_commit="f" * 40,
    command="task 3 structural probe",
)
assert report["formula_count"] == 394
assert report["mismatch_count"] == 0
assert len(report["cases"]) == 394
print("PASS: 394-case finite differential contract")
'@ | python -
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git diff --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

Expected:

```text
PASS: 394-case finite differential contract
```

- [ ] **Step 10: Commit Task 3**

Run:

```powershell
git add -- src/open_np_research/finite.py src/open_np_research/agreement.py tests/test_finite.py tests/test_agreement.py
git diff --cached --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git diff --cached --name-only
git commit -m "feat: add bounded solver agreement runner"
```

Expected staged paths:

```text
src/open_np_research/agreement.py
src/open_np_research/finite.py
tests/test_agreement.py
tests/test_finite.py
```

---

### Task 4: Publish the Reviewed Implementation and Record Evidence

**Files:**
- Create: `experiments/dpll-agreement-v1/README.md`
- Create mechanically: `experiments/dpll-agreement-v1/results.json`
- Modify: `experiments/README.md`
- Read: `.superpowers/sdd/` task review reports

**Interfaces:**
- Consumes: the independently approved Task 1–3 commits and the connected
  GitHub Contents API.
- Produces:
  `PUBLIC_IMPLEMENTATION_COMMIT`, a public commit containing all reviewed
  implementation files, and a local experiment record bound to that commit.

- [ ] **Step 1: Run the pre-publication gate**

Run:

```powershell
python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git diff --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$status = git status --porcelain=v1
if ($status) { $status; exit 1 }
```

Expected: `44 passed`, no whitespace output, and clean status.

- [ ] **Step 2: Publish the reviewed implementation sequentially**

For each path below, fetch public `main` immediately before writing. Update an
existing path with its freshly fetched blob SHA; create a missing path only
after a fresh `404`.

```text
docs/superpowers/specs/2026-07-23-dpll-reference-baseline-design.md
docs/superpowers/plans/2026-07-23-dpll-reference-baseline.md
tests/test_dimacs_contract.py
src/open_np_research/sat3.py
src/open_np_research/__init__.py
tests/test_dpll.py
foundations/3-sat.md
src/open_np_research/finite.py
src/open_np_research/agreement.py
tests/test_finite.py
tests/test_agreement.py
```

Use the applicable local task subject:

```text
docs: design deterministic DPLL baseline
docs: plan deterministic DPLL baseline
test: lock the DIMACS parser contract
feat: add deterministic DPLL reference solver
feat: add bounded solver agreement runner
```

After the last successful write, record its returned commit as
`PUBLIC_IMPLEMENTATION_COMMIT`. Fetch `origin/main`, confirm the commit is its
tip, and compare all eleven public blobs and full UTF-8 contents with local
`HEAD`.

Expected: `11/11 reviewed implementation files match local HEAD`.

- [ ] **Step 3: Run the public-commit-bound experiment**

Run:

```powershell
git fetch origin main
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$publicImplementationCommit = (git rev-parse origin/main).Trim()
if ($publicImplementationCommit -notmatch '^[0-9a-f]{40}$') {
    throw 'origin/main did not resolve to a 40-hex commit'
}
python -m open_np_research.agreement `
  --max-variables 3 `
  --max-clauses 3 `
  --code-commit $publicImplementationCommit `
  --output experiments/dpll-agreement-v1/results.json
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

Expected: one JSON summary line with `formula_count` 3050 and
`mismatch_count` 0.

- [ ] **Step 4: Validate every result invariant**

Run:

```powershell
@'
from pathlib import Path
import json
import re

path = Path("experiments/dpll-agreement-v1/results.json")
report = json.loads(path.read_text(encoding="utf-8"))
assert report["schema_version"] == 1
assert report["experiment_id"] == "dpll-agreement-v1"
assert re.fullmatch(r"[0-9a-f]{40}", report["code_commit"])
assert report["generator"]["max_variables"] == 3
assert report["generator"]["max_clauses"] == 3
assert report["seed"] is None
assert report["formula_count"] == 3050
assert report["sat_count"] + report["unsat_count"] == 3050
assert report["mismatch_count"] == 0
assert report["mismatches"] == []
assert len(report["cases"]) == 3050
assert len(report["input_sha256"]) == 64
assert len(report["outcome_sha256"]) == 64
assert all(
    case["brute_force"]["model_valid"] is not False
    and case["dpll"]["model_valid"] is not False
    and case["mismatch"] is False
    for case in report["cases"]
)
assert "finite family" in report["finite_domain_statement"]
assert report["performance_claim"] is None
print(
    "PASS: 3050 cases, zero mismatches, all returned models verified; "
    f"code_commit={report['code_commit']}"
)
'@ | python -
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
```

- [ ] **Step 5: Prove exact replay determinism**

Run the exact command from the report a second time against the same output
path and compare file hashes:

```powershell
$path = 'experiments\dpll-agreement-v1\results.json'
$firstHash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
$report = Get-Content -Raw -LiteralPath $path | ConvertFrom-Json
python -m open_np_research.agreement `
  --max-variables 3 `
  --max-clauses 3 `
  --code-commit $report.code_commit `
  --output experiments/dpll-agreement-v1/results.json
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$secondHash = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash
if ($firstHash -ne $secondHash) {
    throw "Replay changed results.json: $firstHash != $secondHash"
}
"PASS: exact replay SHA256=$secondHash"
```

- [ ] **Step 6: Add the experiment documentation**

Create `experiments/dpll-agreement-v1/README.md`:

```markdown
# DPLL Agreement v1

This experiment compares the repository's deterministic DPLL reference solver
with its independently structured brute-force solver.

## Finite Domain

The generator enumerates declared variable counts 0 through 3 and formulas
containing at most three distinct canonical clauses. Canonical clauses contain
one to three distinct variables, choose each sign independently, and exclude
tautologies. Formulas exclude duplicate clauses. The resulting record contains
exactly 3,050 cases.

Repeated literals, tautologies, duplicate clauses, and other accepted parser
boundaries are covered separately by focused tests; they are not part of this
enumerated family.

## Artifact

[`results.json`](results.json) stores every formula, both solver outcomes,
returned models, model-verification results, input and outcome digests,
environment data, and the exact public implementation commit.

## Replay

From the repository root:

```powershell
$report = Get-Content -Raw `
  experiments/dpll-agreement-v1/results.json | ConvertFrom-Json
python -m open_np_research.agreement `
  --max-variables 3 `
  --max-clauses 3 `
  --code-commit $report.code_commit `
  --output experiments/dpll-agreement-v1/results.json
```

A successful replay exits zero and reproduces the same file SHA-256 on the same
recorded environment. A disagreement or invalid model remains in the JSON and
causes a nonzero exit.

## Interpretation

Zero mismatches mean only that the two implementations agreed on the recorded
finite family and that every returned SAT model passed the verifier. This is
not a proof of unrestricted solver correctness, a running-time bound, or a
conclusion about P versus NP.
```

Append this section to `experiments/README.md`:

```markdown
## Current Experiments

- [DPLL Agreement v1](dpll-agreement-v1/README.md) records case-by-case
  finite-domain agreement between the deterministic DPLL and brute-force
  reference solvers.
```

- [ ] **Step 7: Run Task 4 verification and commit the evidence**

Run:

```powershell
python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git diff --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git add -- experiments/README.md experiments/dpll-agreement-v1/README.md experiments/dpll-agreement-v1/results.json
git diff --cached --check
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git diff --cached --name-only
git commit -m "experiments: record bounded DPLL agreement"
```

Expected staged paths:

```text
experiments/README.md
experiments/dpll-agreement-v1/README.md
experiments/dpll-agreement-v1/results.json
```

---

### Task 5: Publish Evidence, Open Reproduction Work, and Verify Parity

**Files:**
- Publish: `experiments/README.md`
- Publish: `experiments/dpll-agreement-v1/README.md`
- Publish: `experiments/dpll-agreement-v1/results.json`
- Verify: all fourteen milestone paths
- Create ignored: `.superpowers/sdd/dpll-baseline-final-report.md`

**Interfaces:**
- Consumes: approved local evidence and `PUBLIC_IMPLEMENTATION_COMMIT`.
- Produces: byte-equivalent public evidence, a public reproduction Issue, and
  the final publication report.

- [ ] **Step 1: Run the complete local gate**

Run:

```powershell
python -m pytest -q -p no:cacheprovider
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
git diff --check main..HEAD
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$status = git status --porcelain=v1
if ($status) { $status; exit 1 }
```

Expected: `44 passed`, no whitespace output, and clean status.

- [ ] **Step 2: Publish the three evidence files sequentially**

Freshly fetch each path, then create or update it on public `main` with the
complete local UTF-8 content:

```text
experiments/README.md
experiments/dpll-agreement-v1/README.md
experiments/dpll-agreement-v1/results.json
```

Use commit message:

```text
experiments: record bounded DPLL agreement
```

Record the commit returned by the final results write as
`PUBLIC_EVIDENCE_COMMIT`.

- [ ] **Step 3: Verify all fourteen public files**

Freshly fetch these paths from public `main`:

```text
docs/superpowers/specs/2026-07-23-dpll-reference-baseline-design.md
docs/superpowers/plans/2026-07-23-dpll-reference-baseline.md
tests/test_dimacs_contract.py
src/open_np_research/sat3.py
src/open_np_research/__init__.py
tests/test_dpll.py
foundations/3-sat.md
src/open_np_research/finite.py
src/open_np_research/agreement.py
tests/test_finite.py
tests/test_agreement.py
experiments/README.md
experiments/dpll-agreement-v1/README.md
experiments/dpll-agreement-v1/results.json
```

For every path, compare the returned blob SHA and complete decoded UTF-8
content with local `HEAD:<path>`.

Expected:

```text
14/14 public blobs and UTF-8 contents match local HEAD
```

Also fetch `results.json`, confirm its `code_commit` equals
`PUBLIC_IMPLEMENTATION_COMMIT`, and confirm that commit is an ancestor of
`PUBLIC_EVIDENCE_COMMIT`.

- [ ] **Step 4: Create the public independent-reproduction Issue**

Create one public Issue with:

```text
Title: Reproduce the bounded DPLL agreement baseline
Labels: help wanted, good first issue
```

Construct the body from the actual public commit variables so interpolation
places the 40-hex SHAs and direct links into the GitHub request:

```markdown
## Objective

Independently reproduce and review the DPLL Agreement v1 finite-domain result.

## Bound versions

- Reviewed implementation:
  [`$publicImplementationCommit`](https://github.com/ApacheWang/open-np-hard-research/commit/$publicImplementationCommit)
- Published evidence:
  [`$publicEvidenceCommit`](https://github.com/ApacheWang/open-np-hard-research/commit/$publicEvidenceCommit)
- Experiment record: `experiments/dpll-agreement-v1/results.json`

## Replay

Run the command documented in
`experiments/dpll-agreement-v1/README.md` from a checkout containing the bound
implementation commit. Report the operating system, Python version, command,
input SHA-256, outcome SHA-256, and final file SHA-256.

## Independent checks

- Review the DPLL unit propagation and fixed branching order.
- Recompute at least one shard with an implementation that does not import the
  project solver code.
- Verify every reported SAT model with an independent evaluator.
- If any result differs, attach the complete formula and both raw outcomes.
  Do not average away or omit a mismatch.

## Scope

The record covers exactly 3,050 finite canonical cases. Agreement is not a
proof of unrestricted correctness, a complexity bound, or evidence about
P versus NP.

Confirmed discrepancies will be preserved under `negative-results/`. Credit is
recorded under each contributor's actual role; result-specific mathematical
credit follows `GOVERNANCE.md`.
```

Use an interpolating here-string or equivalent string construction before the
GitHub tool call. The actual Issue must contain full 40-hex SHAs, not the
PowerShell variable names shown in the construction template.

- [ ] **Step 5: Verify the public Issue**

Fetch the Issue and confirm:

- it is open;
- both labels are present;
- both public commit SHAs and the results path are visible;
- it contains `3,050 finite canonical cases`;
- it requests complete mismatch evidence; and
- it explicitly rejects P-versus-NP inference.

- [ ] **Step 6: Write the ignored final report**

Use `apply_patch` to create
`.superpowers/sdd/dpll-baseline-final-report.md` with:

- local commit SHAs and subjects;
- RED and GREEN evidence for Tasks 2 and 3;
- focused and full test outputs;
- exact CI and published family counts;
- input, outcome, and file SHA-256 values;
- `PUBLIC_IMPLEMENTATION_COMMIT`;
- `PUBLIC_EVIDENCE_COMMIT`;
- the fourteen-path parity table;
- the public Issue number and URL;
- final Git status; and
- every remaining concern.

Do not commit the ignored report.

- [ ] **Step 7: Request the final whole-branch review**

Generate a review package from the recorded merge base through final local
`HEAD`. The reviewer must inspect:

- the design and plan;
- parser-contract coverage;
- DPLL correctness and deterministic semantics;
- canonical-family independence and exact case counts;
- mismatch preservation;
- the complete JSON evidence;
- finite-domain language;
- all fourteen public file comparisons; and
- the public reproduction Issue.

Critical and Important findings must be fixed, republished, and re-reviewed.
The required final verdict is:

```text
Ready to merge? Yes
```
