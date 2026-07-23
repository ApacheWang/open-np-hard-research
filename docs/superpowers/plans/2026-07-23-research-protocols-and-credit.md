# Research Protocols and Mathematical Credit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the complete research-protocol and mathematical-credit layer that makes every current README entry resolvable and gives later 3-SAT research a precise, reviewable, and responsibility-based workflow.

**Architecture:** The protocol layer is documentation-only and separates claim state, mathematical foundations, artifact requirements, preservation rules, and translation rules into focused files. The English documents are normative; the Chinese README carries an equivalent credit summary. Each task creates an independently reviewable commit, and final validation checks links, parser-contract probes, policy coverage, tests, and public GitHub parity.

**Tech Stack:** Markdown, PowerShell 7, Python 3.11+, pytest 8+, Git, GitHub Contents API

## Global Constraints

- This milestone does not change solver implementation, public Python APIs, package metadata, CI, GitHub forms, or benchmark data.
- English is the canonical technical language; the Chinese README must preserve the same normative credit meaning.
- Every claim has one primary status from the exact set `idea`, `conjecture`, `experimentally-tested`, `proof-draft`, `internally-checked`, `externally-reviewed`, and `published`.
- Claim status records review progress, not mathematical truth, ownership, prestige, or prize eligibility.
- Finite computational evidence never substitutes for a proof of an unrestricted mathematical or complexity claim.
- In this repository, “3-CNF” means clauses with at most three literals; exact-three work must say “exact-3-CNF.”
- Mathematical result credit requires a documented substantive mathematical contribution, approval of the final statement and proof version, and responsibility for assigned proof portions or dependencies.
- Repository ownership, project initiation, maintenance, funding, or general participation never automatically confers solver or theorem-author credit.
- If substantive mathematical contributions cannot be reliably separated with auditable evidence, the result must use result-specific collective credit and may not name a sole or primary solver on that basis.
- Credit disputes require conflict-free review and never default to the repository owner or project founder.
- Historical and complexity claims use primary or authoritative sources.
- No document may claim that P equals NP, P differs from NP, or a Millennium Prize Problem has been solved unless the applicable externally reviewed evidence actually exists.
- This documentation-only milestone records missing parser-contract regression coverage as test debt; the later DPLL milestone converts the targeted probes into permanent tests.

## File Structure

- `docs/CLAIM_LEVELS.md`: canonical claim states, gates, transitions, and regression rules.
- `README.md`: concise English mathematical-credit summary and link to governance.
- `README.zh-CN.md`: semantically equivalent Chinese mathematical-credit summary.
- `GOVERNANCE.md`: complete credit, responsibility, conflict, collective-credit, and dispute policy.
- `foundations/README.md`: index and rules for mathematical foundation documents.
- `foundations/3-sat.md`: definitions, complexity context, exact parser subset, API preconditions, and sources.
- `hypotheses/TEMPLATE.md`: required structure for falsifiable research claims and their credit ledger.
- `proofs/README.md`: proof package, dependency, objection, review, and responsibility requirements.
- `reductions/README.md`: polynomial reduction correctness and bound requirements.
- `negative-results/README.md`: preservation format for refutations, failed routes, and corrected scope.
- `translations/README.md`: source-commit binding and synchronization rules for translations.

---

### Task 1: Define Claim States and Mathematical Credit

**Files:**
- Create: `docs/CLAIM_LEVELS.md`
- Modify: `README.md` after `## Research Claim Levels`
- Modify: `README.zh-CN.md` after `## 研究主张级别`
- Replace: `GOVERNANCE.md`

**Interfaces:**
- Consumes: `docs/superpowers/specs/2026-07-23-research-protocols-and-credit-design.md`
- Produces: the seven canonical status names, status transition rules, the contribution-responsibility ledger, and the normative mathematical-credit policy used by Tasks 3 and 4.

- [ ] **Step 1: Create the canonical claim-state document**

Create `docs/CLAIM_LEVELS.md` with exactly this content:

