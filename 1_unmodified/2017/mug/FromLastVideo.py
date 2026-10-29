# ==============================================================================
# Scene:      FromLastVideo
# Source:     videos/_2017/mug.py (lines 837-846)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FromLastVideo.py FromLastVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FromLastVideo(Scene):
    def construct(self):
        title = OldTexText("From last video")
        title.to_edge(UP)
        rect = ScreenRectangle(height = 6)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(rect))
        self.wait(2)
