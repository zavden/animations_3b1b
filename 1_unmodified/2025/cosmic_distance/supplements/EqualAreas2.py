# ==============================================================================
# Scene:      EqualAreas2
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 1063-1066)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EqualAreas2.py EqualAreas2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EqualAreas1(InteractiveScene):
    angle = 30 * DEG
    radius = 2
    run_time = 1

    def construct(self):
        # Test
        arc = self.get_slice(1 * DEG)
        self.play(
            UpdateFromAlphaFunc(arc, lambda m, a: m.become(self.get_slice(a * self.angle))),
            run_time=self.run_time
        )
        self.wait()

    def get_slice(self, angle):
        arc = Arc(0, angle, radius=self.radius)
        arc.add_line_to(ORIGIN)
        arc.add_line_to(arc.get_start())
        arc.set_fill(BLUE, 0.5)
        arc.set_stroke(width=0)
        return arc


class EqualAreas2(EqualAreas1):
    angle = 10 * DEG
    radius = 4
    run_time = 1
