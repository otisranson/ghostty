# Neon Phosphor

Cyberpunk neon on a 1970s CRT: phosphor-green text on a violet-black tube,
with a curved-glass bloom shader, a boxed two-line bash prompt, and
matching `ls` colours.

## Files and where they go

| File | Install to | What it is |
| --- | --- | --- |
| `config.ghostty`, `ghostty.css`, `shaders/` | `~/.config/ghostty/` | Ghostty theme: palette, CRT shader, 85% opacity, slim title bar |
| `ghostty-fork/output-delay.ghostty` | `~/.config/ghostty-fork/` | **Fork only** (`feature/output-delay` build). Skip it on stock Ghostty |
| `bashrc` | `~/.bashrc` | Boxed two-line prompt with git branch and a red ❯ on failure |
| `dircolors` | `~/.dircolors` | `ls` colours, with directories in amber so they don't clash with the prompt |
| `ghostty-tray/` | `~/.local/bin/` + `~/.config/autostart/` | Optional XFCE tray helper: minimised Ghostty windows go to the tray |
| `tray-icons/build.py` | — | Optional generator for full-colour tray icons |

## Quick install

```sh
mkdir -p ~/.config/ghostty
cp -r config.ghostty ghostty.css shaders ~/.config/ghostty/
cp dircolors ~/.dircolors
cp bashrc ~/.bashrc            # or merge the "Boxed two-line prompt" section into yours

# Fork build only:
mkdir -p ~/.config/ghostty-fork && cp ghostty-fork/output-delay.ghostty ~/.config/ghostty-fork/
```

Reload Ghostty with Ctrl+Shift+, and open a new shell.

## Notes

- **Portable:** the `~/.config/ghostty/` folder works on stock Ghostty as is. The
  fork-only `output-delay` setting is loaded with `config-file = ?...`, and the
  `?` makes Ghostty skip it silently when the file is missing.
- **Ghostty 1.2+** is needed for the `config.ghostty` filename. Older versions read `config`.
- **Font:** IBM Plex Mono (`sudo apt install fonts-ibm-plex`), with DejaVu Sans Mono as the fallback.
- **Linux/GTK only:** the `gtk-*` options and `ghostty.css`. Everything else works on any platform.
- **Blue is amber:** palette slots 4 and 12 are amber, so apps that use ANSI blue
  (e.g. Claude Code's `dark-ansi` theme) match the amber `ls` directories. The prompt
  path uses a fixed true-colour blue, so it stays blue.
- **Opacity:** `background-opacity` in `config.ghostty` and the alpha in
  `ghostty.css` are linked. Change both together.
