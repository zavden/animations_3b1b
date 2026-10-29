# ==============================================================================
# Scene:      ComingUp
# Source:     videos/_2019/bayes/part1.py (lines 4201-4219)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComingUp.py ComingUp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComingUp(Scene):
    CONFIG = {
        "camera_config": {"background_color": GREY_D}
    }

    def construct(self):
        rect = ScreenRectangle()
        rect.set_height(6)
        rect.set_fill(BLACK, 1)
        rect.set_stroke(WHITE, 2)

        words = OldTexText("Later...")
        words.scale(2)
        words.to_edge(UP)
        rect.next_to(words, DOWN)

        self.add(rect)
        self.play(FadeIn(words))
        self.wait()
