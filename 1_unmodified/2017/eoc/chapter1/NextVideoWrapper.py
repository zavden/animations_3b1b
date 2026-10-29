# ==============================================================================
# Scene:      NextVideoWrapper
# Source:     videos/_2017/eoc/chapter1.py (lines 2645-2664)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NextVideoWrapper.py NextVideoWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NextVideoWrapper(Scene):
    def construct(self):
        rect = Rectangle(height = 9, width = 16)
        rect.set_height(1.5*FRAME_Y_RADIUS)
        titles = [
            OldTexText("Chapter %d:"%d, s)
            for d, s in [
                (2, "The paradox of the derivative"),
                (3, "Derivative formulas through geometry"),
            ]
        ]
        for title in titles:
            title.to_edge(UP)
        rect.next_to(VGroup(*titles), DOWN)

        self.add(titles[0])
        self.play(ShowCreation(rect))
        self.wait(3)
        self.play(Transform(*titles))
        self.wait(3)
