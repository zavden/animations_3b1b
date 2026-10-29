# ==============================================================================
# Scene:      PiHidingWrapper
# Source:     videos/_2018/basel/basel2.py (lines 621-629)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PiHidingWrapper.py PiHidingWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class PiHidingWrapper(Scene):
    def construct(self):
        title = OldTexText("Pi hiding in prime regularities")
        title.to_edge(UP)
        screen = ScreenRectangle(height = 6)
        screen.next_to(title, DOWN)
        self.add(title)
        self.play(ShowCreation(screen))
        self.wait(2)
