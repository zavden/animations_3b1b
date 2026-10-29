# ==============================================================================
# Scene:      NextVideo
# Source:     videos/_2018/eop/combinations.py (lines 3514-3525)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NextVideo.py NextVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NextVideo(Scene):
    def construct(self):
        title = OldTexText("Next video: Binomial distribution")
        title.to_edge(UP)
        screen = ScreenRectangle(height = 6)
        screen.next_to(title, DOWN)

        self.play(
            Write(title),
            ShowCreation(screen)
        )
        self.wait()
