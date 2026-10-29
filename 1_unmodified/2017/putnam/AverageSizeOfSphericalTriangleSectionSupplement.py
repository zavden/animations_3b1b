# ==============================================================================
# Scene:      AverageSizeOfSphericalTriangleSectionSupplement
# Source:     videos/_2017/putnam.py (lines 790-800)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AverageSizeOfSphericalTriangleSectionSupplement.py AverageSizeOfSphericalTriangleSectionSupplement -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AverageSizeOfSphericalTriangleSectionSupplement(Scene):
    def construct(self):
        words = OldTexText(
            "Average size of \\\\", "this section", "?",
            arg_separator = ""
        )
        words.set_color_by_tex("section", GREEN)
        words.set_width(FRAME_WIDTH - 1)
        words.to_edge(DOWN)
        self.play(Write(words))
        self.wait(3)
