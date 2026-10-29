# ==============================================================================
# Scene:      RightAngles
# Source:     videos/_2026/print_gallery/misc_scenes.py (lines 580-586)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RightAngles.py RightAngles -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RightAngles(InteractiveScene):
    def construct(self):
        # Create a right angle symbol
        line1 = Line(ORIGIN, RIGHT)
        line2 = Line(RIGHT, UR).shift(DL * 0.04)
        VGroup(line1, line2).center().set_stroke(width=15, color=PURE_RED)
        self.play(AnimationGroup(ShowCreation(line1), ShowCreation(line2), lag_ratio=0.8))
