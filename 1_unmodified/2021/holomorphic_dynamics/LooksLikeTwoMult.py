# ==============================================================================
# Scene:      LooksLikeTwoMult
# Source:     videos/_2021/holomorphic_dynamics.py (lines 1739-1746)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LooksLikeTwoMult.py LooksLikeTwoMult -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LooksLikeTwoMult(Scene):
    const = "2"

    def construct(self):
        tex = OldTexText(f"Looks like $z \\rightarrow {self.const}\\cdot z$")
        tex.set_stroke(BLACK, 5, background=True)
        self.play(FadeIn(tex, lag_ratio=0.1))
        self.wait()
