#!/usr/bin/env python3

import sys
import os
import shutil

from ghostpm.config import load_config, save_config
from ghostpm.paths import make_paths
from ghostpm.recipes import RECIPES
from ghostpm.db import load as db_load, save as db_save

from ghostpm.installer import tar#, appimage
from ghostpm.installer.common import ensure_dir, download

INSTALLERS = {
    "tar": tar,
    # "appimage": appimage,
}


def handle_set_path(args):
    if not args:
        return False

    if args[0].startswith("--set-path"):
        if "=" in args[0]:
            path = args[0].split("=", 1)[1]
        else:
            if len(args) < 2:
                print("ghostpm --set-path <directory>")
                sys.exit(1)
            path = args[1]

        path = os.path.expanduser(path)

        cfg = load_config()
        cfg["root"] = path
        save_config(cfg)

        print(f"[✓] ghostpm root set to {path}")
        return True

    return False


def install(pkg):
    if pkg not in RECIPES:
        print(f"[-] Unknown package: {pkg}")
        return

    paths = make_paths()
    recipe = RECIPES[pkg]

    ensure_dir(paths["ROOT"])
    ensure_dir(paths["PKG_DIR"])
    ensure_dir(paths["CACHE_DIR"])
    ensure_dir(paths["BIN_DIR"])

    archive_path = os.path.join(paths["CACHE_DIR"], pkg)
    download(recipe["url"], archive_path)

    pkg_path = os.path.join(paths["PKG_DIR"], pkg)
    ensure_dir(pkg_path)

    INSTALLERS[recipe["type"]].install(
        pkg,
        archive_path,
        pkg_path,
        recipe["bin"],
        paths["BIN_DIR"],
    )

    db = db_load()
    db[pkg] = {
        "type": recipe["type"],
        "url": recipe["url"],
    }
    db_save(db)

    print(f"[✓] {pkg} installed")


def remove(pkg):
    paths = make_paths()
    db = db_load()

    if pkg not in db:
        print(f"[-] {pkg} is not installed")
        return

    recipe = RECIPES.get(pkg)

    if recipe:
        for b in recipe["bin"]:
            link = os.path.join(paths["BIN_DIR"], os.path.basename(b))
            if os.path.exists(link) or os.path.islink(link):
                os.remove(link)
                print(f"[+] Removed {link}")

    pkg_path = os.path.join(paths["PKG_DIR"], pkg)
    if os.path.exists(pkg_path):
        shutil.rmtree(pkg_path)
        print(f"[+] Removed {pkg_path}")

    del db[pkg]
    db_save(db)

    print(f"[✓] {pkg} removed")

def list_packages():
    db = db_load()

    if not db:
        print("No packages installed.")
        return

    print("Installed packages:")
    for pkg in sorted(db.keys()):
        print(f"- {pkg}")

def main():
    args = sys.argv[1:]

    if handle_set_path(args):
        return

    if len(args) == 1 and args[0] == "list":
        list_packages()
        return
    if len(args) < 2:
        print("Usage: ghostpm install|remove <package>")
        return

    cmd, pkg = args[0], args[1]

    if cmd == "install":
        install(pkg)
    elif cmd == "remove":
        remove(pkg)
    else:
        print(f"Unknown command: {cmd}")
