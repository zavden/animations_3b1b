# ==============================================================================
# Scene:      WhatVsHow
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 450-469)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhatVsHow.py WhatVsHow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WhatVsHow(InteractiveScene):
    def construct(self):
        # Test
        titles = VGroup(
            Text("What"),
            Text("How"),
        )
        titles.scale(1.5)
        for title, vect in zip(titles, [LEFT, RIGHT]):
            title.move_to(vect * FRAME_WIDTH / 4)
            title.to_edge(UP, buff=0.25)

        v_line = Line(UP, DOWN).set_height(FRAME_HEIGHT)
        self.play(
            FadeIn(titles[0], 0.5 * UP),
            ShowCreation(v_line),
        )
        self.wait()
        self.play(FadeIn(titles[1], 0.5 * UP))
        self.wait()
