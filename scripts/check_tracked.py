"""Reject common secret/data files in tracked content, including force-added files."""
from pathlib import PurePosixPath
import re
import subprocess
import sys

files = subprocess.check_output(["git", "ls-files", "-z"]).decode().split("\0")
bad = []
for name in filter(None, files):
    p = PurePosixPath(name)
    if (p.suffix.lower() in {".jar", ".pem", ".key", ".mca", ".dat", ".db", ".zip", ".log", ".duckdb", ".wal"}
        or "plugins" in p.parts
        or p.name in {"ops.json", "whitelist.json", "usercache.json", "eula.txt"}
        or any(s in {"runtime", "private", "downloads", "dist", "backups", "defaults", "generated", "playerdata", "logs"} or s.startswith("world") for s in p.parts)
        or p.name.startswith(".env")):
        bad.append(name)
    else:
        from pathlib import Path
        text = Path(name).read_text(encoding="utf-8")
        if re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", text):
            bad.append(name)
if bad:
    sys.exit("Prohibited tracked content: " + ", ".join(bad))
print("Tracked file safety: PASS (heuristic, not a substitute for review)")
