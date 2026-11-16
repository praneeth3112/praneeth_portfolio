"""Portfolio repository validator, metadata exporter, and language analyzer."""

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from typing import Dict, List, Tuple

from portfolio_data import PROJECTS, export_portfolio_dict

ROOT_DIR = Path(__file__).resolve().parent
IGNORED_DIRS = {".git", "node_modules", "dist", "__pycache__", ".venv", "venv"}

LANGUAGE_EXTENSIONS: Dict[str, str] = {
    ".py": "Python",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".html": "HTML",
    ".htm": "HTML",
    ".css": "CSS",
}


class MetaTitleParser(HTMLParser):
    """Extracts <title> and <meta> tags from an HTML document."""

    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self._in_title = False
        self.meta_tags: Dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str | None]]) -> None:
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            attr_map = {k: v for k, v in attrs if v is not None}
            key = attr_map.get("name") or attr_map.get("property")
            if key and "content" in attr_map:
                self.meta_tags[key] = attr_map["content"]

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title += data.strip()


def compute_language_bytes(directory: Path = ROOT_DIR) -> Dict[str, int]:
    """Compute byte totals per language matching GitHub Linguist conventions."""
    totals: Dict[str, int] = {}
    for file_path in directory.rglob("*"):
        if not file_path.is_file():
            continue
        if any(part in IGNORED_DIRS for part in file_path.parts):
            continue
        language = LANGUAGE_EXTENSIONS.get(file_path.suffix.lower())
        if language:
            totals[language] = totals.get(language, 0) + file_path.stat().st_size
    return dict(sorted(totals.items(), key=lambda item: item[1], reverse=True))


def compute_language_percentages(directory: Path = ROOT_DIR) -> Dict[str, float]:
    """Return rounded language percentages across tracked code files."""
    totals = compute_language_bytes(directory)
    grand_total = sum(totals.values())
    if grand_total == 0:
        return {}
    return {lang: round((size / grand_total) * 100, 1) for lang, size in totals.items()}


def validate_index_html(html_path: Path = ROOT_DIR / "index.html") -> List[str]:
    """Verify index.html contains title and description metadata."""
    issues: List[str] = []
    if not html_path.exists():
        return [f"Missing {html_path.name}"]

    parser = MetaTitleParser()
    parser.feed(html_path.read_text(encoding="utf-8"))
    if not parser.title:
        issues.append("HTML <title> is empty")
    if "description" not in parser.meta_tags:
        issues.append("Missing <meta name='description'>")
    return issues


def validate_projects() -> List[str]:
    """Verify all portfolio projects have valid HTTPS links and summaries."""
    issues: List[str] = []
    for project in PROJECTS:
        if not project.live_url.startswith("https://"):
            issues.append(f"{project.slug}: invalid live_url")
        if not project.source_url.startswith("https://"):
            issues.append(f"{project.slug}: invalid source_url")
        if not project.summary:
            issues.append(f"{project.slug}: missing summary")
    return issues


def export_metadata(output_path: Path = ROOT_DIR / "portfolio.json") -> Path:
    """Write structured portfolio JSON to disk."""
    payload = export_portfolio_dict()
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate portfolio and inspect language breakdown.")
    parser.add_argument("--export", action="store_true", help="Write portfolio.json snapshot")
    args = parser.parse_args()

    html_issues = validate_index_html()
    project_issues = validate_projects()
    all_issues = html_issues + project_issues

    percentages = compute_language_percentages()
    byte_counts = compute_language_bytes()
    print("Repository Language Breakdown:")
    for lang, pct in percentages.items():
        print(f"  {lang:<12} {pct:5.1f}% ({byte_counts[lang]} bytes)")

    if all_issues:
        raise SystemExit("Validation failed:\n- " + "\n- ".join(all_issues))

    if args.export:
        out = export_metadata()
        print(f"Exported metadata to {out.name}")


if __name__ == "__main__":
    main()