```markdown
# Research Claim Levels

Claim status describes review progress. It does not certify mathematical truth,
ownership, prestige, or eligibility for a prize.

Every research claim has exactly one primary status from the set below. Evidence
and review records remain linked when the primary status changes.

## Levels

### `idea`

An informal direction that may not yet have a fully quantified or falsifiable
statement. Work without explicit quantifiers or a falsification condition stays
at this level.

### `conjecture`

A quantified, falsifiable statement with explicit assumptions, scope,
computational model, and related-work notes.

### `experimentally-tested`

A conjecture tested on a documented finite domain with reproducible inputs,
commands, code versions, environments, and results. This status supports only
claims about that recorded domain and is not a proof of an unrestricted
statement.

### `proof-draft`

A complete proof attempt with explicit quantifiers, named lemmas, dependencies,
scope, contributor responsibilities, and recorded objections.

### `internally-checked`

A proof draft that completed the review count required by
[GOVERNANCE.md](../GOVERNANCE.md) and has no unresolved blocking objection.
Non-blocking objections remain visible.

### `externally-reviewed`

An internally checked result with an additional documented,
conflict-disclosed review by a qualified person outside the result's
contributor team. External review does not replace the internal review count.

### `published`

An externally reviewed result with a stable, citable publication record.
Publicly posting an unreviewed preprint does not by itself confer this status;
record that link separately while retaining the accurate review status.

## Transitions

The normal proof path is:

`idea -> conjecture -> proof-draft -> internally-checked ->
externally-reviewed -> published`

`experimentally-tested` is an optional evidence stage between `conjecture` and
`proof-draft`. It is not required before a proof draft and never substitutes
for proof.

Every transition record states:

- the previous and new status;
- the exact claim and artifact version;
- the date and contributor requesting the transition;
- the linked Issue, review, experiment, or publication evidence;
- the reason for the transition; and
- all unresolved objections.

A counterexample, proof gap, scope error, or review objection can move a claim
backward. The earlier status and rationale remain in the public history.
```

- [ ] **Step 2: Verify all status names and gates**

Run:

```powershell
$path = 'docs\CLAIM_LEVELS.md'
$levels = @(
  'idea',
  'conjecture',
  'experimentally-tested',
  'proof-draft',
  'internally-checked',
  'externally-reviewed',
  'published'
)
$text = Get-Content -Raw -LiteralPath $path
foreach ($level in $levels) {
  if ($text -notmatch [regex]::Escape("``$level``")) {
    throw "Missing claim level: $level"
  }
}
Write-Output 'all seven claim levels found'
```

Expected: `all seven claim levels found`.

- [ ] **Step 3: Add the concise credit summaries to both READMEs**

In `README.md`, insert this section after the existing `## Research Claim
Levels` section and before `## Repository Map`:

```markdown
## Credit for Mathematical Results

Credit for a mathematical result belongs to contributors who made documented,
substantive mathematical contributions, approved the final formal statement
and proof version, and accept responsibility for their assigned portions.
Repository ownership, project initiation, maintenance, funding, or general
participation does not automatically confer solver or theorem-author credit.
When substantive contributions cannot be reliably separated, the result is
credited collectively to its recorded result-specific collaboration team—not
to every repository participant. See [GOVERNANCE.md](GOVERNANCE.md) for the
complete policy.
```

In `README.zh-CN.md`, insert this section after the existing `## 研究主张级别`
section and before `## 仓库地图`:

```markdown
## 数学成果署名

数学成果的功劳归于作出有记录的实质数学贡献、认可最终形式化陈述和证明版本，
并对其负责部分承担责任的贡献者。仓库所有权、项目发起、维护、资助或一般参与，
不会自动带来“问题解决者”或定理作者身份。当实质数学贡献无法可靠分割时，成果
必须归于该结果所记录的专属协作团队，而不是仓库全体参与者。完整规则见
[GOVERNANCE.md](GOVERNANCE.md)。
```

- [ ] **Step 4: Replace governance with the complete normative policy**

Replace `GOVERNANCE.md` with:

