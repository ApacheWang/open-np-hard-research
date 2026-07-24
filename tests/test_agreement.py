from __future__ import annotations

import json
import subprocess

import pytest

from open_np_research import agreement


def test_ci_family_has_394_agreeing_raw_cases() -> None:
    report = agreement.build_agreement_report(
        max_variables=3,
        max_clauses=2,
        code_commit="0" * 40,
        command="finite CI contract",
    )

    assert report["formula_count"] == 394
    assert report["mismatch_count"] == 0
    assert report["sat_count"] + report["unsat_count"] == 394
    assert len(report["cases"]) == 394
    assert len(report["input_sha256"]) == 64
    assert len(report["outcome_sha256"]) == 64
    assert all(
        case["brute_force"]["model_valid"] is not False
        and case["dpll"]["model_valid"] is not False
        for case in report["cases"]
    )


def test_agreement_digests_and_case_order_are_deterministic() -> None:
    first = agreement.build_agreement_report(
        max_variables=2,
        max_clauses=2,
        code_commit="1" * 40,
        command="determinism contract",
    )
    second = agreement.build_agreement_report(
        max_variables=2,
        max_clauses=2,
        code_commit="1" * 40,
        command="determinism contract",
    )

    assert first["formula_count"] == 42
    assert first["input_sha256"] == second["input_sha256"]
    assert first["outcome_sha256"] == second["outcome_sha256"]
    assert first["cases"] == second["cases"]


