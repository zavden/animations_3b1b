# ==============================================================================
# Scene:      ThreeDAnswer
# Source:     videos/_2017/putnam.py (lines 1254-1265)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeDAnswer.py ThreeDAnswer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreeDAnswer(Scene):
    def construct(self):
        words = OldTexText(
            "Probability that the tetrahedron contains center:", 
            "$\\frac{1}{8}$"
        )
        words.set_width(FRAME_WIDTH - 1)
        words.to_edge(DOWN)
        words[1].set_color(BLUE)

        self.play(Write(words))
        self.wait(2)
