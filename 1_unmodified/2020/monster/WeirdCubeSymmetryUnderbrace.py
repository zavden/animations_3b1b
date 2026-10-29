# ==============================================================================
# Scene:      WeirdCubeSymmetryUnderbrace
# Source:     videos/_2020/monster.py (lines 1032-1042)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WeirdCubeSymmetryUnderbrace.py WeirdCubeSymmetryUnderbrace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WeirdCubeSymmetryUnderbrace(Scene):
    def construct(self):
        brace = Brace(Line(LEFT, RIGHT).set_width(3), DOWN)
        tex = brace.get_tex("(8^6)(6!)")
        VGroup(brace, tex).set_color(WHITE)
        VGroup(brace, tex).set_stroke(BLACK, 8, background=True)
        self.play(
            GrowFromCenter(brace),
            FadeIn(tex, 0.25 * UP)
        )
        self.wait()
