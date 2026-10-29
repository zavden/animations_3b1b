# ==============================================================================
# Scene:      OrdinaryApproach
# Source:     videos/_2023/convolutions2/supplements.py (lines 762-851)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OrdinaryApproach.py OrdinaryApproach -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class OrdinaryApproach(InteractiveScene):
    def construct(self):
        # Title
        self.add(FullScreenRectangle().scale(2))
        title = Text("Ordinary (messy) approach")
        title.set_x(0.25 * FRAME_WIDTH)
        title.to_edge(UP, buff=MED_SMALL_BUFF)
        title.set_backstroke()
        underline = Underline(title, buff=-0.05)
        self.play(
            ShowCreation(underline),
            FadeIn(title, lag_ratio=0.1),
        )
        self.wait()

        # Equations
        tex1 = R"f(x) = \frac{1}{\sigma_1 \sqrt{2\pi}} e^{-x^2 / 2\sigma_1^2}"
        tex2 = R"g(y) = \frac{1}{\sigma_2 \sqrt{2\pi}} e^{-y^2 / 2\sigma_2^2}"
        tex_kw = dict(
            font_size=30,
            t2c={"x": BLUE, "y": YELLOW}
        )
        equations = VGroup(
            Tex(tex1, **tex_kw),
            Tex(tex2, **tex_kw),
        )
        equations.arrange(DOWN, buff=0.75, aligned_edge=LEFT)
        equations.next_to(title, DOWN, buff=0.75, aligned_edge=LEFT)

        brace = Brace(equations[0], RIGHT, tex_string=R"\underbrace{\qquad\qquad\qquad}")
        brace.stretch(1.5, 1)
        brace_text = brace.get_text(
            "Formula\nfor a normal\ndistribution",
            font_size=30,
            alignment="LEFT",
            buff=MED_SMALL_BUFF,
        )

        self.play(LaggedStartMap(FadeIn, equations, lag_ratio=0.5, run_time=1))
        self.play(
            GrowFromCenter(brace),
            FadeIn(brace_text, lag_ratio=0.1)
        )
        self.wait()

        # Convolution
        conv_equation = Tex(
            R"""
                [f * g](s) = \int_{-\infty}^\infty f(x)g(s - x) dx
                = \int_{-\infty}^\infty \frac{1}{\sigma_1 \sigma_2 2 \pi} e^{-x^2 / 2\sigma_1^2} e^{-(s - x)^2 / 2\sigma_2^2} \; dx
            """,
            t2c={"x": BLUE, "s": GREEN},
            font_size=36,
        )
        conv_equation.move_to(1.0 * DOWN)
        rhss = conv_equation[re.compile(r"=.*dx")]
        lhs = conv_equation["[f * g](s)"]

        self.play(FadeIn(lhs), FadeIn(rhss[0]))
        self.wait()
        self.play(
            LaggedStart(
                FadeTransform(equations[0].copy(), rhss[1]),
                FadeTransform(equations[1].copy(), rhss[1]),
                FadeTransform(rhss[0].copy(), rhss[1]),
                lag_ratio=0.05,
            ),
            self.frame.animate.move_to(DOWN),
            run_time=2
        )
        self.wait()

        # Low brace
        low_brace = Brace(rhss[1][1:], DOWN, buff=SMALL_BUFF)
        calc_text = low_brace.get_text(
            "Not prohibitively difficult,\nbut a bit clunky",
            font_size=30
        )
        self.play(
            GrowFromCenter(low_brace),
            FadeIn(calc_text, lag_ratio=0.1)
        )
        self.wait()

        # Toss out formula
        to_toss = VGroup(conv_equation, low_brace, calc_text)
        self.play(
            FadeOut(to_toss, 6 * RIGHT, path_arc=-30 * DEGREES, rate_func=running_start, run_time=1)
        )
        self.wait()
