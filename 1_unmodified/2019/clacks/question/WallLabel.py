# ==============================================================================
# Scene:      WallLabel
# Source:     videos/_2019/clacks/question.py (lines 616-627)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WallLabel.py WallLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WallLabel(Scene):
    def construct(self):
        wall = Line(TOP, 2 * DOWN)
        wall.set_stroke(YELLOW, 10)
        word = OldTexText("Wall")
        word.rotate(-90 * DEGREES)
        word.next_to(wall, RIGHT, MED_SMALL_BUFF)
        self.play(
            Write(word),
            ShowPassingFlash(wall)
        )
        self.wait()
