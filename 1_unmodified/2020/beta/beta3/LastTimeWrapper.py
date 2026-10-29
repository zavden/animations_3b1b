# ==============================================================================
# Scene:      LastTimeWrapper
# Source:     videos/_2020/beta/beta3.py (lines 317-335)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LastTimeWrapper.py LastTimeWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LastTimeWrapper(Scene):
    def construct(self):
        fs_rect = FullScreenFadeRectangle(fill_opacity=1, fill_color=GREY_E)
        self.add(fs_rect)

        title = OldTexText("Last Time")
        title.scale(1.5)
        title.to_edge(UP)

        rect = ScreenRectangle()
        rect.set_height(6)
        rect.set_fill(BLACK, 1)
        rect.next_to(title, DOWN)

        self.play(
            DrawBorderThenFill(rect),
            FadeInFromDown(title),
        )
        self.wait()
