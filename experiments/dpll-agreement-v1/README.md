# DPLL Agreement v1

This experiment compares the repository's deterministic DPLL reference solver
with its independently structured brute-force solver.

## Finite Domain

The generator enumerates declared variable counts 0 through 3 and formulas
containing at most three distinct canonical clauses. Canonical clauses contain
one to three distinct variables, choose each sign independently, and exclude
tautologies. Formulas exclude duplicate clauses. The resulting record contains
exactly 3,050 cases.

Repeated literals, tautologies, duplicate clauses, and other accepted parser
boundaries are covered separately by focused tests; they are not part of this
enumerated family.

## Artifact

[`results.json`](results.json) stores every formula, both solver outcomes,
returned models, model-verification results, input and outcome digests,
environment data, the exact public implementation commit, and both replay
command forms.

## Replay

Run replays from the repository root. The `command_argv` array is the
authoritative command representation. Execute it without a shell:

```powershell
@'
from pathlib import Path
import json
import subprocess

path = Path("experiments/dpll-agreement-v1/results.json")
report = json.loads(path.read_text(encoding="utf-8"))
subprocess.run(report["command_argv"], shell=False, check=True)
'@ | python -
```

For a safe human-readable PowerShell command, the same report records this
shell-specific rendering:

```powershell
& 'python' '-m' 'open_np_research.agreement' '--max-variables' '3' `
  '--max-clauses' '3' `
  '--code-commit' 'aeaac15a822ce96a42b3c401100d1caf0cb3f885' `
  '--output=experiments\dpll-agreement-v1\results.json'
```

The artifact declares the human rendering's shell as `PowerShell on Windows`.
A successful replay exits zero and reproduces the same file SHA-256 on the
same recorded environment. A disagreement or invalid model remains in the
JSON and causes a nonzero exit.

## Interpretation

Zero mismatches mean only that the two implementations agreed on the recorded
finite family and that every returned SAT model passed the verifier. This is
not a proof of unrestricted solver correctness, a running-time bound, or a
conclusion about P versus NP.
