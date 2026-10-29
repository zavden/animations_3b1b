# ==============================================================================
# Scene:      LeavittLabel
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 1276-1281)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LeavittLabel.py LeavittLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LeavittLabel(InteractiveScene):
    def construct(self):
        text = TexText(R"From Leavitt's\\1912 Paper")
        text.to_corner(UL)
        self.play(Write(text))
        self.wait()
