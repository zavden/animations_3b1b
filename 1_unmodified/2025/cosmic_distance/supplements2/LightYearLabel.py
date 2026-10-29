# ==============================================================================
# Scene:      LightYearLabel
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 600-605)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LightYearLabel.py LightYearLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LightYearLabel(InteractiveScene):
    def construct(self):
        label = Text("4.25 Light years")
        self.play(Write(label))
        self.wait()
        self.play(FadeOut(label))
