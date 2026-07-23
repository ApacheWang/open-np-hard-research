from __future__ import annotations

from itertools import product
from typing import Mapping, TypeAlias

Clause: TypeAlias = tuple[int, ...]
Formula: TypeAlias = tuple[Clause, ...]


def parse_dimacs_3sat(text: str) -> Formula:
    header: tuple[int, int] | None = None
    clauses: list[Clause] = []
    pending: list[int] = []
    saw_clause_data = False

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("c"):
            continue
        if line.startswith("p"):
            if saw_clause_data:
                raise ValueError("DIMACS header must appear before clause data")
            if header is not None:
                raise ValueError("DIMACS input must contain exactly one header")
            parts = line.split()
            if len(parts) != 4 or parts[:2] != ["p", "cnf"]:
                raise ValueError("expected 'p cnf <variables> <clauses>' header")
            variable_count, declared_clause_count = int(parts[2]), int(parts[3])
            if variable_count < 0 or declared_clause_count < 0:
                raise ValueError("DIMACS header counts must be nonnegative")
            header = (variable_count, declared_clause_count)
            continue

        saw_clause_data = True
        for token in line.split():
            literal = int(token)
            if literal == 0:
                if not pending:
                    raise ValueError("empty clauses are not accepted by this baseline")
                if len(pending) > 3:
                    raise ValueError("3-SAT clauses must contain at most three literals")
                clauses.append(tuple(pending))
                pending = []
            else:
                pending.append(literal)

    if header is None:
        raise ValueError("missing DIMACS header")
    if pending:
        raise ValueError("clause is missing its terminating zero")

    variable_count, declared_clause_count = header
    if len(clauses) != declared_clause_count:
        raise ValueError("DIMACS clause count does not match the header")
    if any(abs(literal) > variable_count for clause in clauses for literal in clause):
        raise ValueError("literal exceeds the declared variable count")
    return tuple(clauses)


def satisfies(formula: Formula, assignment: Mapping[int, bool]) -> bool:
    return all(
        any(
            abs(literal) in assignment
            and assignment[abs(literal)] == (literal > 0)
            for literal in clause
        )
        for clause in formula
    )


def brute_force_solve(formula: Formula) -> dict[int, bool] | None:
    variables = sorted({abs(literal) for clause in formula for literal in clause})
    for values in product((False, True), repeat=len(variables)):
        assignment = dict(zip(variables, values, strict=True))
        if satisfies(formula, assignment):
            return assignment
    return None
