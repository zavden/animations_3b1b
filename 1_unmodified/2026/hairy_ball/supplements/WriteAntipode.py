# ==============================================================================
# Scene:      WriteAntipode
# Source:     videos/_2026/hairy_ball/supplements.py (lines 161-173)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteAntipode.py WriteAntipode -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteAntipode(InteractiveScene):
    def construct(self):
        # Test
        text1 = Text("“Antipodes”")
        text2 = Text("Antipode map")
        for text in [text1, text2]:
            text.scale(1.5)
            text.to_corner(UL)

        self.play(Write(text1), run_time=2)
        self.wait()
        self.play(TransformMatchingStrings(text1, text2), run_time=1)
        self.wait()
