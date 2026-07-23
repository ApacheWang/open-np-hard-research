# README Neutrality Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the English README, Simplified Chinese README, and translation
protocol neutral with respect to nationality, region, language, institution,
identity, ideology, title, and prestige while retaining evidence-based research
and credit rules.

**Architecture:** The English README is the current source document, but its
authority comes from an explicit path and public commit rather than its
language. Publish the reviewed English source first, capture GitHub's returned
commit SHA, then bind the Chinese translation and translation index to that
exact public commit. Validate the three documents as one logical publication.

**Tech Stack:** Markdown, Python 3.11+, PowerShell, pytest, Git, GitHub Contents
API through the connected GitHub app.

## Global Constraints

- Modify only `README.md`, `README.zh-CN.md`, and
  `translations/README.md` for product wording.
- Design and plan artifacts may be added under `docs/superpowers/`.
- Do not praise, criticize, recruit, or assign standing based on country,
  nationality, region, language, institution, demographic identity,
  ideology, title, or reputation.
- Do not describe the project with self-certifying terms including
  `worldwide`, `rigorous`, `trusted`, `outstanding`, `全球化`, `严谨`, `可信`,
  or `卓越`.
- Named languages are permitted only for navigation, locale identification,
  translation availability, or source provenance.
- Authority must bind to a recorded source document path and exact public
  source commit, not to a language.
- Participation, review, and credit must be independent of language choice.
- Preserve the P-versus-NP disclaimer, finite-evidence warning, seven claim
  statuses, mathematical-credit criteria, licenses, and software behavior.
- Use the branch `readme-neutrality`; no branch name may contain `codex`.
- Use `apply_patch` for file edits.
- Local Git credentials are invalid for push. Use connected GitHub file
  operations for public writes, fetching the current remote blob SHA before
  each sequential update.
- A dynamic value named `PUBLIC_SOURCE_COMMIT` is produced by Task 2. It is the
  exact 40-hex GitHub commit SHA returned when public `main` receives the
  reviewed English README. Never write the literal name
  `PUBLIC_SOURCE_COMMIT` into a tracked document.

## File Responsibilities

- `README.md`: neutral source introduction, contribution summary, credit
  summary, and source-binding explanation.
- `README.zh-CN.md`: semantically equivalent Simplified Chinese translation
  with visible source path, exact public source commit, and synchronization
  status.
- `translations/README.md`: language-neutral source-binding protocol and
  metadata for the current Simplified Chinese translation.
- `.superpowers/sdd/readme-neutrality-source-publication.json`: ignored
  machine-readable Task 2 handoff containing the actual remote source commit
  and blob SHA.
- `docs/superpowers/specs/2026-07-23-readme-neutrality-design.md`: approved
  design and acceptance criteria.
- `docs/superpowers/plans/2026-07-23-readme-neutrality.md`: this execution
  plan.

---

### Task 1: Neutralize the English README

**Files:**
- Modify: `README.md`
- Test: inline Python contract and Markdown-link probes

**Interfaces:**
- Consumes: existing claim, credit, contribution, and translation links.
- Produces: reviewed English source content that Task 2 publishes unchanged.

- [ ] **Step 1: Run the English neutrality contract before editing**

Run from the repository root:

```powershell
@'
from pathlib import Path

text = Path("README.md").read_text(encoding="utf-8")
forbidden = (
    "An open, worldwide, rigorous, and reproducible research lab",
    "Chinese mathematicians",
    "Chinese-language mathematics community",
    "outstanding contributions",
    "China and every part of the world",
    "trusted, reproducible 3-SAT baseline",
    "English is the canonical technical language",
)
required = (
    "A public collaboration for research on NP-hard problems.",
    "explicit definitions, reproducible experiments, reviewable claims",
    "Participation is open to contributors regardless of location, language,",
    "recorded under their actual roles",
    "recorded source document and exact source commit",
)
failures = [f"forbidden remains: {item}" for item in forbidden if item in text]
failures += [f"required missing: {item}" for item in required if item not in text]
if failures:
    raise AssertionError("\n".join(failures))
print("PASS: English README neutrality contract")
'@ | python -
```

