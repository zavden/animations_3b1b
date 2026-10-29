# ==============================================================================
# Scene:      InsideOutsideQuestion
# Source:     videos/_2026/hairy_ball/supplements.py (lines 498-510)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl InsideOutsideQuestion.py InsideOutsideQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class InsideOutsideQuestion(InteractiveScene):
    def construct(self):
        # Test
        inside = Text("Inside?", font_size=72)
        outside = Text("Outside?", font_size=72)
        VGroup(inside, outside).set_backstroke(BLACK, 3)
        self.play(FadeIn(inside, lag_ratio=0.1))
        self.wait()
        self.play(
            FadeIn(outside, lag_ratio=0.1),
            FadeOut(inside, lag_ratio=0.1),
        )
        self.wait()
