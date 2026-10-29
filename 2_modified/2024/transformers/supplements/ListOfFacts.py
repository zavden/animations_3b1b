# ==============================================================================
# Scene:      ListOfFacts
# Source:     videos/_2024/transformers/supplements.py (lines 2212-2252)
# Category:   2 · Renders with modifications
# Includes code copied from: _2024/transformers/helpers.py
#
# Run from this folder:
#     manimgl ListOfFacts.py ListOfFacts -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - DATA_DIR points to _lib/data (in the original, to Grant's output folder)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from pathlib import Path


# ----- From _2024/transformers/helpers.py -----

# CHANGE: the data lives in _lib/data (in the original, in Grant's output folder)
DATA_DIR = Path(get_directories()["data"], "2024/transformers/data/")



# ----- From _2024/transformers/supplements.py -----

class ListOfFacts(InteractiveScene):
    def construct(self):
        # Title
        title = Text("Facts", font_size=120)
        title.to_corner(UL, buff=0.75)
        underline = Underline(title)
        underline.scale(1.3)
        underline.set_stroke(width=(0, 5, 5, 5, 0))
        title.add(underline)
        self.add(title)

        # List of facts
        n_facts = 15
        facts = VGroup(
            Text(line)
            for line in Path(DATA_DIR, "facts.txt").read_text().split("\n")[:n_facts]
        )
        facts.set_color(GREY_A)
        facts.arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        facts.set_height(5.5)
        facts.next_to(title, DOWN, buff=0.5).align_to(title[0], LEFT)
        self.add(facts)

        # Add line to LLM
        vline = Line(UP, DOWN).replace(facts, dim_to_match=1)
        vline.next_to(facts, RIGHT, buff=2.0)
        vline.scale(0.7)

        lines = VGroup(
            Line(
                fact.get_right(),
                vline.pfp(a),
                path_arc=interpolate(-20, 20, a) * DEGREES,
                color=random_bright_color(hue_range=(0.1, 0.2))
            ).insert_n_curves(20).set_stroke(width=(0, 5, 5, 0))
            for fact, a in zip(
                facts,
                np.linspace(0, 1, len(facts))
            )
        )
        self.add(lines)
