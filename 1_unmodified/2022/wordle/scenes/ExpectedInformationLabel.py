# ==============================================================================
# Scene:      ExpectedInformationLabel
# Source:     videos/_2022/wordle/scenes.py (lines 2276-2288)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpectedInformationLabel.py ExpectedInformationLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ExpectedInformationLabel(Scene):
    def construct(self):
        eq = OldTex(
            "E[\\text{Information}] = ",
            "\\sum_x p(x) \\cdot \\text{Information}(x)",
            tex_to_color_map={
                "\\text{Information}": YELLOW,
            },
            font_size=60
        )
        eq.to_edge(UP)
        self.play(Write(eq))
        self.wait()
