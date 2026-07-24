from __future__ import annotations

import sys

from open_np_research.sat3 import dpll_solve, satisfies


def test_dpll_solves_empty_formula() -> None:
    assert dpll_solve(()) == {}


def test_dpll_applies_a_unit_propagation_chain() -> None:
    formula = ((1,), (-1, 2), (-2, 3))
    model = dpll_solve(formula)
    assert model == {1: True, 2: True, 3: True}
    assert satisfies(formula, model)


def test_dpll_detects_conflicting_units() -> None:
    assert dpll_solve(((1,), (-1,))) is None


def test_dpll_backtracks_from_false_to_true() -> None:
    formula = ((1, 2), (1, -2), (-1, 2))
    model = dpll_solve(formula)
    assert model == {1: True, 2: True}
    assert satisfies(formula, model)


def test_dpll_proves_a_two_variable_formula_unsatisfiable() -> None:
    formula = ((1, 2), (1, -2), (-1, 2), (-1, -2))
    assert dpll_solve(formula) is None


def test_dpll_handles_repeated_literals_and_tautologies() -> None:
    formula = ((1, -1), (2, 2))
    model = dpll_solve(formula)
    assert model == {1: False, 2: True}
    assert satisfies(formula, model)


def test_dpll_completes_variables_from_satisfied_clauses() -> None:
    formula = ((1,), (2, -2), (3, -3))
    model = dpll_solve(formula)
    assert model == {1: True, 2: False, 3: False}
    assert satisfies(formula, model)


def test_dpll_uses_a_deterministic_false_first_branch() -> None:
    formula = ((1, 2),)
    expected = {1: False, 2: True}
    assert [dpll_solve(formula) for _ in range(5)] == [expected] * 5


def test_dpll_handles_more_branch_decisions_than_recursion_limit() -> None:
    branch_count = sys.getrecursionlimit() + 1
    formula = tuple(
        (variable, variable + 1)
        for variable in range(1, 2 * branch_count + 1, 2)
    )
    expected = {
        variable: variable % 2 == 0
        for variable in range(1, 2 * branch_count + 1)
    }

    model = dpll_solve(formula)

    assert model == expected
    assert satisfies(formula, model)
