

def generate_desktop_entry(desktop_config : dict) -> str:
    desktop_profile = f"""[Desktop Entry]
Type=Application
Name={desktop_config["name"]}
Exec={desktop_config["exec"]}
Icon={desktop_config["icon"]}
Terminal=false
Categories={";".join(desktop_config.get("categories", []))};"""

    return desktop_profile
