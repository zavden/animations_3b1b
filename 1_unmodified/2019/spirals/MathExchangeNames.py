# ==============================================================================
# Scene:      MathExchangeNames
# Source:     videos/_2019/spirals.py (lines 242-251)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MathExchangeNames.py MathExchangeNames -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MathExchangeNames(Scene):
    def construct(self):
        names = VGroup(
            OldTexText("dwymark"),
            OldTexText("Greg Martin"),
        )
        names.arrange(DOWN, buff=1)
        for name in names:
            self.play(FadeIn(name, RIGHT))
            self.wait()
