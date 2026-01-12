![logo](https://raw.githubusercontent.com/ixchele/Ghostpm/refs/heads/main/Logo.png)

# 👻 ghostpm

**ghostpm** is a user-space package manager for Linux.  
It allows you to install CLI tools and applications **without sudo**, directly in your home directory.

Designed for restricted environments (schools, shared machines, servers), ghost installs portable binaries from curated recipes or GitHub releases.

---

## Features

-  Install packages without root privileges
-  Supports official ghost recipes and GitHub repositories (`owner/repo`)
-  Safe by design: no system files are modified

---

## Installation

### Using pipx (recommended)

```bash
pipx install git+https://github.com/ixchele/Ghostpm.git
```
This installs the ghost command globally in user space.

### From source

```bash
git clone https://github.com/ixchele/Ghostpm
cd ghostpm
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

---

## Usage

### Install a package from ghostpm recipes

```bash
ghostpm install bat
ghostpm install nvim
```

### Install directly from Github

```bash
ghostpm install sharkdp/bat
ghostpm install junegunn/fzf
```

### List installed packages

```bash
ghostpm list
```

### Remove a package

```bash
ghostpm remove bat
```

---

## Configuraion

```txt
~/.ghostpm/
└── config.json
```
contain root path

---

##  Limitations

**ghostpm** does not install system libraries\
Some binaries may fail due to system incompatibilities (e.g. GLIBC version)\
.deb / .rpm packages are not supported\
Compilation from source is out of scope\
...

---

##  Roadmap

Planned features:
   - ghost search
   - ghost upgrade
   - version tracking
   - cache management
   - export / import\
See [TODO.md](https://github.com/ixchele/Ghostpm/blob/dev/TODO.md) for the full roadmap.

---

## Contributing

Contributions are welcome!\
Open issues for bugs or ideas\
Keep features small and focused\

---

## License

MIT License
