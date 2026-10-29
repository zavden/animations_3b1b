# ==============================================================================
# Scene:      StateSpaceLabel
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 469-482)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StateSpaceLabel.py StateSpaceLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StateSpaceLabel(InteractiveScene):
    def construct(self):
        # Test
        title = TexText("``State Space''", font_size=60)
        title.to_corner(UL)
        arrow = Arrow(title.get_bottom() + 0.1 * DOWN + 1.0 * RIGHT, 1.0 * UP, thickness=5)
        arrow.set_color(YELLOW)
        title.set_color(YELLOW)

        self.play(
            Write(title),
            GrowArrow(arrow)
        )
        self.wait()
