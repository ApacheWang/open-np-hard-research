# Contributing

Thank you for helping build a rigorous, reproducible public research lab.

## A Newcomer Path

Start with a bounded contribution: reproduce a documented result, add or
improve tests, search for a counterexample, add a well-sourced reference, or
translate an English source. Explain what you changed, how it can be checked,
and any limitation you found.

## Local Setup and Checks

Run these commands from the repository root:

```powershell
python -m pip install -e .[dev]
pytest -q
```

## Research Claims

Open or reference a GitHub Issue for every research claim. State the claim
precisely, identify assumptions and scope, cite related work, and link the
evidence or reproduction instructions. Do not claim a universal result from
finite tests: finite experiments support conclusions only about their documented
tested domain.

## Licensing Your Contribution

By contributing, you license code contributions under Apache-2.0 and your
original prose and diagrams under CC BY 4.0. You must retain the license and
provenance of third-party material, data, and references.

## Review

Keep changes focused, respond to review evidence, and preserve useful
counterexamples and negative results. See [GOVERNANCE.md](GOVERNANCE.md) for
the review rules and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for expected
conduct.
