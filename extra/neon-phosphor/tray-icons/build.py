#!/usr/bin/env python3
"""Build ~/.local/share/icons/NeonPhosphor-Icons: full-colour tray icons.

The XFCE tray plugins (pulseaudio, notifications, power manager) ask for
"-symbolic" icon names, which GTK paints in one flat colour. This theme
answers those names with full-colour Papirus pictures rendered to PNG.
GTK only treats "-symbolic.svg" / ".symbolic.png" files as symbolic, so a
"-symbolic.png" keeps its colours. Everything else is inherited from
Papirus-Dark. Re-run after a Papirus update:  python3 build.py
"""
import os, shutil, subprocess
from pathlib import Path
import gi
gi.require_version("GdkPixbuf", "2.0")
from gi.repository import GdkPixbuf
from PIL import Image, ImageDraw, ImageEnhance

SRC = Path.home() / ".local/share/icons/Papirus-Dark/48x48"  # Papirus-Dark install location
OUT = Path.home() / ".local/share/icons/NeonPhosphor-Icons"
SIZES = [16, 22, 24, 32, 48]
RED, MAGENTA = (255, 46, 99, 255), (255, 43, 214, 255)

def render(rel, size):
    pb = GdkPixbuf.Pixbuf.new_from_file_at_size(str(SRC / f"{rel}.svg"), size, size)
    ok, buf = pb.save_to_bufferv("png", [], [])
    from io import BytesIO
    return Image.open(BytesIO(buf)).convert("RGBA")

def dimmed(im):
    g = ImageEnhance.Color(im).enhance(0.15)
    return ImageEnhance.Brightness(g).enhance(0.7)

def badge(im, colour, cross=False):
    im = im.copy(); s = im.size[0]; r = max(3, s * 0.42)
    d = ImageDraw.Draw(im)
    box = (s - r, s - r, s - 1, s - 1)
    d.ellipse(box, fill=colour, outline=(10, 6, 20, 255), width=max(1, s // 24))
    if cross:
        p = r * 0.3; w = max(1, s // 14)
        d.line((box[0] + p, box[1] + p, box[2] - p, box[3] - p), fill="white", width=w)
        d.line((box[0] + p, box[3] - p, box[2] - p, box[1] + p), fill="white", width=w)
    return im

# name -> function(size) -> Image
ICONS = {}
def add(names, fn):
    for n in names: ICONS[n] = fn

# Volume: speaker picture; muted = greyed speaker with a red x
add([f"audio-volume-{l}-symbolic" for l in ("high", "medium", "low")] + ["audio-volume-high", "audio-volume-medium", "audio-volume-low"],
    lambda s: render("devices/audio-speakers", s))
add(["audio-volume-muted-symbolic", "audio-volume-muted"],
    lambda s: badge(dimmed(render("devices/audio-speakers", s)), RED, cross=True))

# Notifications: yellow bell; new = magenta dot; disabled = Papirus muted bell
bell = lambda s: render("apps/bell", s)
add(["notification-symbolic", "notifications-symbolic"], bell)
add(["notification-new-symbolic", "notifications-new-symbolic"], lambda s: badge(bell(s), MAGENTA))
add(["notification-disabled-symbolic", "notifications-disabled-symbolic",
     "notification-disabled-new-symbolic", "notification-new-disabled-symbolic",
     "notifications-disabled-new-symbolic", "notifications-new-disabled-symbolic"],
    lambda s: render("status/notification-disabled", s))

# Battery (xfce4-power-manager: battery-level-NN[-charging|-charged]-symbolic)
def batt(level, charging):
    state = "caution" if level <= 10 else "low" if level <= 30 else "good" if level <= 70 else "full"
    return f"status/battery-{state}" + ("-charging" if charging else "")
for lvl in range(0, 101, 10):
    add([f"battery-level-{lvl}-symbolic"], (lambda r: lambda s: render(r, s))(batt(lvl, False)))
    add([f"battery-level-{lvl}-charging-symbolic"], (lambda r: lambda s: render(r, s))(batt(lvl, True)))
add(["battery-level-100-charged-symbolic", "battery-full-charged-symbolic"], lambda s: render("status/battery-full-charged", s))
add(["battery-missing-symbolic"], lambda s: render("status/battery-missing", s))
add(["ac-adapter-symbolic", "ac-adapter"], lambda s: render("status/battery-ac-adapter", s))

# Network (nm-applet via the systray; needs systray symbolic-icons = false)
wired = lambda s: render("devices/network-wired", s)
wifi = lambda s: render("devices/network-wireless", s)
add(["nm-device-wired", "nm-device-wired-symbolic", "network-wired-symbolic"], wired)
add(["nm-no-connection", "nm-no-connection-symbolic", "network-offline-symbolic"],
    lambda s: badge(dimmed(wired(s)), RED, cross=True))
add(["nm-device-wireless"] + [f"nm-signal-{n}" for n in ("00", "25", "50", "75", "100")], wifi)

if OUT.exists(): shutil.rmtree(OUT)
dirs = []
for size in SIZES:
    d = OUT / f"{size}x{size}" / "status"; d.mkdir(parents=True)
    dirs.append(f"{size}x{size}/status")
    for name, fn in ICONS.items():
        fn(size).save(d / f"{name}.png")
(OUT / "index.theme").write_text(
    "[Icon Theme]\nName=NeonPhosphor-Icons\nComment=Full-colour tray icons over Papirus-Dark\n"
    "Inherits=Papirus-Dark,hicolor\nDirectories=" + ",".join(dirs) + "\n\n" +
    "".join(f"[{d}]\nSize={d.split('x')[0]}\nContext=Status\nType=Fixed\n\n" for d in dirs))
if shutil.which("gtk-update-icon-cache"):
    subprocess.run(["gtk-update-icon-cache", "-q", "-f", str(OUT)], check=False)
print(f"wrote {len(ICONS)} icons x {len(SIZES)} sizes to {OUT}")
