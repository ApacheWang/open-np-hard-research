# Open NP-Hard Research

An open, worldwide, rigorous, and reproducible research lab for NP-hard problems.

> This project has not solved P versus NP. Finite experiments are evidence about
> tested instances only; they are not proofs of unrestricted complexity claims.

## Start Here

Read the [roadmap](ROADMAP.md), the [contribution guide](CONTRIBUTING.md), and
the [research claim levels](docs/CLAIM_LEVELS.md). The initial shared foundation
is the [3-SAT definition](foundations/3-sat.md).

## Initial Focus: 3-SAT

Our first track builds a trusted, reproducible 3-SAT baseline: precise
definitions, reference solvers, small-instance checks, literature mapping, and
reviewable hypotheses. We welcome exact, parameterized, approximation, and
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

English is the canonical technical language. Community-maintained translations
are welcome; begin with the [Chinese introduction](README.zh-CN.md) and link
translations to their English source.

## Governance and Conduct

Review and decision rules are in [GOVERNANCE.md](GOVERNANCE.md). All
participants must follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Licensing and Citation

Code is licensed under [Apache License 2.0](LICENSE-CODE). Original research
notes, diagrams, and documentation are licensed under [CC BY 4.0](LICENSE-RESEARCH).
For attribution, see [CITATION.cff](CITATION.cff).
