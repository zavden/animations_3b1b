# ==============================================================================
# Scene:      CompareOceansLabels
# Source:     videos/_2017/fractal_dimension.py (lines 2750-2761)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CompareOceansLabels.py CompareOceansLabels -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class CompareOceansLabels(Scene):
    def construct(self):
        label1 = OldTexText("Dimension $\\approx 2.05$")
        label2 = OldTexText("Dimension $\\approx 2.3$")

        label1.shift(FRAME_X_RADIUS*LEFT/2).to_edge(UP)
        label2.shift(FRAME_X_RADIUS*RIGHT/2).to_edge(UP)

        self.play(Write(label1))
        self.wait()
        self.play(Write(label2))
        self.wait()
