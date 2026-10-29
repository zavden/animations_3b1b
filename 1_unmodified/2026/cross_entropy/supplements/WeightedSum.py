# ==============================================================================
# Scene:      WeightedSum
# Source:     videos/_2026/cross_entropy/supplements.py (lines 709-726)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WeightedSum.py WeightedSum -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class WeightedSum(InteractiveScene):
    def construct(self):
        lines = VGroup(
            Tex(R"\frac{1}{2} \cdot 1+\frac{1}{4} \cdot 2+\frac{1}{8} \cdot 3+\frac{1}{8} \cdot 3"),
            Tex(R"=1.75 \text{ bits}")
        )
        lines.arrange(DOWN, aligned_edge=RIGHT)
        lines.to_edge(RIGHT)
        lines.set_backstroke(BLACK, 5)
        self.add(lines)
        self.wait()

        # Test
        self.play(
            lines.animate.arrange(RIGHT, SMALL_BUFF).center().to_edge(UP).set_anim_args(path_arc=45 * DEG),
            run_time=2
        )
        self.wait()
