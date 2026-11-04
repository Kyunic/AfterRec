"""Cheap structural check, including availability of the offline demonstration."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "README.md",
    "README.zh-CN.md",
    "docs/architecture/OVERVIEW.md",
    "docs/contracts/INTERFACES.md",
    "docs/research/SIMULATION_PROTOCOL.md",
    "docs/team/OWNERSHIP.md",
    "frontend/index.html",
    "backend/src/recforgetbench/api/main.py",
    ".github/workflows/ci.yml",
]


def main() -> None:
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).is_file()]
    if missing:
        raise SystemExit(f"Missing scaffold files: {missing}")
    prototype = (ROOT / "frontend/index.html").read_text(encoding="utf-8")
    assert "<html" in prototype and "PROTOTYPE" in prototype
    print(f"Scaffold OK: {len(REQUIRED_FILES)} required files found")


if __name__ == "__main__":
    main()
