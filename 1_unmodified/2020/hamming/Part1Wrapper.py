# ==============================================================================
# Scene:      Part1Wrapper
# Source:     videos/_2020/hamming.py (lines 4873-4888)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Part1Wrapper.py Part1Wrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_background(color=GREY_E):
    background = FullScreenRectangle()
    background.set_fill(color, 1)
    background.set_stroke(width=0)
    return background


class Part1Wrapper(Scene):
    def construct(self):
        self.add(get_background())
        rect = ScreenRectangle()
        rect.set_fill(BLACK, 1)
        rect.set_stroke(GREY_B, 2)
        rect.set_height(6)
        rect.to_edge(DOWN)
        title = OldTexText("Part 1")
        title.set_height(0.7)
        title.to_edge(UP)

        self.add(rect)
        self.add(AnimatedBoundary(rect, max_stroke_width=2, cycle_rate=0.25))
        self.play(Write(title))
        self.wait(35)
