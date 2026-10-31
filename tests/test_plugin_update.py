"""Synthetic plugin update gate tests; no real server/client or host is exercised."""
import copy
from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))
import manage
import plugin_update


class PluginUpdateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.old = copy.deepcopy(manage.lock_data())
        self.new = copy.deepcopy(self.old)
        self.new["verified_on"] = "2026-10-30"
        self.cache = self.root / "cache"
        self.cache.mkdir()
        for item in self.old["artifacts"]:
            path = self.cache / (item["id"] + ".jar")
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("META-INF/MANIFEST.MF", "Manifest-Version: 1.0\n")
                z.writestr("plugin.yml", "name: synthetic\n")
            item["sha256"] = manage.digest(path)
        self.new = copy.deepcopy(self.old)
        item = next(x for x in self.new["artifacts"] if x["id"] == "geyser")
        path = self.cache / "geyser.jar"
        with zipfile.ZipFile(path, "a") as z:
            z.writestr("test.txt", "synthetic candidate")
        item["sha256"] = manage.digest(path)
        item["build"] += 1
        self.old_path = self.root / "old.json"
        self.new_path = self.root / "new.json"
        manage.write_json(self.old_path, self.old)
        manage.write_json(self.new_path, self.new)
        self.full = self.root / "full"
        manage.package(self.cache, self.full, self.new)

    def test_package_and_verify(self):
        out = self.root / "plugins"
        self.assertEqual(plugin_update.package_plugins(self.old_path, self.full, out), ["geyser"])
        plugin_update.verify_plugin_package(self.old_path, out)
        self.assertEqual(set(manage.inventory(out)), {
            "plugins/Geyser-Spigot.jar", "versions.lock.json", "manifest.json"})

    def test_refuse_paper_changes(self):
        bad = copy.deepcopy(self.old)
        bad["artifacts"][0]["build"] += 1
        with self.assertRaises(ValueError):
            plugin_update.changed_plugin_ids(bad, self.new)

    def test_refuse_java_changes(self):
        bad = copy.deepcopy(self.old)
        bad["java"]["host_runtime_exact"] = "other"
        with self.assertRaises(ValueError):
            plugin_update.changed_plugin_ids(bad, self.new)

    def test_refuse_no_binary_changes(self):
        with self.assertRaises(ValueError):
            plugin_update.changed_plugin_ids(self.old, self.old)

    def test_refuse_extra_world_data(self):
        out = self.root / "plugins"
        plugin_update.package_plugins(self.old_path, self.full, out)
        (out / "world").mkdir()
        (out / "world/level.dat").write_bytes(b"private data")
        with self.assertRaises(ValueError):
            plugin_update.verify_plugin_package(self.old_path, out)

    def test_refuse_tampering(self):
        out = self.root / "plugins"
        plugin_update.package_plugins(self.old_path, self.full, out)
        (out / "plugins/Geyser-Spigot.jar").write_bytes(b"tampered")
        with self.assertRaises(ValueError):
            plugin_update.verify_plugin_package(self.old_path, out)


if __name__ == "__main__":
    unittest.main()