```markdown
# Governance

Open NP-Hard Research makes durable decisions and review records publicly.

## Reviews

- Routine changes need one approving review.
- Major theorem claims need two independent reviews.
- At least one reviewer of a major claim must not have drafted that claim.
- Unresolved objections remain public with the claim or review record.

External review is an additional gate for the `externally-reviewed` status and
does not replace the applicable internal review count. A qualified external
reviewer has documented expertise relevant to the portion reviewed and is not
a member of that result's contributor team.

## Claim Status

Every research claim uses one primary status defined in
[docs/CLAIM_LEVELS.md](docs/CLAIM_LEVELS.md). Status changes require public
evidence and rationale. Counterexamples, proof gaps, or scope errors can lower a
status; the earlier state remains visible.

## Mathematical Credit and Responsibility

Result-specific mathematical credit—including credit for a theorem, conjecture
resolution, key lemma, reduction, or formal proof—belongs to contributors who:

1. made a documented, substantive mathematical contribution to that result;
2. approved the final formal statement and proof version; and
3. can explain and take responsibility for their assigned proof portions,
   mathematical dependencies, or formal artifacts, including participating in
   correction or withdrawal if an error is found.

Substantive mathematical work can include decisive definitions, lemmas,
constructions, reductions, counterexamples, proof repairs, or formalization
that materially establishes the result.

Repository ownership, project initiation, maintenance, funding, general
participation, code volume, experiment execution, translation, moderation, or
review does not automatically confer credit as a solver or theorem author.
Those contributions are recorded and acknowledged under their actual roles.
Mathematical credit is distinct from copyright, repository permissions,
software licensing, acknowledgements, and general contributor recognition.

### Contribution-Responsibility Ledger

Every claimed mathematical-credit entry records:

- the claim, theorem, lemma, reduction, or formal-artifact identifier;
- the exact result and proof version or commit;
- the contributor's stable identity;
- the substantive mathematical contribution;
- the proof portion or dependency for which the contributor accepts
  responsibility;
- the recorded approval of the final statement and proof version; and
- any shared or backup responsibility.

Without this ledger, work can be acknowledged under its actual role but the
repository does not publish solver or theorem-author credit.

### Inseparable Contributions

When substantive contributions cannot be reliably separated using auditable
evidence, the result must be credited collectively to the result-specific open
collaboration team recorded for that claim. No person is presented as the sole
or primary solver on that basis.

The result record identifies the claim and proof version, the team's exact
membership, and every member's responsibility entry. The team contains only
contributors who satisfy the contribution and responsibility requirements for
that result. It does not automatically include the repository owner, project
founder, all maintainers, or everyone who participated in the repository.

### Conflicts and Credit Disputes

Credit evidence includes Issues, commits, Pull Requests, proof dependencies,
review discussions, counterexamples, and recorded responsibility approvals. A
person cannot decide a dispute in which they have a direct credit interest.

At least two reviewers without a direct stake examine a credit dispute
publicly. They evaluate documented mathematical contribution and
responsibility rather than title or authority. Reviewers disclose recent
coauthorship, employment or supervision relationships, financial interests,
and other direct personal stakes.

A material conflict prevents a review from satisfying an independence or
external-review gate, although its comments stay in the public record. If
reviewers disagree, attribution remains `unresolved` and an additional
conflict-free reviewer or a new public review may be requested. Disagreement
never defaults to owner or founder credit, and the repository owner cannot
unilaterally publish a final solver-credit decision.

## Governance Changes

Any governance change requires a public Issue and a recorded maintainer
decision. New research tracks follow the same public-proposal and
recorded-decision practice.
```

- [ ] **Step 5: Validate Task 1**

Run:

```powershell
$english = Get-Content -Raw -LiteralPath 'README.md'
$chinese = Get-Content -Raw -LiteralPath 'README.zh-CN.md'
$governance = Get-Content -Raw -LiteralPath 'GOVERNANCE.md'

$checks = @{
  'English substantive contribution' = $english -match 'substantive mathematical contributions'
  'English non-automatic owner credit' = $english -match 'Repository ownership'
  'English collective credit' = $english -match 'result-specific collaboration team'
  'Chinese substantive contribution' = $chinese -match '实质数学贡献'
  'Chinese non-automatic owner credit' = $chinese -match '不会自动'
  'Chinese collective credit' = $chinese -match '专属协作团队'
  'Ledger' = $governance -match 'Contribution-Responsibility Ledger'
  'Conflict-free dispute review' = $governance -match 'conflict-free reviewer'
  'No unilateral owner decision' = $governance -match 'cannot\s+unilaterally'
}

$failed = $checks.GetEnumerator() | Where-Object { -not $_.Value }
if ($failed) {
  $failed.Key | ForEach-Object { Write-Error "Missing policy: $_" }
  throw 'Task 1 policy validation failed'
}

python -m pytest -q
git diff --check
```

Expected: no missing-policy errors, `11 passed`, and no whitespace errors.

- [ ] **Step 6: Commit Task 1**

```powershell
git add -- docs/CLAIM_LEVELS.md README.md README.zh-CN.md GOVERNANCE.md
git diff --cached --check
git commit -m "docs: define claim states and mathematical credit"
```

Expected: one commit containing only the four Task 1 files.

---

### Task 2: Document the 3-SAT Foundation and Executable Contract

**Files:**
- Create: `foundations/README.md`
- Create: `foundations/3-sat.md`

**Interfaces:**
- Consumes: `parse_dimacs_3sat(text: str) -> Formula`, `satisfies(formula: Formula, assignment: Mapping[int, bool]) -> bool`, and `brute_force_solve(formula: Formula) -> dict[int, bool] | None`
- Produces: the normative terminology, accepted input subset, API preconditions, finite-evidence boundary, and source path used by every later solver or experiment.

- [ ] **Step 1: Create the foundation index**

Create `foundations/README.md` with:

```markdown
# Mathematical Foundations

Foundation documents define the terms, computational models, accepted input
formats, and primary source paths used by this repository.

Each foundation must:

- separate standard mathematical definitions from repository-specific software
  conventions;
- identify its assumptions and computational model;
- distinguish finite computation from unrestricted mathematical proof;
- cite primary or authoritative sources; and
- change together with tests when an executable contract changes.

## Current Foundations

- [3-SAT](3-sat.md): Boolean definitions, complexity context, the accepted
  DIMACS subset, and current verifier and solver semantics.
```

