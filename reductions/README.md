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
