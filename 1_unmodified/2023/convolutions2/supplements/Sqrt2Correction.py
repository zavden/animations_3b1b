# ==============================================================================
# Scene:      Sqrt2Correction
# Source:     videos/_2023/convolutions2/supplements.py (lines 594-617)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Sqrt2Correction.py Sqrt2Correction -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class Sqrt2Correction(InteractiveScene):
    def construct(self):
        # Test
        words = TexText(R"Technically, this shape is $\sqrt{2}$ times wider than this shape")
        shape_words = words["this shape"]
        words.to_edge(UP, buff=0.5)

        points = [
            [-3.75, 0.25, 0],
            [2.5, -2.5, 0],
        ]
        colors = [YELLOW, TEAL]
        arrows = VGroup()
        for word, point, color in zip(shape_words, points, colors):
            word.set_color(color)
            arrow = FillArrow(word[:4].get_bottom(), point)
            arrow.scale(0.9)
            arrow.set_fill(color, 1)
            arrow.set_backstroke()
            arrows.add(arrow)

        self.play(FadeIn(words, lag_ratio=0.1))
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.5))
        self.wait()
