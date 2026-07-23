# Open NP-Hard Research Lab Launch Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Launch `ApacheWang/open-np-hard-research` as a public, globally accessible, reproducible research lab with a working 3-SAT verification baseline and clear contribution pathways.

**Architecture:** The repository separates governance, research claims, mathematical foundations, executable experiments, and community workflows. A small Python package provides a trusted 3-SAT parser, assignment verifier, and brute-force reference solver; GitHub Actions validates it. GitHub Discussions host broad conversation, Issues hold bounded work, and Pull Requests carry durable, reviewable changes.

**Tech Stack:** Markdown, YAML, Python 3.11+, pytest 8+, GitHub Actions, Git, GitHub

## Global Constraints

- The repository is public at `ApacheWang/open-np-hard-research`.
- English is the canonical technical language; community-maintained translations are welcome.
- 3-SAT is the initial anchor problem.
- Computational verification over finitely many inputs must never be described as proving an unrestricted theorem.
- No project communication may state that \(P=NP\), \(P\ne NP\), or a Millennium Prize Problem has been solved while the work remains below `externally-reviewed`.
- Source code uses Apache License 2.0.
- Original research notes, diagrams, and documentation use CC BY 4.0.
- Failed and refuted approaches remain visible in `negative-results/`.
- Every executable result records dependencies, commands, and deterministic seeds when randomness is used.

---

### Task 1: Establish the Public Research Charter

**Files:**
- Create: `README.md`
- Create: `README.zh-CN.md`
- Create: `ROADMAP.md`
- Create: `GOVERNANCE.md`
- Create: `CONTRIBUTING.md`
- Create: `CODE_OF_CONDUCT.md`
- Create: `CITATION.cff`
- Create: `LICENSE-CODE`
- Create: `LICENSE-RESEARCH`

**Interfaces:**
- Consumes: the approved repository design.
- Produces: canonical mission, scope, contribution rules, attribution policy, and licensing rules used by every later task.

- [ ] **Step 1: Write the English launch README**

Create `README.md` with these exact top-level sections:

```markdown
# Open NP-Hard Research

An open, worldwide, rigorous, and reproducible research lab for NP-hard problems.

> This project has not solved P versus NP. Finite experiments are evidence about
> tested instances only; they are not proofs of unrestricted complexity claims.

## Start Here
## Initial Focus: 3-SAT
## Ways to Contribute
## Research Claim Levels
## Repository Map
## Reproducibility
## Languages and Translations
## Governance and Conduct
## Licensing and Citation
```

The body must link to `ROADMAP.md`, `CONTRIBUTING.md`, `GOVERNANCE.md`,
`CODE_OF_CONDUCT.md`, `docs/CLAIM_LEVELS.md`, `foundations/3-sat.md`,
`README.zh-CN.md`, both license files, and `CITATION.cff`.

- [ ] **Step 2: Write the Chinese project introduction**

Create `README.zh-CN.md` as a faithful translation of the English README. Add this notice immediately below the title:

```markdown
> 本页是中文翻译；技术规则以 [English README](README.md) 及其所链接的英文规范为准。
```

- [ ] **Step 3: Write roadmap and governance**

Create `ROADMAP.md` with three milestones:

1. reproducible 3-SAT baseline;
2. literature and known-barrier map;
3. reviewed hypothesis and counterexample pipeline.

Create `GOVERNANCE.md` with the approved rules:

- routine changes need one approving review;
- major theorem claims need two independent reviews;
- one major-claim reviewer must not have drafted the claim;
- unresolved objections remain public;
- governance changes require a public issue and recorded maintainer decision.

- [ ] **Step 4: Write contribution and conduct rules**

Create `CONTRIBUTING.md` with:

- a newcomer path for reproduction, tests, counterexamples, references, and translations;
- the requirement to open or reference an Issue for research claims;
- exact local commands: `python -m pip install -e .[dev]` and `pytest -q`;
- a contributor licensing statement assigning code contributions to Apache-2.0 and original prose/diagrams to CC BY 4.0;
- a rule against claiming universal results from finite tests.

