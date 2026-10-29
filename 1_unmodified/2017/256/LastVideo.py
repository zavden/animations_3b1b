# ==============================================================================
# Scene:      LastVideo
# Source:     videos/_2017/256.py (lines 17-28)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LastVideo.py LastVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LastVideo(Scene):
    def construct(self):
        title = OldTexText("Crypto", "currencies", arg_separator = "")
        title[0].set_color(YELLOW)
        title.scale(1.5)
        title.to_edge(UP)
        screen_rect = ScreenRectangle(height = 6)
        screen_rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(screen_rect))
        self.wait()
