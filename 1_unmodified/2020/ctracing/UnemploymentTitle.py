# ==============================================================================
# Scene:      UnemploymentTitle
# Source:     videos/_2020/ctracing.py (lines 23-40)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UnemploymentTitle.py UnemploymentTitle -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UnemploymentTitle(Scene):
    def construct(self):
        words = OldTexText("Unemployment claims\\\\per week in the US")[0]
        words.set_width(FRAME_WIDTH - 1)
        words.to_edge(UP)
        arrow = Arrow(
            words.get_bottom(),
            words.get_bottom() + 3 * RIGHT + 3 * DOWN,
            stroke_width=10,
            tip_length=0.5,
        )
        arrow.set_color(BLUE_E)
        words.set_color(BLACK)
        self.play(
            ShowIncreasingSubsets(words),
            ShowCreation(arrow),
        )
        self.wait()
