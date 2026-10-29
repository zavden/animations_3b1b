# ==============================================================================
# Scene:      TopLabel
# Source:     videos/_2018/WindingNumber.py (lines 2716-2724)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TopLabel.py TopLabel -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings
import mpmath

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


mpmath.mp.dps = 7


class TopLabel(Scene):
    CONFIG = {
        "text" : "Text"
    }
    def construct(self):
        label = OldTexText(self.text)
        label.move_to(3 * UP)
        self.add(label)
        self.wait()
