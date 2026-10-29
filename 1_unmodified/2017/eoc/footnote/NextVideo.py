# ==============================================================================
# Scene:      NextVideo
# Source:     videos/_2017/eoc/footnote.py (lines 862-870)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NextVideo.py NextVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NextVideo(Scene):
    def construct(self):
        title = OldTexText("Chapter 10: Taylor series")
        title.to_edge(UP)
        rect = ScreenRectangle(height = 6)
        rect.next_to(title, DOWN)
        self.add(rect)
        self.play(Write(title))
        self.wait()
