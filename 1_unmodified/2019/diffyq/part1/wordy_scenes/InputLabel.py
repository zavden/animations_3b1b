# ==============================================================================
# Scene:      InputLabel
# Source:     videos/_2019/diffyq/part1/wordy_scenes.py (lines 147-157)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InputLabel.py InputLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InputLabel(Scene):
    def construct(self):
        label = OldTexText("Input")
        label.scale(1.25)
        arrow = Vector(UP)
        arrow.next_to(label, UP)
        self.play(
            FadeIn(label, UP),
            GrowArrow(arrow)
        )
        self.wait()
