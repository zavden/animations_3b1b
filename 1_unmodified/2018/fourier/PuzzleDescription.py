# ==============================================================================
# Scene:      PuzzleDescription
# Source:     videos/_2018/fourier.py (lines 4102-4127)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PuzzleDescription.py PuzzleDescription -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PuzzleDescription(Scene):
    def construct(self):
        lines = VGroup(
            OldTexText("Convex set", "$C$", "in $\\mathds{R}^3$"),
            OldTexText("Boundary", "$B$", "$=$", "$\\partial C$"),
            OldTexText("$D$", "$=\\{p+q | p, q \\in B\\}$"),
            OldTexText("Prove that", "$D$", "is convex")
        )
        for line in lines:
            line.set_color_by_tex_to_color_map({
                "$C$" : BLUE_D,
                "\\partial C" : BLUE_D,
                "$B$" : BLUE_C,
                "$D$" : YELLOW,
            })
        VGroup(lines[2][1][2], lines[2][1][6]).set_color(RED)
        VGroup(lines[2][1][4], lines[2][1][8]).set_color(MAROON_B)
        lines[2][1][10].set_color(BLUE_C)
        lines.scale(1.25)
        lines.arrange(DOWN, buff = LARGE_BUFF, aligned_edge = LEFT)

        lines.to_corner(UP+RIGHT)

        for line in lines:
            self.play(Write(line))
            self.wait(2)
