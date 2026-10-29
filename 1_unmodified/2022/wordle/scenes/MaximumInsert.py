# ==============================================================================
# Scene:      MaximumInsert
# Source:     videos/_2022/wordle/scenes.py (lines 2408-2419)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MaximumInsert.py MaximumInsert -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MaximumInsert(Scene):
    def construct(self):
        text = OldTexText("Maximum possible\\\\", "expected information")
        arrow = Arrow(text.get_top(), text.get_top() + UR)
        arrow.shift(RIGHT)
        VGroup(text, arrow).set_color(YELLOW)
        self.play(
            Write(text),
            ShowCreation(arrow),
            run_time=1
        )
        self.wait()
