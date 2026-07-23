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
