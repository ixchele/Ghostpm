import os
from ghostpm.installer.common import symlink


def install(pkg_name, file_path, pkg_dir, bins, bin_dir):
    os.makedirs(pkg_dir, exist_ok=True)

    appimage_path = os.path.join(pkg_dir, bins[0])
    os.rename(file_path, appimage_path)

    os.chmod(appimage_path, 0o755)
    symlink(appimage_path, bins[0], bin_dir)
