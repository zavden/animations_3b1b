# ==============================================================================
# Scene:      TwoGraphTypeTitles
# Source:     videos/_2019/diffyq/part2/wordy_scenes.py (lines 230-249)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoGraphTypeTitles.py TwoGraphTypeTitles -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoGraphTypeTitles(Scene):
    def construct(self):
        left_title = OldTexText(
            "Represent time\\\\with actual time"
        )
        left_title.shift(FRAME_WIDTH * LEFT / 4)
        right_title = OldTexText(
            "Represent time\\\\with an axis"
        )
        right_title.shift(FRAME_WIDTH * RIGHT / 4)

        titles = VGroup(left_title, right_title)
        for title in titles:
            title.scale(1.25)
            title.to_edge(UP)

        self.play(FadeInFromDown(right_title))
        self.wait()
        self.play(FadeInFromDown(left_title))
        self.wait()
