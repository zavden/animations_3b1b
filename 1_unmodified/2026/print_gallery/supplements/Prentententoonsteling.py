# ==============================================================================
# Scene:      Prentententoonsteling
# Source:     videos/_2026/print_gallery/supplements.py (lines 17-21)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Prentententoonsteling.py Prentententoonsteling -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Prentententoonsteling(InteractiveScene):
    def construct(self):
        text = Text("“Prentententoonstelling.”")
        self.play(Write(text), lag_ratio=0.02, run_time=2)
        self.wait()
