import os
import sys
import urllib.request
import subprocess


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def _print_progress(downloaded, total, width=30):
    if total <= 0:
        return

    ratio = downloaded / total
    filled = int(ratio * width)
    bar = "█" * filled + "-" * (width - filled)
    percent = int(ratio * 100)

    sys.stdout.write(f"\r[{bar}] {percent}%")
    sys.stdout.flush()




def download(url, dest):
    if os.path.exists(dest):
        return

    print(f"[+] Downloading {url}")

    # 1) curl normal
    result = subprocess.run(
        ["curl", "-L", "--progress-bar", url, "-o", dest]
    )

    if result.returncode == 0:
        return

    print("[!] curl failed, retrying with TLS compatibility mode")

    # 2) retry avec options TLS plus permissives
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
