# ==============================================================================
# Scene:      GlintArrow
# Source:     videos/_2024/holograms/supplements.py (lines 37-49)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GlintArrow.py GlintArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GlintArrow(InteractiveScene):
    def construct(self):
        # Test
        circle = Circle(radius=0.25)
        circle.set_stroke(RED, 4)
        circle.insert_n_curves(20)
        arrow = Vector(DR, thickness=5, fill_color=RED)
        arrow.next_to(circle, UL, buff=0)
        self.play(
            GrowArrow(arrow),
            VShowPassingFlash(circle, time_width=1.5, time_span=(0.5, 1.5)),
        )
        self.wait()
