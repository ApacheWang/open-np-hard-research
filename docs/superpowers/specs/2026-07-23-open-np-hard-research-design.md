# Open NP-Hard Research Lab — Repository Design

**Date:** 2026-07-23  
**Proposed repository:** `ApacheWang/open-np-hard-research`  
**Visibility:** Public  
**Canonical language:** English, with community-maintained translations welcome

## 1. Mission

Create a worldwide, open, rigorous, and reproducible research laboratory for studying NP-hard problems.

The repository will not present itself as having solved \(P\) versus \(NP\). Its purpose is to:

- develop and test exact, parameterized, approximation, and heuristic algorithms;
- formulate precise, falsifiable hypotheses;
- construct counterexamples and document failed approaches;
- write proof attempts in reviewable steps;
- preserve reproducible experiments and complexity analyses;
- help new contributors learn enough theory to participate responsibly.

The initial anchor problem will be **3-SAT**. Other NP-hard problems, including graph coloring, traveling salesperson, and subset sum, may be added when they support reductions, comparisons, or independent research tracks.

## 2. Success Criteria

The repository succeeds if it produces a growing body of work that is:

1. **Open:** anyone can read, discuss, reproduce, and propose improvements.
2. **Precise:** every research claim states its definitions, assumptions, and scope.
3. **Falsifiable:** hypotheses include a clear description of what would refute them.
4. **Reproducible:** computational results include code, data provenance, versions, seeds, and commands.
5. **Reviewable:** proof attempts are decomposed into named lemmas and explicit dependencies.
6. **Citable:** contributors, releases, and substantial results have stable attribution.
7. **Honest about negative results:** failed approaches remain searchable and useful.

A complete resolution of an NP-hard problem is not required for the project to be valuable. New algorithms, lower or upper bounds, reductions, counterexamples, datasets, proof techniques, and well-documented dead ends are valid outcomes.

## 3. Scope and Non-Goals

### In scope

- 3-SAT theory and algorithms;
- exact exponential algorithms and rigorously stated running-time bounds;
- parameterized complexity;
- approximation and inapproximability;
- proof complexity, circuit complexity, and relevant lower-bound techniques;
- reductions between NP-hard problems;
- SAT instance generation and benchmark curation;
- exhaustive small-instance searches for counterexamples;
- formal or machine-assisted verification when practical;
- surveys of known barriers and prior art.

### Not in scope

- claims based only on favorable benchmark performance;
- treating a solver for selected instances as evidence that \(P=NP\);
- hidden-source experiments that cannot be reproduced;
- promotional announcements of a proof before independent expert review;
- duplicate proof attempts that do not address known literature or known barriers;
- cryptocurrency, token, investment, or speculative fundraising schemes.

## 4. Repository Model

The repository will operate as a structured open-science lab rather than a loose collection of notes.

```text
.
├── README.md
├── ROADMAP.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── GOVERNANCE.md
├── CITATION.cff
├── LICENSE-CODE
├── LICENSE-RESEARCH
├── foundations/
├── hypotheses/
├── proofs/
├── experiments/
├── reductions/
├── benchmarks/
├── negative-results/
├── translations/
├── docs/
└── .github/
    ├── ISSUE_TEMPLATE/
    ├── PULL_REQUEST_TEMPLATE.md
    └── workflows/
```

### Directory responsibilities

- `foundations/`: definitions, notation, known results, known proof barriers, and curated reading paths.
- `hypotheses/`: numbered, falsifiable conjectures using a standard template.
- `proofs/`: proof drafts, named lemmas, dependency maps, and review status.
- `experiments/`: executable code and reproducible experiment manifests.
- `reductions/`: explicit polynomial-time reductions with correctness and complexity checks.
- `benchmarks/`: generated or redistributable instances plus provenance and licenses.
- `negative-results/`: refuted conjectures, counterexamples, failed proof routes, and lessons learned.
- `translations/`: non-canonical translations linked to the current English source.
- `docs/`: research process, architecture decisions, tutorials, and project documentation.

## 5. Research Claim Protocol

Every substantial claim will carry one status:

1. `idea` — informal direction, not yet a precise conjecture;
2. `conjecture` — precise and falsifiable;
3. `experimentally-tested` — tested only within a documented finite domain;
4. `proof-draft` — a complete argument is claimed but has unresolved review;
5. `internally-checked` — repository reviewers found no known gap;
6. `externally-reviewed` — independent domain experts have reviewed it;
7. `published` — accepted by a qualifying scholarly venue.

