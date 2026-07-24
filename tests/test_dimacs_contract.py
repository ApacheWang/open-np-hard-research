from __future__ import annotations

import pytest

from open_np_research.sat3 import (
    brute_force_solve,
    parse_dimacs_3sat,
    satisfies,
)


def test_accepts_comments_blanks_spanning_and_multiple_clauses() -> None:
    formula = parse_dimacs_3sat(
        "\n"
        "   c contract example\n"
        "p cnf 5 3\n"
        "1 -1 0 2 2 0\n"
        "-3\n"
        "4 0\n"
        "\n"
    )
    assert formula == ((1, -1), (2, 2), (-3, 4))


def test_accepts_empty_formula_and_unused_declared_variables() -> None:
    empty = parse_dimacs_3sat("p cnf 0 0\n")
    assert empty == ()
    assert brute_force_solve(empty) == {}
    assert satisfies(empty, {})

    unused = parse_dimacs_3sat("p cnf 3 1\n1 0\n")
    assert unused == ((1,),)
    assert brute_force_solve(unused) == {1: True}


def test_accepts_one_two_three_literal_tautological_and_repeated_clauses() -> None:
    formula = parse_dimacs_3sat(
        "p cnf 3 6\n"
        "1 0\n"
        "1 -2 0\n"
        "1 -2 3 0\n"
        "2 2 0\n"
        "3 -3 0\n"
        "1 0\n"
    )
    assert formula == (
        (1,),
        (1, -2),
        (1, -2, 3),
        (2, 2),
        (3, -3),
        (1,),
    )


@pytest.mark.parametrize(
    ("text", "message"),
    (
        ("1 0\n", "missing DIMACS header"),
        ("p cnf 1\n1 0\n", "expected 'p cnf"),
        ("p cnf 1 1\np cnf 1 1\n1 0\n", "exactly one header"),
        ("1 0\np cnf 1 1\n", "before clause data"),
        ("p cnf -1 0\n", "counts must be nonnegative"),
        ("p cnf 1 -1\n", "counts must be nonnegative"),
        ("p cnf 1 1\n1\n", "terminating zero"),
        ("p cnf 1 1\n0\n", "empty clauses"),
        ("p cnf 4 1\n1 2 3 4 0\n", "at most three literals"),
        ("p cnf 1 1\n2 0\n", "exceeds the declared variable count"),
        ("p cnf 1 2\n1 0\n", "clause count"),
    ),
)
def test_rejects_inputs_outside_the_documented_subset(
    text: str,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        parse_dimacs_3sat(text)


def test_rejects_inline_comments() -> None:
    with pytest.raises(ValueError):
        parse_dimacs_3sat("p cnf 1 1\n1 0 c inline comments are excluded\n")


def test_partial_assignment_and_extra_keys_keep_documented_semantics() -> None:
    assert not satisfies(((1,),), {})
    assert satisfies(((1,),), {1: True, 99: False})
