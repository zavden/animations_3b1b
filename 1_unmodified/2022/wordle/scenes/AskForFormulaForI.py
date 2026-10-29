# ==============================================================================
# Scene:      AskForFormulaForI
# Source:     videos/_2022/wordle/scenes.py (lines 2132-2141)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskForFormulaForI.py AskForFormulaForI -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AskForFormulaForI(Scene):
    def construct(self):
        tex = OldTex(
            "I = ???",
            tex_to_color_map={"I": YELLOW},
            font_size=72,
        )
        tex.to_edge(UP)
        self.play(Write(tex))
        self.wait()
