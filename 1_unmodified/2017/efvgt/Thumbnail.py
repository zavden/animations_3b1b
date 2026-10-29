# ==============================================================================
# Scene:      Thumbnail
# Source:     videos/_2017/efvgt.py (lines 3354-3369)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Thumbnail.py Thumbnail -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Thumbnail(Scene):
    def construct(self):
        formula = OldTex("e^", "{\\pi i}", "=", "-1")
        formula[1].set_color(GREEN_B)
        formula[3].set_color(YELLOW)
        formula.scale(4)
        formula.to_edge(UP, buff = LARGE_BUFF)
        self.add(formula)

        via = OldTexText("via")
        via.scale(2)
        groups = OldTexText("Group theory")
        groups.scale(3)
        groups.to_edge(DOWN)
        via.move_to(VGroup(formula, groups))
        self.add(via, groups)
