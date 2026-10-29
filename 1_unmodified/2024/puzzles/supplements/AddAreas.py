# ==============================================================================
# Scene:      AddAreas
# Source:     videos/_2024/puzzles/supplements.py (lines 229-243)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AddAreas.py AddAreas -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AddAreas(InteractiveScene):
    def construct(self):
        # Test
        parts = [
            R"\sum_i \textbf{Area}(\text{Hemisphere Strip}_i)",
            R"= \sum_i \pi d_i",
            R"= \pi \sum_i d_i",
            R"\ge 2\pi"
        ]
        top_eq = Tex(" ".join(parts))
        top_eq.to_edge(UP)

        for part in parts:
            self.play(FadeIn(top_eq[part][0], 0.5 * UP))
            self.wait()
