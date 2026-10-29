# ==============================================================================
# Scene:      RightLeftArrow
# Source:     videos/_2023/optics_puzzles/ior_annotations.py (lines 1543-1547)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RightLeftArrow.py RightLeftArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RightLeftArrow(InteractiveScene):
    def construct(self):
        vect = Vector(DOWN)
        vect.to_edge(RIGHT)
        self.play(vect.animate.to_edge(LEFT), run_time=24, rate_func=linear)
