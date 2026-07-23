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
