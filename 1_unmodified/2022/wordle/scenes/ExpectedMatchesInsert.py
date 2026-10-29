# ==============================================================================
# Scene:      ExpectedMatchesInsert
# Source:     videos/_2022/wordle/scenes.py (lines 1817-1827)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpectedMatchesInsert.py ExpectedMatchesInsert -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExpectedMatchesInsert(Scene):
    def construct(self):
        tex = OldTex(
            "\\sum_{x} p(x) \\big(\\text{\\# Matches}\\big)",
            tex_to_color_map={"\\text{\\# Matches}": GREEN}
        )
        cross = Cross(tex).scale(1.25)
        self.play(Write(tex))
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()
