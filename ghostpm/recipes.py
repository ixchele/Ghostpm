RECIPES = {
    "nvim": {
        "type": "tar",
        "url": "https://github.com/neovim/neovim/releases/latest/download/nvim-linux-x86_64.tar.gz",
        "bin": ["bin/nvim"],
        "desc": "Neovim editor",
    },
    "bat": {
        "type": "deb",
        "url": "https://github.com/sharkdp/bat/releases/download/v0.25.0/bat_0.25.0_amd64.deb",
        "bin": ["usr/bin/bat"],
        "desc": "A cat clone with syntax highlighting",
    },
    "fzf": {
        "type": "tar",
        "url": "https://github.com/junegunn/fzf/releases/download/v0.67.0/fzf-0.67.0-linux_amd64.tar.gz",
        "bin": ["fzf"],
        "desc": "Command-line fuzzy finder",
    },
    "ripgrep": {
        "type": "tar",
        "url": "https://github.com/BurntSushi/ripgrep/releases/download/14.1.1/ripgrep-14.1.1-x86_64-unknown-linux-musl.tar.gz",
        "bin": ["rg"],
        "desc": "Fast recursive search tool",
    },
    "fd": {
        "type": "tar",
        "url": "https://github.com/sharkdp/fd/releases/download/v10.2.0/fd-v10.2.0-x86_64-unknown-linux-musl.tar.gz",
        "bin": ["fd"],
        "desc": "Simple and fast find alternative",
    },
    "zoxide": {
        "type": "tar",
        "url": "https://github.com/ajeetdsouza/zoxide/releases/download/v0.9.7/zoxide-0.9.7-x86_64-unknown-linux-musl.tar.gz",
        "bin": ["zoxide"],
        "desc": "Smarter cd command",
    },
    "hyperfine": {
        "type": "tar",
        "url": "https://github.com/sharkdp/hyperfine/releases/download/v1.19.0/hyperfine-v1.19.0-x86_64-unknown-linux-musl.tar.gz",
        "bin": ["hyperfine"],
        "desc": "Command-line benchmarking tool",
    },
    "dust": {
        "type": "tar",
        "url": "https://github.com/bootandy/dust/releases/download/v0.8.6/dust-v0.8.6-x86_64-unknown-linux-musl.tar.gz",
        "bin": ["dust"],
        "desc": "More intuitive du",
    },
    "delta": {
        "type": "tar",
        "url": "https://github.com/dandavison/delta/releases/download/0.17.0/delta-0.17.0-x86_64-unknown-linux-musl.tar.gz",
        "bin": ["delta"],
        "desc": "Syntax-highlighting pager for git",
    },
    "eza": {
        "type": "tar",
        "url": "https://github.com/eza-community/eza/releases/download/v0.18.8/eza_x86_64-unknown-linux-musl.tar.gz",
        "bin": ["eza"],
        "desc": "Modern replacement for ls with tree support",
    },
    "gh": {
        "type": "tar",
        "url": "https://github.com/cli/cli/releases/download/v2.83.2/gh_2.83.2_linux_amd64.tar.gz",
        "bin": ["bin/gh"],
        "desc": "cli for github"
    },
    "rainbow": {
        "type": "tar",
        "url": "https://github.com/arsham/rainbow/releases/download/v1.2.1/figurine_linux_v1.2.1.tar.gz",
        "bin": ["rainbow"],
        "desc": "rainbow cat"
    },
    # "zed": {
    #     "type": "tar",
    #     "url": "https://github.com/zed-industries/zed/releases/download/v0.217.3/zed-linux-x86_64.tar.gz",
    #     "bin": ["bin/zed"],
    #     "desc": "zed editor"
    # },
    "brave": {
        "type": "deb",
        "url": "https://github.com/brave/brave-browser/releases/download/v1.78.97/brave-browser_1.78.97_amd64.deb",
        "bin": ["opt/brave.com/brave/brave"],
        "desktop": {
            "name": "Brave Browser",
            "icon": "",
            "categories": "Network;WebBrowser;",
            "terminal": False,
        },
    },
    "kitty": {
        "type": "tar",
        "url": "https://github.com/kovidgoyal/kitty/releases/download/v0.45.0/kitty-0.45.0-x86_64.txz",
        "bin": ["bin/kitty"],
        "desktop": {
            "name": "kitty",
            "icon": "kitty",
            "categories": "System;TerminalEmulator;",
            "terminal": False,
        },
    },
}
