import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone


REPO = "GiribaldiTTV/Nexus-Desktop-AI"
PREBETA_TAG_RE = re.compile(r"^v(\d+)\.(\d+)\.(\d+)-prebeta$")


@dataclass(frozen=True)
class ReleaseCheck:
    tag_name: str
    name: str
    url: str
    published_at: str
    failures: tuple[str, ...]


def _run_gh_json(args: tuple[str, ...]) -> object:
    completed = subprocess.run(
        ("gh", *args),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip())
    return json.loads(completed.stdout)


def _prebeta_version(tag_name: str) -> tuple[int, int, int] | None:
    match = PREBETA_TAG_RE.fullmatch(tag_name)
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


def _expected_title(tag_name: str) -> str:
    version = _prebeta_version(tag_name)
    if version is None:
        return ""
    major, minor, patch = version
    return f"Pre-Beta v{major}.{minor}.{patch}"


def _release_body_failures(tag_name: str, name: str, body: str) -> tuple[str, ...]:
    failures: list[str] = []
    stripped_body = body.strip()
    expected_title = _expected_title(tag_name)
    if expected_title and name.strip() != expected_title:
        failures.append(f"title should be {expected_title!r}, found {name.strip()!r}")
    if stripped_body.startswith("# "):
        failures.append("body must not start with a top-level release-title heading")
    if "## Release Summary" not in body and "## Release Overview" not in body:
        failures.append("body is missing ## Release Summary or ## Release Overview")
    whats_changed_index = body.find("## What's Changed")
    if whats_changed_index == -1:
        failures.append("body is missing ## What's Changed")
    else:
        heading_matches = re.findall(r"^##\s+(.+)$", body[:whats_changed_index], flags=re.M)
        rich_headings = {
            heading.strip()
            for heading in heading_matches
            if heading.strip() not in {"Release Summary", "Release Overview"}
        }
        if not rich_headings:
            failures.append("body is missing a detailed user-facing section before ## What's Changed")
    if "**Full Changelog**:" not in body:
        failures.append("body is missing **Full Changelog**:")
    return tuple(failures)


def _published_sort_key(release: dict[str, object]) -> datetime:
    published_at = str(release.get("published_at") or "")
    if not published_at:
        return datetime.min.replace(tzinfo=timezone.utc)
    normalized = published_at.replace("Z", "+00:00")
    try:
        return datetime.fromisoformat(normalized)
    except ValueError:
        return datetime.min.replace(tzinfo=timezone.utc)


def _load_prebeta_releases() -> list[dict[str, object]]:
    releases = _run_gh_json(("api", f"repos/{REPO}/releases?per_page=100"))
    if not isinstance(releases, list):
        raise RuntimeError("GitHub release API returned an unexpected payload")
    prebeta_releases = [
        release
        for release in releases
        if _prebeta_version(str(release.get("tag_name") or "")) is not None
        and not bool(release.get("draft"))
    ]
    return sorted(prebeta_releases, key=_published_sort_key, reverse=True)


def _check_release(release: dict[str, object]) -> ReleaseCheck:
    tag_name = str(release.get("tag_name") or "")
    name = str(release.get("name") or "")
    body = str(release.get("body") or "")
    url = str(release.get("html_url") or "")
    published_at = str(release.get("published_at") or "")
    return ReleaseCheck(
        tag_name=tag_name,
        name=name,
        url=url,
        published_at=published_at,
        failures=_release_body_failures(tag_name, name, body),
    )


def main() -> int:
    try:
        checks = [_check_release(release) for release in _load_prebeta_releases()[:11]]
    except Exception as exc:
        print(f"FAIL: unable to inspect GitHub releases: {exc}", file=sys.stderr)
        return 1

    if not checks:
        print("FAIL: no pre-Beta GitHub releases were found", file=sys.stderr)
        return 1

    latest = checks[0]
    print(f"Latest pre-Beta release: {latest.tag_name} ({latest.name})")
    if latest.failures:
        print("FAIL: latest release body does not match the standard:")
        for failure in latest.failures:
            print(f"- {failure}")
        return 1

    print("PASS: latest release body matches the standard.")
    historical_drifts = [check for check in checks[1:] if check.failures]
    if historical_drifts:
        print("Historical release-body drift found in previous 10 releases:")
        for check in historical_drifts:
            print(f"- {check.tag_name}: {'; '.join(check.failures)}")
    else:
        print("Previous 10 releases match the release-body standard.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
