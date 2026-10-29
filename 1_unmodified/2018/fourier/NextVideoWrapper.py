# ==============================================================================
# Scene:      NextVideoWrapper
# Source:     videos/_2018/fourier.py (lines 4030-4038)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NextVideoWrapper.py NextVideoWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NextVideoWrapper(Scene):
    def construct(self):
        title = OldTexText("Next video")
        title.to_edge(UP)
        screen_rect = ScreenRectangle(height = 6)
        screen_rect.next_to(title, DOWN)
        self.add(title)
        self.play(ShowCreation(screen_rect))
        self.wait(2)