Expected: nonzero exit with both forbidden-phrase and missing-required-phrase
diagnostics.

- [ ] **Step 2: Replace the English introduction with operational language**

Use `apply_patch` so the introduction after the language navigation reads:

```markdown
A public collaboration for research on NP-hard problems. Work is organized
through explicit definitions, reproducible experiments, reviewable claims, and
documented responsibilities.

Participation is open to contributors regardless of location, language,
affiliation, background, or experience. Contributions are evaluated by their
documented content and evidence.
```

Delete the entire paragraph that commends Chinese mathematicians and separately
welcomes China.

- [ ] **Step 3: Replace the 3-SAT self-evaluation**

Use `apply_patch` so the first sentence under `## Initial Focus: 3-SAT` reads:

```markdown
Our first track establishes a documented, reviewable, and reproducible 3-SAT
baseline: precise definitions, reference solvers, small-instance checks,
literature mapping, and reviewable hypotheses.
```

Keep the following sentence about exact, parameterized, approximation, and
heuristic work unchanged.

- [ ] **Step 4: Balance the credit summary**

After the sentence denying automatic solver or theorem-author credit, add:

```markdown
Those contributions are recorded and acknowledged under their actual roles.
```

Retain the substantive-contribution, responsibility, result-specific team, and
`GOVERNANCE.md` language.

- [ ] **Step 5: Replace the English language-authority paragraph**

Use `apply_patch` so `## Languages and Translations` reads:

```markdown
## Languages and Translations

Each translation records a source document and exact source commit. If a
translation is out of sync, that recorded source version is the comparison
point; the source language does not affect participation, review, or credit.
See the [translation index](translations/README.md). A
[Simplified Chinese translation](README.zh-CN.md) is currently available.
```

- [ ] **Step 6: Re-run the English contract**

Run the exact command from Step 1.

Expected: `PASS: English README neutrality contract`.

- [ ] **Step 7: Verify the English disclaimer and links**

Run:

```powershell
@'
from pathlib import Path
import re
from urllib.parse import unquote

path = Path("README.md")
text = path.read_text(encoding="utf-8")
assert "This project has not solved P versus NP." in text
assert "Finite experiments are evidence about tested instances only" in text
assert "docs/CLAIM_LEVELS.md" in text
assert "GOVERNANCE.md" in text

for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
    target = raw.strip()
    if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
        continue
    target = unquote(target.split("#", 1)[0].strip("<>"))
    if target:
        assert (path.parent / target).exists(), target
print("PASS: English README disclaimer and links")
'@ | python -
python -m pytest -q
git diff --check
```

Expected:

```text
PASS: English README disclaimer and links
...........                                                              [100%]
```

`git diff --check` produces no output.

- [ ] **Step 8: Commit the English source**

Run:

```powershell
git add -- README.md
git diff --cached --check
git diff --cached --name-only
git commit -m "docs: neutralize English README"
```

Expected staged path: only `README.md`.

---

### Task 2: Publish and Bind the English Source

**Files:**
- Create: `.superpowers/sdd/readme-neutrality-source-publication.json`
- Read remotely: `README.md` on `ApacheWang/open-np-hard-research` branch
  `main`

**Interfaces:**
- Consumes: the exact `README.md` blob from Task 1's reviewed commit.
- Produces: `PUBLIC_SOURCE_COMMIT` and the remote content blob SHA in the
  ignored JSON report for Task 3.

- [ ] **Step 1: Confirm the source task is reviewable**

Run:

```powershell
git status --short --branch
git log -1 --format="%H%n%s"
git show --stat --oneline HEAD
git diff HEAD^..HEAD -- README.md
```

Expected: clean `readme-neutrality` branch; the latest commit subject is
`docs: neutralize English README`; only `README.md` is in that commit.

