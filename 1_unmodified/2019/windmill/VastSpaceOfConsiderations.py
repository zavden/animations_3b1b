# ==============================================================================
# Scene:      VastSpaceOfConsiderations
# Source:     videos/_2019/windmill.py (lines 3495-3515)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VastSpaceOfConsiderations.py VastSpaceOfConsiderations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VastSpaceOfConsiderations(Scene):
    def construct(self):
        considerations = VGroup(*[
            OldTexText(phrase)
            for phrase in [
                "Define ``outer'' points",
                "Convex hulls",
                "Linear equations",
                "Sort points by when they're hit",
                "Sort points by some kind of angle?",
                "How does this permute the $n \\choose 2$ lines through pairs?",
                "Some points are hit more than others, can we quantify this?",
            ]
        ])
        considerations.arrange(DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        considerations.to_edge(LEFT)

        self.play(LaggedStart(*[
            FadeIn(mob, UP)
            for mob in considerations
        ], run_time=3, lag_ratio=0.2))
