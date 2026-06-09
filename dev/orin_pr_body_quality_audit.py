"""Audit and normalize GitHub pull request body quality.

The helper keeps the governed human-review PR body shape while keeping
operator proof, PR posture, and defensive scope language out of GitHub
PR bodies.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory


TOP_LEVEL_SECTION_RE = re.compile(r"(?m)^## ([^\n#].*?)\s*$")
CANONICAL_SECTION_ORDER = ["Summary", "What Changed"]
CANONICAL_SECTIONS = set(CANONICAL_SECTION_ORDER)

CHANGE_SECTION_ALIASES = {
    "branch evidence",
    "changes",
    "context",
    "details",
    "implementation",
    "source truth",
    "what changed",
}

FLATTENED_CHANGE_SECTION_ALIASES = {
    "branch evidence",
}

REMOVED_SECTION_ALIASES = {
    "checks",
    "codex review",
    "deferred",
    "does not include",
    "exclusions",
    "future gated",
    "not included",
    "pr posture",
    "proof",
    "proofs",
    "qa",
    "review posture",
    "status",
    "test plan",
    "testing",
    "tests",
    "validation",
    "verification",
}

PHASE_DIGEST_MARKERS = {
    "Next Legal Phase",
    "Next Safe Move",
    "Continue Decision",
    "Stop Basis",
}

PR_BODY_FIREWALL_MARKERS = PHASE_DIGEST_MARKERS | {
    "Exact next USER decision",
    "Implemented, validated",
    "PR posture",
    "::git-",
}

FORBIDDEN_COPY_PATTERNS = (
    re.compile(r"\bdoes\s+not\s+include\b", flags=re.I),
    re.compile(r"\bnot\s+included\b", flags=re.I),
    re.compile(r"\bnot\s+include\b", flags=re.I),
    re.compile(r"\bnon[-\s]?includes?\b", flags=re.I),
    re.compile(r"\bdeferred\b", flags=re.I),
    re.compile(r"\bfuture[-\s]?gated\b", flags=re.I),
    re.compile(r"\bpr\s+posture\b", flags=re.I),
)

FORBIDDEN_HEADING_PATTERNS = (
    re.compile(r"(?m)^#{2,6}\s+branch\s+evidence\b", flags=re.I),
    re.compile(r"(?m)^#{2,6}\s+checks?\b", flags=re.I),
    re.compile(r"(?m)^#{2,6}\s+pr\s+posture\b", flags=re.I),
    re.compile(r"(?m)^#{2,6}\s+testing\b", flags=re.I),
    re.compile(r"(?m)^#{2,6}\s+validation\b", flags=re.I),
)


@dataclass
class PullRequest:
    number: int
    title: str
    state: str
    is_draft: bool
    head_ref_name: str
    base_ref_name: str
    head_ref_oid: str
    body: str
    url: str


@dataclass
class NormalizedBody:
    body: str
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def run_gh(args: list[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["gh", *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if check and result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "gh command failed")
    return result


def fetch_pull_requests(repo: str, limit: int) -> list[PullRequest]:
    fields = ",".join(
        (
            "number",
            "title",
            "state",
            "isDraft",
            "headRefName",
            "baseRefName",
            "headRefOid",
            "body",
            "url",
        )
    )
    result = run_gh(
        [
            "pr",
            "list",
            "--repo",
            repo,
            "--state",
            "all",
            "--limit",
            str(limit),
            "--json",
            fields,
        ]
    )
    payload = json.loads(result.stdout)
    prs: list[PullRequest] = []
    for item in payload:
        prs.append(
            PullRequest(
                number=int(item["number"]),
                title=str(item.get("title") or ""),
                state=str(item.get("state") or ""),
                is_draft=bool(item.get("isDraft")),
                head_ref_name=str(item.get("headRefName") or ""),
                base_ref_name=str(item.get("baseRefName") or ""),
                head_ref_oid=str(item.get("headRefOid") or ""),
                body=str(item.get("body") or ""),
                url=str(item.get("url") or ""),
            )
        )
    return sorted(prs, key=lambda pr: pr.number, reverse=True)


def strip_bom(text: str) -> str:
    return text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def collapse_blank_lines(text: str) -> str:
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def tidy_markdown(text: str) -> str:
    text = collapse_blank_lines(text)
    text = re.sub(r"\n(?=###\s+)", "\n\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def normalized_text(text: str) -> str:
    lowered = text.casefold()
    lowered = re.sub(r"`([^`]+)`", r"\1", lowered)
    lowered = re.sub(r"[^a-z0-9#]+", " ", lowered)
    return " ".join(lowered.split())


def section_alias(title: str) -> str:
    alias = title.strip().casefold()
    alias = re.sub(r"[^a-z0-9]+", " ", alias)
    return " ".join(alias.split())


def split_top_level_sections(body: str) -> tuple[dict[str, str], str]:
    text = strip_bom(body)
    matches = list(TOP_LEVEL_SECTION_RE.finditer(text))
    if not matches:
        return {}, collapse_blank_lines(text)
    sections: dict[str, str] = {}
    preface = text[: matches[0].start()].strip()
    for index, match in enumerate(matches):
        title = match.group(1).strip()
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[title] = text[start:end].strip()
    return sections, preface


def first_paragraph(text: str) -> str:
    cleaned = collapse_blank_lines(text)
    if not cleaned:
        return ""
    for part in re.split(r"\n\s*\n", cleaned):
        candidate = part.strip()
        if candidate and not candidate.startswith("#"):
            return candidate
    return ""


def default_summary(pr: PullRequest) -> str:
    title = pr.title.strip().rstrip(".")
    if not title:
        return f"Updates PR #{pr.number}."
    if title.casefold() == "update readme.md":
        return "Updates `README.md`."
    if title.casefold() == "create readme.md":
        return "Creates `README.md`."
    if title.casefold() == "fix: readme":
        return "Refines `README.md` content and formatting."
    return f"Updates {title}."


def demoted_section(title: str, content: str) -> str:
    safe_title = title.strip() or "Details"
    return f"### {safe_title}\n\n{content.strip()}"


def is_removed_section(title: str) -> bool:
    alias = section_alias(title)
    if alias in REMOVED_SECTION_ALIASES:
        return True
    return any(token in alias for token in ("validation", "posture", "test", "check", "deferred"))


def is_flattened_change_section(title: str) -> bool:
    return section_alias(title) in FLATTENED_CHANGE_SECTION_ALIASES


def has_forbidden_copy(text: str) -> bool:
    return any(pattern.search(text) for pattern in FORBIDDEN_COPY_PATTERNS)


def normalize_summary(pr: PullRequest, raw_summary: str) -> tuple[str, str, list[str]]:
    reasons: list[str] = []
    preserved_detail: list[str] = []
    summary = collapse_blank_lines(raw_summary)
    if not summary:
        summary = default_summary(pr)
        reasons.append("filled missing summary")

    paragraph = first_paragraph(summary)
    if paragraph.startswith("- "):
        bullet_lines = [line.strip()[2:].strip() for line in paragraph.splitlines() if line.strip().startswith("- ")]
        if bullet_lines:
            paragraph = bullet_lines[0].rstrip(".") + "."
            if len(bullet_lines) > 1:
                preserved_detail.extend(f"- {line}" for line in bullet_lines[1:])
                reasons.append("moved summary bullet detail into What Changed")

    if paragraph and paragraph != summary:
        trailing = summary[len(paragraph) :].strip()
        if trailing:
            preserved_detail.append(trailing)
            reasons.append("moved summary detail into What Changed")
        summary = paragraph

    if normalized_text(summary) == normalized_text(f"This PR records {pr.title}."):
        improved = default_summary(pr)
        if improved != summary:
            summary = improved
            reasons.append("tightened generic summary")

    if len(summary) > 700:
        sentences = re.split(r"(?<=[.!?])\s+", summary)
        if len(sentences) > 1:
            shortened = sentences[0].strip()
            trailing = summary[len(shortened) :].strip()
            if trailing:
                preserved_detail.append(trailing)
                reasons.append("moved overlong summary detail into What Changed")
            summary = shortened
            reasons.append("shortened overlong summary")

    if has_forbidden_copy(summary):
        preserved_detail.append(summary)
        summary = default_summary(pr)
        if has_forbidden_copy(summary):
            summary = f"Updates PR #{pr.number}."
        reasons.append("replaced defensive or deferred summary wording")

    return summary.strip(), collapse_blank_lines("\n\n".join(preserved_detail)), reasons


def remove_duplicate_paragraphs(text: str) -> tuple[str, int]:
    parts = re.split(r"(\n\s*\n)", text)
    seen: set[str] = set()
    removed = 0
    output: list[str] = []
    for index in range(0, len(parts), 2):
        paragraph = parts[index].strip()
        separator = parts[index + 1] if index + 1 < len(parts) else ""
        if not paragraph:
            continue
        key = normalized_text(paragraph)
        is_plain_paragraph = (
            len(key) > 12
            and not paragraph.startswith(("-", "#", "`"))
            and "\n-" not in paragraph
        )
        if is_plain_paragraph and key in seen:
            removed += 1
            continue
        if is_plain_paragraph:
            seen.add(key)
        output.append(paragraph)
        if separator:
            output.append("\n\n")
    return collapse_blank_lines("".join(output)), removed


def remove_summary_duplication(changes: str, summary: str) -> tuple[str, list[str]]:
    reasons: list[str] = []
    summary_key = normalized_text(summary)
    text = collapse_blank_lines(changes)
    if not text:
        return text, reasons

    first = first_paragraph(text)
    if summary_key and normalized_text(first) == summary_key and text.lstrip().startswith(first):
        text = text[len(first) :].strip()
        reasons.append("removed repeated leading summary from What Changed")

    lines = text.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        heading_match = re.match(r"^###\s+(Summary|Purpose|Overview)\s*$", line.strip(), flags=re.I)
        if not heading_match:
            output.append(line)
            index += 1
            continue

        start = index + 1
        end = start
        while end < len(lines) and not lines[end].startswith("### "):
            end += 1
        chunk = "\n".join(lines[start:end]).strip()
        first_chunk_paragraph = first_paragraph(chunk)
        if first_chunk_paragraph and normalized_text(first_chunk_paragraph) == summary_key:
            chunk = chunk[len(first_chunk_paragraph) :].strip()
            reasons.append(f"removed duplicate nested {heading_match.group(1).lower()} paragraph")
        if chunk:
            replacement_heading = "### Context"
            output.append(replacement_heading)
            output.append("")
            output.extend(chunk.splitlines())
        else:
            reasons.append(f"removed empty nested {heading_match.group(1).lower()} section")
        index = end

    text = "\n".join(output)
    text = re.sub(r"(?m)^---+\s*$", "", text)
    text, removed_count = remove_duplicate_paragraphs(text)
    if removed_count:
        reasons.append(f"removed {removed_count} duplicate detail paragraph(s)")
    return tidy_markdown(text), reasons


def scrub_changes(changes: str) -> tuple[str, list[str]]:
    reasons: list[str] = []
    lines = changes.splitlines()
    output: list[str] = []
    skipping_removed_section = False
    skipped_heading = ""

    for line in lines:
        heading_match = re.match(r"^(#{3,6})\s+(.+?)\s*$", line)
        if heading_match:
            title = heading_match.group(2).strip()
            if is_flattened_change_section(title):
                skipping_removed_section = False
                skipped_heading = ""
                reasons.append(f"flattened legacy change heading '{title}'")
                continue
            elif is_removed_section(title):
                skipping_removed_section = True
                skipped_heading = title
                reasons.append(f"removed PR-body-only section '{title}'")
                continue
            skipping_removed_section = False
            skipped_heading = ""

        if skipping_removed_section:
            continue
        if has_forbidden_copy(line):
            reasons.append("removed defensive or deferred PR-body wording")
            continue
        output.append(line)

    if skipped_heading:
        reasons.append(f"removed trailing PR-body-only section '{skipped_heading}'")
    return tidy_markdown("\n".join(output)), sorted(set(reasons))


def remap_noncanonical_sections(sections: dict[str, str]) -> tuple[str, list[str]]:
    extra_changes: list[str] = []
    reasons: list[str] = []
    for title, content in sections.items():
        if title in CANONICAL_SECTIONS:
            continue
        body = collapse_blank_lines(content)
        if not body:
            continue
        alias = section_alias(title)
        if alias in FLATTENED_CHANGE_SECTION_ALIASES:
            extra_changes.append(body)
            reasons.append(f"flattened nonstandard change section '{title}'")
        elif alias in CHANGE_SECTION_ALIASES:
            extra_changes.append(demoted_section(title, body))
            reasons.append(f"preserved nonstandard change section '{title}'")
        elif is_removed_section(title):
            reasons.append(f"removed PR-body-only section '{title}'")
        else:
            extra_changes.append(demoted_section(title, body))
            reasons.append(f"preserved nonstandard detail section '{title}'")
    return collapse_blank_lines("\n\n".join(extra_changes)), reasons


def normalize_changes(
    pr: PullRequest,
    raw_changes: str,
    summary: str,
    preface: str,
) -> tuple[str, list[str], list[str]]:
    reasons: list[str] = []
    warnings: list[str] = []
    changes = collapse_blank_lines(raw_changes)
    if preface:
        changes = collapse_blank_lines(f"{preface}\n\n{changes}" if changes else preface)
        reasons.append("moved preface into What Changed")

    changes, dup_reasons = remove_summary_duplication(changes, summary)
    reasons.extend(dup_reasons)
    changes, scrub_reasons = scrub_changes(changes)
    reasons.extend(scrub_reasons)

    if not changes:
        changes = (
            "Historical metadata preserved for review context:\n"
            f"- Base: `{pr.base_ref_name or 'unknown'}`\n"
            f"- Head: `{pr.head_ref_name or 'unknown'}`"
        )
        reasons.append("filled missing What Changed with historical metadata")

    if re.search(r"(?m)^###\s+(Summary|Purpose)\s*$", changes):
        warnings.append("nested summary/purpose heading remains")
    for marker in PHASE_DIGEST_MARKERS:
        if marker in changes:
            warnings.append(f"phase-digest marker remains in What Changed: {marker}")
    return tidy_markdown(changes), sorted(set(reasons)), warnings


def pr_body_firewall_warnings(body: str) -> list[str]:
    warnings: list[str] = []
    sections, _ = split_top_level_sections(body)
    if list(sections.keys()) != CANONICAL_SECTION_ORDER:
        warnings.append("PR body must use exactly ## Summary and ## What Changed")
    for marker in sorted(PR_BODY_FIREWALL_MARKERS):
        if marker in body:
            warnings.append(f"PR body firewall marker remains: {marker}")
    for pattern in FORBIDDEN_COPY_PATTERNS:
        if pattern.search(body):
            warnings.append(f"PR body contains forbidden copy pattern: {pattern.pattern}")
    for pattern in FORBIDDEN_HEADING_PATTERNS:
        if pattern.search(body):
            warnings.append(f"PR body contains forbidden heading pattern: {pattern.pattern}")
    return warnings


def build_body(summary: str, changes: str) -> str:
    return f"## Summary\n\n{summary.strip()}\n\n## What Changed\n\n{changes.strip()}\n"


def normalize_body(pr: PullRequest) -> NormalizedBody:
    sections, preface = split_top_level_sections(pr.body)
    raw_summary = sections.get("Summary", "")
    raw_changes = sections.get("What Changed", "")
    if not sections:
        raw_changes = strip_bom(pr.body)

    extra_changes, remap_reasons = remap_noncanonical_sections(sections)
    if extra_changes:
        raw_changes = collapse_blank_lines(
            f"{raw_changes}\n\n{extra_changes}" if raw_changes else extra_changes
        )

    summary, summary_detail, summary_reasons = normalize_summary(pr, raw_summary)
    if summary_detail:
        summary_detail_section = demoted_section("Summary Detail", summary_detail)
        raw_changes = collapse_blank_lines(
            f"{summary_detail_section}\n\n{raw_changes}" if raw_changes else summary_detail_section
        )

    changes, change_reasons, change_warnings = normalize_changes(pr, raw_changes, summary, preface)
    body = build_body(summary, changes)
    reasons = summary_reasons + change_reasons + remap_reasons

    if list(sections.keys()) != CANONICAL_SECTION_ORDER:
        reasons.append("enforced two top-level sections")
    original = strip_bom(pr.body).strip()
    if body.strip() != original and not reasons:
        reasons.append("normalized whitespace")
    warnings = change_warnings + pr_body_firewall_warnings(body)
    return NormalizedBody(body=body, reasons=sorted(set(reasons)), warnings=warnings)


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def apply_body(repo: str, pr: PullRequest, body: str, temp_dir: Path) -> None:
    body_path = temp_dir / f"pr-{pr.number}-body.md"
    write_text(body_path, body)
    run_gh(
        [
            "pr",
            "edit",
            str(pr.number),
            "--repo",
            repo,
            "--body-file",
            str(body_path),
        ]
    )


def audit(
    *,
    repo: str,
    limit: int,
    apply: bool,
    backup_dir: Path,
    report_path: Path,
) -> int:
    prs = fetch_pull_requests(repo, limit)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_backup_dir = backup_dir / f"pr_body_quality_audit_{timestamp}"
    run_backup_dir.mkdir(parents=True, exist_ok=True)

    counters: Counter[str] = Counter()
    rows: list[dict[str, object]] = []
    changed: list[tuple[PullRequest, NormalizedBody]] = []

    for pr in prs:
        normalized = normalize_body(pr)
        original = strip_bom(pr.body).strip()
        is_changed = normalized.body.strip() != original
        counters["total"] += 1
        counters["changed" if is_changed else "unchanged"] += 1
        counters["warnings"] += len(normalized.warnings)
        for reason in normalized.reasons:
            counters[f"reason:{reason}"] += 1
        if is_changed:
            changed.append((pr, normalized))
            pr_dir = run_backup_dir / f"pr-{pr.number}"
            write_text(pr_dir / "before.md", strip_bom(pr.body))
            write_text(pr_dir / "after.md", normalized.body)
        rows.append(
            {
                "number": pr.number,
                "title": pr.title,
                "state": pr.state,
                "isDraft": pr.is_draft,
                "url": pr.url,
                "changed": is_changed,
                "reasons": normalized.reasons,
                "warnings": normalized.warnings,
            }
        )

    if apply and changed:
        with TemporaryDirectory() as tmp:
            temp_dir = Path(tmp)
            for pr, normalized in changed:
                apply_body(repo, pr, normalized.body, temp_dir)

    report = {
        "repo": repo,
        "timestampUtc": timestamp,
        "apply": apply,
        "backupDir": str(run_backup_dir),
        "counts": dict(counters),
        "pullRequests": rows,
    }
    write_text(report_path, json.dumps(report, indent=2, ensure_ascii=False))

    print(f"PR body quality audit: {counters['total']} PRs inspected")
    print(f"Changed: {counters['changed']} | Unchanged: {counters['unchanged']} | Warnings: {counters['warnings']}")
    print(f"Backup dir: {run_backup_dir}")
    print(f"Report: {report_path}")
    if apply:
        print(f"Applied updates: {len(changed)}")
    else:
        print("Dry run only; rerun with --apply to update GitHub PR bodies.")
    return 0 if counters["warnings"] == 0 else 1


def audit_body_file(
    *,
    body_file: Path,
    title: str,
    apply: bool,
    report_path: Path,
) -> int:
    body = body_file.read_text(encoding="utf-8")
    pr = PullRequest(
        number=0,
        title=title or body_file.stem,
        state="LOCAL",
        is_draft=False,
        head_ref_name="local-proposed-pr-body",
        base_ref_name="main",
        head_ref_oid="unknown",
        body=body,
        url=str(body_file),
    )
    normalized = normalize_body(pr)
    original = strip_bom(body).strip()
    is_changed = normalized.body.strip() != original
    if apply and is_changed:
        write_text(body_file, normalized.body)

    report = {
        "bodyFile": str(body_file),
        "title": pr.title,
        "apply": apply,
        "changed": is_changed,
        "warnings": normalized.warnings,
        "reasons": normalized.reasons,
    }
    write_text(report_path, json.dumps(report, indent=2, ensure_ascii=False))

    print(f"PR body file audit: {body_file}")
    print(f"Changed: {is_changed} | Warnings: {len(normalized.warnings)}")
    if normalized.reasons:
        print("Reasons:")
        for reason in normalized.reasons:
            print(f"- {reason}")
    if normalized.warnings:
        print("Warnings:")
        for warning in normalized.warnings:
            print(f"- {warning}")
    if apply and is_changed:
        print("Applied normalized body file.")
    elif is_changed:
        print("Dry run only; rerun with --apply before PR creation or replace the proposed PR body.")

    still_changed = is_changed and not apply
    return 1 if still_changed or normalized.warnings else 0


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="GiribaldiTTV/Nexus-Desktop-AI")
    parser.add_argument("--limit", type=int, default=500)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument(
        "--body-file",
        type=Path,
        help=(
            "Validate a proposed PR body file before PR creation. "
            "Without --apply, exits nonzero if normalization would change it."
        ),
    )
    parser.add_argument(
        "--body-title",
        default="",
        help="Title used for fallback summary metadata when --body-file is supplied.",
    )
    parser.add_argument(
        "--backup-dir",
        type=Path,
        default=Path.home() / "AppData" / "Local" / "Temp" / "ndai_pr_body_quality_audit",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=Path("dev/logs/pr_body_quality_audit_report.json"),
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.body_file:
        return audit_body_file(
            body_file=args.body_file,
            title=args.body_title,
            apply=args.apply,
            report_path=args.report,
        )
    return audit(
        repo=args.repo,
        limit=args.limit,
        apply=args.apply,
        backup_dir=args.backup_dir,
        report_path=args.report,
    )


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
