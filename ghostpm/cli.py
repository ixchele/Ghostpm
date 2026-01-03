#!/usr/bin/env python3

import sys
import os
import shutil

from ghostpm.config import load_config, save_config
from ghostpm.paths import make_paths
from ghostpm.recipes import RECIPES
from ghostpm.db import load as db_load, save as db_save

from ghostpm.installer import tar, zip#, appimage
from ghostpm.installer.common import ensure_dir, download

from ghostpm.resolver.github import resolve_github_repo

INSTALLERS = {
    "tar": tar,
    "zip": zip,
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

def normalize_package_name(pkg):
    if '/' in pkg:
        return pkg.split('/')[-1]
    return pkg

def install(pkg : str):
    full_repo = pkg
    pkg_name = normalize_package_name(pkg)
    paths = make_paths()

    ensure_dir(paths["ROOT"])
    ensure_dir(paths["PKG_DIR"])
    ensure_dir(paths["CACHE_DIR"])
    ensure_dir(paths["BIN_DIR"])

    pkg_path = os.path.join(paths["PKG_DIR"], pkg_name)
    ensure_dir(pkg_path)

    if pkg_name in RECIPES:
        print(f"[+] Installing {pkg} from recipe")
        recipe = RECIPES[pkg_name]

        url = recipe["url"]
        installer_type = recipe["type"]
        bins = recipe["bin"]

    else:
        print(f"[+] Installing {pkg_name} from GitHub releases")
        asset = resolve_github_repo(full_repo)

        url = asset["url"]
        installer_type = asset["type"]
        bins = [pkg.split('/')[1]]

    if installer_type not in INSTALLERS:
        raise RuntimeError(f"Unsupported archive type: {installer_type}")

    archive_path = os.path.join(
        paths["CACHE_DIR"],
        os.path.basename(url)
    )

    download(url, archive_path)

    INSTALLERS[installer_type].install(
        pkg,
        archive_path,
        pkg_path,
        bins,
        paths["BIN_DIR"],
    )

    db = db_load()

    if pkg_name in db:
        print(f"[!] {pkg_name} is already installed, overwriting")

    db[pkg_name] = {
        "installer": installer_type,
        "url": url,
        "path": paths["ROOT"],
        "bins": bins,
        "source" : full_repo if '/' in full_repo else None,
    }

    db_save(db)

    print(f"[✓] {pkg_name} installed")


def remove(pkg):
    pkg_name = normalize_package_name(pkg)
    paths = make_paths()
    db = db_load()

    if pkg_name not in db:
        print(f"[-] {pkg_name} is not installed")
        return

    bins = db[pkg_name].get("bins", [])
    for b in bins:
        link = os.path.join(paths["BIN_DIR"], os.path.basename(b))
        if os.path.exists(link) or os.path.islink(link):
            os.remove(link)
            print(f"[+] Removed {link}")

    pkg_path = os.path.join(paths["PKG_DIR"], pkg_name)
    if os.path.exists(pkg_path):
        shutil.rmtree(pkg_path)
        print(f"[+] Removed {pkg_path}")

    del db[pkg_name]
    db_save(db)

    print(f"[✓] {pkg_name} removed")

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
