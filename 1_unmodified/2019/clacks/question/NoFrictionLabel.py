# ==============================================================================
# Scene:      NoFrictionLabel
# Source:     videos/_2019/clacks/question.py (lines 634-644)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NoFrictionLabel.py NoFrictionLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NoFrictionLabel(Scene):
    def construct(self):
        words = OldTexText("Frictionless")
        words.shift(2 * RIGHT)
        words.add_updater(
            lambda m, dt: m.shift(dt * LEFT)
        )

        self.play(VFadeIn(words))
        self.wait(2)
        self.play(VFadeOut(words))
