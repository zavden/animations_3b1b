# ==============================================================================
# Scene:      ShowAbstractionArrows
# Source:     videos/_2025/grover/qc_supplements.py (lines 863-870)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowAbstractionArrows.py ShowAbstractionArrows -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ShowAbstractionArrows(InteractiveScene):
    def construct(self):
        arrows = VGroup(
            Arrow(point + 4 * LEFT, ORIGIN + 0.35 * point, buff=1.0, thickness=5)
            for point in np.linspace(2.5 * DOWN, 2.5 * UP, 3)
        )
        arrows.set_fill(border_width=2)
        self.play(LaggedStartMap(GrowArrow, arrows, lag_ratio=0.1))