- [ ] **Step 2: Fetch the current public source**

Use the connected GitHub app to fetch:

```text
repository_full_name: ApacheWang/open-np-hard-research
path: README.md
ref: main
encoding: utf-8
```

Record the current remote blob SHA returned by GitHub. Confirm it matches the
pre-update public content and do not infer it from local history.

- [ ] **Step 3: Update public `README.md`**

Read the complete local source from:

```powershell
git show --no-textconv HEAD:README.md
```

Use the GitHub Contents API update operation with:

```text
repository_full_name: ApacheWang/open-np-hard-research
branch: main
path: README.md
sha: the freshly fetched remote blob SHA
message: docs: neutralize English README
content: the complete UTF-8 local README.md
```

Expected: a successful result containing a new 40-hex commit SHA and content
blob SHA. The returned commit SHA is `PUBLIC_SOURCE_COMMIT`.

- [ ] **Step 4: Verify the public English source**

Fetch public `README.md` again. Compare:

```powershell
git rev-parse HEAD:README.md
```

Expected: the remote content blob SHA equals the local blob SHA and the remote
decoded UTF-8 content equals `git show --no-textconv HEAD:README.md`.

- [ ] **Step 5: Record the dynamic handoff**

Use `apply_patch` to create
`.superpowers/sdd/readme-neutrality-source-publication.json` with these exact
keys and the actual values returned by GitHub:

```text
repository
branch
path
remote_commit_sha
remote_blob_sha
local_blob_sha
verified_equal
```

The values must satisfy:

```python
assert report["repository"] == "ApacheWang/open-np-hard-research"
assert report["branch"] == "main"
assert report["path"] == "README.md"
assert re.fullmatch(r"[0-9a-f]{40}", report["remote_commit_sha"])
assert report["remote_blob_sha"] == report["local_blob_sha"]
assert report["verified_equal"] is True
```

The report is ignored scratch evidence. Do not create a local Git commit for
Task 2.

---

### Task 3: Neutralize and Bind the Translation Documents

**Files:**
- Modify: `README.zh-CN.md`
- Modify: `translations/README.md`
- Read: `.superpowers/sdd/readme-neutrality-source-publication.json`
- Test: inline Python semantic, source-binding, and Markdown-link probes

**Interfaces:**
- Consumes: `PUBLIC_SOURCE_COMMIT` and remote blob evidence from Task 2.
- Produces: a Chinese README and translation index that both record the exact
  public source commit and have matching neutral semantics.

- [ ] **Step 1: Validate the Task 2 handoff**

Run:

```powershell
@'
from pathlib import Path
import json
import re

path = Path(".superpowers/sdd/readme-neutrality-source-publication.json")
report = json.loads(path.read_text(encoding="utf-8"))
assert report["repository"] == "ApacheWang/open-np-hard-research"
assert report["branch"] == "main"
assert report["path"] == "README.md"
assert re.fullmatch(r"[0-9a-f]{40}", report["remote_commit_sha"])
assert report["remote_blob_sha"] == report["local_blob_sha"]
assert report["verified_equal"] is True
print("PUBLIC_SOURCE_COMMIT=" + report["remote_commit_sha"])
'@ | python -
```

Expected: exactly one `PUBLIC_SOURCE_COMMIT=` line followed by a 40-hex SHA.

- [ ] **Step 2: Run the translation neutrality contract before editing**

Run:

