# ==============================================================================
# Scene:      Nicheness
# Source:     videos/_2021/some1.py (lines 1045-1061)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Nicheness.py Nicheness -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Nicheness(Scene):
    def construct(self):
        words = OldTexText(
            "Perceived ", "nicheness",
            " $>$ ",
            "Actual ", "nichness",
        )
        words[:2].set_color(BLUE_B)
        words[3:].set_color(BLUE_D)

        self.add(words[:2])
        self.wait()
        self.play(
            FadeTransformPieces(words[:2].copy(), words[3:], path_arc=PI / 2),
            GrowFromCenter(words[2]),
        )
        self.wait()
