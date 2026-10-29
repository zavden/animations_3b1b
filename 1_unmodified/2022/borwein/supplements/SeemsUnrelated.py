# ==============================================================================
# Scene:      SeemsUnrelated
# Source:     videos/_2022/borwein/supplements.py (lines 122-129)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SeemsUnrelated.py SeemsUnrelated -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SeemsUnrelated(InteractiveScene):
    def construct(self):
        # Test
        morty = Mortimer(height=2.0)
        morty.to_edge(DOWN)
        self.play(morty.says("That should modify\nthe area, right?", mode="maybe"))
        self.play(Blink(morty))
        self.wait()
