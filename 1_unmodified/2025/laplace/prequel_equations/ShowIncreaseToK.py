# ==============================================================================
# Scene:      ShowIncreaseToK
# Source:     videos/_2025/laplace/prequel_equations.py (lines 917-939)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowIncreaseToK.py ShowIncreaseToK -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowIncreaseToK(InteractiveScene):
    def construct(self):
        # Test
        k = Tex(R"k")

        box = SurroundingRectangle(k)
        box.set_stroke(GREEN, 5)
        arrow = Vector(UP, thickness=6)
        arrow.set_fill(GREEN)
        center = box.get_center()

        self.play(
            ShowCreation(box),
            UpdateFromAlphaFunc(
                arrow, lambda m, a: m.move_to(
                    center + interpolate(-1, 1, a) * UP
                ).set_fill(
                    opacity=there_and_back(a) * 0.7
                ),
                run_time=4
            ),
        )
        self.wait()
