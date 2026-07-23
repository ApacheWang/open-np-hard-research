# Research Protocols and Mathematical Credit Design

**Status:** Approved in conversation on 2026-07-23

## Goal

Create the protocol layer that every later hypothesis, proof, reduction,
experiment, counterexample, translation, and mathematical-credit decision will
use. The milestone must repair the repository's current broken documentation
links, define review states without implying truth, and make mathematical
credit depend on substantive contribution and responsibility rather than
repository ownership or general participation.

## Context

The repository already has a trusted finite 3-SAT parser, assignment verifier,
and brute-force solver. Its README links to claim-level, foundation,
hypothesis, proof, reduction, and negative-result material that does not yet
exist. GitHub collaboration forms and the planned DPLL solver depend on these
protocols, so the protocol layer is the next independent milestone.

## Scope

This milestone creates:

- `docs/CLAIM_LEVELS.md`
- `foundations/README.md`
- `foundations/3-sat.md`
- `hypotheses/TEMPLATE.md`
- `proofs/README.md`
- `reductions/README.md`
- `negative-results/README.md`
- `translations/README.md`

It also adds a concise mathematical-credit section to `README.md` and
`README.zh-CN.md`, and adds the complete policy and dispute procedure to
`GOVERNANCE.md`.

This milestone does not add GitHub Issue forms, CI configuration, random
experiments, a DPLL solver, new solver APIs, or performance claims. Those are
separate, reviewable milestones.

## Claim-State Model

Every research claim has one primary status:

1. `idea`: an informal direction that may not yet have a quantified statement.
2. `conjecture`: a quantified, falsifiable statement with explicit assumptions,
   scope, computational model, and related-work notes.
3. `experimentally-tested`: a conjecture tested on a documented finite domain
   with reproducible inputs, commands, versions, and results.
4. `proof-draft`: a complete proof attempt with named lemmas, explicit
   quantifiers, dependencies, and recorded objections.
5. `internally-checked`: a proof draft that completed the applicable project
   review requirements and has no unresolved blocking objection.
6. `externally-reviewed`: an internally checked result with a documented,
   conflict-disclosed review by at least one qualified person outside the
   result's contributor team. This is an additional gate and does not replace
   the internal review count required by `GOVERNANCE.md`.
7. `published`: an externally reviewed result with a stable, citable
   publication record.

The normal proof path is:

`idea -> conjecture -> proof-draft -> internally-checked ->
externally-reviewed -> published`

`experimentally-tested` is an optional evidence stage between `conjecture` and
`proof-draft`; it is never a substitute for a proof of an unrestricted
mathematical statement. A claim may move backward whenever a counterexample,
proof gap, scope error, or review objection is found. Status records review
progress, not mathematical truth, prestige, ownership, or prize eligibility.

An online preprint without the required external review does not receive the
`published` status merely because it is publicly accessible. Its stable link is
recorded separately while its primary review status remains accurate.

## 3-SAT Foundation Contract

`foundations/3-sat.md` will define Boolean variables, literals, clauses, CNF,
3-CNF, assignments, satisfiable formulas, and unsatisfiable formulas. It will
distinguish:

- solving one finite instance;
- improving an exponential algorithm on a stated model or domain; and
- proving a polynomial worst-case bound.

The document states that 3-SAT is an NP-complete decision problem and supports
that statement with primary or authoritative sources. At minimum, the
bibliography identifies Cook's 1971 SAT result, Karp's 1972 reductions paper,
and the 1993 DIMACS satisfiability format. References use stable DOI, publisher,
author-hosted, or institutional links.

The repository convention uses “3-CNF” for clauses containing at most three
literals. Work that requires exactly three literals per clause must say
“exact-3-CNF.”

The accepted parser subset will be documented exactly as implemented:

- Repository interchange files must be UTF-8. The Python API itself accepts an
  already-decoded `str`, does not accept `bytes`, and does not detect or validate
  the source encoding. Callers reading files must decode them strictly before
  calling the parser.
- Blank lines and full comment lines whose first non-whitespace character is
  `c` are ignored.
- Exactly one `p cnf <variables> <clauses>` header is required, and it must
  precede all clause data.
- Declared variable and clause counts must be nonnegative.
- A literal is a nonzero signed integer whose absolute value does not exceed
  the declared variable count.
- `0` terminates a clause. Clauses may span lines, and a line may contain more
  than one terminated clause.
