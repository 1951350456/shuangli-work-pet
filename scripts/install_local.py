#!/usr/bin/env python3
"""Install the validated atlas using the desktop client's local pet file format.

Python 3.9+, standard library only. This installs files; it does not select a
pet, disable cloud migration, alter the application, or change account state.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import struct
import tempfile

ROOT = Path(__file__).resolve().parents[1]
LOCAL_SLUG = "shuangli-local"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def package_files(root):
    root = Path(root)
    metadata = json.loads((root / "pet.json").read_text(encoding="utf-8"))
    native = json.loads((root / "native/pet.json").read_text(encoding="utf-8"))
    if native["spriteVersionNumber"] != 2 or native["spritesheetPath"] != "spritesheet.png":
        raise ValueError("Native metadata must reference the local v2 spritesheet.png")
    if not native["displayName"].strip():
        raise ValueError("Native pet display name is empty")
    raw = (root / "assets/spritesheet.png").read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != metadata["sha256"]:
        raise ValueError("Atlas checksum differs from the accepted pet.json")
    if not 24 <= len(raw) <= 20 * 1024 * 1024:
        raise ValueError("Atlas file size is outside the supported range")
    if raw[:8] != PNG_SIGNATURE or raw[12:16] != b"IHDR":
        raise ValueError("Expected an encoded PNG")
    if struct.unpack(">II", raw[16:24]) != (1536, 2288):
        raise ValueError("Expected a 1536 x 2288 v2 atlas")
    manifest = (json.dumps(native, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return {"pet.json": manifest, "spritesheet.png": raw}, digest


def default_destination():
    configured = os.environ.get("CODEX_HOME")
    home = Path(configured).expanduser() if configured else Path.home() / ".codex"
    if not home.is_absolute():
        raise ValueError("CODEX_HOME must be an absolute path")
    return home / "pets" / LOCAL_SLUG


def status(destination, root=ROOT):
    destination = Path(destination).expanduser().absolute()
    files, digest = package_files(root)
    exists = destination.exists()
    matches = exists and not destination.is_symlink() and all(
        (destination / name).is_file() and (destination / name).read_bytes() == raw
        for name, raw in files.items()
    )
    return {
        "installed": bool(matches),
        "directory_exists": exists,
        "directory": str(destination),
        "local_pet_id": "custom:" + destination.name,
        "sha256": digest,
        "runtime_selection_verified": False,
        "permanent_offline_verified": False,
        "client_cloud_migration": "must be checked in the desktop client",
    }


def install(destination, root=ROOT):
    destination = Path(destination).expanduser().absolute()
    files, digest = package_files(root)
    if destination.is_symlink():
        raise FileExistsError("Refusing to install into a symlink: " + str(destination))
    if destination.exists():
        result = status(destination, root)
        if not result["installed"]:
            raise FileExistsError("Existing target differs; back it up explicitly before reinstalling: " + str(destination))
        result["changed"] = False
        return result
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".shuangli-install-", dir=str(destination.parent)) as temporary:
        staged = Path(temporary) / "pet"
        staged.mkdir()
        for name, raw in files.items():
            (staged / name).write_bytes(raw)
        # Same parent filesystem. The client sees a complete manifest/image pair.
        staged.rename(destination)
    result = status(destination, root)
    if not result["installed"]:
        raise RuntimeError("Installed files failed readback verification")
    result["changed"] = True
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["install", "status", "bundle"])
    parser.add_argument("--destination", type=Path, help="Exact target pet directory; default: CODEX_HOME/pets/shuangli-local")
    args = parser.parse_args()
    destination = args.destination
    if args.command == "bundle":
        if destination is None:
            destination = ROOT / "build" / LOCAL_SLUG
        result = install(destination)
        result["purpose"] = "portable local pet files; not installed in the desktop client"
    else:
        if destination is None:
            destination = default_destination()
        result = install(destination) if args.command == "install" else status(destination)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if args.command == "status" and not result["installed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
