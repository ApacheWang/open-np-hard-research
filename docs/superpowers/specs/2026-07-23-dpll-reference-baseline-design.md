# Deterministic DPLL Reference Baseline Design

**Date:** 2026-07-23
**Repository:** `ApacheWang/open-np-hard-research`
**Status:** Selected for implementation under the repository owner's standing
instruction to continue autonomously without further approval questions.

## 1. Decision

The next milestone will add a deterministic DPLL reference solver, close the
recorded DIMACS parser-contract test debt, and publish a bounded,
case-by-case differential experiment against the existing brute-force solver.

This is the preferred next step because:

1. the roadmap requires multiple reference solvers and repeatable
   small-instance experiments;
2. the existing protocol design explicitly names deterministic DPLL as the
   follow-up milestone; and
3. a second independently structured solver is a prerequisite for a useful
   public benchmark challenge.

Two alternatives were considered:

- publish a benchmark challenge before the second solver exists; and
- add CI and GitHub submission forms before extending the executable baseline.

Both remain valuable follow-ups. They do not replace the missing independent
solver and finite differential evidence, so they are outside this milestone.

## 2. Scientific Scope

This milestone concerns correctness evidence over explicitly bounded finite
families of 3-CNF formulas. It does not claim:

- a polynomial-time algorithm for 3-SAT;
- a new worst-case running-time bound;
- evidence that \(P=NP\) or \(P\ne NP\);
- correctness for malformed hand-built formula tuples outside the documented
  `Formula` contract; or
- benchmark superiority over another SAT solver.

The DPLL implementation remains an exponential reference algorithm. Agreement
with brute force is finite-domain validation, not a proof about unrestricted
inputs.

## 3. Public Solver Interface

Add this root-package export:

```python
dpll_solve(formula: Formula) -> dict[int, bool] | None
```

It consumes the same well-formed `Formula` values as `satisfies` and
`brute_force_solve`. It performs no general runtime validation of arbitrary
tuples.

For a satisfiable formula, the result:

- contains exactly the variables occurring in the original formula;
- assigns a Boolean value to every such variable;
- passes `satisfies(original_formula, result)`; and
- is deterministic for the same input and solver version.

For an unsatisfiable formula, the result is `None`. The empty formula returns
`{}`.

## 4. Deterministic DPLL Procedure

The search uses these fixed rules:

1. Build the ordered set of variables occurring in the original formula.
2. Normalize clauses for internal search only:
   - remove duplicate copies of the same literal;
   - discard tautological clauses containing both \(x\) and \(\neg x\);
   - keep the public input object unchanged.
3. Simplify clauses under the current partial assignment.
4. If simplification creates an empty clause, report conflict for that branch.
5. Repeatedly apply unit propagation to a fixed point. When more than one unit
   is available, process the lowest variable number first.
6. If all clauses are satisfied, set every still-unassigned original variable
   to `False`, verify the completed model with `satisfies`, and return it.
7. Otherwise branch on the lowest-numbered unassigned variable still present
   in the residual formula.
8. Try `False` before `True`.
9. If both branches conflict, return `None`.

The final model check is an internal invariant. Failure raises
`AssertionError` rather than publishing an invalid model.

The implementation may use private helpers, but only `dpll_solve` becomes a
new root-package API.

## 5. Permanent Parser-Contract Coverage

Before the DPLL implementation depends on the parser contract, permanent tests
will cover the currently documented cases that were previously checked only by
runtime probes.

Accepted cases include:

- comments and blank lines;
- clauses spanning lines;
- multiple terminated clauses on one line;
- one-, two-, and three-literal clauses;
- repeated literals, tautological clauses, and duplicate clauses;
- unused declared variables; and
- `p cnf 0 0`.

Rejected cases include:

- missing, malformed, duplicate, or late headers;
- negative header counts;
- unterminated clauses;
- empty clauses;
- clauses wider than three literals;
- out-of-range literals; and
- inline comments.

Tests will preserve the existing rule that the parsed `Formula` does not retain
unused variables from the DIMACS header.

## 6. Canonical Finite Formula Family

Add a research utility module, not a root-package export:

```python
canonical_clauses(variable_count: int) -> tuple[Clause, ...]
iter_canonical_formulas(
    variable_count: int,
    max_clauses: int,
) -> Iterator[Formula]
```

For variables \(1,\ldots,n\), the clause universe contains every width-one,
width-two, and width-three clause that:

- uses distinct variables;
- orders variables increasingly;
- chooses each literal sign independently; and
- therefore contains no repeated literal or tautology.

Formulas are emitted as combinations of distinct canonical clauses, ordered by
clause count and then by the deterministic clause-universe order. The empty
formula is included. Negative parameters are rejected.

This family deliberately excludes duplicate clauses, repeated literals, and
tautologies to keep the exhaustive domain finite and auditable. Those syntax
cases remain covered by focused parser and solver tests.

## 7. Differential Agreement Experiment

Add an executable module:

