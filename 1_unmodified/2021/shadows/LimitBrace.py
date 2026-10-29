# ==============================================================================
# Scene:      LimitBrace
# Source:     videos/_2021/shadows.py (lines 5163-5173)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LimitBrace.py LimitBrace -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LimitBrace(Scene):
    def construct(self):
        brace = Brace(Line().set_width(3), UP)
        tex = brace.get_tex("n \\to \\infty")
        VGroup(brace, tex).set_color(TEAL)
        VGroup(brace, tex).set_backstroke()
        self.play(
            GrowFromCenter(brace),
            FadeIn(tex, shift=0.25 * UP)
        )
        self.wait()
