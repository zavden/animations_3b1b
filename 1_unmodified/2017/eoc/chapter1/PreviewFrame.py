# ==============================================================================
# Scene:      PreviewFrame
# Source:     videos/_2017/eoc/chapter1.py (lines 442-464)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl PreviewFrame.py PreviewFrame -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class PreviewFrame(Scene):
    def construct(self):
        frame = Rectangle(height = 9, width = 16, color = WHITE)
        frame.set_height(1.5*FRAME_Y_RADIUS)

        colors = iter(color_gradient([BLUE, YELLOW], 3))
        titles = [
            OldTexText("Chapter %d:"%d, s).to_edge(UP).set_color(next(colors))
            for d, s in [
                (3, "Derivative formulas through geometry"),
                (4, "Chain rule, product rule, etc."),
                (7, "Limits"),
            ]
        ]
        title = titles[0]

        frame.next_to(title, DOWN)

        self.add(frame, title)
        self.wait(3)
        for next_title in titles[1:]:
            self.play(Transform(title, next_title))
            self.wait(3)
