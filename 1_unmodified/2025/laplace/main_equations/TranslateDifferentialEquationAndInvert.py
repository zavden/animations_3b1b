# ==============================================================================
# Scene:      TranslateDifferentialEquationAndInvert
# Source:     videos/_2025/laplace/main_equations.py (lines 378-485)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TranslateDifferentialEquationAndInvert.py TranslateDifferentialEquationAndInvert -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TranslateDifferentialEquationAndInvert(InteractiveScene):
    def construct(self):
        # Translate the equations
        colors = color_gradient([TEAL, RED], 3, interp_by_hsl=True)
        t2c = {
            R"{s}": YELLOW,
            R"x(t)": colors[0],
            R"x'(t)": colors[1],
            R"x''(t)": colors[2],
            R"\omega": PINK,
        }
        kw = dict(t2c=t2c, font_size=30)
        lhs = Tex(R"m x''(t) + \mu x'(t) + k x(t) = F_0 \cos(\omega t)", **kw)
        rhs1 = Tex(R"m {s}^2 X({s}) + \mu {s} X({s}) + k X({s}) = \frac{F_0 {s}}{({s}^2 + \omega^2)}", **kw)
        rhs2 = Tex(R"X({s}) \left( m {s}^2 + \mu {s} + k \right) = \frac{F_0 {s}}{({s}^2 + \omega^2)}", **kw)
        rhs3 = Tex(R"X({s}) = \frac{F_0 {s}}{\left({s}^2 + \omega^2\right) \left( m {s}^2 + \mu {s} + k \right)}", **kw)

        for sign, term in zip([-1, 1, 1, 1], [lhs, rhs1, rhs2, rhs3]):
            term.set_x(sign * FRAME_WIDTH / 4)
            term.set_y(3.25)
            term.scale(2)
            term.set_x(0)
            term.set_y(-sign * 2)

        arrow = Arrow(lhs, rhs1, thickness=6, buff=0.5)
        arrow_label = Tex(R"\mathcal{L}", font_size=72)
        arrow_label.next_to(arrow, RIGHT, SMALL_BUFF)

        ode_word = Text("Differential Equation")
        algebra_word = Text("Algebra")
        ode_word.next_to(lhs, DOWN)
        algebra_word.next_to(rhs1, DOWN)

        VGroup(ode_word, algebra_word).set_opacity(0)

        # Add domain backgrounds
        time_domain = FullScreenRectangle()
        time_domain.set_stroke(BLUE, 2)
        time_domain.set_fill(BLACK, 1)
        time_domain.stretch(0.5, 1, about_edge=UP)
        time_label = Text("Time domain")

        s_domain = time_domain.copy()
        s_domain.to_edge(DOWN, buff=0)
        s_domain.set_fill(GREY_E, 1)
        s_domain.set_stroke(YELLOW, 2)
        s_label = Text("s domain")

        for label, domain in [(time_label, time_domain), (s_label, s_domain)]:
            label.next_to(domain.get_corner(UL), DR)

        self.add(time_domain, time_label)
        self.add(s_domain, s_label)

        # Do the algebra
        self.play(
            FadeIn(lhs, lag_ratio=0.1),
            FadeIn(ode_word, lag_ratio=0.1),
        )
        self.wait()
        self.play(
            GrowArrow(arrow),
            FadeIn(arrow_label, DOWN),
        )
        self.play(
            TransformMatchingTex(
                lhs.copy(),
                rhs1,
                path_arc=-10 * DEG,
                lag_ratio=3e-2,
                key_map={
                    R"F_0 \cos(\omega t)": R"\frac{F_0 {s}}{({s}^2 + \omega^2)}",
                    "x(t) = ": "X({s}) = ",
                    "x'(t)": R"{s} X({s})",
                    "x''(t)": "{s}^2 X({s})",
                    "(t)": "({s})",
                }
            )
        )
        self.wait()
        self.play(
            FadeIn(algebra_word, 0.5 * DOWN),
            TransformMatchingTex(rhs1, rhs2, path_arc=-30 * DEG),
        )
        self.play(
            TransformMatchingTex(
                rhs2,
                rhs3,
                path_arc=-10 * DEG,
                matched_keys=[R"\left( m {s}^2 \mu s + k \right)", R"X({s})"]
            )
        )
        self.wait()

        # Show inversion
        inv_L = Tex(R"\mathcal{L}^{-1}", font_size=72)
        inv_L.next_to(arrow, LEFT, buff=0)

        xt = Text(R"Solution", font_size=72)
        xt.next_to(arrow, UP, MED_LARGE_BUFF)

        self.play(LaggedStart(
            Rotate(arrow, PI),
            ReplacementTransform(arrow_label, inv_L),
            lhs.animate.scale(0.5).to_corner(UR),
        ))
        self.play(FadeIn(xt, 2 * UP))
        self.wait()
