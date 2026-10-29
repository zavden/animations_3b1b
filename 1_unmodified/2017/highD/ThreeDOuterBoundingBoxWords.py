# ==============================================================================
# Scene:      ThreeDOuterBoundingBoxWords
# Source:     videos/_2017/highD.py (lines 3070-3081)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeDOuterBoundingBoxWords.py ThreeDOuterBoundingBoxWords -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ThreeDOuterBoundingBoxWords(Scene):
    def construct(self):
        words = OldTexText(
            "$4 \\!\\times\\! 4\\!\\times\\! 4$ outer\\\\",
            "bounding box"
        )
        words.set_width(FRAME_WIDTH-1)
        words.to_edge(DOWN)
        words.set_color(MAROON_B)

        self.play(Write(words))
        self.wait(4)
