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


def _literal_order(literal: int) -> tuple[int, bool]:
    return (abs(literal), literal < 0)


def _normalize_for_dpll(formula: Formula) -> Formula:
    normalized: list[Clause] = []
    for clause in formula:
        literals = set(clause)
        if any(-literal in literals for literal in literals):
            continue
        normalized.append(tuple(sorted(literals, key=_literal_order)))
    return tuple(normalized)


def _apply_literal(clauses: Formula, literal: int) -> Formula | None:
    false_literal = -literal
    simplified: list[Clause] = []
    for clause in clauses:
        if literal in clause:
            continue
        reduced = tuple(
            candidate for candidate in clause if candidate != false_literal
        )
        if not reduced:
            return None
        simplified.append(reduced)
    return tuple(simplified)


def _dpll_search(
    clauses: Formula,
    assignment: dict[int, bool],
    variables: tuple[int, ...],
) -> dict[int, bool] | None:
    stack = [(clauses, assignment)]
    while stack:
        clauses, assignment = stack.pop()
        if any(not clause for clause in clauses):
            continue

        conflict = False
        while clauses:
            units = sorted(
                (clause[0] for clause in clauses if len(clause) == 1),
                key=_literal_order,
            )
            if not units:
                break

            literal = units[0]
            variable = abs(literal)
            value = literal > 0
            previous = assignment.get(variable)
            if previous is not None and previous != value:
                conflict = True
                break

            simplified = _apply_literal(clauses, literal)
            if simplified is None:
                conflict = True
                break
            assignment = {**assignment, variable: value}
            clauses = simplified

        if conflict:
            continue
        if not clauses:
            return {
                variable: assignment.get(variable, False)
                for variable in variables
            }

        variable = min(
            abs(literal)
            for clause in clauses
            for literal in clause
            if abs(literal) not in assignment
        )
        # Push True first so the LIFO stack explores False first.
        for value in (True, False):
            literal = variable if value else -variable
            simplified = _apply_literal(clauses, literal)
            if simplified is not None:
                stack.append(
                    (
                        simplified,
                        {**assignment, variable: value},
                    )
                )
    return None


def dpll_solve(formula: Formula) -> dict[int, bool] | None:
    variables = tuple(
        sorted(
            {
                abs(literal)
                for clause in formula
                for literal in clause
            }
        )
    )
    model = _dpll_search(_normalize_for_dpll(formula), {}, variables)
    if model is not None and not satisfies(formula, model):
        raise AssertionError("DPLL returned a model that does not satisfy the formula")
    return model
