# ==============================================================================
# Scene:      ByHandVsSoftwareVsHardware
# Source:     videos/_2020/hamming.py (lines 4765-4809)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ByHandVsSoftwareVsHardware.py ByHandVsSoftwareVsHardware -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_background(color=GREY_E):
    background = FullScreenRectangle()
    background.set_fill(color, 1)
    background.set_stroke(width=0)
    return background


class ByHandVsSoftwareVsHardware(Scene):
    def construct(self):
        self.add(get_background(GREY_E))

        rects = VGroup(*[ScreenRectangle() for x in range(3)])
        rects.set_stroke(GREY_B)
        rects.set_fill(BLACK, 1)
        rects.arrange(RIGHT, buff=MED_LARGE_BUFF)
        rects.set_width(FRAME_WIDTH - 1)
        rects[0].shift(UP)
        rects[2].shift(DOWN)
        self.add(rects)

        labels = VGroup(
            OldTexText("By hand"),
            OldTexText("In software"),
            OldTexText("In hardware"),
        )
        for label, rect in zip(labels, rects):
            label.next_to(rect, DOWN)

        randy = Randolph(height=1.25)
        randy.next_to(rects[0], UP, SMALL_BUFF)

        self.play(
            LaggedStartMap(
                FadeIn, labels,
                lambda m: (m, 0.5 * UP),
                lag_ratio=0.4,
            ),
            randy.change, 'thinking', rects[0],
        )
        self.play(Blink(randy))
        self.wait()

        randy.generate_target()
        randy.target.next_to(rects[1], UP, SMALL_BUFF)
        randy.target.change("hooray", rects[1])
        self.play(
            MoveToTarget(randy, path_arc=-45 * DEGREES)
        )
        self.play(Blink(randy))
        self.play(randy.change, 'thinking', rects[1])
        self.play(Blink(randy))
        self.wait()
