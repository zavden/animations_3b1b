# ==============================================================================
# Scene:      LoadSolutionIntoHead
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 248-263)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LoadSolutionIntoHead.py LoadSolutionIntoHead -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LoadSolutionIntoHead(InteractiveScene):
    def construct(self):
        # Test
        self.add(FullScreenFadeRectangle().set_fill(interpolate_color(GREY_E, BLACK, 0.5), 1))
        randy = Randolph()
        randy.to_edge(DOWN, buff=0.25)
        bubble = ThoughtBubble(direction=RIGHT, filler_shape=(4, 2.5)).pin_to(randy)
        bubble[0][-1].set_fill(GREEN_SCREEN, 1)

        self.play(
            ShowCreation(bubble),
            randy.change("concentrating", 3 * UR)
        )
        for _ in range(2):
            self.play(Blink(randy))
            self.wait(2)
