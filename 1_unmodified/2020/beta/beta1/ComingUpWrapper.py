# ==============================================================================
# Scene:      ComingUpWrapper
# Source:     videos/_2020/beta/beta1.py (lines 2162-2179)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComingUpWrapper.py ComingUpWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComingUpWrapper(Scene):
    def construct(self):
        background = FullScreenFadeRectangle()
        background.set_fill(GREY_E, 1)

        title = OldTexText("What's coming...")
        title.scale(1.5)
        title.to_edge(UP)

        rect = ScreenRectangle()
        rect.set_height(6)
        rect.set_stroke(WHITE)
        rect.set_fill(BLACK, 1)
        rect.next_to(title, DOWN)

        self.add(background, rect)
        self.play(FadeInFromDown(title))
        self.wait()
