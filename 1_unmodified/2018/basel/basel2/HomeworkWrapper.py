# ==============================================================================
# Scene:      HomeworkWrapper
# Source:     videos/_2018/basel/basel2.py (lines 2731-2739)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl HomeworkWrapper.py HomeworkWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class HomeworkWrapper(Scene):
    def construct(self):
        title = OldTexText("Homework")
        title.to_edge(UP)
        screen = ScreenRectangle(height = 6)
        screen.center()
        self.add(title)
        self.play(ShowCreation(screen))
        self.wait(5)
