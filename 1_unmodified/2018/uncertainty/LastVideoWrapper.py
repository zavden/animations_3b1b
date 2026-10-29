# ==============================================================================
# Scene:      LastVideoWrapper
# Source:     videos/_2018/uncertainty.py (lines 1121-1130)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LastVideoWrapper.py LastVideoWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class LastVideoWrapper(Scene):
    def construct(self):
        title = OldTexText("Visualizing the Fourier Transform")
        title.to_edge(UP)
        screen_rect = ScreenRectangle(height = 6)
        screen_rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(screen_rect))
        self.wait()
