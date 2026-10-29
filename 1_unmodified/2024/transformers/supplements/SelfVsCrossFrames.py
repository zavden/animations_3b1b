# ==============================================================================
# Scene:      SelfVsCrossFrames
# Source:     videos/_2024/transformers/supplements.py (lines 1108-1130)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SelfVsCrossFrames.py SelfVsCrossFrames -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class SelfVsCrossFrames(InteractiveScene):
    def construct(self):
        # Add screens
        self.add(FullScreenRectangle())
        screens = ScreenRectangle().replicate(2)
        screens.set_fill(BLACK, 1)
        screens.set_stroke(WHITE, 2)
        screens.set_height(0.45 * FRAME_HEIGHT)
        screens.arrange(RIGHT, buff=0.5)
        self.add(screens)

        # Add titles
        titles = VGroup(
            Text("Self-attention", font_size=60),
            Text("Cross-attention", font_size=60),
        )
        for title, screen in zip(titles, screens):
            title.next_to(screen, UP, buff=MED_LARGE_BUFF)

        self.play(Write(titles[0]))
        self.wait()
        self.play(TransformMatchingStrings(titles[0].copy(), titles[1]))
        self.wait()
