# ==============================================================================
# Scene:      StaysConstant
# Source:     videos/_2025/colliding_blocks_v2/supplements.py (lines 424-442)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl StaysConstant.py StaysConstant -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class StaysConstant(InteractiveScene):
    word = "Unchanged!"
    color = YELLOW

    def construct(self):
        # Note the change
        unchanged_label = Text(self.word)
        unchanged_label.set_color(self.color)
        unchanged_label.next_to(ORIGIN, DOWN, buff=1.5)
        unchanged_label.shift(0.5 * RIGHT)
        unchanged_arrow = Arrow(unchanged_label, ORIGIN, buff=0.25)
        unchanged_arrow.set_fill(self.color)

        self.play(
            FadeIn(unchanged_label),
            GrowArrow(unchanged_arrow),
        )
        self.wait()
        self.play(FadeOut(VGroup(unchanged_label, unchanged_arrow)))