- [ ] **Step 2: Create the complete 3-SAT foundation**

Create `foundations/3-sat.md` with:

```markdown
# 3-SAT Foundation

This document separates standard mathematical terminology from the narrower
input and API conventions of this repository.

## Mathematical Definitions

A **Boolean variable** takes a value in `{false, true}`. A **literal** is a
variable \(x_i\) or its negation \(\neg x_i\). A **clause** is a disjunction of
literals. A formula is in **conjunctive normal form (CNF)** when it is a
conjunction of clauses.

A total **assignment** gives every variable in a formula a Boolean value. It
**satisfies** a literal when the literal evaluates to true, satisfies a clause
when at least one literal in that clause is true, and satisfies a CNF formula
when every clause is true. A formula is **satisfiable (SAT)** when such an
assignment exists and **unsatisfiable (UNSAT)** otherwise.

The literature uses both “exactly three” and “at most three” conventions for
3-CNF. In this repository, **3-CNF** means that every clause contains one, two,
or three literals. Work that requires exactly three literals per clause must
say **exact-3-CNF**.

The **3-SAT decision problem** asks whether a given 3-CNF formula is
satisfiable. A proposed assignment is verifiable in polynomial time, so 3-SAT
is in NP. SAT is NP-complete, and the standard polynomial transformation from
CNF-SAT to 3-SAT establishes NP-hardness; therefore 3-SAT is NP-complete.

This classification does not mean that every finite instance is equally hard.
It also does not determine whether a particular heuristic is useful on a
specific distribution.

## Three Different Kinds of Result

These statements must not be conflated:

1. **Solving one instance:** a model or an UNSAT result concerns that input.
2. **Improving an exponential algorithm:** a proved bound or finite benchmark
   concerns its stated model, implementation, or domain.
3. **Proving a polynomial worst-case bound:** this is an unrestricted
   complexity claim and requires a proof independent of finite testing.

No finite collection of experiments proves the third statement.

## Accepted DIMACS Subset

Repository interchange files must use UTF-8. The Python parser accepts an
already-decoded `str`; it does not accept `bytes` and does not detect or
validate the source encoding. File-reading callers must decode strictly before
calling it.

`parse_dimacs_3sat` accepts this subset:

- Blank lines are ignored.
- A full line whose first non-whitespace character is `c` is a comment.
- Exactly one header of the form `p cnf <variables> <clauses>` is required.
- The header must appear before all clause data.
- The declared variable and clause counts must be nonnegative integers.
- Each literal is a nonzero signed integer whose absolute value does not exceed
  the declared variable count.
- `0` terminates a clause.
- Clauses may span lines, and one line may contain multiple terminated clauses.
- Every accepted clause contains one, two, or three literals.
- The number of terminated clauses must equal the declared clause count.
- Declared variables may be unused.
- Repeated literals and tautological clauses are accepted without
  normalization.
- `p cnf 0 0` is accepted as the empty, satisfiable formula.

This is deliberately narrower than general DIMACS CNF: an empty clause is
rejected by the baseline parser even though general CNF uses an empty clause to
represent an unsatisfiable formula. Inline comments are not accepted.

## Current Python API Contract

The public functions are:

```python
parse_dimacs_3sat(text: str) -> Formula
satisfies(formula: Formula, assignment: Mapping[int, bool]) -> bool
brute_force_solve(formula: Formula) -> dict[int, bool] | None
```

`parse_dimacs_3sat` returns only a tuple of clause tuples. It does not retain
the header's declared variable count or clause count.

The semantic guarantee for `satisfies` and `brute_force_solve` applies to
parser output or an equivalent well-formed `Formula`: every clause contains one
to three nonzero signed-integer literals. These functions do not perform
runtime structural validation; malformed hand-built tuples are outside the
contract.

`satisfies` accepts a mapping that may be partial. A literal whose variable is
absent from the mapping does not satisfy its clause. Values must be `bool`
under the type contract, but runtime code does not enforce that type. Keys for
variables absent from the formula are ignored.

`brute_force_solve` enumerates variables that occur in clauses in ascending
numeric order, tries `False` before `True`, and returns the first satisfying
mapping it finds. It returns `None` for UNSAT. Unused variables declared only
in the DIMACS header are not present in the returned mapping.

Any change to these semantics requires failing regression tests first and a
coordinated update to this document.

## Sources

- Stephen A. Cook, “The Complexity of Theorem-Proving Procedures,” STOC 1971,
  pp. 151–158. [DOI: 10.1145/800157.805047](https://doi.org/10.1145/800157.805047)
- Richard M. Karp, “Reducibility Among Combinatorial Problems,” in *Complexity
  of Computer Computations*, 1972, pp. 85–103.
  [DOI: 10.1007/978-1-4684-2001-2_9](https://doi.org/10.1007/978-1-4684-2001-2_9)
- DIMACS, “Satisfiability: Suggested Format,” revision of May 8, 1993.
  [Institutional PDF](https://www.cs.ubc.ca/~babic/doc/dimacs_cnf.pdf)
```

