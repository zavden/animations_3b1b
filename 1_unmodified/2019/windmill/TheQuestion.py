# ==============================================================================
# Scene:      TheQuestion
# Source:     videos/_2019/windmill.py (lines 1744-1752)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TheQuestion.py TheQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TheQuestion(Scene):
    def construct(self):
        words = OldTexText(
            "Will each point be hit infinitely many times?"
        )
        words.set_width(FRAME_WIDTH - 1)
        words.to_edge(UP)

        self.add(words)
