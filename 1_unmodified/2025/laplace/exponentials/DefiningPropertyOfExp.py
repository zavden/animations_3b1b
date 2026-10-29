# ==============================================================================
# Scene:      DefiningPropertyOfExp
# Source:     videos/_2025/laplace/exponentials.py (lines 313-362)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DefiningPropertyOfExp.py DefiningPropertyOfExp -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DefiningPropertyOfExp(InteractiveScene):
    def construct(self):
        # Key property
        tex_kw = dict(t2c={"{t}": GREY_B, "x": BLUE})
        equation = Tex(R"\frac{d}{d{t}} e^{t} = e^{t}", font_size=90, **tex_kw)

        exp_parts = equation["e^{t}"]
        ddt = equation[R"\frac{d}{d{t}}"]

        self.play(Write(exp_parts[0]))
        self.wait()
        self.play(FadeIn(ddt, scale=2))
        self.play(
            Write(equation["="]),
            TransformFromCopy(*exp_parts, path_arc=PI / 2),
        )
        self.wait()

        # Differential Equation
        ode = Tex(R"x'(t) = x(t)", font_size=72, **tex_kw)
        ode.move_to(equation).to_edge(UP)
        ode_label = Text("Differential\nEquation", font_size=36)
        ode_label.next_to(ode, LEFT, LARGE_BUFF, aligned_edge=DOWN)

        self.play(
            FadeTransform(equation.copy(), ode),
            FadeIn(ode_label)
        )
        self.wait()

        # Initial condition
        frame = self.frame
        abs_ic = Tex(R"x(0) = 1", font_size=72, **tex_kw)
        exp_ic = Tex(R"e^{0} = 1", font_size=90, t2c={"0": GREY_B})
        abs_ic.next_to(ode, RIGHT, buff=2.0)
        exp_ic.match_x(abs_ic).match_y(equation).shift(0.1 * UP)
        ic_label = Text("Initial\nCondition", font_size=36)
        ic_label.next_to(abs_ic, RIGHT, buff=0.75)

        self.play(
            FadeIn(abs_ic, RIGHT),
            FadeIn(exp_ic, RIGHT),
            frame.animate.set_x(2),
            Write(ic_label)
        )
        self.wait()

        # Scroll down
        self.play(frame.animate.set_y(-2.5), run_time=2)
        self.wait()