- [ ] **Step 3: Run targeted parser-contract probes**

Run:

```powershell
@'
from open_np_research.sat3 import (
    brute_force_solve,
    parse_dimacs_3sat,
    satisfies,
)

formula = parse_dimacs_3sat(
    "c contract probe\n"
    "p cnf 5 3\n"
    "1 -1 0 2 2 0\n"
    "-3\n"
    "4 0\n"
)
assert formula == ((1, -1), (2, 2), (-3, 4))

empty = parse_dimacs_3sat("p cnf 0 0\n")
assert empty == ()
assert brute_force_solve(empty) == {}
assert satisfies(empty, {})

unused = parse_dimacs_3sat("p cnf 3 1\n1 0\n")
model = brute_force_solve(unused)
assert model == {1: True}
assert 2 not in model and 3 not in model

assert not satisfies(((1,),), {})
assert satisfies(((1,),), {1: True, 99: False})

invalid_inputs = (
    "1 0\n",
    "p cnf 1 1\n1\n",
    "p cnf 1 1\n0\n",
    "p cnf 1 1\n2 0\n",
)
for text in invalid_inputs:
    try:
        parse_dimacs_3sat(text)
    except ValueError:
        pass
    else:
        raise AssertionError(f"expected ValueError for {text!r}")

print("3-SAT contract probes passed")
'@ | python -
```

Expected: `3-SAT contract probes passed`.

- [ ] **Step 4: Validate sources, links, tests, and whitespace**

Open the three source links and confirm that their titles, authors or
institution, and dates match the bibliography. Then run:

```powershell
$paths = @('foundations\README.md', 'foundations\3-sat.md')
foreach ($path in $paths) {
  if (-not (Test-Path -LiteralPath $path -PathType Leaf)) {
    throw "Missing foundation file: $path"
  }
}

rg -n 'NP-complete|finite|DIMACS|parse_dimacs_3sat|brute_force_solve' foundations
python -m pytest -q
git diff --check
```

Expected: the key terms appear in `foundations/3-sat.md`, `11 passed`, and no
whitespace errors.

- [ ] **Step 5: Commit Task 2**

```powershell
git add -- foundations/README.md foundations/3-sat.md
git diff --cached --check
git commit -m "docs: define the 3-SAT foundation"
```

Expected: one commit containing only the two foundation files.

---

### Task 3: Add Hypothesis, Proof, and Reduction Protocols

**Files:**
- Create: `hypotheses/TEMPLATE.md`
- Create: `proofs/README.md`
- Create: `reductions/README.md`

**Interfaces:**
- Consumes: the status names from `docs/CLAIM_LEVELS.md`, the review rules in `GOVERNANCE.md`, and terminology from `foundations/3-sat.md`
- Produces: the mandatory record shapes for falsifiable claims, proof packages, responsibility ledgers, and polynomial reductions.

- [ ] **Step 1: Create the hypothesis template**

Create `hypotheses/TEMPLATE.md` with:

```markdown
# Hypothesis Record Template

Copy this file for one bounded research claim. Keep all headings and replace
the instructional text with the claim's evidence.

## Identification

Record the stable claim identifier, title, linked public Issue, contributor
responsible for maintaining the record, creation date, and exact artifact
version or commit.

## Primary Claim Status

Choose exactly one status from [the canonical levels](../docs/CLAIM_LEVELS.md)
and link the evidence for the latest transition.

## Formal Statement

State the claim with explicit quantifiers. Define every symbol and identify
whether the claim concerns all inputs, a distribution, a parameterized family,
or one finite set.

## Assumptions and Computational Model

List mathematical assumptions, input representation, computational model,
resource measure, and every promise on admissible instances.

## Falsification Condition

Describe a concrete observation, counterexample, derivation, or failed
dependency that would refute or narrow the claim.

## Motivation and Related Work

Explain why the claim matters. Cite primary or authoritative sources, record
the searches performed, and distinguish the claim from known results.

## Tested Domain

Record the smallest and largest tested inputs, generation or selection rules,
seeds, commands, code commit, environment, data provenance, checksums, and raw
results. State explicitly that finite tests do not prove an unrestricted claim.

## Known Barriers and Objections

List relevant proof barriers, unresolved objections, failed routes, and the
current response to each one.

## Linked Evidence

Link experiments, counterexamples, proof drafts, reductions, negative results,
reviews, and superseded versions.

## Contribution-Responsibility Ledger

For every person receiving result-specific mathematical credit, record one row:

| Artifact ID | Result/proof version | Contributor identity | Substantive mathematical contribution | Responsible proof portion or dependency | Final approval record | Shared or backup responsibility |
| --- | --- | --- | --- | --- | --- | --- |

Without a complete row, acknowledge the work under its actual role rather than
publishing solver or theorem-author credit.

## Status History

For each change, record the date, previous status, new status, exact artifact
version, requester, evidence, rationale, and unresolved objections.
```

