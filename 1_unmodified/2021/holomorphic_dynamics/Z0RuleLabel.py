# ==============================================================================
# Scene:      Z0RuleLabel
# Source:     videos/_2021/holomorphic_dynamics.py (lines 2601-2604)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Z0RuleLabel.py Z0RuleLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Z0RuleLabel(Scene):
    def construct(self):
        label = OldTex("z_0 = (r_1 + r_2 + r_3) / 3")
        self.add(label)
