# ==============================================================================
# Scene:      ETitleCard
# Source:     videos/_2021/matrix_exp.py (lines 2818-2822)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ETitleCard.py ETitleCard -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ETitleCard(Scene):
    def construct(self):
        title = OldTexText("A brief review of $e$\\\\and exponentials")
        title.scale(2)
        self.add(title)
