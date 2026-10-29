# ==============================================================================
# Scene:      SumUpWrapper
# Source:     videos/_2019/clacks/solution1.py (lines 2869-2885)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SumUpWrapper.py SumUpWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SumUpWrapper(Scene):
    def construct(self):
        title = OldTexText("To sum up:")
        title.scale(1.5)
        title.to_edge(UP)
        screen_rect = ScreenRectangle(height=6)
        screen_rect.set_fill(BLACK, 1)
        screen_rect.next_to(title, DOWN)
        self.add(FullScreenFadeRectangle(
            fill_color=GREY_D,
            fill_opacity=0.5
        ))
        self.play(
            FadeInFromDown(title),
            FadeIn(screen_rect),
        )
        self.wait()
