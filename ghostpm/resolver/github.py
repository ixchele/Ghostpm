import urllib.request
import urllib.error
import json
import re
from ghostpm.errors import AssetsError, GhostpmError, GithubError
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

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode("utf-8")
        return json.loads(data)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            raise GithubError(f"Github repository not found: {repo} (code:{e.code}, {e.url} {e.reason})") from None
        raise GithubError(f"Github API error ({e.code}) for {repo} ({e.reason})") from None 
    except urllib.error.URLError as e:
        raise GithubError(f"{e.reason}")

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
        raise AssetsError("No compatible asset found")

    return max(candidates, key=lambda a: a["priority"])


def resolve_github_repo(repo):
    system, arch = detect_platform()
    release = get_latest_release(repo)
    asset = resolve_asset(release.get("assets", []), system, arch)

    return asset
