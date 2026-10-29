# ==============================================================================
# Scene:      TakePartialDerivatives
# Source:     videos/_2017/gradient.py (lines 172-318)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TakePartialDerivatives.py TakePartialDerivatives -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TakePartialDerivatives(Scene):
    def construct(self):
        tex_to_color_map = {
            "x": BLUE,
            "y": RED,
        }
        func_tex = OldTex(
            "f", "(", "x", ",", "y", ")", "=",
            "e^{", "-x^2", "+ \\cos(2y)}",
            tex_to_color_map=tex_to_color_map
        )
        partial_x = OldTex(
            "{\\partial", "f", "\\over", "\\partial", "x}", "=",
            "\\left(", "e^", "{-x^2", "+ \\cos(2y)}", "\\right)",
            "(", "-2", "x", ")",
            tex_to_color_map=tex_to_color_map,
        )
        partial_y = OldTex(
            "{\\partial", "f", "\\over", "\\partial", "y}", "=",
            "\\left(", "e^", "{-x^2", "+ \\cos(", "2", "y)}", "\\right)",
            "(", "-\\sin(", "2", "y)", "\\cdot 2", ")",
            tex_to_color_map=tex_to_color_map,
        )
        partials = VGroup(partial_x, partial_y)
        for mob in func_tex, partials:
            mob.scale(1.5)

        func_tex.move_to(2 * UP + 3 * LEFT)
        for partial in partials:
            partial.next_to(func_tex, DOWN, buff=LARGE_BUFF)
            top_eq_x = func_tex.get_part_by_tex("=").get_center()[0]
            low_eq_x = partial.get_part_by_tex("=").get_center()[0]
            partial.shift((top_eq_x - low_eq_x) * RIGHT)

        index = func_tex.index_of_part_by_tex("e^")
        exp_rect = SurroundingRectangle(func_tex[index + 1:], buff=0)
        exp_rect.set_stroke(width=0)
        exp_rect.set_fill(GREEN, opacity=0.5)

        xs = func_tex.get_parts_by_tex("x", substring=False)
        ys = func_tex.get_parts_by_tex("y", substring=False)
        for terms in xs, ys:
            terms.rects = VGroup(*[
                SurroundingRectangle(term, buff=0.5 * SMALL_BUFF)
                for term in terms
            ])
            terms.arrows = VGroup(*[
                Vector(0.5 * DOWN).next_to(rect, UP, SMALL_BUFF)
                for rect in terms.rects
            ])
        treat_as_constant = OldTexText("Treat as a constant")
        treat_as_constant.next_to(ys.arrows[1], UP)

        # Start to show partial_x
        self.play(FadeInFromDown(func_tex))
        self.wait()
        self.play(
            ReplacementTransform(func_tex[0].copy(), partial_x[1]),
            Write(partial_x[0]),
            Write(partial_x[2:4]),
            Write(partial_x[6]),
        )
        self.play(
            ReplacementTransform(func_tex[2].copy(), partial_x[4])
        )
        self.wait()

        # Label y as constant
        self.play(LaggedStartMap(ShowCreation, ys.rects))
        self.play(
            LaggedStartMap(GrowArrow, ys.arrows, lag_ratio=0.8),
            Write(treat_as_constant)
        )
        self.wait(2)

        # Perform partial_x derivative
        self.play(FadeIn(exp_rect), Animation(func_tex))
        self.wait()
        pxi1 = 8
        pxi2 = 15
        self.play(
            ReplacementTransform(
                func_tex[7:].copy(),
                partial_x[pxi1:pxi2],
            ),
            FadeIn(partial_x[pxi1 - 1:pxi1]),
            FadeIn(partial_x[pxi2]),
        )
        self.wait(2)
        self.play(
            ReplacementTransform(
                partial_x[10:12].copy(),
                partial_x[pxi2 + 2:pxi2 + 4],
                path_arc=-(TAU / 4)
            ),
            FadeIn(partial_x[pxi2 + 1]),
            FadeIn(partial_x[-1]),
        )
        self.wait(2)

        # Swap out partial_x for partial_y
        self.play(
            FadeOutAndShiftDown(partial_x),
            FadeOut(ys.rects),
            FadeOut(ys.arrows),
            FadeOut(treat_as_constant),
            FadeOut(exp_rect),
            Animation(func_tex)
        )
        self.play(FadeInFromDown(partial_y[:7]))
        self.wait()

        treat_as_constant.next_to(xs.arrows[1], UP, SMALL_BUFF)
        self.play(
            LaggedStartMap(ShowCreation, xs.rects),
            LaggedStartMap(GrowArrow, xs.arrows),
            Write(treat_as_constant),
            lag_ratio=0.8
        )
        self.wait()

        # Show same outer derivative
        self.play(
            ReplacementTransform(
                func_tex[7:].copy(),
                partial_x[pxi1:pxi2],
            ),
            FadeIn(partial_x[pxi1 - 2:pxi1]),
            FadeIn(partial_x[pxi2]),
        )
        self.wait()
        self.play(
            ReplacementTransform(
                partial_y[12:16].copy(),
                partial_y[pxi2 + 3:pxi2 + 7],
                path_arc=-(TAU / 4)
            ),
            FadeIn(partial_y[pxi2 + 2]),
            FadeIn(partial_y[-1]),
        )
        self.wait()
        self.play(ReplacementTransform(
            partial_y[-5].copy(),
            partial_y[-2],
            path_arc=-PI
        ))
        self.wait()
