# README Neutrality Design

Date: 2026-07-23

## Purpose

The repository introductions must describe the project without endorsing,
ranking, or centering any country, nationality, region, language community,
institution, identity group, ideology, title, or prestige claim.

Neutrality does not mean removing research standards. Requirements based on
documented evidence, relevant expertise, reproducibility, disclosed conflicts,
substantive contribution, and responsibility remain in force because they
apply consistently to all contributors and are directly related to the work.

## Scope

This change updates:

- `README.md`;
- `README.zh-CN.md`; and
- `translations/README.md`.

It does not change the claim ladder, mathematical-credit criteria, review
counts, governance authority, Code of Conduct, licenses, 3-SAT definitions, or
software behavior.

## Neutrality Rules

The three documents must follow these rules:

1. Do not praise, criticize, recruit, or assign standing based on country,
   nationality, region, language, institution, demographic identity,
   ideology, title, or reputation.
2. Apply invitations to participate symmetrically to all contributors.
3. Use named languages only for a functional reason, such as navigation,
   locale identification, translation availability, or source provenance.
4. Do not use self-certifying quality or prestige terms such as `worldwide`,
   `rigorous`, `trusted`, `outstanding`, `全球化`, `可信`, or `卓越` to describe
   the project or its community.
5. Describe observable mechanisms instead: explicit definitions,
   reproducible experiments, reviewable claims, recorded evidence, versioned
   sources, and documented responsibilities.
6. Keep participation, review, and credit independent of language choice.
7. Record every contribution under its actual role. Mathematical-result credit
   continues to require the result-specific substantive contribution and
   responsibility defined in `GOVERNANCE.md`.

Protected participation and anti-harassment rules are not political or
national endorsements and remain unchanged.

## Document Changes

### English README

The introduction will:

- replace the evaluative project tagline with a factual description of a
  public collaboration on NP-hard problems;
- state that work is organized through explicit definitions, reproducible
  experiments, reviewable claims, and documented responsibilities;
- remove the paragraph that singles out Chinese mathematicians, China, and the
  Chinese-language mathematics community; and
- replace it with a universal invitation whose participation criteria do not
  depend on location, language, affiliation, background, or experience.

The 3-SAT section will replace `trusted` with operational properties such as
`documented`, `reviewable`, and `reproducible`.

The credit summary will state that maintenance, software, experiments,
translation, review, funding, and other contributions are recorded under their
actual roles even though those roles do not automatically confer solver or
theorem-author credit.

The language section will define version control by recorded source document
and commit rather than by declaring a language inherently canonical. It will
link the translation index and describe the Simplified Chinese README only as
an available translation.

### Simplified Chinese README

The Chinese introduction will carry the same normative meaning as the English
introduction:

- no country- or language-specific commendation;
- no China-first welcome order;
- `贡献者` rather than the narrower, status-bearing `研究者`;
- no self-evaluative terms such as `全球化`, `严谨`, `可信`, or `卓越`; and
- an operational description of definitions, reproducibility, review, and
  responsibility.

The source notice will refer to the recorded source document and source commit,
not to English as an intrinsically higher-authority language.

The credit section will replace `专属协作团队` with the result-specific,
publicly recorded collaboration team and will acknowledge non-mathematical
work under its actual role.

The language section will point to the translation index and use the same
source-path-and-commit rule as the English README.

### Translation Rules

`translations/README.md` will describe a language-neutral source-binding
protocol:

- every translation records a source path and exact source commit;
- the recorded source version controls when a translation is out of sync;
- authority comes from that explicit version binding, not from the source
  language;
- translation corrections use a public, reviewable change;
- changes that reveal an error in the source are made in the source first and
  then synchronized to translations; and
- every available translation is listed using the same metadata fields and
  display rule.

The current source files may be English files. That is a repository fact, not
a statement of linguistic or mathematical superiority.

## Consistency and Failure Handling

If a translation and its recorded source disagree, the repository will:

1. keep both versions visible;
2. identify the source path, source commit, and conflicting passage;
3. mark the translation as out of sync;
4. correct the source first if the source is wrong; and
5. synchronize the translation through a reviewed change.

No conflict is resolved by appealing to nationality, language prestige,
institution, title, or repository ownership.

## Validation

The implementation must pass all of the following:

1. A negative scan finds none of the removed national commendations or
   self-certifying project terms in the three scoped documents.
2. A positive semantic check confirms:
   - universal participation;
   - source path and exact commit binding;
   - language-independent participation, review, and credit;
   - actual-role acknowledgement; and
   - result-specific, publicly recorded mathematical collaboration credit.
3. The English and Chinese summaries have matching normative meaning.
4. All relative Markdown links in the three scoped documents resolve.
5. The P-versus-NP and finite-evidence disclaimers retain their meaning.
6. The seven claim statuses and mathematical-credit policy remain linked and
   unchanged in substance.
7. `python -m pytest -q` passes all existing tests.
8. `git diff --check` reports no whitespace errors.
9. The public `main` versions of all changed files match the reviewed local
   content by Git blob SHA after publication.

Named language terms used solely for navigation, locale labels, actual file
paths, or factual translation availability are permitted and must not be
treated as scan failures.

## Publication

Local work will use the `readme-neutrality` branch. The public repository will
be updated through authenticated GitHub file operations because the current
local Git credential is not valid for pushing.

Each remote file update must fetch the current blob SHA immediately before the
write. Writes must be sequential. After publication, every changed public file
must be fetched again and compared with the reviewed local blob.

The source-commit dependency requires this order:

1. complete and review the English README change locally;
2. publish that reviewed English README to public `main` and record the remote
   commit SHA returned by GitHub;
3. write that exact public commit SHA into the Simplified Chinese translation
   metadata and translation index;
4. review and commit the finalized translation documents locally; and
5. publish the translation rules and Simplified Chinese README sequentially.

No tracked document may contain a provisional source-commit placeholder. The
English source update and the two dependent translation updates form one
logical publication operation; completion is claimed only after all three
public files pass final content and blob-parity checks.

## Non-goals

This change will not:

- make multiple translations independently normative;
- remove conduct protections or equal-participation safeguards;
- weaken evidence, review, reproducibility, or credit requirements;
- rewrite unrelated governance, citation, roadmap, or software files; or
- claim that the project has solved P versus NP.
