# ==============================================================================
# Scene:      NamePdfs
# Source:     videos/_2020/beta/beta2.py (lines 419-423)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NamePdfs.py NamePdfs -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NamePdfs(Scene):
    def construct(self):
        label = OldTexText("Probability density\\\\function")
        self.play(Write(label))
        self.wait()
