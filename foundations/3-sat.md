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