```powershell
@'
from pathlib import Path
import json

zh = Path("README.zh-CN.md").read_text(encoding="utf-8")
translations = Path("translations/README.md").read_text(encoding="utf-8")
report = json.loads(
    Path(".superpowers/sdd/readme-neutrality-source-publication.json")
    .read_text(encoding="utf-8")
)
source_commit = report["remote_commit_sha"]

forbidden = (
    "中国数学家",
    "中文数学社区为世界数学发展作出了卓越贡献",
    "来自中国及",
    "全球化",
    "严谨",
    "可信",
    "专属协作团队",
    "英语是规范技术语言",
    "English is the canonical technical language",
    "canonical English source",
)
combined = zh + "\n" + translations
required = (
    "项目面向所有贡献者开放",
    "不因所在地、使用语言、所属机构、个人背景或经验水平而改变",
    "按实际角色记录并致谢",
    "针对该成果公开记录的协作团队",
    "recorded source document",
    "exact source commit",
    "not from the source language",
    source_commit,
)
failures = [f"forbidden remains: {item}" for item in forbidden if item in combined]
failures += [f"required missing: {item}" for item in required if item not in combined]
if failures:
    raise AssertionError("\n".join(failures))
print("PASS: translation neutrality and source binding")
'@ | python -
```

Expected: nonzero exit with forbidden-phrase and missing-required-phrase
diagnostics.

- [ ] **Step 3: Replace the Chinese source notice and introduction**

Read the actual `PUBLIC_SOURCE_COMMIT` from Step 1. Use `apply_patch` and write
the actual 40-hex SHA—not the interface name—into both the Markdown link target
and visible commit text.

The top of `README.zh-CN.md` after navigation must carry this meaning and
structure:

```markdown
> 本页为简体中文译文。记录的源文档为 [README.md](README.md)，源版本为公开
> `main` 上的准确提交，并链接到该提交。若译文与记录的源版本不同，以该源版本
> 作为核对基准；翻译问题通过公开、可审查的变更修正。

本项目围绕 NP-困难问题开展公开协作。工作通过明确的定义、可复现实验、可审查
的主张和有记录的责任分工进行组织。

项目面向所有贡献者开放；参与、审查与成果署名不因所在地、使用语言、所属机构、
个人背景或经验水平而改变。贡献依据其有记录的内容与证据接受评估。
```

The source-version sentence must contain a Markdown link to:

```text
https://github.com/ApacheWang/open-np-hard-research/commit/{actual 40-hex PUBLIC_SOURCE_COMMIT}
```

The literal braces and interface name must not appear in the tracked file.

- [ ] **Step 4: Replace Chinese evaluative and exclusionary wording**

Use `apply_patch` so the first 3-SAT sentence reads:

```markdown
我们的首个研究方向是建立有文档记录、可审查且可复现的 3-SAT 基线：精确定义、
参考求解器、小实例检查、文献梳理及可审查的假设。
```

In the credit section:

- replace `专属协作团队` with `针对该成果公开记录的协作团队`; and
- add `上述贡献均按实际角色记录并致谢。`

Keep the substantive mathematical contribution and responsibility criteria.

- [ ] **Step 5: Replace the Chinese language section**

Use `apply_patch` so `## 语言与翻译` reads:

```markdown
## 语言与翻译

每份译文都记录源文档和准确的源提交。译文不同步时，以该记录的源版本作为核对
基准；源文档所用语言不影响参与、审查或成果署名。现有译文及同步状态见
[翻译索引](translations/README.md)。
```

- [ ] **Step 6: Rewrite the translation protocol**

Use `apply_patch` to replace `translations/README.md` with a protocol containing
these exact normative statements:

```markdown
# Translations

Translations provide access to versioned project documents. Each translation
is bound to a recorded source document and exact source commit. When content
differs, authority comes from that explicit source-version record, not from the
source language.
```

Required metadata must include:

- language and locale;
- translated document path;
- recorded source document path;
- exact source commit;
- translation contributor record and current maintainer;
- translation date;
- known omissions or terminology choices; and
- synchronization status.

Add a `## Current Translations` entry for Simplified Chinese (`zh-CN`) with:

- translation path `README.zh-CN.md`;
- source path `README.md`;
- the actual `PUBLIC_SOURCE_COMMIT`;
- contributor record `Git history for README.zh-CN.md`;
- current maintainer `ApacheWang`;
- translation date `2026-07-23`;
- known omissions `none`; and
- synchronization status `current`.