Create `CODE_OF_CONDUCT.md` using Contributor Covenant 2.1 language and set the enforcement contact to repository-owner contact through GitHub rather than publishing a private email address.

- [ ] **Step 5: Add attribution and licenses**

Create `CITATION.cff`:

```yaml
cff-version: 1.2.0
title: Open NP-Hard Research
message: If you use this project, cite the repository release and the named contributors to the specific result.
type: software
authors:
  - family-names: Wang
    given-names: ApacheWang
repository-code: https://github.com/ApacheWang/open-np-hard-research
license: Apache-2.0
```

Copy the complete, unmodified Apache License 2.0 text into `LICENSE-CODE` and
the complete, unmodified CC BY 4.0 legal code into `LICENSE-RESEARCH`.

- [ ] **Step 6: Validate and commit the charter**

Run:

```powershell
rg -n "P ?= ?NP|P ?!= ?NP|P ?≠ ?NP" README.md README.zh-CN.md ROADMAP.md GOVERNANCE.md CONTRIBUTING.md
git diff --check
```

Expected: the only matches are disclaimers or claim-review rules; `git diff --check` emits no output.

Commit:

```powershell
git add README.md README.zh-CN.md ROADMAP.md GOVERNANCE.md CONTRIBUTING.md CODE_OF_CONDUCT.md CITATION.cff LICENSE-CODE LICENSE-RESEARCH
git commit -m "docs: establish open research charter"
```

### Task 2: Build the Trusted 3-SAT Baseline with TDD

**Files:**
- Create: `pyproject.toml`
- Create: `src/open_np_research/__init__.py`
- Create: `src/open_np_research/sat3.py`
- Create: `tests/test_sat3.py`
- Create: `experiments/README.md`
- Create: `benchmarks/README.md`

**Interfaces:**
- Consumes: integers as DIMACS literals and UTF-8 DIMACS CNF text.
- Produces:
  - `parse_dimacs_3sat(text: str) -> Formula`
  - `satisfies(formula: Formula, assignment: Mapping[int, bool]) -> bool`
  - `brute_force_solve(formula: Formula) -> dict[int, bool] | None`

- [ ] **Step 1: Create package metadata**

Create `pyproject.toml`:

```toml
[build-system]
requires = ["setuptools>=75"]
build-backend = "setuptools.build_meta"

[project]
name = "open-np-research"
version = "0.1.0"
requires-python = ">=3.11"
license = {text = "Apache-2.0"}
dependencies = []

[project.optional-dependencies]
dev = ["pytest>=8.3,<9"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
```

Create `src/open_np_research/__init__.py` exporting the three public functions.

- [ ] **Step 2: Write failing parser and verifier tests**

Create `tests/test_sat3.py`:

```python
import pytest

from open_np_research.sat3 import (
    brute_force_solve,
    parse_dimacs_3sat,
    satisfies,
)


def test_parse_and_verify_satisfying_assignment() -> None:
    formula = parse_dimacs_3sat(
        "c example\np cnf 3 2\n1 -2 3 0\n-1 2 3 0\n"
    )
    assert satisfies(formula, {1: True, 2: True, 3: True})


def test_incomplete_assignment_does_not_satisfy_a_negative_literal() -> None:
    formula = parse_dimacs_3sat("p cnf 1 1\n-1 0\n")
    assert not satisfies(formula, {})


def test_rejects_clause_with_more_than_three_literals() -> None:
    with pytest.raises(ValueError, match="at most three"):
        parse_dimacs_3sat("p cnf 4 1\n1 2 3 4 0\n")


def test_rejects_header_count_mismatch() -> None:
    with pytest.raises(ValueError, match="clause count"):
        parse_dimacs_3sat("p cnf 2 2\n1 2 0\n")


def test_brute_force_solver_finds_model() -> None:
    formula = parse_dimacs_3sat("p cnf 2 2\n1 2 0\n-1 2 0\n")
    model = brute_force_solve(formula)
    assert model is not None
    assert satisfies(formula, model)


def test_brute_force_solver_reports_unsatisfiable() -> None:
    formula = parse_dimacs_3sat("p cnf 1 2\n1 0\n-1 0\n")
    assert brute_force_solve(formula) is None
```

