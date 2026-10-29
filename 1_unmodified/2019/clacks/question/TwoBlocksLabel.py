# ==============================================================================
# Scene:      TwoBlocksLabel
# Source:     videos/_2019/clacks/question.py (lines 599-613)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoBlocksLabel.py TwoBlocksLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoBlocksLabel(Scene):
    def construct(self):
        label = OldTexText("Two sliding \\\\ blocks")
        label.to_edge(UP)
        arrows = VGroup(*[
            Arrow(label.get_bottom(), point)
            for point in [RIGHT, LEFT]
        ])
        arrows.set_color(RED)
        self.play(
            Write(label),
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.7),
            run_time=1
        )
        self.wait()