The synchronization section must require public review, retain both versions
while a mismatch is investigated, mark stale translations `needs-sync`, fix a
wrong source first, and then synchronize translations.

Retain this contribution rule in substance:

```markdown
Translation, terminology review, and maintenance are recorded and acknowledged
under their actual roles. They do not automatically confer result-specific
solver or theorem-author credit unless the contributor also meets the
mathematical contribution and responsibility requirements in
[GOVERNANCE.md](../GOVERNANCE.md).
```

- [ ] **Step 7: Re-run the translation contract**

Run the exact command from Step 2.

Expected: `PASS: translation neutrality and source binding`.

- [ ] **Step 8: Validate parity, links, disclaimers, and placeholders**

Run:

```powershell
@'
from pathlib import Path
import json
import re
from urllib.parse import unquote

report = json.loads(
    Path(".superpowers/sdd/readme-neutrality-source-publication.json")
    .read_text(encoding="utf-8")
)
source_commit = report["remote_commit_sha"]
zh = Path("README.zh-CN.md").read_text(encoding="utf-8")
translations = Path("translations/README.md").read_text(encoding="utf-8")

assert source_commit in zh
assert source_commit in translations
assert "本项目尚未解决 P versus NP 问题。" in zh
assert "有限实验仅是关于已测试实例的证据" in zh
assert "研究主张级别" in zh
assert "数学成果署名" in zh
assert "PUBLIC_SOURCE_COMMIT" not in zh + translations
assert "{actual 40-hex" not in zh + translations

for name in ("README.zh-CN.md", "translations/README.md"):
    path = Path(name)
    text = path.read_text(encoding="utf-8")
    for raw in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = raw.strip()
        if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I) or target.startswith("#"):
            continue
        target = unquote(target.split("#", 1)[0].strip("<>"))
        if target:
            assert (path.parent / target).exists(), (name, target)
print("PASS: translation parity, disclaimers, links, and concrete source SHA")
'@ | python -
python -m pytest -q
git diff --check
```

Expected:

```text
PASS: translation parity, disclaimers, links, and concrete source SHA
...........                                                              [100%]
```

`git diff --check` produces no output.

- [ ] **Step 9: Commit the translation documents**

Run:

```powershell
git add -- README.zh-CN.md translations/README.md
git diff --cached --check
git diff --cached --name-only
git commit -m "docs: neutralize translation language"
```

Expected staged paths:

```text
README.zh-CN.md
translations/README.md
```

---

### Task 4: Final Review, Publication, and Parity

**Files:**
- Read/verify: `README.md`
- Read/verify: `README.zh-CN.md`
- Read/verify: `translations/README.md`
- Publish: `docs/superpowers/specs/2026-07-23-readme-neutrality-design.md`
- Publish: `docs/superpowers/plans/2026-07-23-readme-neutrality.md`
- Create: `.superpowers/sdd/readme-neutrality-final-report.md`

**Interfaces:**
- Consumes: all reviewed local commits and Task 2 source-publication report.
- Produces: exact public/local parity for all five changed public files and a
  final review report.

- [ ] **Step 1: Run the combined neutrality gate**

Run:

```powershell
@'
from pathlib import Path
import json

en = Path("README.md").read_text(encoding="utf-8")
zh = Path("README.zh-CN.md").read_text(encoding="utf-8")
tr = Path("translations/README.md").read_text(encoding="utf-8")
report = json.loads(
    Path(".superpowers/sdd/readme-neutrality-source-publication.json")
    .read_text(encoding="utf-8")
)
source_commit = report["remote_commit_sha"]
combined = en + "\n" + zh + "\n" + tr

forbidden = (
    "Chinese mathematicians",
    "outstanding contributions",
    "China and every part of the world",
    "中国数学家",
    "卓越贡献",
    "来自中国及",
    "An open, worldwide, rigorous",
    "trusted, reproducible 3-SAT baseline",
    "全球化",
    "可信",
    "专属协作团队",
    "English is the canonical technical language",
    "英语是规范技术语言",
    "canonical English source",
    "PUBLIC_SOURCE_COMMIT",
)
found = [item for item in forbidden if item in combined]
assert not found, found

required = (
    "A public collaboration for research on NP-hard problems.",
    "Participation is open to contributors regardless of location, language,",
    "recorded under their actual roles",
    "项目面向所有贡献者开放",
    "不因所在地、使用语言、所属机构、个人背景或经验水平而改变",
    "按实际角色记录并致谢",
    "针对该成果公开记录的协作团队",
    "recorded source document and exact source commit",
    "not from the source language",
    source_commit,
)
missing = [item for item in required if item not in combined]
assert not missing, missing
print("PASS: combined README neutrality gate")
'@ | python -
```

