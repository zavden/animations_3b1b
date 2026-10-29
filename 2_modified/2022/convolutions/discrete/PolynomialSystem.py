# ==============================================================================
# Scene:      PolynomialSystem
# Source:     videos/_2022/convolutions/discrete.py (lines 2192-2465)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PolynomialSystem.py PolynomialSystem -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - label and short_label change from OldTexText to TexText: TransformMatchingTex only accepts StringMobject (OldTexText has no get_symbol_substrings)
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class PolynomialSystem(InteractiveScene):
    N = 8

    def construct(self):
        # Setup polynomials
        frame = self.camera.frame
        N = self.N
        coefs = VGroup(*(Tex(Rf"c_{{{n}}}") for n in range(N)))
        coefs.set_submobject_colors_by_gradient(BLUE, TEAL)
        x_powers = VGroup(*(Tex(Rf"x^{{{n}}}") for n in range(N)))
        poly_x = self.get_polynomial(coefs, x_powers)

        top_lhs = Tex("h(x) = ")
        top_lhs.next_to(poly_x[0][0], LEFT, buff=0.1)
        top_eq = VGroup(top_lhs, poly_x)
        top_eq.center()

        fg = Tex(R"f(x) \cdot g(x)")
        eq = Tex("=")
        eq.rotate(PI / 2)
        eq.next_to(top_lhs[:4], UP)
        fg.next_to(eq, UP).shift_onto_screen()

        self.add(top_eq)

        # Suppose you don't know coefficients
        words = Text("Suppose these are a mystery")
        words.next_to(poly_x, UP, buff=2.0)
        arrows = VGroup(*(
            Arrow(
                interpolate(
                    words.get_corner(DL) + 0.5 * RIGHT,
                    words.get_corner(DR) + 0.5 * LEFT,
                    n / (N - 1)),
                coef,
                color=coef.get_color(),
            )
            for n, coef in enumerate(poly_x.coefs)
        ))

        self.play(
            FadeIn(words, lag_ratio=0.1),
            LaggedStartMap(GrowArrow, arrows),
            LaggedStart(*(
                FlashAround(coef, time_width=1)
                for coef in poly_x.coefs
            ), lag_ratio=0.1, run_time=3)
        )
        self.wait()
        self.play(
            Write(eq),
            FadeIn(fg, 0.25 * UP)
        )
        self.wait()

        # Sweep away
        self.play(
            LaggedStart(
                FadeOut(words, UP),
                FadeOut(arrows, 2 * UP, lag_ratio=0.05),
                FadeOut(fg, UP),
                FadeOut(eq, 1.5 * UP),
                top_eq.animate.to_edge(UP)
            ),
            frame.animate.set_height(11, about_edge=UR),
            run_time=2
        )

        # Set up the large system
        lhss = VGroup(*(Tex(f"h({n})=") for n in range(N)))
        rhss = VGroup(*(
            self.get_polynomial(
                coefs.copy(),
                # VGroup(*(Integer(x**n) for n in range(N)))
                VGroup(*(Tex(f"{x}^{{{n}}}") for n in range(N)))
            )
            for x in range(N)
        ))
        equations = VGroup()
        for lhs, rhs in zip(lhss, rhss):
            lhs.next_to(rhs[0][0], LEFT, 0.1)
            equations.add(VGroup(lhs, rhs))
        equations.arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        equations.next_to(top_eq, DOWN, aligned_edge=LEFT, buff=1.5)

        self.play(
            LaggedStart(*(
                FadeTransform(top_eq.copy(), eq)
                for eq in equations
            ), lag_ratio=0.02, run_time=3),
        )

        # Suppose you _do_ know h(0), h(1), h(2), etc.
        words2 = Text("But suppose\nyou do know\nthese", t2s={"do": ITALIC})
        words2.set_color(YELLOW)
        words2.move_to(midpoint(equations.get_left(), frame.get_left()))
        words2.align_to(equations, UP)

        self.play(
            Write(words2),
            LaggedStart(*(FlashAround(lhs[:4], time_width=1.5) for lhs in lhss), run_time=5, lag_ratio=0.1)
        )
        self.wait()

        # Trow out the inputs
        inputs = VGroup(*(lhs[2] for lhs in lhss))
        inputs.save_state()
        consts = VGroup(*(
            power
            for eq in rhss
            for power in eq.powers
        ))
        boxes = VGroup(*(VGroup(SurroundingRectangle(const, buff=0)) for const in consts))
        boxes.set_stroke(RED, 1)

        self.play(
            FadeOut(words2, LEFT, rate_func=running_start),
            inputs.animate.set_color(RED).shift(2 * LEFT).set_anim_args(run_time=1.5, lag_ratio=0.2, path_arc=PI / 2),
            Transform(consts, boxes, lag_ratio=0.01, run_time=3),
        )
        self.play(FadeOut(inputs, LEFT, lag_ratio=0.2, rate_func=running_start))
        inputs.restore()
        inputs.set_opacity(0)
        self.add(lhss)

        # Add roots of unity
        kw = dict(tex_to_color_map={R"\omega": YELLOW})
        omega_def = OldTex(
            Rf"""
            \text{{Let }} \omega = e^{{2\pi i / {N}}} \qquad
            \text{{Notice }} \omega^{{{N}}} = 1
            """,
            font_size=60,
            **kw
        )
        omega_def.next_to(lhss, UP, buff=1.5, aligned_edge=LEFT)

        all_omega_powers = [
            VGroup(*(
                Tex(Rf"\omega^{{{(k * n) % N}}}", **kw)
                for n in range(N)
            ))
            for k in range(0, N)
        ]
        new_rhss = VGroup(*(
            self.get_polynomial(coefs.copy(), omega_powers)
            for omega_powers in all_omega_powers
        ))

        new_lhss = VGroup(
            *(Tex(Rf"h(\omega^{n}) = ") for n in range(N))
        )

        self.play(
            frame.animate.set_height(13, about_edge=DR),
            FadeIn(omega_def),
            top_eq.animate.shift(1.75 * UP),
        )
        for old_lhs, old_rhs, new_lhs, new_rhs in zip(lhss, rhss, new_lhss, new_rhss):
            new_lhs.move_to(old_lhs, LEFT)
            new_rhs.next_to(new_lhs, RIGHT, buff=0.1)
            new_lhs[2].set_color(YELLOW)
            self.play(
                FadeTransformPieces(old_lhs, new_lhs),
                FadeTransformPieces(old_rhs, new_rhs),
            )
        self.wait()

        # Label as DFT
        brace = Brace(new_lhss, LEFT)
        kw = dict(font_size=60)
        # CHANGE: TransformMatchingTex requires a StringMobject (new Tex/TexText); OldTexText has no get_symbol_substrings
        label = TexText(R"Discrete\\Fourier\\Transform", alignment=R"\raggedright", isolate=list("DFT"), **kw)
        label.next_to(brace, LEFT)

        sub_label = OldTexText("of $(c_i)$", **kw)[0]
        sub_label[2:].set_color(BLUE)
        sub_label.next_to(label, DOWN, MED_LARGE_BUFF, aligned_edge=LEFT)

        self.play(GrowFromCenter(brace), FadeIn(label))
        self.play(Write(sub_label))
        self.wait()

        # Show redundancy
        last_rects = VGroup()
        for n in range(N):
            tex = Rf"\omega^{{{n}}}"
            rects = VGroup()
            for rhs in new_rhss:
                for power in rhs.powers[1:]:
                    if power.get_tex() == tex:
                        rects.add(SurroundingRectangle(power))
            rects.set_stroke(RED, 3)
            self.play(FadeIn(rects), FadeOut(last_rects))
            last_rects = rects
        self.play(FadeOut(last_rects))

        # Set up two arrays
        pre_h_list = VGroup(*(lhs[:5] for lhs in new_lhss))
        h_list = pre_h_list.copy()
        h_list.next_to(new_lhss, LEFT, buff=2.0)
        h_rect = SurroundingRectangle(h_list, buff=0.25)
        h_rect.set_stroke(WHITE, 1)
        h_rect.set_fill(GREY_E, 1)

        c_list = poly_x.coefs.copy()
        for c, h in zip(c_list, h_list):
            c.scale(1.25)
            c.move_to(h)

        c_rect = h_rect.copy()
        c_rect.shift(5 * LEFT)
        c_list.move_to(c_rect)

        # CHANGE: new TexText (see above) so that TransformMatchingTex can be used
        short_label = TexText("DFT", isolate=list("DFT"))
        short_label.next_to(h_rect, UP, buff=0.5).shift(sub_label.get_width() * LEFT / 2)

        self.play(
            FadeIn(c_rect),
            TransformFromCopy(new_rhss[0].coefs, c_list, path_arc=-PI / 3)
        )
        self.play(
            TransformMatchingTex(label, short_label),
            sub_label.animate.scale(48 / 60).next_to(short_label, RIGHT),
            FadeInFromPoint(h_rect, pre_h_list.get_center()),
            TransformFromCopy(pre_h_list, h_list),
        )

        # Indicate fast back and forth
        top_arrow = Arrow(c_rect, h_rect).shift(2 * UP)
        low_arrow = Arrow(h_rect, c_rect).shift(2 * DOWN)

        for arrow in (top_arrow, low_arrow):
            fft_label = Text("FFT")
            fft_label.next_to(arrow, UP)
            run_time = OldTex(R"\mathcal{O}\big(N\log(N)\big)")
            run_time.next_to(arrow, DOWN)
            arrow.fft_label = fft_label
            arrow.run_time = run_time

            self.play(
                GrowArrow(arrow),
                FadeIn(fft_label, arrow.get_vector())
            )
            self.play(FadeIn(run_time, 0.5 * DOWN))
            self.wait()

    def get_polynomial(self, coefs, powers, buff=0.1):
        result = VGroup()
        result.plusses = VGroup()
        result.dots = VGroup()
        for coef, power in zip(coefs, powers):
            if power is powers[0]:
                power.scale(0, about_edge=LEFT)
            plus = OldTex("+")  # Font size?
            result.add(coef)
            if isinstance(power, Integer):
                dot = OldTex(R"\cdot")
            else:
                dot = VGroup(VectorizedPoint())
            result.dots.add(dot)
            result.add(dot)
            result.add(power, plus)
            result.plusses.add(plus)
        result.remove(result[-1])  # Stray plus
        result.arrange(RIGHT, buff=buff)
        for mob in result:
            mob.shift(mob[0].get_y(DOWN) * DOWN)
        for coef, dot in zip(coefs, result.dots):
            if not isinstance(dot, Tex):
                coef.shift(buff * RIGHT)
        result.dots.set_y(result.get_y())
        result.coefs = coefs
        result.powers = powers
        return result