Status labels describe review state, not truth. Computational verification over finitely many inputs never establishes an unrestricted theorem.

Major claims must include:

- a formal statement with quantified variables;
- explicit assumptions and computational model;
- dependencies on prior lemmas or external results;
- a search for minimal counterexamples;
- complexity analysis where algorithms are involved;
- a known-barriers checklist;
- reviewer names and unresolved objections.

No project communication may state that \(P=NP\), \(P\ne NP\), or a Millennium Prize Problem has been solved while the work remains below `externally-reviewed`.

## 6. Collaboration and Global Participation

### Public channels

- **GitHub Discussions:** broad questions, reading groups, idea incubation, and multilingual community coordination.
- **GitHub Issues:** bounded research tasks, hypotheses, counterexample requests, experiment proposals, and proof-review assignments.
- **Pull Requests:** all durable changes to proofs, notes, code, data manifests, and governance.

### Contributor experience

- English is the canonical technical language so reviewers share one authoritative version.
- Translations are encouraged and credited, but must link to the canonical source commit.
- A newcomer guide will offer tasks requiring different skill levels.
- Issue labels will identify field, difficulty, required background, claim status, and review needs.
- First-time contributors can begin with reproduction, counterexample search, references, tests, or translations.
- Substantial contributions will be recorded in `CITATION.cff` and release notes.
- Conduct rules will prohibit harassment, credential-based dismissal, spam, and unsupported grandstanding while protecting rigorous criticism.

### Decision process

- Routine changes require one approving review.
- New research tracks or governance changes require a public proposal and a recorded maintainer decision.
- Major theorem claims require at least two independent reviews, including at least one reviewer not involved in drafting the claim.
- Review objections remain visible until resolved or explicitly documented as open.

## 7. Initial 3-SAT Research Track

The first track will establish a common, verifiable baseline:

1. define the exact 3-SAT decision problem and input encoding;
2. implement a small trusted verifier;
3. implement brute-force and DPLL-style reference solvers;
4. generate exhaustive and randomized small instances;
5. verify solver agreement and record performance without extrapolating to asymptotic claims;
6. document known reductions and known barriers;
7. open the first hypothesis only after the baseline and literature map exist.

The initial goal is not to announce a new polynomial-time algorithm. It is to create an environment in which a proposed idea can be rapidly formalized, tested, refuted, improved, and reviewed.

## 8. Reproducibility and Automation

Continuous integration will:

- run unit and property-based tests;
- compare independent solvers on small instances;
- validate benchmark manifests and checksums;
- reproduce designated lightweight experiments;
- check document links and required hypothesis/proof metadata;
- reject performance claims that lack a machine-readable experiment manifest.

Large experiments will publish environment specifications and summarized artifacts rather than committing oversized generated data.

## 9. Licensing and Attribution

- Source code will use the **Apache License 2.0**.
- Research notes, diagrams, and original documentation will use **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
- Third-party datasets and references must retain their original licenses and provenance.
- Contributions remain attributable through Git history, `CITATION.cff`, release notes, and acknowledgements.

This split permits broad reuse while keeping licensing terms clear for both software and research writing.

## 10. Safety, Quality, and Moderation

The maintainers will close or redirect submissions that:

- cannot state a checkable claim;
- repeatedly ignore identified counterexamples;
- misrepresent finite experiments as universal proofs;
- contain copied material without attribution;
- introduce malicious code, unsafe binaries, or unverifiable datasets;
- use the project to solicit money or promote unrelated products.

Rejected mathematical ideas should be treated respectfully. The project evaluates arguments and evidence, not status or credentials.

## 11. Launch Contents

The first public release will contain:

- a bilingual project introduction;
- mission, scope, roadmap, governance, contribution guide, and code of conduct;
- claim, proof-review, experiment, counterexample, and negative-result templates;
- the 3-SAT formal definition and glossary;
- a trusted verifier and baseline solver plan;
- reproducibility requirements;
- initial newcomer issues;
- licenses and citation metadata.

GitHub Discussions, Issues, and Pull Requests will be enabled from launch.

## 12. Acceptance

This design is ready for implementation when the repository owner confirms:

- the public repository name `ApacheWang/open-np-hard-research`;
- the structured open-science model;
- 3-SAT as the initial anchor problem;
- English as canonical with translations welcome;
- the claim-review protocol;
- dual licensing for code and research writing.
