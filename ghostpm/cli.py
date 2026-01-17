#!/usr/bin/env python3

from subprocess import run
import sys
import os
from pathlib import Path
import shutil

from typing import Callable

from ghostpm import recipes
from ghostpm.config import load_config, save_config
from ghostpm.errors import GhostpmError, InstallError, InvalidCommandError, PermissionDeniedError
from ghostpm.paths import make_paths
from ghostpm.recipes import RECIPES
from ghostpm.db import load as db_load, save as db_save
from ghostpm.desktop.manager import generate_desktop_entry, remove_desktop_entry

from ghostpm.installer import tar, zip, deb
from ghostpm.installer.common import ensure_dir, download

from ghostpm.resolver.github import resolve_github_repo
from ghostpm.help_message import HELP_MESSAGE
import tempfile

type CommandFn = Callable[...]

INSTALLERS = {
    "tar": tar,
    "zip": zip,
    "deb": deb,
}

def can_create_path(path: str):
    parent = os.path.abspath(path)

    while not os.path.exists(parent):
        parent = os.path.dirname(parent)
        if parent == "/":
            break

    try:
        tmp = tempfile.TemporaryFile(dir=parent)
        tmp.close()
        return True
    except PermissionError:
        return False


def setPath(args):
    if len(args) < 2:
        raise InvalidCommandError("Usage: ghostpm --set-path <directory>")

    path = args[1]
    path = os.path.expanduser(path)
    if not can_create_path(path):
        raise PermissionDeniedError(f"Permission denied: {path}")

    cfg = load_config()
    cfg["root"] = path
    save_config(cfg)

    print(f"[✓] ghostpm root set to {path}")

def normalize_package_name(pkg):
    if '/' in pkg:
        return pkg.split('/')[-1]
    return pkg

def install(args : list[str]):
    if len(args) != 2:
        raise InvalidCommandError("Usage: ghostpm install <package_name>")

    pkg = args[1]
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
        print(f"[+] Installing {pkg_name} from recipe")
        recipe = RECIPES[pkg_name]

        url = recipe["url"]
        installer_type = recipe["type"]
        bins = recipe["bin"]

    elif full_repo == pkg_name:
        raise InstallError(f"Unknown package: {pkg_name}")

    else:
        print(f"[+] Searching for {pkg_name} from GitHub releases")
        asset = resolve_github_repo(full_repo)
        print(f"[+] Installing {pkg_name} from GitHub releases")

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
        pkg_name,
        archive_path,
        pkg_path,
        bins,
        paths["BIN_DIR"],
    )
    desktop_cfg = RECIPES[pkg_name].get("desktop")
    if desktop_cfg:
        generate_desktop_entry(
            name=desktop_cfg["name"],
            exec_path=str(Path(paths["BIN_DIR"]) / pkg_name),
            icon=desktop_cfg.get("icon", ""),
            categories=desktop_cfg.get("categories", "Utility;"),
            terminal=desktop_cfg.get("terminal", False),
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


def remove(args: list[str]):
    if len(args) != 2:
        raise InvalidCommandError("Usage: ghostpm remove <package_name>")

    pkg = args[1]
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

    desktop_cfg = RECIPES[pkg_name].get("desktop")
    if desktop_cfg:
        remove_desktop_entry(desktop_cfg["name"])

    del db[pkg_name]
    db_save(db)

    print(f"[✓] {pkg_name} removed")


def listInstalled(args):
    if len(args) != 1:
        raise InvalidCommandError("Usage: ghostpm list")
    db = db_load()

    if not db:
        print("No packages installed.")
        return

    print("Installed packages:")
    for pkg in sorted(db.keys()):
        print(f"- {pkg}")


def listRecipes(args: list[str]):
    if len(args) != 1:
        raise InvalidCommandError("Usage: ghostpm list-recipes")

    width = max(len(f"[{p}]") for p in recipes.RECIPES)
    for package in recipes.RECIPES:
        description = recipes.RECIPES[package].get("desc", "google is your friend")
        print(f"[{package}]".ljust(width + 2) + f": {description}")



def help(args):
    if len(args) != 1:
        raise InvalidCommandError("Usage: ghostpm --help")
    print(HELP_MESSAGE)


commands : dict[str, CommandFn] = {
    "install": install,
    "remove": remove, 
    "set-path": setPath,
    "list": listInstalled,
    "--help": help,
    "list-recipes": listRecipes,
}

def handle_command():
    args : list[str] = sys.argv[1:]

    if len(args) == 0:
        print("Run `ghostpm --help` to see available commands.")
        return

    cmd: str = args[0]
    command = commands.get(cmd)
    if command is None:
        raise InvalidCommandError(f"Unknown command: {cmd}")
    command(args)

def main():
    try:
        handle_command()
    except GhostpmError as e:
        print(f"[!] {e}")
        return 1
    except KeyboardInterrupt:
        print("\n[!] Aborted by user")
        return 130