- [ ] **Step 3: Run tests and confirm the intended failure**

Run:

```powershell
python -m pip install -e ".[dev]"
pytest -q
```

Expected: collection fails because `open_np_research.sat3` does not yet exist.

- [ ] **Step 4: Implement the minimal trusted baseline**

Create `src/open_np_research/sat3.py`:

```python
from __future__ import annotations

from itertools import product
from typing import Mapping, TypeAlias

Clause: TypeAlias = tuple[int, ...]
Formula: TypeAlias = tuple[Clause, ...]


def parse_dimacs_3sat(text: str) -> Formula:
    header: tuple[int, int] | None = None
    clauses: list[Clause] = []
    pending: list[int] = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            parts = line.split()
            if len(parts) != 4 or parts[:2] != ["p", "cnf"]:
                raise ValueError("expected 'p cnf <variables> <clauses>' header")
            header = (int(parts[2]), int(parts[3]))
            continue

        for token in line.split():
            literal = int(token)
            if literal == 0:
                if not pending:
                    raise ValueError("empty clauses are not accepted by this baseline")
                if len(pending) > 3:
                    raise ValueError("3-SAT clauses must contain at most three literals")
                clauses.append(tuple(pending))
                pending = []
            else:
                pending.append(literal)

    if header is None:
        raise ValueError("missing DIMACS header")
    if pending:
        raise ValueError("clause is missing its terminating zero")

    variable_count, declared_clause_count = header
    if len(clauses) != declared_clause_count:
        raise ValueError("DIMACS clause count does not match the header")
    if any(abs(literal) > variable_count for clause in clauses for literal in clause):
        raise ValueError("literal exceeds the declared variable count")
    return tuple(clauses)


def satisfies(formula: Formula, assignment: Mapping[int, bool]) -> bool:
    return all(
        any(
            abs(literal) in assignment
            and assignment[abs(literal)] == (literal > 0)
            for literal in clause
        )
        for clause in formula
    )


def brute_force_solve(formula: Formula) -> dict[int, bool] | None:
    variables = sorted({abs(literal) for clause in formula for literal in clause})
    for values in product((False, True), repeat=len(variables)):
        assignment = dict(zip(variables, values, strict=True))
        if satisfies(formula, assignment):
            return assignment
    return None
```

Create `src/open_np_research/__init__.py`:

```python
from .sat3 import brute_force_solve, parse_dimacs_3sat, satisfies

__all__ = ["brute_force_solve", "parse_dimacs_3sat", "satisfies"]
```

- [ ] **Step 5: Run tests and confirm success**

Run:

```powershell
pytest -q
```

Expected: `6 passed`.

- [ ] **Step 6: Document experiments and benchmarks**

Create `experiments/README.md` requiring:

- exact command;
- Git commit;
- Python and dependency versions;
- machine description;
- input provenance and checksums;
- deterministic seed;
- raw and summarized outputs;
- explicit finite-domain limitation.

Create `benchmarks/README.md` requiring license, provenance, generator version,
checksum, variable count, clause count, and known satisfiability status.

- [ ] **Step 7: Commit the baseline**

```powershell
git add pyproject.toml src tests experiments benchmarks
git commit -m "feat: add trusted 3-SAT baseline"
```

### Task 3: Add Research Protocols and Failure Preservation

**Files:**
- Create: `docs/CLAIM_LEVELS.md`
- Create: `foundations/README.md`
- Create: `foundations/3-sat.md`
- Create: `hypotheses/TEMPLATE.md`
- Create: `proofs/README.md`
- Create: `reductions/README.md`
- Create: `negative-results/README.md`
- Create: `translations/README.md`

