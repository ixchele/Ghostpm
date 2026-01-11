import os
import tarfile
from ghostpm.errors import InstallError
from ghostpm.installer.common import symlink


def _find_root_dir(path):
    entries = os.listdir(path)
    if len(entries) == 1:
        root = os.path.join(path, entries[0])
        if os.path.isdir(root):
            return root
    return path


def install(pkg_name, archive, pkg_dir, bins, bin_dir):
    print(f"[+] Extracting {pkg_name}")

    with tarfile.open(archive) as tar:
        tar.extractall(pkg_dir)

    root = _find_root_dir(pkg_dir)

    for b in bins:
        src = os.path.join(root, b)
        if not os.path.exists(src):
            raise InstallError(f"Binary not found: {src}")
        symlink(src, os.path.basename(b), bin_dir)
