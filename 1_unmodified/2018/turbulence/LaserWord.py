# ==============================================================================
# Scene:      LaserWord
# Source:     videos/_2018/turbulence.py (lines 1769-1771)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LaserWord.py LaserWord -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LaserWord(Scene):
    def construct(self):
        self.add(OldTexText("Laser").scale(2))