def test_mismatches_preserve_complete_raw_cases(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(agreement, "dpll_solve", lambda formula: None)
    report = agreement.build_agreement_report(
        max_variables=1,
        max_clauses=1,
        code_commit="2" * 40,
        command="forced mismatch contract",
    )

    assert report["formula_count"] == 4
    assert report["mismatch_count"] == 4
    assert report["mismatches"] == report["cases"]
    assert all("formula" in case for case in report["mismatches"])
    assert all("brute_force" in case for case in report["mismatches"])
    assert all("dpll" in case for case in report["mismatches"])


@pytest.mark.parametrize(
    "invalid_model",
    (
        object(),
        {True: True},
        {"1": True},
        {1: True, "2": False},
        {1: 1},
        {1: object()},
    ),
    ids=(
        "non-dict",
        "boolean-key",
        "string-key",
        "unorderable-keys",
        "integer-value",
        "non-json-value",
    ),
)
def test_malformed_models_are_json_safe_mismatches(
    monkeypatch: pytest.MonkeyPatch,
    invalid_model: object,
) -> None:
    monkeypatch.setattr(
        agreement,
        "dpll_solve",
        lambda formula: invalid_model,
    )

    report = agreement.build_agreement_report(
        max_variables=0,
        max_clauses=0,
        code_commit="4" * 40,
        command="invalid model contract",
    )

    assert report["formula_count"] == 1
    assert report["mismatch_count"] == 1
    assert report["mismatches"] == report["cases"]
    outcome = report["cases"][0]["dpll"]
    assert outcome["status"] == "error"
    assert outcome["model"] is None
    assert outcome["model_valid"] is False
    assert outcome["error"].startswith("InvalidModelError: ")
    assert json.loads(json.dumps(report)) == report


def test_validation_errors_are_recorded_in_complete_cases(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def fail_validation(formula, model) -> bool:
        raise RuntimeError("forced validation failure")

    monkeypatch.setattr(agreement, "satisfies", fail_validation)
    report = agreement.build_agreement_report(
        max_variables=0,
        max_clauses=0,
        code_commit="5" * 40,
        command="validation error contract",
    )

    assert report["formula_count"] == 1
    assert report["mismatch_count"] == 1
    assert report["mismatches"] == report["cases"]
    assert all(
        case[solver]["status"] == "error"
        and case[solver]["model_valid"] is False
        and case[solver]["error"] == (
            "RuntimeError: forced validation failure"
        )
        for case in report["cases"]
        for solver in ("brute_force", "dpll")
    )
    assert json.loads(json.dumps(report)) == report


def test_cli_writes_malformed_outcomes_before_nonzero_exit(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(agreement, "_require_public_commit", lambda commit: None)
    monkeypatch.setattr(agreement, "dpll_solve", lambda formula: object())
    output = tmp_path / "invalid-results.json"

    exit_code = agreement.main(
        [
            "--max-variables",
            "0",
            "--max-clauses",
            "0",
            "--code-commit",
            "6" * 40,
            "--output",
            str(output),
        ]
    )

    assert exit_code == 1
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["formula_count"] == 1
    assert report["mismatch_count"] == 1
    assert report["mismatches"] == report["cases"]
    assert report["cases"][0]["dpll"]["status"] == "error"
    assert report["cases"][0]["dpll"]["model_valid"] is False


def test_cli_ascii_escapes_surrogate_errors_without_truncation(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    def raise_surrogate(formula):
        raise ValueError("\ud800")

    monkeypatch.setattr(agreement, "_require_public_commit", lambda commit: None)
    monkeypatch.setattr(agreement, "dpll_solve", raise_surrogate)
    output = tmp_path / "surrogate-results.json"
    output.write_text('{"prior": true}\n', encoding="utf-8")

    try:
        exit_code = agreement.main(
            [
                "--max-variables",
                "1",
                "--max-clauses",
                "1",
                "--code-commit",
                "7" * 40,
                "--output",
                str(output),
            ]
        )
    except UnicodeEncodeError:
        exit_code = None

    raw_report = output.read_bytes()
    assert exit_code == 1
    assert raw_report
    assert b"\\ud800" in raw_report
    report = json.loads(raw_report)
    assert report["formula_count"] == 4
    assert report["mismatch_count"] == 4
    assert report["mismatches"] == report["cases"]
    assert all(
        case["dpll"]["error"] == "ValueError: \ud800"
        for case in report["cases"]
    )


def test_cli_rejects_hostile_dict_subclasses_without_aborting(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    class HostileModel(dict[int, bool]):
        def __getitem__(self, key: int) -> object:
            return object()

    monkeypatch.setattr(agreement, "_require_public_commit", lambda commit: None)
    monkeypatch.setattr(
        agreement,
        "dpll_solve",
        lambda formula: HostileModel({1: True}),
    )
    output = tmp_path / "hostile-model-results.json"

    try:
        exit_code = agreement.main(
            [
                "--max-variables",
                "0",
                "--max-clauses",
                "0",
                "--code-commit",
                "8" * 40,
                "--output",
                str(output),
            ]
        )
    except TypeError:
        exit_code = None

    assert exit_code == 1
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["formula_count"] == 1
    assert report["mismatch_count"] == 1
    assert report["mismatches"] == report["cases"]
    outcome = report["cases"][0]["dpll"]
    assert outcome["status"] == "error"
    assert outcome["model"] is None
    assert outcome["model_valid"] is False
    assert outcome["error"] == (
        "InvalidModelError: solver model must be an exact dict"
    )


def test_cli_records_safe_argument_vector_for_replay(tmp_path) -> None:
    code_commit = subprocess.run(
        ["git", "rev-parse", "origin/main"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    output = tmp_path / "replay path & evidence.json"
    arguments = [
        "--max-variables",
        "0",
        "--max-clauses",
        "0",
        "--code-commit",
        code_commit,
        "--output",
        str(output),
    ]

    assert agreement.main(arguments) == 0
    report = json.loads(output.read_text(encoding="utf-8"))
    command_argv = report["command_argv"]

    assert command_argv == [
        "python",
        "-m",
        "open_np_research.agreement",
        *arguments[:-2],
        f"--output={output}",
    ]
    assert report["command_shell"]
    assert str(output) in report["command"]

    replay = subprocess.run(
        command_argv,
        check=False,
        capture_output=True,
        text=True,
        shell=False,
    )
    assert replay.returncode == 0, replay.stderr
    replayed = json.loads(output.read_text(encoding="utf-8"))
    assert replayed["command_argv"] == command_argv
    assert replayed["formula_count"] == 1
    assert replayed["mismatch_count"] == 0


def test_cli_preserves_leading_dash_output_for_vector_replay(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(agreement, "_require_public_commit", lambda commit: None)
    monkeypatch.chdir(tmp_path)
    arguments = [
        "--max-variables",
        "0",
        "--max-clauses",
        "0",
        "--code-commit",
        "9" * 40,
        "--output=-report.json",
    ]

    assert agreement.main(arguments) == 0
    output = tmp_path / "-report.json"
    report = json.loads(output.read_text(encoding="utf-8"))
    command_argv = report["command_argv"]

    assert command_argv == [
        "python",
        "-m",
        "open_np_research.agreement",
        *arguments,
    ]
    assert agreement.main(command_argv[3:]) == 0
    replayed = json.loads(output.read_text(encoding="utf-8"))
    assert replayed["command_argv"] == command_argv
    assert replayed["formula_count"] == 1
    assert replayed["mismatch_count"] == 0


def test_cli_rejects_an_unavailable_public_commit(
    tmp_path,
) -> None:
    output = tmp_path / "results.json"
    exit_code = agreement.main(
        [
            "--max-variables",
            "1",
            "--max-clauses",
            "1",
            "--code-commit",
            "0" * 40,
            "--output",
            str(output),
        ]
    )
    assert exit_code == 2
    assert not output.exists()


def test_report_is_json_serializable() -> None:
    report = agreement.build_agreement_report(
        max_variables=1,
        max_clauses=1,
        code_commit="3" * 40,
        command="serialization contract",
    )
    assert json.loads(json.dumps(report)) == report
