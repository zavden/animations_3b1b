# ==============================================================================
# Scene:      ExpectedScoreEqualsQMark
# Source:     videos/_2019/hyperdarts.py (lines 2763-2777)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpectedScoreEqualsQMark.py ExpectedScoreEqualsQMark -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExpectedScoreEqualsQMark(Scene):
    def construct(self):
        equation = OldTexText(
            "\\textbf{E}[Score] = ???",
            tex_to_color_map={
                "???": YELLOW,
            }
        )
        aka = OldTexText("a.k.a. Long-term average")
        aka.next_to(equation, DOWN)

        self.play(Write(equation))
        self.wait(2)
        self.play(FadeIn(aka, UP))
        self.wait()
