# ==============================================================================
# Scene:      RationalFunctions
# Source:     videos/_2021/holomorphic_dynamics.py (lines 501-630)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RationalFunctions.py RationalFunctions -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RationalFunctions(Scene):
    def construct(self):
        # Show function
        equation = OldTex(
            "f(z)",
            "=", "z - {P(z) \\over P'(z)}",
            "=", "z - {z^3 - 1 \\over 3z^2}",
            "=", "{2z^3 + 1 \\over 3z^2}"
        )
        iter_brace = Brace(equation[2], UP)
        iter_text = iter_brace.get_text("What's being iterated")
        VGroup(iter_brace, iter_text).set_color(BLUE_D)
        example_brace = Brace(equation[4], DOWN)
        example_text = example_brace.get_text("For example")
        VGroup(example_brace, example_text).set_color(TEAL_D)

        self.play(
            FadeIn(equation[:3]),
            GrowFromCenter(iter_brace),
            FadeIn(iter_text, 0.5 * UP)
        )
        self.wait()
        self.play(
            FadeIn(equation[3:5]),
            GrowFromCenter(example_brace),
            FadeIn(example_text, 0.5 * DOWN),
        )
        self.wait()
        self.play(
            Write(equation[5]),
            LaggedStart(*(
                FadeTransform(equation[4][i].copy(), equation[6][j])
                for i, j in zip(
                    [1, 0, *range(2, 10)],
                    [0, 0, *range(1, 9)],
                )
            ), lag_ratio=0.02)
        )
        self.add(equation[6])
        self.play(
            LaggedStart(*(
                FadeTransform(equation[4][i].copy().set_opacity(0), equation[6][j].copy().set_opacity(0))
                for i, j in zip(
                    [0, 0, 0, 0],
                    [0, 0, 0, 0],
                )
            ), lag_ratio=0.02)
        )
        self.add(equation)
        self.wait()

        # Name rational function
        box = SurroundingRectangle(equation[6], buff=SMALL_BUFF)
        box.set_stroke(YELLOW, 2)
        rational_name = OldTexText("``Rational function''")
        rational_name.next_to(box, UP, buff=1.5)
        arrow = Arrow(rational_name, box)

        self.play(
            Write(rational_name),
            ShowCreation(arrow),
            ShowCreation(box),
        )
        self.wait()

        # Forget about the Newton's method origins
        self.play(
            equation[:2].animate.next_to(ORIGIN, LEFT, SMALL_BUFF),
            equation[2:6].animate.set_opacity(0.5).scale(0.5).to_corner(DR),
            VGroup(equation[6], box).animate.next_to(ORIGIN, RIGHT, SMALL_BUFF),
            MaintainPositionRelativeTo(
                VGroup(rational_name, arrow),
                box,
            ),
            FadeOut(
                VGroup(example_brace, example_text, iter_brace, iter_text),
                shift=2 * RIGHT + DOWN
            )
        )
        self.wait()

        # Other rational functions
        frame = self.camera.frame

        rhs = equation[6]
        functions = VGroup(
            OldTex("3z^4 + z^3 + 4 \\over z^5 + 5z + 9"),
            OldTex("2z^6 + 7z^4 + 1z \\over 8z^3 + 2z^2 + 8"),
            OldTex("(z^2 + 1)^2 \\over 4z(z^2 - 1)"),
            OldTex("az + b \\over cz + d"),
            OldTex("z^2 + az + b \\over z^2 + cz + d"),
            OldTex(
                "a_n z^n + \\cdots + a_0 \\over "
                "b_m z^m + \\cdots + b_0"
            ),
            OldTex("z^2 + c \\over 1"),
        )

        for function in functions:
            function.replace(rhs, dim_to_match=1)
            function.move_to(rhs, LEFT)
            function.set_max_width(rhs.get_width() + 2)

        for n, function in enumerate(functions):
            self.play(
                FadeOut(rhs, lag_ratio=0.1),
                FadeIn(function, lag_ratio=0.1),
                box.animate.set_opacity(0),
            )
            self.remove(box)
            self.wait()
            if n == 0:
                self.play(
                    rational_name.animate.next_to(box, UP),
                    arrow.animate.scale(0, about_edge=DOWN),
                    ApplyMethod(frame.shift, 2 * DOWN, run_time=2),
                    FadeOut(equation[2:6]),
                )
            else:
                self.wait()
            rhs = function[0]

        self.play(
            FadeOut(box),
            FadeOut(rational_name),
            FadeOut(rhs[4:]),
            rhs[:4].animate.next_to(ORIGIN, RIGHT, SMALL_BUFF).shift(0.07 * UP),
            frame.animate.shift(DOWN),
        )
        self.wait()
