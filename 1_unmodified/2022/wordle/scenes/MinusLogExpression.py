# ==============================================================================
# Scene:      MinusLogExpression
# Source:     videos/_2022/wordle/scenes.py (lines 2144-2152)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MinusLogExpression.py MinusLogExpression -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class MinusLogExpression(Scene):
    def construct(self):
        tex = OldTex(
            "I = -\\log_2(p)",
            tex_to_color_map={"I": YELLOW},
            font_size=60,
        )
        self.play(FadeIn(tex, DOWN))
        self.wait()
