# ==============================================================================
# Scene:      VideoWrapper
# Source:     videos/_2019/diffyq/part4/long_fourier_scenes.py (lines 222-242)
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
        screen_rect = ScreenRectangle()
        screen_rect.set_height(4)
        screen_rect.set_fill(BLACK, 1)
        screen_rect.set_stroke(width=0)

        boundary = AnimatedBoundary(screen_rect)

        title = OldTexText("Learn the math")
        title.scale(1.5)
        title.next_to(screen_rect, UP)

        self.add(fade_rect)
        self.add(screen_rect)
        self.add(boundary)

        self.play(FadeInFromDown(title))
        self.wait(19)
