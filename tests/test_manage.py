"""Synthetic safety tests; these do not represent Minecraft gameplay or recovery."""
import copy
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.error
import zipfile

spec = importlib.util.spec_from_file_location("manage", Path(__file__).parents[1] / "scripts/manage.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class SafetyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.cache = self.root / "cache"
        self.cache.mkdir()
        self.lock = copy.deepcopy(m.lock_data())
        for a in self.lock["artifacts"]:
            p = self.cache / (a["id"] + ".jar")
            with zipfile.ZipFile(p, "w") as z:
                z.writestr("META-INF/MANIFEST.MF", "Manifest-Version: 1.0\n")
                z.writestr("plugin.yml", "name: fixture\n")
            a["sha256"] = m.digest(p)

    def test_lock_valid(self):
        self.assertEqual(m.lock_data()["minecraft_java"], "26.3")

    def test_bad_url_rejected(self):
        for url in ["http://download.geysermc.org/foo", "https://evil.test/a.jar",
                    "https://download.geysermc.org/latest", "https://user:password@fill.papermc.io/a"]:
            with self.subTest(url=url), self.assertRaises(ValueError):
                m.official_url(url)

    def test_invalid_hash_lock_rejected(self):
        self.lock["artifacts"][0]["sha256"] = "guess"
        path = self.root / "lock.json"; m.write_json(path, self.lock)
        with self.assertRaises(ValueError): m.lock_data(path)

    def test_download_cache_reuse(self):
        with patch.object(m.urllib.request, "build_opener") as opener:
            m.download(self.cache, self.lock)
            opener.return_value.open.assert_not_called()

    def test_corrupt_cache_not_overwritten(self):
        p = self.cache / "paper.jar"; p.write_bytes(b"broken")
        with self.assertRaises(ValueError): m.download(self.cache, self.lock)
        self.assertEqual(p.read_bytes(), b"broken")

    def test_http_error_does_not_leave_artifact(self):
        (self.cache / "paper.jar").unlink()
        with patch.object(m.urllib.request, "build_opener") as opener:
            opener.return_value.open.side_effect = urllib.error.HTTPError("url", 404, "missing", {}, None)
            with self.assertRaises(urllib.error.HTTPError): m.download(self.cache, self.lock)
        self.assertFalse((self.cache / "paper.jar").exists())
        self.assertFalse(list(self.cache.glob(".download-*")))

    def test_invalid_download_cleanup(self):
        (self.cache / "paper.jar").unlink()
        response = io.BytesIO(b"<html>Not a JAR</html>")
        response.status = 200
        response.geturl = lambda: self.lock["artifacts"][0]["url"]
        with patch.object(m.urllib.request, "build_opener") as opener:
            opener.return_value.open.return_value = response
            with self.assertRaises(ValueError): m.download(self.cache, self.lock)
        self.assertFalse((self.cache / "paper.jar").exists())
        self.assertFalse(list(self.cache.glob(".download-*")))

    def test_nonjar_even_with_matching_hash_rejected(self):
        p = self.cache / "paper.jar"; p.write_bytes(b"not zip")
        a = dict(self.lock["artifacts"][0], sha256=m.digest(p))
        with self.assertRaises(zipfile.BadZipFile): m.verify_jar(p, a)

    def test_package_exact_manifest(self):
        out = self.root / "package"; m.package(self.cache, out, self.lock)
        m.verify_package(out, self.lock)
        self.assertEqual(set(m.inventory(out)), set(m.DESTINATIONS.values()) | {"versions.lock.json", "manifest.json"})

    def test_package_rejects_extra_secret_even_if_manifest_updated(self):
        out = self.root / "package"; m.package(self.cache, out, self.lock)
        (out / "key.pem").write_text("synthetic")
        files = m.inventory(out); files.pop("manifest.json")
        m.write_json(out / "manifest.json", {"files": files})
        with self.assertRaises(ValueError): m.verify_package(out, self.lock)

    def test_package_tampering(self):
        out = self.root / "package"; m.package(self.cache, out, self.lock)
        (out / "server.jar").write_bytes(b"bad")
        with self.assertRaises(ValueError): m.verify_package(out, self.lock)

    def test_init_refuses_existing_world(self):
        out = self.root / "package"; m.package(self.cache, out, self.lock)
        target = self.root / "server"; target.mkdir()
        (target / "world.dat").write_text("keep")
        with self.assertRaises(ValueError): m.initial_install(out, target, self.lock)
        self.assertEqual((target / "world.dat").read_text(), "keep")

    def test_second_init_safe(self):
        out = self.root / "package"; m.package(self.cache, out, self.lock)
        target = self.root / "server"; m.initial_install(out, target, self.lock)
        with self.assertRaises(ValueError): m.initial_install(out, target, self.lock)

    def test_properties_preserve_unrelated(self):
        original = "# operator comment\nfoo=old\nother=custom\n"
        self.assertEqual(m.properties_patch(original, {"foo": "new"}), "# operator comment\nfoo=new\nother=custom\n")

    def test_properties_unknown_and_duplicate_fail(self):
        for text, changes in [("foo=x\n", {"bar": "y"}), ("foo=x\nfoo=y\n", {"foo": "z"})]:
            with self.assertRaises(ValueError): m.properties_patch(text, changes)

    def test_yaml_preserves_comments_unknown_values(self):
        original = "# comment\njava:\n  auth-type: online # reason\nother: keep\n"
        text = m.yaml_patch(original, {"java.auth-type": "floodgate"})
        self.assertIn('# reason', text); self.assertIn('other: keep', text)
        self.assertIn('auth-type: "floodgate"', text)

    def test_yaml_unknown_duplicate_alias_fail(self):
        for text in ["java: {}", "java: 1\njava: 2", "a: &a {}\nb: *a"]:
            with self.subTest(text=text), self.assertRaises(ValueError):
                m.yaml_patch(text, {"java.auth-type": "floodgate"})

    def test_port_validation(self):
        for java, bedrock in [(0, 123), (25565, 25565), (25565, 70000)]:
            with self.assertRaises(ValueError):
                m.render(self.root, self.root / "out", java, bedrock, self.lock)

    def defaults_fixture(self):
        # Deliberately synthetic, not claimed as real Paper-generated defaults.
        server = self.root / "boot"; server.mkdir()
        for a in self.lock["artifacts"]:
            dest = server / a["destination"]; dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes((self.cache / (a["id"] + ".jar")).read_bytes())
        policy = m.read_json(m.ROOT / "config/policy.json")
        (server / m.CONFIGS[0]).write_text("".join(k + "=default\n" for k in policy["server.properties"]) + "server-port=25565\ncustom=preserve\n")
        geyser = server / m.CONFIGS[1]; geyser.parent.mkdir(parents=True)
        geyser.write_text("# synthetic\njava:\n  auth-type: online\nbedrock:\n  port: 19132\n  transport: nethernet\n  clone-remote-port: false\n  webrtc-port: 0\n  signaling:\n    mode: builtin\ncustom: preserve\n")
        flood = server / m.CONFIGS[2]; flood.parent.mkdir(parents=True)
        flood.write_text("key-file-name: key.pem\n")
        return server

    def test_capture_render_preserves_source(self):
        server = self.defaults_fixture(); before = m.inventory(server)
        defaults = self.root / "defaults"; m.capture(server, defaults, self.lock)
        out = self.root / "rendered"; m.render(defaults, out, 25575, 19142, self.lock)
        self.assertEqual(before, m.inventory(server))
        self.assertIn("custom=preserve", (out / m.CONFIGS[0]).read_text())
        self.assertIn("server-port=25575", (out / m.CONFIGS[0]).read_text())
        self.assertFalse((out / m.CONFIGS[2]).exists())
        with self.assertRaises(ValueError): m.render(defaults, out, 25575, 19142, self.lock)

    def test_changed_defaults_rejected(self):
        server = self.defaults_fixture(); defaults = self.root / "defaults"
        m.capture(server, defaults, self.lock)
        (defaults / m.CONFIGS[0]).write_text("tampered")
        with self.assertRaises(ValueError): m.render(defaults, self.root / "out", 25575, 19142, self.lock)

    def test_defaults_from_other_lock_rejected(self):
        server = self.defaults_fixture(); defaults = self.root / "defaults"
        m.capture(server, defaults, self.lock)
        prov = m.read_json(defaults / "provenance.json"); prov["lock_sha256"] = "0" * 64
        m.write_json(defaults / "provenance.json", prov)
        with self.assertRaises(ValueError): m.render(defaults, self.root / "out", 25575, 19142, self.lock)

    def make_source(self):
        source = self.root / "source"; source.mkdir()
        (source / "world").mkdir(); (source / "world/level.dat").write_bytes(b"synthetic world")
        (source / "plugins").mkdir(); (source / "plugins/key.pem").write_bytes(b"synthetic secret")
        (source / "ops.json").write_text("[]")
        return source

    def test_backup_restore_byte_identical(self):
        source = self.make_source(); out = self.root / "backup"
        m.backup(source, out); m.verify_backup(out)
        dest = self.root / "restored"; m.restore(out, dest)
        self.assertEqual(m.inventory(source), m.inventory(dest))

    def test_backup_corruption_prevents_restore(self):
        source = self.make_source(); out = self.root / "backup"; m.backup(source, out)
        (out / "data/world/level.dat").write_bytes(b"corrupt")
        with self.assertRaises(ValueError): m.restore(out, self.root / "restored")
        self.assertFalse((self.root / "restored").exists())

    def test_restore_refuses_existing_target(self):
        source = self.make_source(); out = self.root / "backup"; m.backup(source, out)
        with self.assertRaises(ValueError): m.restore(out, source)

    def test_backup_not_inside_source(self):
        source = self.make_source()
        with self.assertRaises(ValueError): m.backup(source, source / "backup")

    def test_symlink_rejected(self):
        source = self.make_source()
        try: (source / "link").symlink_to(source / "ops.json")
        except OSError: self.skipTest("Platform does not permit symlink creation")
        with self.assertRaises(ValueError): m.backup(source, self.root / "backup")


if __name__ == "__main__": unittest.main()
