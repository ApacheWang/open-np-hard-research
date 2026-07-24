from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shlex
import subprocess
import sys
import tempfile
from importlib.metadata import version
from pathlib import Path
from typing import Callable, Sequence

from .finite import iter_canonical_formulas
from .sat3 import (
    Formula,
    brute_force_solve,
    dpll_solve,
    satisfies,
)

Solver = Callable[[Formula], object]
COMMIT_PATTERN = re.compile(r"[0-9a-f]{40}")
SCHEMA_VERSION = 1
GENERATOR_VERSION = 1


class InvalidModelError(ValueError):
    pass


def _canonical_json(value: object) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
    )


def _formula_data(formula: Formula) -> list[list[int]]:
    return [list(clause) for clause in formula]


def _model_data(
    model: object,
) -> dict[str, bool]:
    if type(model) is not dict:
        raise InvalidModelError("solver model must be an exact dict")
    if any(type(variable) is not int for variable in model):
        raise InvalidModelError(
            "solver model keys must be integers other than bool"
        )
    if any(type(value) is not bool for value in model.values()):
        raise InvalidModelError("solver model values must be Boolean")
    return {
        str(variable): model[variable]
        for variable in sorted(model)
    }


def _error_text(error: Exception) -> str:
    try:
        message = str(error)
    except Exception:
        message = "<error message unavailable>"
    return f"{type(error).__name__}: {message}"


def _solver_outcome(
    solver: Solver,
    formula: Formula,
) -> dict[str, object]:
    try:
        model = solver(formula)
        if model is None:
            return {
                "status": "unsat",
                "model": None,
                "model_valid": None,
                "error": None,
            }

        model_data = _model_data(model)
        model_valid = satisfies(formula, model)
        if type(model_valid) is not bool:
            raise InvalidModelError(
                "model validation must return a Boolean"
            )
        return {
            "status": "sat",
            "model": model_data,
            "model_valid": model_valid,
            "error": None,
        }
    except Exception as error:
        return {
            "status": "error",
            "model": None,
            "model_valid": False,
            "error": _error_text(error),
        }


def build_agreement_report(
    *,
    max_variables: int,
    max_clauses: int,
    code_commit: str,
    command: str,
    command_argv: Sequence[str] | None = None,
    command_shell: str | None = None,
) -> dict[str, object]:
    if max_variables < 0 or max_clauses < 0:
        raise ValueError("finite-domain limits must be nonnegative")
    if COMMIT_PATTERN.fullmatch(code_commit) is None:
        raise ValueError("code_commit must be exactly 40 lowercase hex characters")

    input_digest = hashlib.sha256()
    outcome_digest = hashlib.sha256()
    cases: list[dict[str, object]] = []
    mismatches: list[dict[str, object]] = []
    sat_count = 0
    unsat_count = 0

    for variable_count in range(max_variables + 1):
        for formula in iter_canonical_formulas(
            variable_count,
            max_clauses,
        ):
            input_record = {
                "variable_count": variable_count,
                "formula": _formula_data(formula),
            }
            input_line = _canonical_json(input_record)
            input_digest.update((input_line + "\n").encode("utf-8"))

            brute_force = _solver_outcome(brute_force_solve, formula)
            dpll = _solver_outcome(dpll_solve, formula)
            mismatch = (
                brute_force["status"] != dpll["status"]
                or brute_force["model_valid"] is False
                or dpll["model_valid"] is False
            )
            if brute_force["status"] == "sat":
                sat_count += 1
            elif brute_force["status"] == "unsat":
                unsat_count += 1

            case = {
                "case_number": len(cases) + 1,
                "case_id": hashlib.sha256(
                    input_line.encode("utf-8")
                ).hexdigest(),
                **input_record,
                "brute_force": brute_force,
                "dpll": dpll,
                "mismatch": mismatch,
            }
            outcome_digest.update(
                (_canonical_json(case) + "\n").encode("utf-8")
            )
            cases.append(case)
            if mismatch:
                mismatches.append(case)

    return {
        "schema_version": SCHEMA_VERSION,
        "experiment_id": "dpll-agreement-v1",
        "code_commit": code_commit,
        "command": command,
        "command_argv": (
            list(command_argv)
            if command_argv is not None
            else None
        ),
        "command_shell": command_shell,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "project_version": version("open-np-research"),
            "runtime_dependencies": [],
        },
        "generator": {
            "version": GENERATOR_VERSION,
            "max_variables": max_variables,
            "max_clauses": max_clauses,
            "clause_widths": [1, 2, 3],
            "distinct_variables_per_clause": True,
            "tautologies": False,
            "duplicate_clauses": False,
        },
        "seed": None,
        "formula_count": len(cases),
        "sat_count": sat_count,
        "unsat_count": unsat_count,
        "mismatch_count": len(mismatches),
        "input_sha256": input_digest.hexdigest(),
        "outcome_sha256": outcome_digest.hexdigest(),
        "finite_domain_statement": (
            "This report covers only the enumerated finite family and does not "
            "prove unrestricted solver correctness or any complexity claim."
        ),
        "performance_claim": None,
        "mismatches": mismatches,
        "cases": cases,
    }


