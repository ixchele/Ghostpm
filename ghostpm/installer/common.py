import os
import subprocess
from ghostpm.errors import DownloadError


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def download(url, dest):
    if os.path.exists(dest):
        return

    try:
        print(f"[+] Downloading {url}")
        result = subprocess.run(
            ["curl", "-L", "--progress-bar", url, "-o", dest]
        )
        if result.returncode == 0:
            return

        print("[!] curl failed, retrying with TLS compatibility mode")
        result = subprocess.run(
            [
                "curl",
                "-L",
                "--progress-bar",
                "--tlsv1.2",
                "--ciphers",
                "DEFAULT:@SECLEVEL=1",
                url,
                "-o",
                dest,
            ]
        )
        if result.returncode == 0:
            return
    except Exception as e:
        raise DownloadError("Download failed") from e


    # 3) échec total
    raise RuntimeError(
        "Download failed (SSL issue). Try using a different network or VPN."
    )

def symlink(src, name, bin_dir):
    dst = os.path.join(bin_dir, name)
    if os.path.exists(dst) or os.path.islink(dst):
        os.remove(dst)
    os.symlink(src, dst)
    print(f"[+] Linked {name}")
