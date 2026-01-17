from pathlib import Path
from ghostpm.desktop.templates import DESKTOP_TEMPLATE

DESKTOP_DIR = Path.home() / ".local/share/applications"


def generate_desktop_entry(
    name: str,
    exec_path: str,
    icon: str = "",
    categories: str = "Utility;",
    terminal: bool = False,
):
    DESKTOP_DIR.mkdir(parents=True, exist_ok=True)

    content = DESKTOP_TEMPLATE.format(
        name=name,
        exec=exec_path,
        icon=icon,
        terminal=str(terminal).lower(),
        categories=categories,
    )

    filename = f"ghost-{name.lower().replace(' ', '-')}.desktop"
    desktop_file = DESKTOP_DIR / filename
    desktop_file.write_text(content)

    return desktop_file


def remove_desktop_entry(name: str):
    filename = f"ghost-{name.lower().replace(' ', '-')}.desktop"
    desktop_file = DESKTOP_DIR / filename

    if desktop_file.exists():
        desktop_file.unlink()
