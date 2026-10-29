# ==============================================================================
# Scene:      NewNCubedArrow
# Source:     videos/_2024/puzzles/supplements.py (lines 125-133)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NewNCubedArrow.py NewNCubedArrow -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class NewNCubedArrow(InteractiveScene):
    def construct(self):
        arrow = Vector(1.5 * DOWN)
        label = Tex(R"N^3", font_size=72)
        label.next_to(arrow, RIGHT)
        self.play(GrowArrow(arrow))
        self.wait()
        self.play(Write(label))
        self.wait()
