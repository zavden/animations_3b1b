# ==============================================================================
# Scene:      DistillationArrow
# Source:     videos/_2026/cross_entropy/part2_supplements.py (lines 418-432)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DistillationArrow.py DistillationArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DistillationArrow(InteractiveScene):
    def construct(self):
        # Test
        arrow = Line(3 * UP, 4 * LEFT, path_arc=90 * DEG, buff=0.1, stroke_width=10)
        arrow.add_tip()
        arrow.set_color(TEAL)
        word = Text("Distillation", font_size=72)
        word.set_backstroke(BLACK, 5)
        word.next_to(arrow.pfp(0.5), UL)

        self.play(
            ShowCreation(arrow),
            FadeIn(word, 0.5 * LEFT, lag_ratio=0.05),
        )
        self.wait()
