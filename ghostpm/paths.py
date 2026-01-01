import os
from ghostpm.config import get_root

HOME = os.path.expanduser("~")


def make_paths():
    root = get_root()
    if not root:
        root = os.path.join(HOME, ".ghostpm")

    root = os.path.expanduser(root)

    return {
        "ROOT": root,
        "PKG_DIR": os.path.join(root, "packages"),
        "CACHE_DIR": os.path.join(HOME, ".cache", "ghostpm"),
        "DB_FILE": os.path.join(HOME, ".config", "ghostpm", "db.json"),
        "BIN_DIR": os.path.join(HOME, ".local", "bin"),
    }
