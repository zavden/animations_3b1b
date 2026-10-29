# ==============================================================================
# Scene:      EndScreen
# Source:     videos/_2020/hamming.py (lines 4812-4839)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EndScreen.py EndScreen -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_background(color=GREY_E):
    background = FullScreenRectangle()
    background.set_fill(color, 1)
    background.set_stroke(width=0)
    return background


class EndScreen(Scene):
    def construct(self):
        self.add(get_background(GREY_E))

        rects = VGroup(*[ScreenRectangle() for x in range(2)])
        rects.set_stroke(WHITE, 1)
        rects.set_fill(BLACK, 1)
        rects.set_height(3)
        rects.arrange(RIGHT, buff=1)
        rects.shift(UP)
        self.add(rects)

        labels = VGroup(
            OldTexText("Part 2\\\\", "the elegance of it all"),
            OldTexText("Ben Eater\\\\", "doing this on breadboards"),
        )

        for label, rect in zip(labels, rects):
            label[0].scale(1.5, about_edge=DOWN)
            label.scale(0.9)
            label.next_to(rect, DOWN)

        self.add(labels)

        self.add(AnimatedBoundary(rects[0]))
        self.wait()
        self.add(AnimatedBoundary(rects[1]))
        self.wait(19)
