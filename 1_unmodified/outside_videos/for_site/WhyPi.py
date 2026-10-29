# ==============================================================================
# Scene:      WhyPi
# Source:     videos/outside_videos/for_site.py (lines 4-36)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhyPi.py WhyPi -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhyPi(Scene):
    def construct(self):
        title = OldTexText("Why $\\pi$?")
        title.scale(3)
        title.to_edge(UP)

        formula1 = OldTex(
            "1 +"
            "\\frac{1}{4} +"
            "\\frac{1}{9} +"
            "\\frac{1}{16} +"
            "\\frac{1}{25} + \\cdots"
            "=\\frac{\\pi^2}{6}"
        )
        formula1.set_color(YELLOW)
        formula1.set_width(FRAME_WIDTH - 2)
        formula1.next_to(title, DOWN, MED_LARGE_BUFF)

        formula2 = OldTex(
            "1 -"
            "\\frac{1}{3} +"
            "\\frac{1}{5} -"
            "\\frac{1}{7} +"
            "\\frac{1}{9} - \\cdots"
            "=\\frac{\\pi}{4}"
        )
        formula2.set_color(BLUE_C)
        formula2.set_width(FRAME_WIDTH - 2)
        formula2.next_to(formula1, DOWN, LARGE_BUFF)

        self.add(title)
        self.add(formula1)
        self.add(formula2)
