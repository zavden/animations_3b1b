# ==============================================================================
# Scene:      ReplaceCentralAuthorityWithWork
# Source:     videos/_2017/crypto.py (lines 3981-3998)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReplaceCentralAuthorityWithWork.py ReplaceCentralAuthorityWithWork -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ReplaceCentralAuthorityWithWork(Scene):
    def construct(self):
        trust, central = words = OldTexText("Trust", "central authority")
        words.scale(1.5)
        cross = Cross(central)
        work = OldTexText("computational work")
        work.scale(1.5)
        work.move_to(central, LEFT)
        work.set_color(YELLOW)

        self.play(Write(words))
        self.play(ShowCreation(cross))
        central.add(cross)
        self.play(
            central.shift, DOWN,
            Write(work)
        )
        self.wait()