```powershell
python -m open_np_research.agreement `
  --max-variables 3 `
  --max-clauses 3 `
  --code-commit <40-hex implementation commit> `
  --output experiments/dpll-agreement-v1/results.json
```

The experiment enumerates the canonical family independently for
`variable_count = 0, 1, 2, 3` and at most three clauses. It runs both
`brute_force_solve` and `dpll_solve` on every case. Under the clause-universe
rules above, this is exactly 3,050 declared-domain cases.

For each case the raw result records:

- a stable sequential case number;
- the declared finite-domain variable count;
- the complete canonical formula;
- the brute-force SAT/UNSAT result and returned model;
- the DPLL SAT/UNSAT result and returned model; and
- whether each returned model passed `satisfies`.

The top-level record includes:

- schema and generator versions;
- the exact implementation commit and replay command;
- Python, project, and machine information;
- deterministic input and outcome SHA-256 digests;
- total, SAT, UNSAT, and mismatch counts;
- `seed: null`, because the family is exhaustive and deterministic;
- the complete mismatch list; and
- an explicit finite-domain and no-performance-claim statement.

The runner writes the report even when a mismatch is found, then exits
nonzero. This preserves the counterexample instead of losing it in an
exception. A mismatch report must contain the full formula and both outcomes.

The implementation code is committed and independently reviewed first. Those
files are then published sequentially to public `main`. The last publication
commit whose tree contains the complete reviewed implementation becomes the
`code_commit`; it is fetched into the local repository before the run. The
experiment is run against that exact public commit, and the generated evidence
is committed and published separately. The record therefore never points to an
unpublished or uncommitted implementation.

## 8. Data Flow

```text
canonical finite generator
        |
        v
   well-formed Formula
      /          \
     v            v
brute force      DPLL
     \            /
      v          v
 model checks + SAT/UNSAT comparison
              |
              v
 versioned JSON evidence + nonzero exit on mismatch
```

The two solvers share only the `Formula` representation and `satisfies` model
checker. Their search procedures remain structurally independent.

## 9. Tests

The permanent suite will include:

1. the parser-contract acceptance and rejection cases in Section 5;
2. DPLL unit-propagation chains;
3. conflicting units;
4. a satisfiable case requiring backtracking;
5. an unsatisfiable case requiring both branches;
6. empty, repeated-literal, and tautological formulas;
7. full-variable model completion;
8. deterministic repeated calls;
9. canonical generator ordering and parameter validation;
10. bounded exhaustive SAT/UNSAT agreement for the 394-case CI family with
    `variable_count = 0, 1, 2, 3` and at most two clauses; and
11. experiment report schema, digests, raw cases, and failure preservation.

Every SAT model from either solver is checked with `satisfies`. The full
existing suite remains green, and `git diff --check` must be silent.

## 10. Documentation and Sources

Update `foundations/3-sat.md` with the new API and exact deterministic
semantics. Add the original reference:

- Martin Davis, George Logemann, and Donald W. Loveland, “A Machine Program for
  Theorem-Proving,” *Communications of the ACM* 5(7), 394–397, 1962.
  [DOI: 10.1145/368273.368557](https://doi.org/10.1145/368273.368557)

Create `experiments/dpll-agreement-v1/README.md` describing the exact domain,
command, artifacts, replay rules, and finite-domain interpretation. Link it
from `experiments/README.md`.

## 11. Public Collaboration Entry

After the implementation and evidence are published, create one public GitHub
Issue requesting independent reproduction and review.

The Issue will:

- bind to the public implementation and evidence commits;
- provide the exact replay command;
- invite independent implementations and environment reproductions;
- require complete mismatch inputs and outputs;
- direct confirmed failures to `negative-results/`; and
- state that agreement on the finite family is not evidence for a universal
  complexity claim.

Use existing `help wanted` and `good first issue` labels if available. New
research label infrastructure remains a separate milestone.

## 12. Error Handling and Preservation

- Invalid generator parameters raise `ValueError`.
- Malformed `Formula` tuples remain outside the public runtime contract.
- Invalid CLI arguments fail before enumeration.
- An unavailable, unpublished, or non-40-hex implementation commit fails
  before writing a successful report.
- A solver mismatch or invalid model is recorded in `results.json` before the
  runner exits nonzero.
- No mismatch may be averaged away or omitted from the summary.
- Confirmed discrepancies become durable negative-result records.

## 13. Acceptance Criteria

The milestone is complete only when:

- all parser-contract debt is represented by permanent tests;
- `dpll_solve` satisfies the documented deterministic contract;
- every case in the bounded family has a raw result;
- both solvers agree on every published case and all SAT models verify, or any
  discrepancy is preserved and the milestone remains failed;
- the evidence names the exact implementation commit;
- the experiment replay command reproduces its input and outcome digests;
- the full local test suite and whitespace checks pass;
- an independent task review and whole-branch review find no unresolved
  Critical or Important issue;
- public repository files match the reviewed local versions byte for byte; and
- the public reproduction Issue is open and links the exact evidence.
