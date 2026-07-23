# Translations

Translations provide access to versioned project documents. Each translation
is bound to a recorded source document and exact source commit. When content
differs, authority comes from that explicit source-version record, not from the source language.

## Required Metadata

Every translation records:

- language and locale;
- translated document path;
- recorded source document path;
- exact source commit;
- translation contributor record and current maintainer;
- translation date;
- known omissions or terminology choices; and
- synchronization status.

## Current Translations

### Simplified Chinese (`zh-CN`)

- Translation path: [README.zh-CN.md](../README.zh-CN.md)
- Recorded source document path: [README.md](../README.md)
- Exact source commit:
  [`884194b7ff6ec2ce1845feccd690de70f727014c`](https://github.com/ApacheWang/open-np-hard-research/commit/884194b7ff6ec2ce1845feccd690de70f727014c)
- Translation contributor record: Git history for `README.zh-CN.md`
- Current maintainer: ApacheWang
- Translation date: 2026-07-23
- Known omissions or terminology choices: none
- Synchronization status: current

## Synchronization

Synchronization changes require public review. If a possible mismatch is
reported, retain both the recorded source version and translation while the
mismatch is investigated. Each mismatch report must identify the recorded
source document path, exact source commit, and specific conflicting passage.
When the recorded source document changes, compare it with the exact source
commit and mark stale translations `needs-sync` until they are updated and
reviewed.

If the recorded source is wrong, fix that source first and then synchronize its
translations. Do not treat an outdated translation as current.

Translation, terminology review, and maintenance are recorded and acknowledged
under their actual roles. They do not automatically confer result-specific
solver or theorem-author credit unless the contributor also meets the
mathematical contribution and responsibility requirements in
[GOVERNANCE.md](../GOVERNANCE.md).
