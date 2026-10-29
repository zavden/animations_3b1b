# ==============================================================================
# Scene:      EvaluateF1
# Source:     videos/_2022/puzzles/subsets.py (lines 4909-4939)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl EvaluateF1.py EvaluateF1 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class EvaluateF1(InteractiveScene):
    def construct(self):
        tex_x = "f(x) = (1 + x)(1 + x^2)(1 + x^3)(1 + x^4)(1 + x^5)\\cdots\\left(1 + x^{2{,}000}\\right)"
        tex_1 = tex_x.replace("x", "{1}")
        fx = Tex(tex_x, tex_to_color_map={"x": BLUE})
        f1 = Tex(tex_1, tex_to_color_map={"{1}": GREEN})
        f1.match_width(fx)
        fx.to_edge(UP)
        f1.next_to(fx, DOWN, MED_LARGE_BUFF)

        xs = fx.select_parts("x")
        ones = f1.select_parts("{1}")
        fx_copy = fx.copy().move_to(f1)
        fx_copy.select_parts("x").set_opacity(0)

        brace = Brace(f1[5:], DOWN, buff=SMALL_BUFF)
        brace.stretch(0.5, 1, about_edge=UP)
        ans = Tex("2^{2{,}000}")
        ans.next_to(brace, DOWN, SMALL_BUFF)

        self.add(fx)
        self.play(TransformFromCopy(fx, fx_copy))
        self.play(Transform(xs.copy(), ones, lag_ratio=0.1, run_time=2, remover=True))
        self.remove(fx_copy)
        self.add(f1)
        self.wait()
        self.play(
            GrowFromCenter(brace),
            FadeIn(ans, 0.25 * DOWN)
        )
        self.wait()
