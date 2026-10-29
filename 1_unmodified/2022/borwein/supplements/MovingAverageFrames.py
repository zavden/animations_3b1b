# ==============================================================================
# Scene:      MovingAverageFrames
# Source:     videos/_2022/borwein/supplements.py (lines 169-195)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MovingAverageFrames.py MovingAverageFrames -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MovingAverageFrames(InteractiveScene):
    def construct(self):
        # Frames
        self.add(FullScreenRectangle())
        screens = ScreenRectangle(height=4).replicate(2)
        screens.arrange(RIGHT, buff=1.0)
        screens.set_width(FRAME_WIDTH - 1)
        screens.set_stroke(WHITE, 1)
        screens.set_fill(BLACK, 1)
        screens.move_to(0.5 * DOWN)
        self.add(screens)

        # Titles
        titles = VGroup(
            Text("Step 1:\nAn easier analogy", alignment="LEFT"),
            Text("Step 2:\nReveal it's more than an analogy", alignment="LEFT"),
        )
        titles.match_width(screens[0])
        for title, screen in zip(titles, screens):
            title.next_to(screen, UP, aligned_edge=LEFT)

        # Animations
        n = len("Step1:")
        for i in range(2):
            self.play(Write(titles[i][:n]))
            self.play(FadeIn(titles[i][n:], 0.5 * DOWN))
            self.wait()
