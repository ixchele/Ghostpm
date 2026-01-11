import os
from ghostpm.errors import InvalidArchiveType

def detect_archive_type(url: str) -> str:
    name = os.path.basename(url)

    if name.endswith((".tar.gz", ".tgz", ".tar.xz", ".tar.bz2")):
        return "tar"
    if name.endswith(".zip"):
        return "zip"
    raise InvalidArchiveType("archive type unknown")
    # return "raw"
