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
From the time a credit dispute opens until independent review completes, the
disputed attribution must remain marked `unresolved`. No final solver or
theorem-author attribution may be published while the dispute is unresolved.

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

Unresolved objections and the reviewers' final rationale must remain attached
to the result record.

## Governance Changes

Any governance change requires a public Issue and a recorded maintainer
decision. New research tracks follow the same public-proposal and
recorded-decision practice.
