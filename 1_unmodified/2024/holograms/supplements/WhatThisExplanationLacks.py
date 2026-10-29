# ==============================================================================
# Scene:      WhatThisExplanationLacks
# Source:     videos/_2024/holograms/supplements.py (lines 1198-1227)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatThisExplanationLacks.py WhatThisExplanationLacks -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatThisExplanationLacks(InteractiveScene):
    def construct(self):
        # Title
        title = Text("Gaps in the single-point explanation", font_size=60)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        underline = Underline(title, buff=-0.05)

        self.play(
            FadeIn(title, lag_ratio=0.1),
            ShowCreation(underline),
        )
        self.wait()

        # Add points
        points = BulletedList(
            "How do errors in the various approximations accumulate?",
            "Why don't higher order beams exist?",
            "What happens when you change the reference beam angle?",
            buff=0.5,
            font_size=48,
        )
        points.next_to(underline, DOWN, buff=0.5)
        points.to_edge(LEFT, buff=LARGE_BUFF)

        self.play(
            LaggedStartMap(FadeIn, points, shift=UP, lag_ratio=0.5)
        )
        self.wait()
        self.play(points[:2].animate.set_opacity(0.5))
        self.wait()
