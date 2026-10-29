# ==============================================================================
# Scene:      WriteHarvardComputer
# Source:     videos/_2025/cosmic_distance/part2.py (lines 1083-1089)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteHarvardComputer.py WriteHarvardComputer -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteHarvardComputer(InteractiveScene):
    def construct(self):
        words = Text("Harvard Computers", font_size=72)
        words.set_backstroke(BLACK, 8)
        words.to_corner(UL)
        self.play(Write(words))
        self.wait()
