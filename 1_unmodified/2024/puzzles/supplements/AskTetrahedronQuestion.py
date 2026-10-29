# ==============================================================================
# Scene:      AskTetrahedronQuestion
# Source:     videos/_2024/puzzles/supplements.py (lines 373-384)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskTetrahedronQuestion.py AskTetrahedronQuestion -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskTetrahedronQuestion(InteractiveScene):
    def construct(self):
        question = Text("What is the volume\nof this solid?")
        # question = TexText(R"""
        #     What is the volume in terms of \\
        #     $(x_1, y_1, z_1)$, $(x_2, y_2, z_2)$\\
        #     $(x_3, y_3, z_3)$, and $(x_4, y_4, z_4)$
        # """)
        question.to_corner(UL)

        self.play(Write(question))
        self.wait()
