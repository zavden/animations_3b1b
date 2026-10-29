# ==============================================================================
# Scene:      FromPreviousTopologyVideo
# Source:     videos/_2017/borsuk.py (lines 70-80)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FromPreviousTopologyVideo.py FromPreviousTopologyVideo -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class FromPreviousTopologyVideo(Scene):
    def construct(self):
        rect = Rectangle(height = 9, width = 16)
        rect.set_height(FRAME_HEIGHT-2)
        title = OldTexText("From original ``Who cares about topology'' video")
        title.to_edge(UP)
        rect.next_to(title, DOWN)

        self.add(title)
        self.play(ShowCreation(rect))
        self.wait()