- [ ] **Step 2: Create the proof protocol**

Create `proofs/README.md` with:

```markdown
# Proof Records

Every proof record is tied to one hypothesis identifier and one exact claim
version.

## Required Contents

A proof package records:

- the exact quantified claim and all definitions;
- assumptions, scope, and computational model;
- named lemmas with stable identifiers;
- a dependency list or directed dependency graph;
- the proof of every lemma or an exact external source;
- boundary cases and degenerate inputs;
- links to computational checks, which remain evidence rather than proof;
- open, resolved, and non-blocking reviewer objections;
- status history and links to superseded versions;
- all counterexamples and related negative results; and
- the contribution-responsibility ledger defined in
  [GOVERNANCE.md](../GOVERNANCE.md).

## Review Record

Each review identifies the reviewer, relevant expertise, scope reviewed,
artifact commit, conflicts disclosed, objections, author responses, and final
recommendation. A major theorem claim follows the review count in
[GOVERNANCE.md](../GOVERNANCE.md).

`internally-checked` requires no unresolved blocking objection.
`externally-reviewed` additionally requires a qualified, conflict-disclosed
reviewer outside the result's contributor team; that review does not replace
the internal review count.

## Corrections and Withdrawal

If a proof gap is found, lower the claim status, link the objection, preserve
the affected proof version, and create or link a record under
[`negative-results/`](../negative-results/). Do not silently rewrite the
historical claim.
```

- [ ] **Step 3: Create the reduction protocol**

Create `reductions/README.md` with:

```markdown
# Reduction Records

Every claimed polynomial-time reduction must be independently reviewable.

## Required Contents

Record:

- the exact source problem and target problem;
- input encodings, size measures, and promise conditions;
- the construction algorithm;
- a polynomial upper bound on construction time;
- an explicit bound on output size as a function of input size;
- forward correctness: every yes-instance maps to a yes-instance;
- reverse correctness: every mapped yes-instance implies the source instance
  is a yes-instance;
- treatment of no-instances, malformed inputs, and boundary cases;
- all introduced variables, gadgets, and invariants;
- links to source theorems and earlier reductions;
- tests or worked examples; and
- known limitations, objections, and negative results.

Tests and examples can expose errors but do not replace the two correctness
directions or the polynomial bounds.

## Review

Reviewers check the construction, both correctness directions, the size bound,
the time bound, hidden assumptions, and compatibility with the stated
computational model. Record the exact reduction version reviewed.
```

- [ ] **Step 4: Validate Task 3**

Run:

```powershell
$required = @{
  'hypotheses\TEMPLATE.md' = @(
    'Formal Statement',
    'Falsification Condition',
    'Tested Domain',
    'Contribution-Responsibility Ledger',
    'Status History'
  )
  'proofs\README.md' = @(
    'named lemmas',
    'dependency',
    'reviewer objections',
    'contribution-responsibility ledger',
    'Corrections and Withdrawal'
  )
  'reductions\README.md' = @(
    'construction time',
    'output size',
    'forward correctness',
    'reverse correctness',
    'polynomial bounds'
  )
}

foreach ($entry in $required.GetEnumerator()) {
  $text = Get-Content -Raw -LiteralPath $entry.Key
  foreach ($term in $entry.Value) {
    if ($text -notmatch [regex]::Escape($term)) {
      throw "Missing '$term' in $($entry.Key)"
    }
  }
}

python -m pytest -q
git diff --check
```

Expected: no missing-term errors, `11 passed`, and no whitespace errors.

- [ ] **Step 5: Commit Task 3**

```powershell
git add -- hypotheses/TEMPLATE.md proofs/README.md reductions/README.md
git diff --cached --check
git commit -m "docs: add claim proof and reduction protocols"
```

Expected: one commit containing only the three Task 3 files.

---

### Task 4: Preserve Negative Results and Bind Translations

**Files:**
- Create: `negative-results/README.md`
- Create: `translations/README.md`