**Interfaces:**
- Consumes: governance and claim-review requirements.
- Produces: templates and definitions used by Issues, Pull Requests, and reviewers.

- [ ] **Step 1: Define claim levels**

Create `docs/CLAIM_LEVELS.md` defining exactly:

`idea`, `conjecture`, `experimentally-tested`, `proof-draft`,
`internally-checked`, `externally-reviewed`, and `published`.

State that status describes review progress rather than mathematical truth.

- [ ] **Step 2: Document the 3-SAT foundation**

Create `foundations/3-sat.md` with:

- Boolean variables, literals, clauses, CNF, 3-CNF, assignment, satisfiable, and unsatisfiable;
- the repository's accepted DIMACS subset;
- a statement that 3-SAT is an NP-complete decision problem;
- a bibliography section linking to primary or authoritative sources;
- a clear distinction among solving one instance, improving an exponential algorithm, and proving a polynomial worst-case bound.

- [ ] **Step 3: Create hypothesis and proof templates**

Create `hypotheses/TEMPLATE.md` requiring:

- identifier and status;
- quantified formal statement;
- motivation and related work;
- assumptions and computational model;
- falsification condition;
- smallest tested domain;
- known barriers;
- linked experiments, counterexamples, and proof dependencies.

Create `proofs/README.md` requiring named lemmas, a dependency list, explicit
quantifiers, reviewer objections, and claim status.

- [ ] **Step 4: Preserve reductions, failures, and translations**

Create:

- `reductions/README.md` requiring polynomial-time construction, forward and reverse correctness, and size/time bounds;
- `negative-results/README.md` requiring attempted claim, counterexample or failure point, reproducibility information, and lessons;
- `translations/README.md` requiring a link to the canonical English source commit.

- [ ] **Step 5: Validate and commit protocols**

Run:

```powershell
rg -n "idea|conjecture|experimentally-tested|proof-draft|internally-checked|externally-reviewed|published" docs/CLAIM_LEVELS.md
git diff --check
```

Expected: all seven levels are present; whitespace check emits no output.

Commit:

```powershell
git add docs/CLAIM_LEVELS.md foundations hypotheses proofs reductions negative-results translations
git commit -m "docs: add rigorous research protocols"
```

### Task 4: Add Global Collaboration Workflows

**Files:**
- Create: `.github/ISSUE_TEMPLATE/config.yml`
- Create: `.github/ISSUE_TEMPLATE/hypothesis.yml`
- Create: `.github/ISSUE_TEMPLATE/experiment.yml`
- Create: `.github/ISSUE_TEMPLATE/counterexample.yml`
- Create: `.github/ISSUE_TEMPLATE/proof-review.yml`
- Create: `.github/ISSUE_TEMPLATE/negative-result.yml`
- Create: `.github/PULL_REQUEST_TEMPLATE.md`

**Interfaces:**
- Consumes: `CONTRIBUTING.md`, `GOVERNANCE.md`, and `docs/CLAIM_LEVELS.md`.
- Produces: structured GitHub submissions that link durable research artifacts to review.

- [ ] **Step 1: Configure Issue routing**

Create `.github/ISSUE_TEMPLATE/config.yml`:

```yaml
blank_issues_enabled: false
contact_links:
  - name: Open discussion
    url: https://github.com/ApacheWang/open-np-hard-research/discussions
    about: Ask broad questions or incubate an idea before opening a bounded research issue.
```

- [ ] **Step 2: Add structured Issue forms**

Each form must collect:

- a check confirming the contributor read `CONTRIBUTING.md`;
- a precise, bounded statement;
- related work or search notes;
- reproducibility or falsification information;
- the requested reviewer action.

The hypothesis form additionally requires quantifiers and a falsification
condition. The experiment form requires command, commit, environment, data
provenance, and seed. The counterexample form requires the exact claim and
minimal reproducer. The proof-review form requires lemma dependencies and known
barriers. The negative-result form requires lessons and links to superseded work.

