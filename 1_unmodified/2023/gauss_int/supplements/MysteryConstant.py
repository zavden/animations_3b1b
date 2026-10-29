# ==============================================================================
# Scene:      MysteryConstant
# Source:     videos/_2023/gauss_int/supplements.py (lines 528-545)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MysteryConstant.py MysteryConstant -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MysteryConstant(InteractiveScene):
    def construct(self):
        eq_C = Tex("= C", t2c={"C": RED}, font_size=24)
        eq_C.to_edge(UP).shift(3 * LEFT)

        words = Text("Mystery Constant", font_size=56)
        words.set_color(RED)
        words.next_to(ORIGIN, RIGHT)
        words.to_edge(UP)

        arrow = Arrow(words, eq_C, stroke_color=RED)

        self.play(
            Write(words),
            FadeIn(eq_C, LEFT),
            GrowArrow(arrow)
        )
        self.wait()
