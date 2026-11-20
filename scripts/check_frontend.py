"""Validate static HTML prototype and JavaScript syntax (if Node is installed)."""

from html.parser import HTMLParser
from pathlib import Path
import shutil
import subprocess
import tempfile


class InlineScripts(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.capturing = False
        self.blocks: list[str] = []
        self.current: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "script" and "src" not in dict(attrs):
            self.capturing = True
            self.current = []

    def handle_data(self, data: str) -> None:
        if self.capturing:
            self.current.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.capturing:
            self.blocks.append("".join(self.current))
            self.capturing = False


def main() -> None:
    source = Path(__file__).resolve().parents[1] / "frontend" / "index.html"
    html = source.read_text(encoding="utf-8")
    if "</html>" not in html or "<title>AfterRec" not in html:
        raise SystemExit("Missing complete HTML document or project name")
    if "模拟" not in html and "演示" not in html:
        raise SystemExit("The offline demo requires a visible synthetic-data disclaimer")
    scripts = InlineScripts()
    scripts.feed(html)
    if not scripts.blocks:
        raise SystemExit("Expected an interactive offline prototype with embedded JavaScript")
    node = shutil.which("node")
    if not node:
        print("HTML found; Node is unavailable, skipped JS syntax check")
        return
    with tempfile.TemporaryDirectory() as directory:
        for index, code in enumerate(scripts.blocks):
            file = Path(directory) / f"inline-{index}.js"
            file.write_text(code, encoding="utf-8")
            subprocess.run([node, "--check", str(file)], check=True)
    print(f"Prototype OK: {len(scripts.blocks)} JavaScript block(s) parsed")


if __name__ == "__main__":
    main()
