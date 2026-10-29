# ==============================================================================
# Scene:      Chapter4Wrapper
# Source:     videos/_2017/eoc/chapter5.py (lines 1226-1236)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Chapter4Wrapper.py Chapter4Wrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Chapter4Wrapper(Scene):
    def construct(self):
        title = OldTexText("Chapter 4 chain rule intuition")
        title.to_edge(UP)
        rect = Rectangle(width = 16, height = 9)
        rect.set_height(1.5*FRAME_Y_RADIUS)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(rect))
        self.wait(3)