**Interfaces:**
- Consumes: claim transitions from `docs/CLAIM_LEVELS.md`, dispute history from `GOVERNANCE.md`, and artifact identifiers from Task 3
- Produces: the durable failure record and exact English-source binding required for public corrections and translations.

- [ ] **Step 1: Create the negative-result protocol**

Create `negative-results/README.md` with:

```markdown
# Negative Results

Refuted claims, failed proof routes, counterexamples, and unreproducible
experiments are durable research outputs. Preserve them so later contributors
do not repeat hidden failures.

## Required Record

Record:

- the stable identifier and linked public Issue;
- the attempted claim and its exact version;
- its previous and current claim status;
- the smallest known counterexample or exact failure point;
- the failed lemma, dependency, assumption, implementation, or reproduction
  step;
- commands, code commit, environment, input provenance, checksums, and seeds
  needed to reproduce computational evidence;
- the affected proofs, hypotheses, reductions, experiments, or publications;
- reviewer objections and author responses;
- any corrected or narrowed claim; and
- lessons and promising routes that remain open.

## Preservation Rules

- Do not delete or overwrite the failed artifact.
- Link the negative result from every affected current artifact.
- Distinguish a refutation from lack of evidence, timeout, implementation
  failure, and irreproducibility.
- Keep finite counterexamples scoped to the exact claim they refute.
- Lower the primary claim status when the evidence requires it and preserve the
  transition rationale.
```

- [ ] **Step 2: Create the translation protocol**

Create `translations/README.md` with:

```markdown
# Translations

English is the canonical technical language. Translations improve access but
do not silently replace or amend their English source.

## Required Metadata

Every translation records:

- language and locale;
- translated document path;
- canonical English source path;
- exact English source commit;
- translator and current maintainer identities;
- translation date;
- known omissions or terminology choices; and
- synchronization status.

## Synchronization

When the English source changes, compare it with the recorded source commit.
Until the translation is updated and reviewed, mark it visibly as
`needs-sync` and link the newer English commit. Do not present an outdated
translation as current.

Normative disputes defer to the recorded English source. Update the canonical
English document before translating a policy change.

Translation, terminology review, and maintenance receive explicit
acknowledgement under those roles. They do not automatically confer
result-specific solver or theorem-author credit unless the contributor also
meets the mathematical contribution and responsibility requirements in
[GOVERNANCE.md](../GOVERNANCE.md).
```

- [ ] **Step 3: Validate Task 4**

Run:

```powershell
$negative = Get-Content -Raw -LiteralPath 'negative-results\README.md'
$translations = Get-Content -Raw -LiteralPath 'translations\README.md'

foreach ($term in @(
  'smallest known counterexample',
  'exact failure point',
  'reproduce computational evidence',
  'Do not delete',
  'Lower the primary claim status'
)) {
  if ($negative -notmatch [regex]::Escape($term)) {
    throw "Missing negative-result rule: $term"
  }
}

foreach ($term in @(
  'canonical English source path',
  'exact English source commit',
  'needs-sync',
  'Normative disputes',
  'do not automatically confer'
)) {
  if ($translations -notmatch [regex]::Escape($term)) {
    throw "Missing translation rule: $term"
  }
}

python -m pytest -q
git diff --check
```

Expected: no missing-rule errors, `11 passed`, and no whitespace errors.

- [ ] **Step 4: Commit Task 4**

```powershell
git add -- negative-results/README.md translations/README.md
git diff --cached --check
git commit -m "docs: preserve failures and bind translations"
```

Expected: one commit containing only the two Task 4 files.

---

### Task 5: Verify and Publish the Protocol Milestone

**Files:**
- Verify: all Markdown files tracked by Git
- Publish new: the eight files created in Tasks 1–4
- Publish updates: `README.md`, `README.zh-CN.md`, and `GOVERNANCE.md`

**Interfaces:**
- Consumes: all four local implementation commits and the public repository `ApacheWang/open-np-hard-research`
- Produces: a clean local `main`, a public `main` with byte-equivalent protocol files, and evidence that links, tests, policies, and finite-domain safeguards pass.

- [ ] **Step 1: Run the full local test and policy checks**

Run:

```powershell
python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw 'pytest failed' }

$protocolPaths = @(
  'README.md',
  'README.zh-CN.md',
  'GOVERNANCE.md',
  'docs\CLAIM_LEVELS.md',
  'foundations\README.md',
  'foundations\3-sat.md',
  'hypotheses\TEMPLATE.md',
  'proofs\README.md',
  'reductions\README.md',
  'negative-results\README.md',
  'translations\README.md'
)

$combined = ($protocolPaths | ForEach-Object {
  Get-Content -Raw -LiteralPath $_
}) -join "`n"