- Each accepted clause contains one, two, or three literals.
- The number of terminated clauses must match the header.
- Unused declared variables, repeated literals, and tautological clauses are
  accepted without normalization.
- `p cnf 0 0` is accepted as the empty, satisfiable formula.
- Empty clauses are deliberately rejected by this narrower baseline even
  though general CNF formats can use an empty clause to represent an
  unsatisfiable formula.

The foundation also documents current API semantics:

- `parse_dimacs_3sat` returns only the clause tuple; it does not retain header
  metadata.
- The public semantic guarantee for `satisfies` and `brute_force_solve` applies
  to parser output or an equivalent well-formed `Formula`: every clause has one
  to three nonzero signed-integer literals. These functions do not perform
  runtime structural validation; behavior for malformed hand-built tuples is
  outside the contract.
- `satisfies` accepts a mapping that may be partial. A literal whose variable
  is absent from the mapping does not satisfy its clause. Assignment values
  must be `bool` under the type contract, although this is not checked at
  runtime; keys for variables not present in the formula are ignored.
- `brute_force_solve` enumerates only variables that appear in clauses, so
  unused declared variables are not included in a returned model.

Any future change to this contract requires tests and a coordinated update to
the foundation document.

## Artifact Protocols

### Foundation Index

`foundations/README.md` explains that foundation documents define accepted
terms, models, formats, and source paths. It links to the 3-SAT foundation and
requires later foundations to distinguish mathematical definitions from local
software conventions.

### Hypotheses

`hypotheses/TEMPLATE.md` requires:

- a stable identifier and linked public Issue;
- primary claim status;
- a fully quantified formal statement;
- motivation and primary or authoritative related work;
- assumptions, scope, and computational model;
- a concrete falsification condition;
- the smallest tested domain and all finite-domain limits;
- known barriers and unresolved objections;
- linked experiments, counterexamples, proof dependencies, and negative
  results; and
- a contribution-responsibility ledger for any claimed mathematical credit.

A submission missing quantifiers or a falsification condition remains an
`idea`.

### Proofs

`proofs/README.md` requires each proof record to include the exact claim,
explicit quantifiers, named lemmas, a dependency list, scope and model,
contributor roles, a contribution-responsibility ledger, reviewer identities
and scopes, open objections, status history, and links to counterexamples or
superseded versions.

### Reductions

`reductions/README.md` requires the source and target problems, the
polynomial-time construction, forward and reverse correctness arguments,
input-size mapping, construction-time bound, edge cases, and tests or examples
that do not substitute for the proof.

### Negative Results

`negative-results/README.md` preserves the attempted claim, prior status,
smallest known counterexample or exact failure point, reproduction
instructions, affected artifacts, revised scope, and lessons. A refuted or
withdrawn route is not silently deleted.

### Translations

`translations/README.md` requires the language, maintainer, canonical English
source path, and exact source commit. When the English source changes, an
out-of-date translation is labelled as needing synchronization rather than
silently treated as current. Normative disputes defer to the identified
English source.

## Mathematical Credit and Responsibility

The two READMEs contain a concise version of this rule. `GOVERNANCE.md`
contains the complete normative policy.

Result-specific mathematical credit—including credit for a theorem, conjecture
resolution, key lemma, reduction, or formal proof—belongs to the people who:

1. made a documented, substantive mathematical contribution to that result;
2. approve the final formal statement and the version of the proof being
   claimed; and
3. can explain and take responsibility for the exact proof portions,
   mathematical dependencies, or formal artifacts assigned to them, including
   participating in correction or withdrawal if an error is found.

Substantive mathematical contributions can include decisive definitions,
lemmas, constructions, reductions, counterexamples, proof repairs, or
formalization work that materially establishes the result. Repository
ownership, project initiation, maintenance, funding, general participation,
code volume, experiment execution, translation, moderation, or review does not
automatically confer credit as a solver or theorem author. Those contributions
are recorded and acknowledged under their actual roles.

When substantive contributions cannot be reliably separated using auditable
evidence, the result must be credited collectively to the result-specific open
collaboration team recorded for that claim; no person may be presented as its
sole or primary solver on that basis. The published result record must identify
the claim and proof version, the team's exact membership, and every member's
responsibility entry. That team contains only contributors who meet the
contribution and responsibility requirements for the result. It does not
automatically include the repository owner, project founder, all maintainers,
or everyone who has participated in the repository.

