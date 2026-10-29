# ==============================================================================
# Scene:      LastChapterWrapper
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 69-88)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LastChapterWrapper.py LastChapterWrapper -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LastChapterWrapper(Scene):
    def construct(self):
        full_rect = FullScreenFadeRectangle(
            fill_color=GREY_D,
            fill_opacity=1,
        )
        rect = ScreenRectangle(height=6)
        rect.set_stroke(WHITE, 2)
        rect.set_fill(BLACK, 1)
        title = OldTexText("Last chapter")
        title.scale(2)
        title.to_edge(UP)
        rect.next_to(title, DOWN)

        self.add(full_rect)
        self.play(
            FadeIn(rect),
            Write(title, run_time=2),
        )
        self.wait()
