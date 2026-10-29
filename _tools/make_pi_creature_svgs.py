"""Generates the pi creature SVGs in the format that custom/characters/pi_creature.py expects.

The public repo only ships the old `PiCreatures_<mode>.svg` designs, with 6 parts:
    [left_eye, right_eye, left_pupil, right_pupil, body, mouth]
The current code expects `<mode>.svg` exported from Figma, with 12 parts where:
    2, 6 -> iris    8, 9 -> pupils    10 -> body    11 -> mouth
The rest is discarded, so here they are filled with tiny rectangles.

Usage: python make_pi_creature_svgs.py   (writes to _lib/assets/PiCreature)"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path

PI_DIR = Path(__file__).resolve().parents[1] / "_lib" / "assets" / "PiCreature"
SVG_NS = "http://www.w3.org/2000/svg"
DRAWABLE = {"path", "rect", "circle", "ellipse", "polygon", "polyline", "line"}
# How many placeholders to insert before each of the 6 original parts
FILLERS_BEFORE = [2, 3, 1, 0, 0, 0]


def local_name(tag):
    return tag.split("}")[-1]


def drawable_elements(root):
    """Drawable elements in document order, together with their parent."""
    result = []

    def walk(parent):
        for child in list(parent):
            name = local_name(child.tag)
            if name in ("defs", "style", "clipPath", "mask", "title"):
                continue
            if name in DRAWABLE:
                result.append((parent, child))
            else:
                walk(child)

    walk(root)
    return result


def convert(src: Path, dst: Path):
    ET.register_namespace("", SVG_NS)
    ET.register_namespace("xlink", "http://www.w3.org/1999/xlink")
    tree = ET.parse(src)
    parts = drawable_elements(tree.getroot())
    if len(parts) != 6:
        raise ValueError(f"{src.name}: se esperaban 6 partes, hay {len(parts)}")
    for (parent, elem), n_fillers in zip(parts, FILLERS_BEFORE):
        index = list(parent).index(elem)
        for _ in range(n_fillers):
            filler = ET.Element(f"{{{SVG_NS}}}rect", {
                "x": "0", "y": "0", "width": "0.01", "height": "0.01",
                "fill": "none",
            })
            parent.insert(index, filler)
    tree.write(dst, encoding="unicode", xml_declaration=False)


def main():
    for src in sorted(PI_DIR.glob("PiCreatures_*.svg")):
        mode = re.sub(r"^PiCreatures_", "", src.stem)
        convert(src, PI_DIR / f"{mode}.svg")
        print("ok", mode)


if __name__ == "__main__":
    main()
