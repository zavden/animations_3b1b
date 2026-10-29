# ==============================================================================
# Scene:      WriteShorName
# Source:     videos/_2025/grover/qc_supplements.py (lines 1138-1143)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteShorName.py WriteShorName -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteShorName(InteractiveScene):
    def construct(self):
        name = Text("Peter Shor", font_size=72)
        name.to_corner(UR)
        self.play(Write(name, run_time=3))
        self.wait()
