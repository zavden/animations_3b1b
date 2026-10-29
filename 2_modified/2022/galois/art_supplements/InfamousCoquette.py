# ==============================================================================
# Scene:      InfamousCoquette
# Source:     videos/_2022/galois/art_supplements.py (lines 121-132)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl InfamousCoquette.py InfamousCoquette -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - A light background is added (FullScreenRectangle): the text is black and in the video it goes over a light illustration; on a black background it was not visible
# ==============================================================================

from manim_imports_ext import *

class InfamousCoquette(InteractiveScene):
    def construct(self):
        # CHANGE: the text is black (in the video it goes over a light illustration); without a light background it would not be visible on the black background
        self.add(FullScreenRectangle(fill_color="#D8CBA8", fill_opacity=1))

        # Write quote
        quote = OldTexText(
            "``I die the victim of an infamous coquette and her two dupes.''",
        )
        quote.to_edge(UP)
        quote.set_width(FRAME_WIDTH - 1)
        quote.set_stroke(BLACK, 0)
        quote.set_fill(BLACK)
        self.play(Write(quote, run_time=3))
        self.wait()
