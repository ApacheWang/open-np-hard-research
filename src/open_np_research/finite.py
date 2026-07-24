from __future__ import annotations

from itertools import combinations, product
from typing import Iterator

from .sat3 import Clause, Formula


def canonical_clauses(variable_count: int) -> tuple[Clause, ...]:
    if variable_count < 0:
        raise ValueError("variable_count must be nonnegative")

    clauses: list[Clause] = []
    variables = range(1, variable_count + 1)
    for width in range(1, min(3, variable_count) + 1):
        for selected in combinations(variables, width):
            for signs in product((-1, 1), repeat=width):
                clauses.append(
                    tuple(
                        variable * sign
                        for variable, sign in zip(
                            selected,
                            signs,
                            strict=True,
                        )
                    )
                )
    return tuple(clauses)


def iter_canonical_formulas(
    variable_count: int,
    max_clauses: int,
) -> Iterator[Formula]:
    if variable_count < 0:
        raise ValueError("variable_count must be nonnegative")
    if max_clauses < 0:
        raise ValueError("max_clauses must be nonnegative")

    clauses = canonical_clauses(variable_count)
    for clause_count in range(0, min(max_clauses, len(clauses)) + 1):
        yield from combinations(clauses, clause_count)
