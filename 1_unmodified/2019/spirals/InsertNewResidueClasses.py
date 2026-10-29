# ==============================================================================
# Scene:      InsertNewResidueClasses
# Source:     videos/_2019/spirals.py (lines 3916-3924)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InsertNewResidueClasses.py InsertNewResidueClasses -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InsertNewResidueClasses(Scene):
    def construct(self):
        nums = VGroup(*map(Integer, [3, 7, 9]))
        colors = [GREEN, TEAL, BLUE]
        for num, color in zip(nums, colors):
            num.set_color(color)
            num.add_background_rectangle(buff=SMALL_BUFF, opacity=1)
            self.play(FadeIn(num, UP))
            self.wait()
