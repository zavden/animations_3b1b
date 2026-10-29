# ==============================================================================
# Scene:      ThreePointFiveCorrection
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 814-825)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreePointFiveCorrection.py ThreePointFiveCorrection -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreePointFiveCorrection(InteractiveScene):
    def construct(self):
        # Test
        four_hours = Text("4 hours")
        correction = Text("3.5 hours")
        correction.next_to(four_hours, UP, MED_LARGE_BUFF)
        cross = Line(LEFT, RIGHT).replace(four_hours, 0)
        cross.set_stroke(RED, 6)

        self.play(ShowCreation(cross))
        self.play(Write(correction))
        self.wait()
