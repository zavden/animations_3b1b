# ==============================================================================
# Scene:      VideoWrapper
# Source:     videos/_2019/diffyq/part5/staging.py (lines 1486-1517)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl VideoWrapper.py VideoWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class VideoWrapper(Scene):
    def construct(self):
        fade_rect = FullScreenFadeRectangle()
        fade_rect.set_fill(GREY_D, 1)
        screen_rects = VGroup(
            ScreenRectangle(),
            ScreenRectangle(),
        )
        screen_rects.set_height(3)
        screen_rects.set_fill(BLACK, 1)
        screen_rects.set_stroke(width=0)
        screen_rects.arrange(RIGHT, buff=LARGE_BUFF)
        screen_rects.shift(1.25 * UP)

        boundary = VGroup(*map(AnimatedBoundary, screen_rects))

        titles = VGroup(
            OldTexText("Want more?"),
            OldTexText("Learn calculus"),
        )
        titles.scale(1.5)
        for rect, title, in zip(screen_rects, titles):
            title.next_to(rect, UP)

        self.add(fade_rect)
        self.add(screen_rects)

        self.add(boundary[0])
        self.play(FadeInFromDown(titles[0]))
        self.add(boundary[1])
        self.play(FadeInFromDown(titles[1]))
        self.wait(18)
