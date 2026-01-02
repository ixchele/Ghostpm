import urllib.request
import json
import re
from ghostpm.resolver.get_arch import detect_platform
from ghostpm.resolver.archive import detect_archive_type


SYSTEM_ALIASES = {
    "linux": ["linux", "gnu"],
    "darwin": ["darwin", "mac", "macos", "osx"],
    "windows": ["windows", "win"]
}

ARCH_ALIASES = {
    "amd64": ["amd64", "x86_64", "x64"],
    "arm64": ["arm64", "aarch64"],
    "armv7": ["armv7", "armhf"],
}

IGNORED_KEYWORDS = [
    "sha256",
    "sha512",
    "checksum",
    "checksums",
    ".asc",
    ".sig",
    "signature",
    "symbols",
    "debug",
    "src",
    "source",
]

PRIORITY = {
    "tar": 100,
    "zip": 90,
    "raw": 80,
    "deb": 60,
    "appimage": 50,
}

def get_latest_release(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    with urllib.request.urlopen(url) as response:
        data = response.read().decode("utf-8")
    return json.loads(data)

def matches_system_arch(name: str, system: str, arch: str) -> bool:
    name = name.lower()

    system_aliases = SYSTEM_ALIASES.get(system, [])
    arch_aliases = ARCH_ALIASES.get(arch, [])

    system_match = any(alias in name for alias in system_aliases)
    arch_match = any(alias in name for alias in arch_aliases)

    if system_match and arch_match:
        return True
    return False

def is_checksum_or_source(name: str) -> bool:
    name = name.lower()

    for keyword in IGNORED_KEYWORDS:
        if keyword in name:
            return True

    return False

def resolve_asset(assets, system, arch):
    candidates = []

    for asset in assets:
        if not matches_system_arch(asset["name"], system, arch):
            continue
        if is_checksum_or_source(asset["name"]):
            continue

        asset_type = detect_archive_type(asset["name"])
        if asset_type not in PRIORITY:
            continue

        candidates.append({
            "name": asset["name"],
            "url": asset["browser_download_url"],
            "type": asset_type,
            "priority": PRIORITY[asset_type],
        })

    if not candidates:
        return None
    return max(candidates, key=lambda a: a["priority"])


# def find_asset(assets, system, arch):
#     if arch == "amd64":
#         pattern = re.compile(
#             f"({system}.*({arch}|x86_64))|(({arch}|x86_64).*{system})",
#             re.IGNORECASE
#         )
#     else:
#         pattern = re.compile(
#             f"({system}.*{arch})|({arch}.*{system})",
#             re.IGNORECASE
#         )
#
#     for asset in assets:
#         name = asset.get("name", "")
#         if pattern.search(name):
#             return {
#                 "name": name,
#                 "url": asset.get("browser_download_url"),
#                 "type": detect_archive_type(name)
#             }
#
#     return None

def resolve_github_repo(repo):
    system, arch = detect_platform()
    release = get_latest_release(repo)
    # asset = find_asset(release.get("assets", []), system, arch)
    asset = resolve_asset(release.get("assets", []), system, arch)

    if not asset:
        raise RuntimeError("No compatible asset found")

    return asset
