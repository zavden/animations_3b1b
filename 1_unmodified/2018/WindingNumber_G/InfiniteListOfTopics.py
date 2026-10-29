# ==============================================================================
# Scene:      InfiniteListOfTopics
# Source:     videos/_2018/WindingNumber_G.py (lines 2987-3012)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/WindingNumber.py, _2018/uncertainty.py
#
# Run from this folder:
#     manimgl InfiniteListOfTopics.py InfiniteListOfTopics -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath


# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2018/WindingNumber.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7



# ----- From _2018/WindingNumber_G.py -----

class InfiniteListOfTopics(Scene):
    def construct(self):
        rect = Rectangle(width = 5, height = 7)
        rect.to_edge(RIGHT)
        title = OldTexText("Infinite list \\\\ of topics")
        title.next_to(rect.get_top(), DOWN)
        lines = VGroup(*[
            OldTexText(words).scale(0.5)
            for words in [
                "Winding number",
                "Laplace transform",
                "Wallis product",
                "Quantum information",
                "Elliptic curve cryptography",
                "Strange attractors",
                "Convolutional neural networks",
                "Fixed points",
            ]
        ] + [Tex("\\vdots")])
        lines.arrange(DOWN, buff = MED_SMALL_BUFF, aligned_edge = LEFT)
        lines.next_to(title, DOWN, MED_LARGE_BUFF)
        lines[-1].next_to(lines[-2], DOWN)

        self.add(rect, title)
        self.play(LaggedStartMap(FadeIn, lines, run_time = 5))
        self.wait()
