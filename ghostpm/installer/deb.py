import subprocess
import os
from ghostpm.errors import InstallError
from ghostpm.installer.common import symlink


def install(pkg_name, archive, pkg_dir, bins, bin_dir):
    print(f"[+] Extracting {pkg_name}")

    os.makedirs(pkg_dir, exist_ok=True)

    try:
        subprocess.run(
            ["dpkg-deb", "-x", archive, pkg_dir],
            check=True,
        )
    except FileNotFoundError:
        raise InstallError("dpkg-deb not found (dpkg is required)")
    except subprocess.CalledProcessError:
        raise InstallError("Failed to extract .deb")

    for b in bins:
        src = os.path.join(pkg_dir, b)
        print(src)
        if not os.path.exists(src):
            raise InstallError(f"Binary not found: {src}")
        symlink(src, os.path.basename(b), bin_dir)

