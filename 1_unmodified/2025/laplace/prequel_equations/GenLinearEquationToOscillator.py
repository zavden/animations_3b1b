# ==============================================================================
# Scene:      GenLinearEquationToOscillator
# Source:     videos/_2025/laplace/prequel_equations.py (lines 633-667)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl GenLinearEquationToOscillator.py GenLinearEquationToOscillator -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class GenLinearEquationToOscillator(InteractiveScene):
    def construct(self):
        # General equation
        a_texs = ["a_n", "a_2", "a_1", "a_0"]
        x_texs = ["x^{n}(t)", "x''(t)", "x'(t)", "x(t)"]
        x_colors = color_gradient([BLUE, TEAL], len(x_texs), interp_by_hsl=True)
        t2c = dict()
        t2c.update({a: WHITE for a in a_texs})
        t2c.update({x: color for x, color in zip(x_texs, x_colors)})
        ode = Tex(R"a_n x^{n}(t) + \cdots + a_2 x''(t) + a_1 x'(t) + a_0 x(t) = 0", t2c=t2c, font_size=60)
        ode.move_to(DOWN)
        ode_2nd = ode["a_2 x''(t) + a_1 x'(t) + a_0 x(t) = 0"]

        self.play(Write(ode))
        self.wait()
        self.play(
            FadeOut(ode[R"a_n x^{n}(t) + \cdots + "]),
            ode_2nd.animate.move_to(UP),
            self.frame.animate.set_height(7)
        )

        # Transition
        alt_consts = VGroup(Tex(R"m"), Tex(R"\mu"), Tex(R"k"))
        alt_consts.scale(60 / 48)
        a_parts = VGroup(ode[tex][0] for tex in a_texs[1:])
        for const, a_part in zip(alt_consts, a_parts):
            const.move_to(a_part, RIGHT)
            const.align_to(ode[-1], DOWN)
            if const is alt_consts[1]:
                const.shift(0.1 * DOWN)
            self.play(
                FadeOut(a_part, 0.25 * UP),
                FadeIn(const, 0.25 * UP),
            )
        self.wait()