Mathematical credit is distinct from copyright ownership, repository
permissions, software licensing, acknowledgements, and general contributor
recognition.

Every claimed mathematical-credit entry requires a contribution-responsibility
ledger containing:

- the claim, theorem, lemma, reduction, or formal-artifact identifier;
- the exact result and proof version or commit;
- the contributor's stable identity;
- the substantive mathematical contribution;
- the proof portion or dependency for which the contributor accepts
  responsibility;
- the recorded approval of the final statement and proof version; and
- any shared or backup responsibility.

Without this ledger, the repository may acknowledge work under its actual role
but does not publish solver or theorem-author credit.

### Credit Evidence and Disputes

Credit evidence includes the claim's Issue, commits, Pull Requests, proof
dependency records, review discussions, counterexamples, and recorded
responsibility approvals. A person may not decide a dispute in which they have
a direct credit interest.

An attribution dispute is handled publicly by at least two reviewers without a
direct stake in the disputed credit. They evaluate documented mathematical
contributions and responsibility rather than title or authority. Until the
review is complete, the attribution remains marked unresolved; the repository
owner cannot unilaterally publish a final solver-credit determination.
If the reviewers disagree, the credit remains unresolved and an additional
conflict-free reviewer or a new public review may be requested; disagreement
never defaults to owner or founder credit. Unresolved objections and the final
rationale remain attached to the result.

For the external-review gate, a qualified reviewer has documented expertise
relevant to the portion reviewed and is not a member of the result's contributor
team. The review record discloses recent coauthorship, employment or
supervision relationships, financial interests, and other direct personal
stakes. A material conflict prevents that review from satisfying the external
gate, although the comments remain part of the public record.

## Research Record Flow

1. A public Issue receives a stable claim identifier.
2. The hypothesis template records a bounded, falsifiable claim.
3. Experiments attach reproducible finite evidence without universal
   extrapolation.
4. Proof drafts attach explicit dependencies and objections.
5. Review records justify every status transition.
6. Counterexamples or proof gaps lower the status and create a preserved
   negative-result record.
7. A mature result records substantive contributors, responsibility, and any
   result-specific collective attribution.
8. Translations bind to an exact canonical English commit.

## Error Handling

- A claim without quantifiers or a falsification condition stays at `idea`.
- An experiment without its command, code version, environment, input
  provenance, or finite-domain statement cannot receive
  `experimentally-tested`.
- A proof with an unresolved blocking objection cannot receive
  `internally-checked` or a later status.
- Finite computational agreement cannot be described as a proof of an
  unrestricted complexity claim.
- A translation without a source commit is incomplete.
- A credit dispute without enough independent reviewers remains unresolved;
  authority defaults do not decide it.
- A foundation statement that differs from executable parser behavior blocks
  the milestone until either the document or tested implementation is
  deliberately reconciled in a separate change.

## Validation

Before commit:

1. Confirm all seven claim statuses are present and consistently spelled.
2. Check every relative Markdown link in the modified documentation and
   require every target file to exist.
3. Compare every accepted-DIMACS rule in `foundations/3-sat.md` against the
   current parser and its tests.
4. Confirm the English and Chinese README credit summaries have the same
   normative meaning.
5. Confirm the detailed governance policy includes substantive contribution,
   responsibility, result-specific collective credit, non-automatic owner or
   founder credit, the contribution-responsibility ledger, evidence, conflicts
   of interest, and unresolved-dispute handling.
6. Verify every mathematical history or complexity statement against a primary
   or authoritative source.
7. Run the existing test suite and whitespace checks.
8. Scan for unsupported statements that P equals NP, P differs from NP, or a
   Millennium Prize Problem has been solved.

The milestone is complete only when the documentation links resolve, the
foundation matches executable behavior, all tests pass, whitespace checks are
clean, and the working tree contains only the intended protocol changes.

This documentation-only milestone does not add permanent parser-contract
tests. Validation will use targeted runtime probes for contract bullets not
covered by the current suite and will record the missing regression coverage
as test debt. The later DPLL milestone must convert those probes into permanent
tests before its solver depends on the contract.

## Follow-Up Milestone

After this protocol milestone is implemented and reviewed, a separate design
will specify a deterministic DPLL reference solver with unit propagation,
fixed branching order, model verification, and bounded differential testing
against the brute-force solver. Agreement on finite test families will be
reported only as finite-domain validation, never as a complexity proof.
