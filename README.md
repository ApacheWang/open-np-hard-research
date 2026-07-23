# Open NP-Hard Research

**English** | [简体中文](README.zh-CN.md)

A public collaboration for research on NP-hard problems. Work is organized
through explicit definitions, reproducible experiments, reviewable claims, and
documented responsibilities.

Participation is open to contributors regardless of location, language,
affiliation, background, or experience. Contributions are evaluated by their
documented content and evidence.

> This project has not solved P versus NP. Finite experiments are evidence about tested instances only; they are not proofs of unrestricted complexity claims.

## Start Here

Read the [roadmap](ROADMAP.md), the [contribution guide](CONTRIBUTING.md), and
the [research claim levels](docs/CLAIM_LEVELS.md). The initial shared foundation
is the [3-SAT definition](foundations/3-sat.md).

## Initial Focus: 3-SAT

Our first track establishes a documented, reviewable, and reproducible 3-SAT
baseline: precise definitions, reference solvers, small-instance checks,
literature mapping, and reviewable hypotheses.
We welcome exact, parameterized, approximation, and
heuristic work when its scope and evidence are stated precisely.

## Ways to Contribute

New contributors can reproduce experiments, add tests, search for
counterexamples, improve references, or translate documentation. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the newcomer path and research-claim
requirements.

## Research Claim Levels

Claims are labelled from an informal idea through published work so that review
state is visible. A label describes review progress, not mathematical truth.
See [docs/CLAIM_LEVELS.md](docs/CLAIM_LEVELS.md) for the canonical definitions.

## Credit for Mathematical Results

Credit for a mathematical result belongs to contributors who made documented,
substantive mathematical contributions, approved the final formal statement
and proof version, and accept responsibility for their assigned portions.
Repository ownership, project initiation, maintenance, funding, or general
participation does not automatically confer solver or theorem-author credit.
Maintenance, software, experiments, translation, review, funding, and other
contributions are recorded under their actual roles and acknowledged
accordingly.
When substantive contributions cannot be reliably separated, the result is
credited collectively to its recorded result-specific collaboration team—not
to every repository participant. See [GOVERNANCE.md](GOVERNANCE.md) for the
complete policy.

## Repository Map

- [foundations/](foundations/) holds definitions, notation, and reading paths.
- [hypotheses/](hypotheses/) holds precise, falsifiable conjectures.
- [proofs/](proofs/) holds reviewable proof drafts and dependencies.
- [experiments/](experiments/) holds executable, reproducible studies.
- [reductions/](reductions/) holds explicit reductions and their checks.
- [benchmarks/](benchmarks/) holds provenance-bearing instances.
- [negative-results/](negative-results/) preserves refuted claims and failed routes.

## Reproducibility

Computational results must state their code version, commands, dependencies,
data provenance, and deterministic seeds when applicable. Results from finite
domains must retain their finite-domain limitation.

## Languages and Translations

Each translation identifies its recorded source document and exact source commit using
the source path and public commit SHA. When a translation is out of sync, the
recorded path and public commit are the comparison point; the source language
does not affect participation, review, or credit.
See the [translation index](translations/README.md). A
[Simplified Chinese translation](README.zh-CN.md) is currently available.

## Governance and Conduct

Review and decision rules are in [GOVERNANCE.md](GOVERNANCE.md). All
participants must follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Licensing and Citation

Code is licensed under [Apache License 2.0](LICENSE-CODE). Original research
notes, diagrams, and documentation are licensed under [CC BY 4.0](LICENSE-RESEARCH).
For attribution, see [CITATION.cff](CITATION.cff).
