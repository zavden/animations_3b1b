# ==============================================================================
# Scene:      ImpossibleToReasonable
# Source:     videos/_2020/hamming.py (lines 1299-1322)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ImpossibleToReasonable.py ImpossibleToReasonable -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ImpossibleToReasonable(Scene):
    def construct(self):
        group = VGroup(
            OldTexText("Impossible"),
            Vector(RIGHT, color=GREY_B),
            OldTexText("Utterly reasonable"),
        )
        group.arrange(RIGHT)
        group.scale(1.5)
        group.to_edge(UP)

        line = Line(LEFT, RIGHT)
        line.set_width(FRAME_WIDTH)
        line.set_stroke(GREY, 2)
        line.next_to(group, DOWN, SMALL_BUFF)
        self.add(line)

        self.play(FadeIn(group[0], 0.5 * UP))
        self.wait()
        self.play(
            GrowArrow(group[1]),
            FadeIn(group[2], LEFT),
        )
        self.wait()
