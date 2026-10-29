# ==============================================================================
# Scene:      RecommendedMathologerVideo
# Source:     videos/_2019/spirals.py (lines 3214-3230)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RecommendedMathologerVideo.py RecommendedMathologerVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RecommendedMathologerVideo(Scene):
    def construct(self):
        full_rect = FullScreenFadeRectangle()
        full_rect.set_fill(GREY_D, 1)
        self.add(full_rect)

        title = OldTexText("Recommended Mathologer video")
        title.set_width(FRAME_WIDTH - 1)
        title.to_edge(UP)
        screen_rect = SurroundingRectangle(ScreenRectangle(height=5.9), buff=SMALL_BUFF)
        screen_rect.next_to(title, DOWN)
        screen_rect.set_fill(BLACK, 1)
        screen_rect.set_stroke(WHITE, 3)

        self.add(screen_rect)
        self.play(Write(title))
        self.wait()
