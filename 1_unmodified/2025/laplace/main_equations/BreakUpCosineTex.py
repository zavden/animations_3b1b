# ==============================================================================
# Scene:      BreakUpCosineTex
# Source:     videos/_2025/laplace/main_equations.py (lines 74-105)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl BreakUpCosineTex.py BreakUpCosineTex -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class BreakUpCosineTex(InteractiveScene):
    def construct(self):
        # Show sum
        pure_cos = Tex(R"\cos(t)", font_size=72)
        pure_cos.to_edge(UP)
        tex_pieces = [R"\cos(t)", "=", R"\frac{1}{2}", "e^{+it}", "{+}", R"{1 \over 2}", "e^{-it}"]
        sum_tex = Tex(" ".join(tex_pieces), t2c={"+i": YELLOW, "-i": YELLOW})
        sum_tex.to_edge(UP, buff=MED_SMALL_BUFF).shift(0.5 * RIGHT)
        cos, equals, half1, eit, plus, half2, enit = pieces = VGroup(
            sum_tex[tex][0] for tex in remove_list_redundancies(tex_pieces)
        )

        self.add(pure_cos)
        self.wait()
        self.play(
            FadeTransform(pure_cos, cos),
            Write(pieces[1:])
        )
        self.wait()

        # Fade parts
        pieces.generate_target()
        pieces.target.set_fill(opacity=0.35)
        pieces.target[3].set_fill(opacity=1)
        pieces.target.space_out_submobjects(1.2)
        self.play(MoveToTarget(pieces))
        self.wait()
        self.play(VGroup(plus, enit).animate.set_fill(opacity=1))
        self.wait()
        self.play(pieces.animate.set_fill(opacity=1))
        self.play(pieces.animate.space_out_submobjects(1 / 1.2))
        self.wait()
