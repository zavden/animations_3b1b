# ==============================================================================
# Scene:      ListOfConfusions
# Source:     videos/_2025/grover/clarification.py (lines 688-716)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ListOfConfusions.py ListOfConfusions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ListOfConfusions(InteractiveScene):
    def construct(self):
        # Test
        items = BulletedList(
            "Insufficient detail",
            "Bad framing",
            "Glossing over linearity",
            buff=1.0
        )
        rects = VGroup(
            SurroundingRectangle(item[1:])
            for item in items
        )
        rects.set_stroke(width=0)
        rects.set_fill(GREY_D, 1)

        self.add(items)
        self.add(rects[1:])
        self.wait()
        self.play(
            items[0].animate.fade(0.5),
            rects[1].animate.stretch(0, 0, about_edge=RIGHT),
        )
        self.wait()
        self.play(
            items[1].animate.fade(0.5),
            rects[2].animate.stretch(0, 0, about_edge=RIGHT),
        )
        self.wait()
