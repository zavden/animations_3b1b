# ==============================================================================
# Scene:      RdLabels
# Source:     videos/_2018/sphere_area.py (lines 2091-2102)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RdLabels.py RdLabels -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RdLabels(Scene):
    def construct(self):
        rect = Rectangle(height=1, width=0.5)
        cR = OldTex("cR")
        cR.next_to(rect, LEFT, SMALL_BUFF)
        cd = OldTex("cd")
        cd.next_to(rect, DOWN, SMALL_BUFF)

        labels = VGroup(cd, cR)
        for label in labels:
            label[1].set_color(BLUE)
            self.play(FadeInFromDown(label))
