# ==============================================================================
# Scene:      BorweinIntegrals
# Source:     videos/outside_videos/talk_scenes.py (lines 145-203)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BorweinIntegrals.py BorweinIntegrals -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BorweinIntegrals(Scene):
    def construct(self):
        ints = VGroup(
            OldTex(
                "\\int_0^\\infty",
                "\\frac{\\sin(x)}{x}",
                "dx = \\frac{\\pi}{2}"
            ),
            OldTex(
                "\\int_0^\\infty",
                "\\frac{\\sin(x)}{x}",
                "\\frac{\\sin(x/3)}{x/3}",
                "dx = \\frac{\\pi}{2}"
            ),
            OldTex(
                "\\int_0^\\infty",
                "\\frac{\\sin(x)}{x}",
                "\\frac{\\sin(x/3)}{x/3}",
                "\\frac{\\sin(x/5)}{x/5}",
                "dx = \\frac{\\pi}{2}"
            ),
            OldTex("\\vdots"),
            OldTex(
                "\\int_0^\\infty",
                "\\frac{\\sin(x)}{x}",
                "\\frac{\\sin(x/3)}{x/3}",
                "\\frac{\\sin(x/5)}{x/5}",
                "\\dots",
                "\\frac{\\sin(x/13)}{x/13}",
                "dx = \\frac{\\pi}{2}"
            ),
            OldTex(
                "\\int_0^\\infty",
                "\\frac{\\sin(x)}{x}",
                "\\frac{\\sin(x/3)}{x/3}",
                "\\frac{\\sin(x/5)}{x/5}",
                "\\dots",
                "\\frac{\\sin(x/13)}{x/13}",
                "\\frac{\\sin(x/15)}{x/15}",
                "dx = \\frac{\\pi}{2}",
                "- 0.0000000000231006..."
            ),
        )

        ints.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=RIGHT)
        ints.set_height(FRAME_HEIGHT - 1)
        ints[-1][:-1].align_to(ints[:-1], RIGHT)
        ints[-1][-1].next_to(ints[-1][:-1], RIGHT, SMALL_BUFF)
        ints[3].shift(SMALL_BUFF * LEFT)
        ints.center()

        for integral in ints:
            integral.set_color_by_tex("\\sin(x)", BLUE)
            integral.set_color_by_tex("x/3", TEAL)
            integral.set_color_by_tex("x/5", GREEN)
            integral.set_color_by_tex("x/13", YELLOW)
            integral.set_color_by_tex("x/15", RED_B)

        self.add(ints)
