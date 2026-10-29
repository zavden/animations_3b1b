"""Generates placeholder assets for images that are not in the public repo
(they lived in Grant's Dropbox). They are always visibly marked as placeholders.

Usage:
    python placeholder.py image <output.png> --label "Photo of X" [--size 1920x1080] [--bg "#333"]
    python placeholder.py page  <output.png> --title "IMO 2025 · page 1" [--lines 38]
    python placeholder.py svg   <output.svg> [--size 200x200]"""
import argparse
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT_PATHS = [
    "/usr/share/fonts/cm-unicode/cmunrm.otf",
    "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans.ttf",
]


def font(size):
    for p in FONT_PATHS:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


def parse_size(s):
    w, h = s.lower().split("x")
    return int(w), int(h)


def make_image(out, label, size, bg):
    w, h = size
    img = Image.new("RGB", size, bg)
    d = ImageDraw.Draw(img)
    pad = max(6, min(w, h) // 30)
    d.rectangle([pad, pad, w - pad, h - pad], outline="#888888", width=max(2, pad // 3))
    d.line([pad, pad, w - pad, h - pad], fill="#555555", width=2)
    d.line([pad, h - pad, w - pad, pad], fill="#555555", width=2)
    f = font(max(14, min(w, h) // 12))
    text = f"{label}\n[imagen de relleno]"
    box = d.multiline_textbbox((0, 0), text, font=f, align="center")
    tw, th = box[2] - box[0], box[3] - box[1]
    d.rectangle([(w - tw) / 2 - 12, (h - th) / 2 - 10, (w + tw) / 2 + 12, (h + th) / 2 + 14], fill=bg)
    d.multiline_text(((w - tw) / 2, (h - th) / 2), text, font=f, fill="#dddddd", align="center")
    img.save(out)


def make_page(out, title, n_lines, seed):
    w, h = 1700, 2200  # letter proportion
    img = Image.new("RGB", (w, h), "white")
    d = ImageDraw.Draw(img)
    d.text((w / 2, 160), title, font=font(54), fill="black", anchor="mm")
    d.text((w / 2, 240), "[página de relleno]", font=font(36), fill="#888888", anchor="mm")
    rng = random.Random(seed)
    y = 360
    for i in range(n_lines):
        if i % 8 == 0:
            y += 40  # spacing between "problems"
            d.text((150, y), f"Problem {i // 8 + 1}.", font=font(40), fill="black", anchor="lm")
            y += 60
        length = rng.uniform(0.55, 0.95) if (i % 8) != 7 else rng.uniform(0.2, 0.5)
        d.rounded_rectangle([150, y - 9, 150 + length * (w - 300), y + 9], radius=8, fill="#c8c8c8")
        y += 46
        if y > h - 150:
            break
    img.save(out)


def make_svg(out, size):
    w, h = size
    Path(out).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
        f'<rect x="2" y="2" width="{w - 4}" height="{h - 4}" rx="{min(w, h) / 10}" fill="#888888"/>'
        f'<path d="M {w * .25} {h * .25} L {w * .75} {h * .75} M {w * .75} {h * .25} L {w * .25} {h * .75}" '
        f'stroke="#333333" stroke-width="{min(w, h) / 15}" fill="none"/></svg>'
    )


def main():
    p = argparse.ArgumentParser()
    p.add_argument("kind", choices=["image", "page", "svg"])
    p.add_argument("out")
    p.add_argument("--label", default="")
    p.add_argument("--title", default="")
    p.add_argument("--size", default="1920x1080")
    p.add_argument("--bg", default="#333333")
    p.add_argument("--lines", type=int, default=38)
    p.add_argument("--seed", type=int, default=0)
    a = p.parse_args()
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    if a.kind == "image":
        make_image(a.out, a.label, parse_size(a.size), a.bg)
    elif a.kind == "page":
        make_page(a.out, a.title, a.lines, a.seed)
    else:
        make_svg(a.out, parse_size(a.size))


if __name__ == "__main__":
    main()
