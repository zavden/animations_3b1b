# ==============================================================================
# Scene:      CylinderAreaAnnotation
# Source:     videos/_2024/puzzles/supplements.py (lines 246-271)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CylinderAreaAnnotation.py CylinderAreaAnnotation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CylinderAreaAnnotation(InteractiveScene):
    def construct(self):
        # Test
        expr = Tex(R"\text{Area} = 2 \pi R \cdot d")
        expr.to_corner(UL)
        circum_brace = Brace(expr[R"2 \pi R"])
        circum_label = Text("Circumference", font_size=30)
        circum_label.next_to(circum_brace, DOWN, SMALL_BUFF)

        thickness_rect = SurroundingRectangle(expr["d"])
        thickness_rect.set_stroke(BLUE)
        thickness_label = Text("Thickness", font_size=30)
        thickness_label.set_color(BLUE)
        thickness_label.next_to(thickness_rect, RIGHT, SMALL_BUFF)

        self.add(expr)
        self.wait()
        self.play(
            GrowFromCenter(circum_brace),
            FadeIn(circum_label, lag_ratio=0.1),
        )
        self.play(
            ShowCreation(thickness_rect),
            FadeIn(thickness_label, lag_ratio=0.1),
        )
        self.wait()
