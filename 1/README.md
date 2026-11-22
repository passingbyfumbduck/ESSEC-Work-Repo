# Shell and Python setup

Run these in your own terminal to see the current shell, the configured login shell, and the Python version.

```sh
ps -p "$$" -o comm=
printf '%s\n' "$SHELL"
python3 --version
```

For Bash, install [Oh My Bash](https://github.com/ohmybash/oh-my-bash) and set `OSH_THEME="font"` in `~/.bashrc`. For Zsh, install [Oh My Zsh](https://github.com/ohmyzsh/ohmyzsh) and set `ZSH_THEME="robbyrussell"` in `~/.zshrc`. Add `git` to the existing `plugins=(...)` list before the framework loads. Run `source ~/.bashrc` or `source ~/.zshrc` in the matching shell. The `source` command executes the file in your current shell so the aliases and prompt take effect immediately. Check the prompt and compare `gst` with `git status` inside a repository.

From this folder, run `./env_install.sh` on macOS with Homebrew or on Debian/Ubuntu with apt. It installs missing tools, checks Python and pip, installs Notebook in a local virtual environment, and runs Homebrew diagnostics on macOS. Launch it with `.venv/bin/jupyter notebook`.
