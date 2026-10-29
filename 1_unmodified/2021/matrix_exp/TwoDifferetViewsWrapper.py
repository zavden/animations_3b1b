# ==============================================================================
# Scene:      TwoDifferetViewsWrapper
# Source:     videos/_2021/matrix_exp.py (lines 4762-4782)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoDifferetViewsWrapper.py TwoDifferetViewsWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoDifferetViewsWrapper(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        screens = VGroup(*(ScreenRectangle() for x in range(2)))
        screens.arrange(RIGHT)
        screens.set_width(FRAME_WIDTH - 1)
        screens.set_fill(BLACK, 1)
        screens[0].set_stroke(BLUE, 2)
        screens[1].set_stroke(GREY_BROWN, 2)
        self.add(screens)

        titles = VGroup(
            Text("Geometric"),
            Text("Analytic"),
        )
        for title, screen in zip(titles, screens):
            title.next_to(screen, UP)
            title.align_to(titles[0], UP)
            self.play(Write(title))
            self.wait()
        self.wait()
