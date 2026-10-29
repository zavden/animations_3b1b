# ==============================================================================
# Scene:      EndingAnimation
# Source:     videos/_2022/some2/announcement.py (lines 236-246)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EndingAnimation.py EndingAnimation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EndingAnimation(InteractiveScene):
    def construct(self):
        self.add(FullScreenRectangle())
        frame = ScreenRectangle(height=4)
        frame.set_fill(BLACK, 1)
        frame.set_stroke(WHITE, 0)
        boundary = AnimatedBoundary(frame)
        self.add(frame)
        self.add(boundary)

        self.wait(20)
