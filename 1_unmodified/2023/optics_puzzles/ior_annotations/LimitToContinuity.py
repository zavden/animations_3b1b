# ==============================================================================
# Scene:      LimitToContinuity
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1415-1424)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LimitToContinuity.py LimitToContinuity -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LimitToContinuity(InteractiveScene):
    def construct(self):
        arrow = Arrow(3 * UP, 3 * DOWN, buff=0, stroke_width=10, stroke_color=YELLOW)
        words = Text("Continuous in\nthe limit", font_size=60)
        words.next_to(arrow, RIGHT, buff=0.5)
        self.play(
            GrowArrow(arrow),
            FadeIn(words),
        )
        self.wait()
