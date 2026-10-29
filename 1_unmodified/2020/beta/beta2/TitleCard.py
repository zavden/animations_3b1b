# ==============================================================================
# Scene:      TitleCard
# Source:     videos/_2020/beta/beta2.py (lines 403-416)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TitleCard.py TitleCard -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TitleCard(Scene):
    def construct(self):
        text = OldTexText("A beginner's guide to\\\\probability density")
        text.scale(2)
        text.to_edge(UP, buff=1.5)

        subtext = OldTexText("Probabilities of probabilities, ", "part 2")
        subtext.set_width(FRAME_WIDTH - 3)
        subtext[0].set_color(BLUE)
        subtext.next_to(text, DOWN, LARGE_BUFF)

        self.add(text)
        self.play(FadeIn(subtext, lag_ratio=0.1, run_time=2))
        self.wait(2)
