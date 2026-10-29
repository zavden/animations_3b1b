# ==============================================================================
# Scene:      CopernicanPrinciple
# Source:     videos/_2025/cosmic_distance/part2.py (lines 1425-1444)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CopernicanPrinciple.py CopernicanPrinciple -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CopernicanPrinciple(InteractiveScene):
    def construct(self):
        back = FullScreenRectangle()
        back.set_fill(BLACK, 0.8)
        self.add(back)

        # Test
        title = Text("Copernican principle", font_size=72)
        title.to_edge(UP)
        title.set_color(RED_B)

        body = Text("""
            Observations from earth are representative of
            observations from anywhere else in the universe
        """)
        body.next_to(title, DOWN, MED_LARGE_BUFF)

        self.add(title)
        self.play(Write(body, run_time=5, lag_ratio=0.1))
        self.wait()
