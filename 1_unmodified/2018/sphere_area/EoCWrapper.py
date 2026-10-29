# ==============================================================================
# Scene:      EoCWrapper
# Source:     videos/_2018/sphere_area.py (lines 2402-2412)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EoCWrapper.py EoCWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EoCWrapper(Scene):
    def construct(self):
        title = OldTexText("Essence of calculus")
        title.scale(1.5)
        title.to_edge(UP)
        rect = ScreenRectangle(height=6)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(rect))
        self.wait()
