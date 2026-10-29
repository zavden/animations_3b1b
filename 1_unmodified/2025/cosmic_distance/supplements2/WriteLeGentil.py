# ==============================================================================
# Scene:      WriteLeGentil
# Source:     videos/_2025/cosmic_distance/supplements2.py (lines 1390-1396)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteLeGentil.py WriteLeGentil -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteLeGentil(InteractiveScene):
    def construct(self):
        name = Text("Guillaume Le Gentil", font_size=72)
        name.to_corner(UL)
        name.set_backstroke(BLACK, 3)
        self.play(Write(name, stroke_color=WHITE))
        self.wait()
