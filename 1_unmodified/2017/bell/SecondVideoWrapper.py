# ==============================================================================
# Scene:      SecondVideoWrapper
# Source:     videos/_2017/bell.py (lines 409-418)
# Category:   1 · Renders unmodified
# Includes code copied from: _2017/waves.py
#
# Run from this folder:
#     manimgl SecondVideoWrapper.py SecondVideoWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2017/waves.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")



# ----- From _2017/bell.py -----

class SecondVideoWrapper(Scene):
    def construct(self):
        title = OldTexText("Some light quantum mechanics")
        title.to_edge(UP)
        self.add(title)

        screen_rect = ScreenRectangle(height = 6)
        screen_rect.next_to(title, DOWN)
        self.play(ShowCreation(screen_rect))
        self.wait(3)
