# ==============================================================================
# Scene:      WriteCurlEquations
# Source:     videos/_2017/waves.py (lines 953-982)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteCurlEquations.py WriteCurlEquations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


E_COLOR = BLUE


M_COLOR = YELLOW


class WriteCurlEquations(Scene):
    def construct(self):
        eq1 = OldTex(
            "\\nabla \\times", "\\textbf{E}", "=",
            "-\\frac{1}{c}", 
            "\\frac{\\partial \\textbf{B}}{\\partial t}"
        )
        eq2 = OldTex(
            "\\nabla \\times", "\\textbf{B}", "=^*",
            "\\frac{1}{c}", 
            "\\frac{\\partial \\textbf{E}}{\\partial t}"
        )
        eqs = VGroup(eq1, eq2)
        eqs.arrange(DOWN, buff = LARGE_BUFF)
        eqs.set_height(FRAME_HEIGHT - 1)
        eqs.to_edge(LEFT)
        for eq in eqs:
            eq.set_color_by_tex_to_color_map({
                "E" : E_COLOR,            
                "B" : M_COLOR,
            })
        footnote = OldTexText("*Ignoring currents")
        footnote.next_to(eqs[1], RIGHT)
        footnote.to_edge(RIGHT)

        self.play(Write(eq1, run_time = 2))
        self.wait(3)
        self.play(Write(eq2, run_time = 2))
        self.play(FadeIn(footnote))
        self.wait(3)
