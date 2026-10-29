# ==============================================================================
# Scene:      Chapter1Wrapper
# Source:     videos/_2017/eoc/chapter8.py (lines 1484-1487)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Chapter1Wrapper.py Chapter1Wrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Chapter2Wrapper(Scene):
    CONFIG = {
        "title" : "Chapter 2: The paradox of the derivative",
    }
    def construct(self):
        title = OldTexText(self.title)
        title.to_edge(UP)
        rect = Rectangle(width = 16, height = 9, color = WHITE)
        rect.set_height(1.5*FRAME_Y_RADIUS)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(rect))
        self.wait(3)


class Chapter1Wrapper(Chapter2Wrapper):
    CONFIG = {
        "title" : "Essence of calculus, chapter 1",
    }
