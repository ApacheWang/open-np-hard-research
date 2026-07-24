# Experiments

Each experiment record must include:

- the exact command used to run it;
- the Git commit identifier;
- Python and dependency versions;
- a machine description;
- input provenance and checksums;
- the deterministic seed (when one is used);
- raw outputs and summarized outputs; and
- an explicit statement that this baseline operates only over a finite domain.

The baseline solver exhaustively enumerates assignments and is therefore not
intended to establish behavior beyond the finite instances recorded with an
experiment.

## Current Experiments

- [DPLL Agreement v1](dpll-agreement-v1/README.md) records case-by-case
  finite-domain agreement between the deterministic DPLL and brute-force
  reference solvers.
