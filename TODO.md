# Ghostpm – TODO / Roadmap

##  Package management (core)
- [ ] `ghostpm search <query>` – search available packages (recipes + GitHub hints)
- [ ] `ghostpm info <package>` – show detailed package information
- [x] `ghostpm install <package>` – support owner/repo (GitHub releases)
- [x] `ghostpm remove <package>` – remove installed package
- [x] `ghostpm list` – list installed packages
- [ ] `ghostpm list-available` – list all known recipes
- [ ] `ghostpm upgrade [<package>]` – upgrade one or all packages
- [ ] `ghostpm pin <package>` – prevent a package from being upgraded
- [ ] `ghostpm unpin <package>` – allow upgrades again
- [ ] `ghostpm --zsh` Shell integration;
      `source <(ghostpm --zsh)`
      - Verify installed packages at shell startup
      - Detect missing / broken installations
      - Future: upgrade notifications

---

##  Versioning & upgrades
- [ ] Track installed package version in `db.json`
- [ ] Compare installed vs latest version (recipes / GitHub)
- [ ] Support `--dry-run` for upgrades
- [ ] Support `--force` reinstall

---

##  Configuration & paths
- [x] `ghostpm set-path <path>` – set install root
- [ ] `ghostpm use <profile>` – switch install profile
- [ ] Support multiple named roots (`default`, `school`, `work`)
- [ ] `ghostpm config list` – show current configuration
- [ ] `ghostpm config edit` – open config in editor

---

##  Desktop integration
- [ ] Desktop profile support for GUI apps
- [ ] Auto-generate `.desktop` files (user-level)
- [ ] Remove desktop profiles on uninstall
- [ ] Optional `--no-desktop` flag
- [ ] Validate desktop profiles (`ghostpm doctor`)

---

##  GitHub integration
- [ ] Select asset interactively if ambiguous

---

##  Error handling & UX
- [x] Centralized error handling
- [ ] Consistent exit codes
- [ ] Colored output (optional, e.g. `rich`)
- [ ] Verbose / debug mode (`-v`, `--debug`)
- [ ] Quiet mode (`-q`)
- [ ] Better progress indicator
- [ ] Human-readable error messages with suggestions

---

##  Cache & cleanup
- [x] Package cache directory (`~/.ghostpm/cache`)
- [ ] `ghostpm clean` – remove unused cache files
- [ ] Automatic cache cleanup policy
- [ ] Cache integrity checks

---

##  Diagnostics
- [ ] `ghostpm doctor` – verify:
  - PATH configuration
  - Broken symlinks
  - Missing binaries
  - Desktop entry validity
- [ ] Suggest automatic fixes when possible

---

##  Backup & portability
- [ ] `ghostpm export` – export installed packages + config
- [ ] `ghostpm import` – restore from backup
- [ ] Machine migration support
- [x] Portable config format (JSON)

---

##  Suggested priorities

### High priority (v0.2)
- `ghostpm info`
- `ghostpm list-available`
- Desktop profiles

### Medium priority
- `ghostpm upgrade`
- `ghostpm doctor`
- Cache management

### Low priority
- Export / import
