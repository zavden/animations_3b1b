# ==============================================================================
# Scene:      ApplicationNames
# Source:     videos/_2017/eoc/chapter3.py (lines 171-178)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ApplicationNames.py ApplicationNames -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ApplicationNames(Scene):
    def construct(self):
        for name in "Velocity", "Oscillation", "Population growth":
            mob = OldTexText(name)
            mob.scale(2)
            self.play(Write(mob))
            self.wait(2)
            self.play(FadeOut(mob))