$requiredPatterns = @(
  'experimentally-tested',
  'externally-reviewed',
  'substantive\s+mathematical\s+contribution',
  'must\s+be\s+credited\s+collectively',
  'Contribution-Responsibility Ledger',
  'Falsification Condition',
  'forward correctness',
  'smallest known counterexample',
  'exact English source commit'
)
foreach ($pattern in $requiredPatterns) {
  if ($combined -notmatch $pattern) {
    throw "Missing required protocol pattern: $pattern"
  }
}

git diff --check HEAD
git status --short
```

Expected: `11 passed`, no missing-pattern or whitespace errors, and an empty
working-tree status.

- [ ] **Step 2: Check all relative Markdown links**

Run:

```powershell
$errors = [System.Collections.Generic.List[string]]::new()
$markdownFiles = git ls-files '*.md'
$linkPattern = '\[[^\]]+\]\(([^)]+)\)'

foreach ($file in $markdownFiles) {
  $text = Get-Content -Raw -LiteralPath $file
  foreach ($match in [regex]::Matches($text, $linkPattern)) {
    $target = $match.Groups[1].Value.Trim()
    if (
      $target -match '^[a-z][a-z0-9+.-]*:' -or
      $target.StartsWith('#')
    ) {
      continue
    }

    $target = $target.Split('#')[0].Trim('<', '>')
    if (-not $target) {
      continue
    }

    $target = [Uri]::UnescapeDataString($target)
    $base = Split-Path -Parent $file
    if (-not $base) {
      $base = '.'
    }
    $resolved = Join-Path $base $target
    if (-not (Test-Path -LiteralPath $resolved)) {
      $errors.Add("${file}: missing relative link target '$target'")
    }
  }
}

if ($errors.Count -gt 0) {
  $errors | ForEach-Object { Write-Error $_ }
  throw 'Markdown link validation failed'
}
Write-Output 'all relative Markdown links resolve'
```

Expected: `all relative Markdown links resolve`.

- [ ] **Step 3: Re-run the targeted parser-contract probes**

Repeat the exact probe command from Task 2, Step 3.

Expected: `3-SAT contract probes passed`.

- [ ] **Step 4: Review unsupported-claim scan**

Run:

```powershell
rg -n -i `
  'P\s*(=|==|equals)\s*NP|P\s*(!=|≠|differs\s+from)\s*NP|Millennium Prize.{0,40}solved' `
  README.md README.zh-CN.md GOVERNANCE.md docs foundations hypotheses proofs reductions negative-results translations
```

Expected: no affirmative solution claim. Matches are allowed only when they
explicitly prohibit, disclaim, or scope such a claim.

- [ ] **Step 5: Verify the local commit sequence**

Run:

```powershell
git status --short --branch
git log --oneline -5
```

Expected: clean `main` and these four protocol commits, newest first:

```text
docs: preserve failures and bind translations
docs: add claim proof and reduction protocols
docs: define the 3-SAT foundation
docs: define claim states and mathematical credit
```

- [ ] **Step 6: Publish through the connected GitHub app**

The local HTTPS credential is not trusted for this repository, and the public
branch history was previously written through the GitHub Contents API. Keep the
established publication method:

1. For each modified path—`README.md`, `README.zh-CN.md`, and
   `GOVERNANCE.md`—fetch the current remote blob SHA on `main`, then replace the
   file with the exact output of `git show HEAD:<path>`.
2. For each new path—`docs/CLAIM_LEVELS.md`, `foundations/README.md`,
   `foundations/3-sat.md`, `hypotheses/TEMPLATE.md`, `proofs/README.md`,
   `reductions/README.md`, `negative-results/README.md`, and
   `translations/README.md`—confirm a fetch returns `404 NOT_FOUND`, then
   create it on `main` with the exact output of `git show HEAD:<path>`.
3. Use commit messages matching the applicable local task commit.
4. Do not run same-path writes in parallel. Different new files may still be
   written sequentially to avoid branch-head races.
5. Do not emit a `git-push` success claim because this is Contents API
   publication rather than a local `git push`.

- [ ] **Step 7: Verify public byte parity**

Fetch all eleven published paths from `ApacheWang/open-np-hard-research` at
`main` with UTF-8 decoding. For each path, compare remote content with
`git show HEAD:<path>` and fail on the first difference.

Expected:

```text
11/11 remote protocol files match local HEAD
```

Finally verify the public links:

- `https://github.com/ApacheWang/open-np-hard-research/blob/main/docs/CLAIM_LEVELS.md`
- `https://github.com/ApacheWang/open-np-hard-research/blob/main/foundations/3-sat.md`
- `https://github.com/ApacheWang/open-np-hard-research/blob/main/GOVERNANCE.md`

The protocol milestone is ready for review only after the local tree is clean,
all local checks pass, and all eleven remote files match local `HEAD`.
