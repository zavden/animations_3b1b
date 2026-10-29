# ==============================================================================
# Scene:      FromTwoToThree
# Source:     videos/_2021/newton_fractal.py (lines 3673-3687)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FromTwoToThree.py FromTwoToThree -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_newton_rule(font_size=36, var="z", **kwargs):
    terms = [f"{var}_n", f"{var}_{{n + 1}}"]
    t0, t1 = terms
    return OldTex(
        t1, "=", t0, "-",
        "{P(", t0, ")", "\\over ", "P'(", t0, ")}",
        font_size=36,
        **kwargs
    )


class EquationToFrame(Scene):
    def construct(self):
        self.add(FullScreenRectangle())
        screens = self.get_screens()
        arrow = Arrow(*screens)

        equation = get_newton_rule()
        equation.next_to(screens[0], UP)

        title = OldTexText("Unreasonable intricacy")
        title.next_to(screens[1], UP)

        self.wait()
        self.add(screens)
        self.add(equation)
        self.play(
            ShowCreation(arrow),
            FadeTransform(equation.copy(), title),
        )
        self.wait()

    def get_screens(self):
        screens = Square().get_grid(1, 2)
        screens.set_height(6)
        screens.set_width(FRAME_WIDTH - 1, stretch=True)
        screens.set_stroke(WHITE, 3)
        screens.set_fill(BLACK, 1)
        screens.arrange(RIGHT, buff=2.0)
        screens.to_edge(DOWN)
        return screens


class FromTwoToThree(EquationToFrame):
    def construct(self):
        self.add(FullScreenRectangle())
        screens = self.get_screens()
        arrow = Arrow(*screens)

        quadratic = OldTex("x^2 + c_1 x + c_0")
        cubic = OldTex("x^3 + c_2 x^2 + c_1 x + c_0")
        quadratic.next_to(screens[0], UP)
        cubic.next_to(screens[1], UP)

        self.add(screens)
        self.add(quadratic, cubic)
        self.play(ShowCreation(arrow))
        self.wait()
