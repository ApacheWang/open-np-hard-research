from __future__ import annotations

import pytest

from open_np_research.finite import (
    canonical_clauses,
    iter_canonical_formulas,
)


def test_canonical_clause_counts_and_order() -> None:
    assert canonical_clauses(0) == ()
    assert canonical_clauses(1) == ((-1,), (1,))
    assert canonical_clauses(2) == (
        (-1,),
        (1,),
        (-2,),
        (2,),
        (-1, -2),
        (-1, 2),
        (1, -2),
        (1, 2),
    )
    assert len(canonical_clauses(3)) == 26


def test_formula_iteration_uses_distinct_canonical_combinations() -> None:
    assert tuple(iter_canonical_formulas(1, 3)) == (
        (),
        ((-1,),),
        ((1,),),
        ((-1,), (1,)),
    )


@pytest.mark.parametrize(
    ("variable_count", "max_clauses"),
    ((-1, 0), (0, -1)),
)
def test_formula_family_rejects_negative_parameters(
    variable_count: int,
    max_clauses: int,
) -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        tuple(iter_canonical_formulas(variable_count, max_clauses))
