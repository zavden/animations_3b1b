# ==============================================================================
# Scene:      WriteName
# Source:     videos/_2022/galois/art_supplements.py (lines 35-41)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteName.py WriteName -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteName(InteractiveScene):
    def construct(self):
        self.play(Write(
            Text("Évariste Galois", font_size=90).to_corner(UL),
            run_time=3
        ))
        self.wait()
