# ==============================================================================
# Scene:      LevelsOfUnderstanding
# Source:     videos/_2025/laplace/main_supplements.py (lines 58-79)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LevelsOfUnderstanding.py LevelsOfUnderstanding -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LevelsOfUnderstanding(InteractiveScene):
    def construct(self):
        items = BulletedList(
            "1) Use",
            "2) Dissect",
            "3) Reinvent",
            font_size=72,
            buff=2
        )
        numbers = VGroup()
        words = VGroup()
        for item in items:
            item[0].scale(0).set_opacity(0)
            numbers.add(item[1:3])
            words.add(item[3:])
        items.to_edge(LEFT)

        self.play(LaggedStartMap(FadeIn, numbers, shift=DOWN, lag_ratio=0.35))
        self.wait()
        for word in words:
            self.play(Write(word))
            self.wait()
