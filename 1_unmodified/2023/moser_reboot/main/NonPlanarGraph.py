# ==============================================================================
# Scene:      NonPlanarGraph
# Source:     videos/_2023/moser_reboot/main.py (lines 668-681)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NonPlanarGraph.py NonPlanarGraph -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NonPlanarGraph(InteractiveScene):
    def construct(self):
        # Test
        circle = Circle(radius=3)
        dots = Dot().get_grid(2, 3, h_buff=1.5, v_buff=3.0)
        lines = VGroup(*(
            Line(d1.get_center(), d2.get_center())
            for d1, d2 in it.product(dots[:3], dots[3:])
        ))
        lines.set_stroke(BLUE_B, 2)

        self.add(lines, dots)
        self.play(ShowCreation(lines, lag_ratio=0.1, run_time=2))
        self.wait()
