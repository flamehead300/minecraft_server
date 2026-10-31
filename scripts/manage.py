#!/usr/bin/env python3
"""Offline-first release tools. Never start a server or accept an EULA.

Run on the operator's computer, not in a presumed hosting shell.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile
import urllib.parse
import urllib.request
import zipfile

import yaml

ROOT = Path(__file__).resolve().parents[1]
HOSTS = {"fill-data.papermc.io", "fill.papermc.io", "download.geysermc.org"}
DESTINATIONS = {"paper": "server.jar", "geyser": "plugins/Geyser-Spigot.jar",
                "floodgate": "plugins/floodgate-spigot.jar"}
CONFIGS = ["server.properties", "plugins/Geyser-Spigot/config.yml",
           "plugins/floodgate/config.yml"]


def require(ok, message):
    if not ok:
        raise ValueError(message)


def digest(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, obj):
    Path(path).write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def official_url(url):
    p = urllib.parse.urlsplit(url)
    require(p.scheme == "https" and p.hostname in HOSTS and not p.username
            and not p.password and p.port in (None, 443) and not p.fragment,
            "Artifact URL must use an approved official HTTPS host")
    require("latest" not in p.path.lower(), "Floating latest URLs are prohibited")


def lock_data(path=ROOT / "versions.lock.json"):
    lock = read_json(path)
    require(lock["schema_version"] == 1, "Unsupported lock schema")
    datetime.date.fromisoformat(lock["verified_on"])
    require(lock["java"]["major"] == 25 and lock["minecraft_java"] == "26.3",
            "Re-review compatibility policy for a Minecraft/Java major change")
    artifacts = lock["artifacts"]
    require(len(artifacts) == 3 and {a["id"] for a in artifacts} == set(DESTINATIONS),
            "Expected exactly Paper, Geyser and Floodgate")
    for a in artifacts:
        require(a["destination"] == DESTINATIONS[a["id"]], "Unexpected artifact destination")
        require(re.fullmatch(r"[0-9a-f]{64}", a["sha256"]), "Invalid SHA-256")
        require(isinstance(a["build"], int) and a["build"] > 0 and a["version"], "Missing version/build")
        official_url(a["url"])
        official_url(a["metadata_url"])
    return lock


def verify_jar(path, artifact):
    require(not Path(path).is_symlink(), "Symlink artifact rejected")
    require(digest(path) == artifact["sha256"], f"Checksum mismatch: {artifact['id']}")
    with zipfile.ZipFile(path) as z:
        require(z.testzip() is None, "Corrupt JAR")
        require("META-INF/MANIFEST.MF" in z.namelist(), "Not a valid Java artifact")
        if artifact["id"] != "paper":
            require("plugin.yml" in z.namelist(), "Missing Spigot plugin descriptor")


class OfficialRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        official_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def download(cache, lock):
    cache = Path(cache)
    cache.mkdir(parents=True, exist_ok=True)
    opener = urllib.request.build_opener(OfficialRedirect())
    for a in lock["artifacts"]:
        target = cache / (a["id"] + ".jar")
        if target.exists():
            verify_jar(target, a)  # Never silently replace a mismatched cache entry.
            continue
        fd, name = tempfile.mkstemp(prefix=".download-", dir=cache)
        os.close(fd)
        temp = Path(name)
        try:
            req = urllib.request.Request(a["url"], headers={"User-Agent": "minecraft-crossplay-server/1.0"})
            with opener.open(req, timeout=90) as response, temp.open("wb") as f:
                require(response.status == 200, "Expected HTTP 200")
                official_url(response.geturl())
                shutil.copyfileobj(response, f)
            verify_jar(temp, a)
            require(not target.exists(), "Destination appeared during download")
            temp.rename(target)
        finally:
            temp.unlink(missing_ok=True)


def fresh_dir(path):
    path = Path(path)
    require(not path.exists() and not path.is_symlink(), f"Refusing existing destination: {path}")
    path.mkdir(parents=True)
    return path


def inventory(root):
    root = Path(root)
    require(root.is_dir() and not root.is_symlink(), "Expected a real directory")
    result = {}
    for p in sorted(root.rglob("*")):
        require(not p.is_symlink(), f"Symlinks prohibited: {p}")
        if p.is_file():
            name = p.relative_to(root).as_posix()
            result[name] = {"sha256": digest(p), "bytes": p.stat().st_size}
        else:
            require(p.is_dir(), "Non-regular filesystem entry")
    return result


def package(cache, output, lock):
    for a in lock["artifacts"]:
        verify_jar(Path(cache) / (a["id"] + ".jar"), a)
    out = fresh_dir(output)
    for a in lock["artifacts"]:
        target = out / a["destination"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path(cache) / (a["id"] + ".jar"), target)
    write_json(out / "versions.lock.json", lock)
    write_json(out / "manifest.json", {"schema_version": 1, "files": inventory(out)})
    verify_package(out, lock)


def verify_package(path, lock):
    path = Path(path)
    actual = inventory(path)
    actual.pop("manifest.json", None)
    expected = set(DESTINATIONS.values()) | {"versions.lock.json"}
    require(set(actual) == expected, "Unexpected or missing deployment files; persistent data prohibited")
    require(read_json(path / "manifest.json")["files"] == actual, "Deployment manifest mismatch")
    require(read_json(path / "versions.lock.json") == lock, "Package lock differs from repository")
    for a in lock["artifacts"]:
        verify_jar(path / a["destination"], a)


def initial_install(package_path, target, lock):
    verify_package(package_path, lock)
    fresh_dir(target)
    shutil.copytree(package_path, target, dirs_exist_ok=True)


def properties_patch(text, changes):
    lines = text.splitlines(keepends=True)
    found = {}
    for i, line in enumerate(lines):
        if not line.strip() or line.lstrip().startswith(("#", "!")):
            continue
        match = re.match(r"^([a-zA-Z0-9_.-]+)=(.*?)(?:\r?\n)?$", line)
        require(match is not None, "Unsupported properties syntax; review manually")
        key = match[1]
        require(key not in found, "Duplicate property: " + key)
        found[key] = i
    require(set(changes) <= set(found), "Policy keys missing in generated server defaults")
    for key, value in changes.items():
        require("\n" not in value and "\r" not in value, "Multiline property rejected")
        lines[found[key]] = f"{key}={value}\n"
    return "".join(lines)


def yaml_nodes(text):
    node = yaml.compose(text)
    require(isinstance(node, yaml.MappingNode), "Expected YAML mapping")
    paths, seen = {}, set()

    def visit(n, prefix=""):
        require(id(n) not in seen, "YAML aliases not permitted in configuration input")
        seen.add(id(n))
        if isinstance(n, yaml.MappingNode):
            keys = set()
            for k, v in n.value:
                require(isinstance(k, yaml.ScalarNode) and k.value not in keys, "Duplicate/non-scalar YAML key")
                keys.add(k.value)
                visit(v, (prefix + "." if prefix else "") + k.value)
        elif isinstance(n, yaml.ScalarNode):
            paths[prefix] = n
        elif isinstance(n, yaml.SequenceNode):
            for i, v in enumerate(n.value):
                visit(v, prefix + f"[{i}]")
    visit(node)
    return paths


def yaml_patch(text, changes):
    nodes = yaml_nodes(text)
    require(set(changes) <= set(nodes), "Policy keys missing in generated Geyser defaults")
    edits = []
    for key, value in changes.items():
        node = nodes[key]
        replacement = json.dumps(value)  # JSON scalars are valid YAML, including false.
        edits.append((node.start_mark.index, node.end_mark.index, replacement))
    for start, end, value in sorted(edits, reverse=True):
        text = text[:start] + value + text[end:]
    yaml_nodes(text)
    return text


def capture(server, output, lock):
    """Capture only configs from a clean, stopped first boot of pinned software."""
    server = Path(server)
    for a in lock["artifacts"]:
        verify_jar(server / a["destination"], a)
    for name in CONFIGS:
        require((server / name).is_file() and not (server / name).is_symlink(), "Missing generated configuration: " + name)
    out = fresh_dir(output)
    for name in CONFIGS:
        dest = out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(server / name, dest)
    write_json(out / "provenance.json", {"lock_sha256": digest(ROOT / "versions.lock.json"),
               "files": inventory(out), "origin": "Operator-supplied stopped first boot; review logs separately"})


def render(defaults, output, java_port, bedrock_port, lock):
    require(1 <= java_port <= 65535 and 1 <= bedrock_port <= 65535, "Invalid port")
    require(java_port != bedrock_port, "NetherNet TCP port must differ from Java TCP port")
    defaults = Path(defaults)
    provenance = read_json(defaults / "provenance.json")
    require(provenance["lock_sha256"] == digest(ROOT / "versions.lock.json"), "Defaults belong to another release")
    actual = inventory(defaults)
    actual.pop("provenance.json", None)
    require(actual == provenance["files"] and set(actual) == set(CONFIGS), "Default provenance mismatch")
    policy = read_json(ROOT / "config/policy.json")
    props = dict(policy["server.properties"], **{"server-port": str(java_port)})
    geyser = dict(policy["geyser"], **{"bedrock.port": bedrock_port})
    rendered = {
        CONFIGS[0]: properties_patch((defaults / CONFIGS[0]).read_text(), props),
        CONFIGS[1]: yaml_patch((defaults / CONFIGS[1]).read_text(), geyser),
    }
    # Floodgate remains generated in place, including key references and identities.
    out = fresh_dir(output)
    for name, content in rendered.items():
        dest = out / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    write_json(out / "manifest.json", {"files": inventory(out), "purpose": "initial configuration proposal ONLY"})


def backup(source, output):
    source, output = Path(source).resolve(), Path(output).resolve()
    require(not output.is_relative_to(source), "Backup must be outside source")
    before = inventory(source)
    require(before, "Empty backup source")
    out = fresh_dir(output)
    shutil.copytree(source, out / "data")
    require(inventory(source) == before == inventory(out / "data"), "Source changed or copy incomplete; discard this snapshot")
    write_json(out / "backup-manifest.json", {"files": before,
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "consistency": "operator attested clean shutdown; hashes verify transfer only"})


def verify_backup(path):
    path = Path(path)
    require(read_json(path / "backup-manifest.json")["files"] == inventory(path / "data"), "Backup checksum mismatch")


def restore(source, output):
    verify_backup(source)
    out = fresh_dir(output)
    shutil.copytree(Path(source) / "data", out, dirs_exist_ok=True)
    require(inventory(out) == read_json(Path(source) / "backup-manifest.json")["files"], "Restore checksum mismatch")


def validate():
    lock_data()
    policy = read_json(ROOT / "config/policy.json")
    require(policy["server.properties"]["online-mode"] == "true", "Java authentication must stay enabled")
    require(policy["geyser"]["java.auth-type"] == "floodgate", "Floodgate required")
    yaml_nodes((ROOT / ".github/workflows/validate.yml").read_text())
    for name in ["README.md", "DEPLOYMENT.md", "BACKUP_RESTORE.md", "TEST_PLAN.md", "HANDOFF.md"]:
        require((ROOT / (name if name == "README.md" else "docs/" + name)).is_file(), "Missing documentation: " + name)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    d = sub.add_parser("download"); d.add_argument("--cache", type=Path, default=ROOT / "downloads")
    q = sub.add_parser("package"); q.add_argument("--cache", type=Path, default=ROOT / "downloads"); q.add_argument("output", type=Path)
    q = sub.add_parser("verify-package"); q.add_argument("source", type=Path)
    q = sub.add_parser("init"); q.add_argument("source", type=Path); q.add_argument("output", type=Path)
    q = sub.add_parser("capture-defaults"); q.add_argument("source", type=Path); q.add_argument("output", type=Path)
    q = sub.add_parser("render-initial"); q.add_argument("source", type=Path); q.add_argument("output", type=Path)
    q.add_argument("--java-port", type=int, required=True); q.add_argument("--bedrock-port", type=int, required=True)
    q = sub.add_parser("backup"); q.add_argument("source", type=Path); q.add_argument("output", type=Path)
    q.add_argument("--confirmed-stopped", action="store_true", required=True)
    q = sub.add_parser("verify-backup"); q.add_argument("source", type=Path)
    q = sub.add_parser("restore"); q.add_argument("source", type=Path); q.add_argument("output", type=Path)
    a = p.parse_args()
    lock = lock_data()
    if a.command == "validate": validate()
    elif a.command == "download": download(a.cache, lock)
    elif a.command == "package": package(a.cache, a.output, lock)
    elif a.command == "verify-package": verify_package(a.source, lock)
    elif a.command == "init": initial_install(a.source, a.output, lock)
    elif a.command == "capture-defaults": capture(a.source, a.output, lock)
    elif a.command == "render-initial": render(a.source, a.output, a.java_port, a.bedrock_port, lock)
    elif a.command == "backup": backup(a.source, a.output)
    elif a.command == "verify-backup": verify_backup(a.source)
    elif a.command == "restore": restore(a.source, a.output)
    print(a.command + ": PASS")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, zipfile.BadZipFile, yaml.YAMLError) as error:
        sys.exit("ERROR: " + str(error))
