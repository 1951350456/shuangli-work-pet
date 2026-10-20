"""Exercise installation safety and exact offline file readback."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_local", ROOT / "scripts/install_local.py")
local = importlib.util.module_from_spec(spec)
spec.loader.exec_module(local)


class LocalInstallTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.target = self.base / "pets" / "shuangli-local"

    def test_complete_local_install_and_repeat(self):
        first = local.install(self.target)
        self.assertTrue(first["installed"])
        self.assertTrue(first["changed"])
        self.assertFalse(first["runtime_selection_verified"])
        self.assertFalse(first["permanent_offline_verified"])
        self.assertEqual((self.target / "spritesheet.png").read_bytes(), (ROOT / "assets/spritesheet.png").read_bytes())
        native = json.loads((self.target / "pet.json").read_text(encoding="utf-8"))
        self.assertEqual(native["spritesheetPath"], "spritesheet.png")
        self.assertEqual(native["spriteVersionNumber"], 2)
        self.assertFalse(local.install(self.target)["changed"])

    def test_existing_unrelated_target_is_preserved(self):
        self.target.mkdir(parents=True)
        sentinel = self.target / "user.txt"
        sentinel.write_text("keep", encoding="utf-8")
        with self.assertRaises(FileExistsError):
            local.install(self.target)
        self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
        self.assertFalse((self.target / "pet.json").exists())

    def test_changed_installed_image_is_not_silently_replaced(self):
        local.install(self.target)
        image = self.target / "spritesheet.png"
        image.write_bytes(b"changed by user")
        with self.assertRaises(FileExistsError):
            local.install(self.target)
        self.assertEqual(image.read_bytes(), b"changed by user")

    def test_bad_source_checksum_fails_before_install(self):
        fixture = self.base / "source"
        (fixture / "assets").mkdir(parents=True)
        (fixture / "native").mkdir()
        shutil.copyfile(ROOT / "pet.json", fixture / "pet.json")
        shutil.copyfile(ROOT / "native/pet.json", fixture / "native/pet.json")
        (fixture / "assets/spritesheet.png").write_bytes(b"corrupt")
        with self.assertRaises(ValueError):
            local.install(self.target, fixture)
        self.assertFalse(self.target.exists())


if __name__ == "__main__":
    unittest.main()