Expected: `PASS: combined README neutrality gate`.

- [ ] **Step 2: Run repository verification**

Run:

```powershell
python -m pytest -q
git diff --check main..HEAD
git status --short --branch
git log --oneline --decorate main..HEAD
```

Expected: 11 tests pass; no whitespace errors; clean
`readme-neutrality` branch; only the planned design, plan, and README commits
appear after `main`.

- [ ] **Step 3: Verify source publication is still exact**

Fetch public `README.md` from `main` through the GitHub app. Confirm:

```powershell
git rev-parse HEAD:README.md
```

equals the public content blob SHA and the public commit containing that
version equals the `remote_commit_sha` in the Task 2 report.

- [ ] **Step 4: Publish the translation protocol**

Fetch the current public `translations/README.md` blob SHA, then update it
sequentially with:

```text
message: docs: neutralize translation language
branch: main
content: complete local UTF-8 translations/README.md
```

Expected: success with a new remote commit SHA and blob SHA equal to:

```powershell
git rev-parse HEAD:translations/README.md
```

- [ ] **Step 5: Publish the Chinese README**

After Step 4 succeeds, fetch the current public `README.zh-CN.md` blob SHA and
update it with:

```text
message: docs: neutralize translation language
branch: main
content: complete local UTF-8 README.zh-CN.md
```

Expected: success with a new remote commit SHA and blob SHA equal to:

```powershell
git rev-parse HEAD:README.zh-CN.md
```

- [ ] **Step 6: Publish the design and plan**

For each path below, fetch it first. If GitHub returns not found, create it; if
it already exists, update it with the freshly fetched blob SHA:

```text
docs/superpowers/specs/2026-07-23-readme-neutrality-design.md
docs/superpowers/plans/2026-07-23-readme-neutrality.md
```

Use these commit messages respectively:

```text
docs: design neutral README language
docs: plan neutral README implementation
```

Perform the two writes sequentially.

- [ ] **Step 7: Verify all public blobs**

Fetch all five paths freshly from public `main`:

```text
README.md
README.zh-CN.md
translations/README.md
docs/superpowers/specs/2026-07-23-readme-neutrality-design.md
docs/superpowers/plans/2026-07-23-readme-neutrality.md
```

For every path, compare the returned blob SHA with:

```powershell
git rev-parse "HEAD:<path>"
```

Expected: `5/5 public blobs match local HEAD`.

- [ ] **Step 8: Write the ignored final report**

Use `apply_patch` to create
`.superpowers/sdd/readme-neutrality-final-report.md` containing:

- local commit SHAs and subjects;
- exact commands and outputs for neutrality, links, tests, and whitespace;
- `PUBLIC_SOURCE_COMMIT`;
- every remote update/create commit SHA and blob SHA;
- the five-path final parity table;
- final Git status; and
- any remaining concerns.

Do not commit the ignored report.

- [ ] **Step 9: Request final whole-branch review**

Generate a review package for `main..HEAD`. The reviewer must inspect the
actual three product files, design, plan, test evidence, source-commit binding,
and public parity. Critical and Important findings must be fixed and
re-reviewed before branch completion.

Expected final verdict: `Ready to merge? Yes`.