def _require_public_commit(code_commit: str) -> None:
    if COMMIT_PATTERN.fullmatch(code_commit) is None:
        raise ValueError("code_commit must be exactly 40 lowercase hex characters")

    exists = subprocess.run(
        ["git", "cat-file", "-e", f"{code_commit}^{{commit}}"],
        check=False,
        capture_output=True,
        text=True,
    )
    if exists.returncode != 0:
        raise ValueError("code_commit is unavailable in the local repository")

    public = subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            code_commit,
            "origin/main",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
    if public.returncode != 0:
        raise ValueError("code_commit is not reachable from public origin/main")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compare deterministic DPLL with brute force on a finite family."
    )
    parser.add_argument("--max-variables", type=int, required=True)
    parser.add_argument("--max-clauses", type=int, required=True)
    parser.add_argument("--code-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser


def _command_metadata(
    arguments: Sequence[str],
) -> tuple[list[str], str, str]:
    command_argv = [
        "python",
        "-m",
        "open_np_research.agreement",
        *arguments,
    ]
    if os.name == "nt":
        command_shell = "PowerShell on Windows"
        command = "& " + " ".join(
            "'" + argument.replace("'", "''") + "'"
            for argument in command_argv
        )
    else:
        command_shell = "POSIX sh"
        command = shlex.join(command_argv)
    return command_argv, command, command_shell


def _write_report(
    output: Path,
    report: dict[str, object],
) -> None:
    rendered = (
        json.dumps(report, ensure_ascii=True, indent=2)
        + "\n"
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=output.parent,
            prefix=".agreement-",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            temporary.write(rendered)
            temporary.flush()
            os.fsync(temporary.fileno())
        temporary_path.replace(output)
    except BaseException:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)
        raise


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        _require_public_commit(args.code_commit)
        arguments = [
            "--max-variables",
            str(args.max_variables),
            "--max-clauses",
            str(args.max_clauses),
            "--code-commit",
            args.code_commit,
            f"--output={args.output}",
        ]
        command_argv, command, command_shell = _command_metadata(
            arguments
        )
        report = build_agreement_report(
            max_variables=args.max_variables,
            max_clauses=args.max_clauses,
            code_commit=args.code_commit,
            command=command,
            command_argv=command_argv,
            command_shell=command_shell,
        )
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    _write_report(args.output, report)
    print(
        _canonical_json(
            {
                "formula_count": report["formula_count"],
                "mismatch_count": report["mismatch_count"],
                "input_sha256": report["input_sha256"],
                "outcome_sha256": report["outcome_sha256"],
                "output": args.output.as_posix(),
            }
        )
    )
    return 1 if report["mismatch_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
