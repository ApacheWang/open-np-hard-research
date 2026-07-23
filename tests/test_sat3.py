import pytest

from open_np_research.sat3 import (
    brute_force_solve,
    parse_dimacs_3sat,
    satisfies,
)


def test_parse_and_verify_satisfying_assignment() -> None:
    formula = parse_dimacs_3sat(
        "c example\np cnf 3 2\n1 -2 3 0\n-1 2 3 0\n"
    )
    assert satisfies(formula, {1: True, 2: True, 3: True})


def test_incomplete_assignment_does_not_satisfy_a_negative_literal() -> None:
    formula = parse_dimacs_3sat("p cnf 1 1\n-1 0\n")
    assert not satisfies(formula, {})


def test_rejects_clause_with_more_than_three_literals() -> None:
    with pytest.raises(ValueError, match="at most three"):
        parse_dimacs_3sat("p cnf 4 1\n1 2 3 4 0\n")


def test_rejects_header_count_mismatch() -> None:
    with pytest.raises(ValueError, match="clause count"):
        parse_dimacs_3sat("p cnf 2 2\n1 2 0\n")


def test_rejects_header_after_clause_data() -> None:
    with pytest.raises(ValueError, match="before clause data"):
        parse_dimacs_3sat("1 0\np cnf 1 1\n")


def test_rejects_header_after_pending_literals() -> None:
    with pytest.raises(ValueError, match="before clause data"):
        parse_dimacs_3sat("1\np cnf 1 1\n")


def test_rejects_duplicate_header() -> None:
    with pytest.raises(ValueError, match="exactly one"):
        parse_dimacs_3sat("p cnf 1 1\np cnf 1 1\n1 0\n")


def test_rejects_negative_variable_count() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        parse_dimacs_3sat("p cnf -1 0\n")


def test_rejects_negative_clause_count() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        parse_dimacs_3sat("p cnf 1 -1\n")


def test_brute_force_solver_finds_model() -> None:
    formula = parse_dimacs_3sat("p cnf 2 2\n1 2 0\n-1 2 0\n")
    model = brute_force_solve(formula)
    assert model is not None
    assert satisfies(formula, model)


def test_brute_force_solver_reports_unsatisfiable() -> None:
    formula = parse_dimacs_3sat("p cnf 1 2\n1 0\n-1 0\n")
    assert brute_force_solve(formula) is None
