#!/usr/bin/env python3
"""Create and verify a plugin-only Geyser/Floodgate update from a verified release package.

Does not connect to a host, stop a process, write a live server, or accept an EULA.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import sys

import manage


PLUGIN_IDS = {"geyser", "floodgate"}


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def changed_plugin_ids(old, new):
    manage.require(old["minecraft_java"] == new["minecraft_java"],
                   "Plugin-only path cannot change the Minecraft version")
    manage.require(old["java"] == new["java"],
                   "Plugin-only path cannot change the Java runtime record")
    old_items = {item["id"]: item for item in old["artifacts"]}
    new_items = {item["id"]: item for item in new["artifacts"]}
    manage.require(old_items["paper"] == new_items["paper"],
                   "Plugin-only path must retain the exact Paper version, build, URL and SHA-256")
    changed = []
    for plugin in sorted(PLUGIN_IDS):
        before, after = old_items[plugin], new_items[plugin]
        if before != after:
            manage.require(before["sha256"] != after["sha256"],
                           "Updated plugin metadata without changing binary hash")
            changed.append(plugin)
    manage.require(changed, "Nothing to update: both plugin binaries are unchanged")
    return changed


def package_plugins(old_lock_path, candidate_package, output):
    old_lock_path, candidate_package, output = map(Path, (old_lock_path, candidate_package, output))
    old = manage.lock_data(old_lock_path)
    new = manage.lock_data(candidate_package / "versions.lock.json")
    changed = changed_plugin_ids(old, new)
    manage.verify_package(candidate_package, new)
    manage.require(not output.resolve().is_relative_to(candidate_package.resolve()),
                   "Output must be outside full candidate package")
    out = manage.fresh_dir(output)
    for artifact in new["artifacts"]:
        if artifact["id"] not in changed:
            continue
        relative = artifact["destination"]
        target = out / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(candidate_package / relative, target)
        manage.verify_jar(target, artifact)
    shutil.copyfile(candidate_package / "versions.lock.json", out / "versions.lock.json")
    manifest = {
        "schema_version": 1,
        "kind": "geyser-floodgate-plugin-update-only",
        "old_lock_sha256": sha256(old_lock_path),
        "new_lock_sha256": sha256(out / "versions.lock.json"),
        "changed_plugin_ids": changed,
        "files": manage.inventory(out),
    }
    manage.write_json(out / "manifest.json", manifest)
    verify_plugin_package(old_lock_path, out)
    return changed


def verify_plugin_package(old_lock_path, plugin_package):
    path = Path(plugin_package)
    old = manage.lock_data(old_lock_path)
    new = manage.lock_data(path / "versions.lock.json")
    changed = changed_plugin_ids(old, new)
    manifest = manage.read_json(path / "manifest.json")
    expected = {"versions.lock.json"} | {
        a["destination"] for a in new["artifacts"] if a["id"] in changed
    }
    actual = manage.inventory(path)
    actual.pop("manifest.json", None)
    manage.require(manifest["schema_version"] == 1 and
                   manifest["kind"] == "geyser-floodgate-plugin-update-only" and
                   manifest["changed_plugin_ids"] == changed and
                   manifest["old_lock_sha256"] == sha256(old_lock_path) and
                   manifest["new_lock_sha256"] == sha256(path / "versions.lock.json"),
                   "Plugin-only update manifest header mismatch")
    manage.require(set(actual) == expected and actual == manifest["files"],
                   "Plugin-only package has missing, unexpected or altered files")
    for item in new["artifacts"]:
        if item["id"] in changed:
            manage.verify_jar(path / item["destination"], item)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="command", required=True)
    p = subs.add_parser("package")
    p.add_argument("old_lock", type=Path)
    p.add_argument("candidate_full_package", type=Path)
    p.add_argument("output", type=Path)
    p = subs.add_parser("verify")
    p.add_argument("old_lock", type=Path)
    p.add_argument("plugin_only_package", type=Path)
    args = parser.parse_args()
    if args.command == "package":
        print("Changed plugins: " + ", ".join(package_plugins(
            args.old_lock, args.candidate_full_package, args.output)))
    else:
        verify_plugin_package(args.old_lock, args.plugin_only_package)
        print("plugin-only package: PASS")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as exc:
        sys.exit("ERROR: " + str(exc))
