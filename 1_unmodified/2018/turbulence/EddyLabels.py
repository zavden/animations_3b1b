# ==============================================================================
# Scene:      EddyLabels
# Source:     videos/_2018/turbulence.py (lines 392-404)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EddyLabels.py EddyLabels -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EddyLabels(Scene):
    def construct(self):
        labels = VGroup(
            OldTexText("Large eddy"),
            OldTexText("Medium eddy"),
            OldTexText("Small eddy"),
        )
        for label in labels:
            self.play(FadeIn(
                label,
                rate_func=there_and_back_with_pause,
                run_time=3
            ))
