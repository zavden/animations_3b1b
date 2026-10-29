# ==============================================================================
# Scene:      SphereVideoWrapper
# Source:     videos/_2018/for_flammy.py (lines 26-35)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SphereVideoWrapper.py SphereVideoWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SphereVideoWrapper(Scene):
    def construct(self):
        title = OldTexText("Surface area of a sphere")
        title.scale(1.5)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6)
        rect.next_to(title, DOWN)
        self.add(title)
        self.play(ShowCreation(rect))
        self.wait()
