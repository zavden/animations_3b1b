# ==============================================================================
# Scene:      ModeledAs2D
# Source:     videos/_2024/holograms/supplements.py (lines 1299-1311)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ModeledAs2D.py ModeledAs2D -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ModeledAs2D(InteractiveScene):
    def construct(self):
        # Test
        words = Text("Modeled as 2D")
        words.to_edge(UP)
        point = 1.5 * RIGHT
        arrow = Arrow(words.get_right(), point, path_arc=-180 * DEGREES, thickness=4)

        self.play(
            FadeIn(words, 0.25 * UP),
            DrawBorderThenFill(arrow, run_time=2)
        )
        self.wait()
