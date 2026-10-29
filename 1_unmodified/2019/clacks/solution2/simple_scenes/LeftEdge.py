# ==============================================================================
# Scene:      LeftEdge
# Source:     videos/_2019/clacks/solution2/simple_scenes.py (lines 48-64)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LeftEdge.py LeftEdge -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LeftEdge(Scene):
    CONFIG = {
        "text": "Left edge",
        "vect": LEFT,
    }

    def construct(self):
        words = OldTexText(self.text)
        arrow = Vector(self.vect)
        arrow.match_width(words)
        arrow.next_to(words, DOWN)

        self.play(
            FadeInFromDown(words),
            GrowArrow(arrow)
        )
        self.wait()
