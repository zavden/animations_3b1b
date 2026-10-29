# ==============================================================================
# Scene:      CornerDistance
# Source:     videos/_2026/spheres_talk/supplements.py (lines 125-139)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CornerDistance.py CornerDistance -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CornerDistance(InteractiveScene):
    def construct(self):
        words = Text("Distance to corner")
        pythag = Tex(R"\sqrt{1^2 + 1^2 + \cdots + 1^2 + 1^2}")
        sqrt3 = Tex(R"= \sqrt{N}")
        r_eq = Tex(R"r = \sqrt{N} - 1")

        words.move_to(2 * UP)
        equals = Tex(R"=", font_size=72).rotate(90 * DEG)
        equals.next_to(words, DOWN)
        pythag.next_to(equals, DOWN)
        sqrt3.next_to(pythag, RIGHT)
        r_eq.next_to(pythag, DOWN, buff=LARGE_BUFF)

        self.add(words, equals, pythag, sqrt3, r_eq)