- [ ] **Step 3: Add the Pull Request checklist**

Create `.github/PULL_REQUEST_TEMPLATE.md` with checkboxes for:

- linked Issue;
- scope and claim level;
- tests and exact reproduction command;
- finite-test limitation;
- citations and license provenance;
- updated English canonical text before translations;
- no unsupported \(P\) versus \(NP\) claim.

- [ ] **Step 4: Commit collaboration workflows**

```powershell
git add .github
git commit -m "community: add structured research workflows"
```

### Task 5: Add Continuous Reproducibility Checks

**Files:**
- Create: `.github/workflows/ci.yml`

**Interfaces:**
- Consumes: Python package and pytest suite from Task 2.
- Produces: a required, repeatable validation command on every push and pull request.

- [ ] **Step 1: Create the CI workflow**

Create `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
  pull_request:

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip
      - run: python -m pip install --upgrade pip
      - run: python -m pip install -e ".[dev]"
      - run: pytest -q
```

- [ ] **Step 2: Run final local verification**

Run:

```powershell
pytest -q
git diff --check
git status --short
```

Expected: `6 passed`; no whitespace errors; only the intended workflow is untracked.

- [ ] **Step 3: Commit CI**

```powershell
git add .github/workflows/ci.yml
git commit -m "ci: verify the 3-SAT baseline"
```

### Task 6: Publish and Verify the GitHub Repository

**Files:**
- Modify: Git remote configuration
- Remote target: `https://github.com/ApacheWang/open-np-hard-research.git`

**Interfaces:**
- Consumes: clean local `main` branch with all launch commits.
- Produces: public GitHub repository, working clone URL, visible content, enabled Issues and Discussions, and initial contributor tasks.

- [ ] **Step 1: Verify local publication state**

Run:

```powershell
git status --short --branch
git log --oneline --decorate -6
pytest -q
```

Expected: clean `main`; launch commits are visible; `6 passed`.

- [ ] **Step 2: Create the public repository**

Create `ApacheWang/open-np-hard-research` with:

- visibility: public;
- description: `Open, rigorous, reproducible research on NP-hard problems — starting with 3-SAT.`;
- default branch: `main`;
- Issues: enabled;
- Discussions: enabled;
- no auto-generated README, license, or `.gitignore`.

If browser creation is required, verify the signed-in account is `ApacheWang`
before submitting the form.

- [ ] **Step 3: Push the exact local history**

Run:

```powershell
git remote add origin https://github.com/ApacheWang/open-np-hard-research.git
git push -u origin main
```

Expected: `main -> main` and upstream set to `origin/main`.

- [ ] **Step 4: Create initial contributor issues**

Create these public Issues:

1. `Reproduce the trusted 3-SAT baseline on Linux, macOS, and Windows`
2. `Build a primary-source map of known P vs NP proof barriers`
3. `Review the formal 3-SAT definitions and DIMACS subset`
4. `Translate the contributor guide into another language`
5. `Design property-based tests for the assignment verifier`

Apply `good first issue` only to Issues 1 and 4. Do not label a theorem or proof
claim as beginner work.

- [ ] **Step 5: Verify the public result**

Verify through the GitHub API or public page:

- repository visibility is `public`;
- `README.md` renders;
- `main` is the default branch;
- all five Issues are visible;
- clone URL is `https://github.com/ApacheWang/open-np-hard-research.git`;
- CI has started or completed.

Run:

```powershell
git ls-remote --heads https://github.com/ApacheWang/open-np-hard-research.git main
```

Expected: one `refs/heads/main` entry.

- [ ] **Step 6: Record launch**

Create `docs/journal/2026-07-23-launch.md` recording:

- repository launch time;
- initial commit IDs;
- verification results;
- known limitations;
- links to the five initial Issues.

Commit and push:

```powershell
git add docs/journal/2026-07-23-launch.md
git commit -m "docs: record public research lab launch"
git push
```

Expected: the journal entry renders publicly on `main`.
