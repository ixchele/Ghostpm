HELP_MESSAGE : str = f"""
ghostpm — user-space package manager (no sudo)

Usage:
  ghostpm <command> [options]

Core commands:
  install <package>        Install a package
                            - from ghostpm recipes (e.g. bat, nvim)
                            - or from GitHub (<owner>/<repo>)
  remove <package>         Remove an installed package
  list                     List installed packages
  list-recipes             List all available ghostpm packages

Configuration:
  set-path <path>          Set the ghostpm installation root

Maintenance:
  **coming soon**

Search & discovery:
  **coming soon**


Shell integration:
  **coming soon**

Options:
  **coming soon**

Examples:
  ghostpm install bat
  ghostpm install sharkdp/bat
  ghostpm remove bat 

Notes:
  - ghostpm installs packages in user space (no sudo required)
  - Some binaries may not work due to system compatibility (e.g. GLIBC)

Project:
  https://github.com/ixchele/Ghostpm
"""
