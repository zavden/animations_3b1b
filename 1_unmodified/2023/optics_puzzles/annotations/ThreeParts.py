# ==============================================================================
# Scene:      ThreeParts
# Source:     videos/_2023/optics_puzzles/annotations.py (lines 347-370)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeParts.py ThreeParts -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThreeParts(InteractiveScene):
    def construct(self):
        # Setup
        self.add(FullScreenRectangle())
        parts = ScreenRectangle().replicate(3)
        parts.set_height(0.3 * FRAME_HEIGHT)
        parts.arrange(RIGHT)
        parts.arrange_to_fit_width(FRAME_WIDTH - 0.5)
        parts.set_fill(BLACK, 1)
        parts.set_stroke(width=0)
        self.add(parts)

        self.clear()

        rect = SurroundingRectangle(parts[0], buff=0)
        rect.set_stroke(WHITE, 4)

        self.add(rect)

        # Test
        self.wait()
        for part in parts[1:]:
            self.play(rect.animate.surround(part, buff=0))
            self.wait()
