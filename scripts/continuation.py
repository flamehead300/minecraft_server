"""Print a portable, current continuation prompt; reads no runtime/player files."""
from pathlib import Path
import subprocess

root = Path(__file__).resolve().parents[1]
def git(*args):
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()

print("Continue minecraft-crossplay-server.")
print("Branch:", git("branch", "--show-current"))
print("Commit:", git("rev-parse", "HEAD"))
print("Working tree:", "dirty; inspect and preserve changes" if git("status", "--porcelain") else "clean")
print("Read AGENTS.md if present and docs/HANDOFF.md before acting.\n")
print((root / "docs/HANDOFF.md").read_text(encoding="utf-8"))
