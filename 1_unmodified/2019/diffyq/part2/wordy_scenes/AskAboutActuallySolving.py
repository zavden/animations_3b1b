# ==============================================================================
# Scene:      AskAboutActuallySolving
# Source:     videos/_2019/diffyq/part2/wordy_scenes.py (lines 614-648)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutActuallySolving.py AskAboutActuallySolving -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class WriteHeatEquationTemplate(Scene):
    CONFIG = {
        "tex_mobject_config": {
            "tex_to_color_map": {
                "{T}": WHITE,
                "{t}": YELLOW,
                "{x}": GREEN,
                "{y}": RED,
                "{z}": BLUE,
                "\\partial": WHITE,
                "2": WHITE,
            },
        },
    }

    def get_d1_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}({x}, {t})", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2} ({x}, {t})",
            **self.tex_mobject_config
        )

    def get_d1_equation_without_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            **self.tex_mobject_config
        )

    def get_d3_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2} + ",
            "{\\partial^2 {T} \\over \\partial {y}^2} + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_general_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha", "\\nabla^2 {T}",
            **self.tex_mobject_config,
        )

    def get_d3_equation_with_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}",
            "({x}, {y}, {z}, {t})", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {y}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "({x}, {y}, {z}, {t})",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_d1_words(self):
        return OldTexText("Heat equation\\\\", "(1 dimension)")

    def get_d3_words(self):
        return OldTexText("Heat equation\\\\", "(3 dimensions)")

    def get_d1_group(self):
        group = VGroup(
            self.get_d1_words(),
            self.get_d1_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group

    def get_d3_group(self):
        group = VGroup(
            self.get_d3_words(),
            self.get_d3_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group


class AskAboutActuallySolving(WriteHeatEquationTemplate):
    def construct(self):
        equation = self.get_d1_equation()
        equation.center()

        q1 = OldTexText("Solve for T?")
        q1.next_to(equation, UP, LARGE_BUFF)
        q2 = OldTexText("What does it \\emph{mean} to solve this?")
        q2.next_to(equation, UP, LARGE_BUFF)
        formula = OldTex(
            "T({x}, {t}) = \\sin\\big(a{x}\\big) e^{-\\alpha \\cdot a^2 {t}}",
            tex_to_color_map={
                "{x}": GREEN,
                "{t}": YELLOW,
            }
        )
        formula.next_to(equation, DOWN, LARGE_BUFF)
        q3 = OldTexText("Is this it?")
        arrow = Vector(LEFT, color=WHITE)
        arrow.next_to(formula, RIGHT)
        q3.next_to(arrow, RIGHT)

        self.add(equation)
        self.play(FadeInFromDown(q1))
        self.wait()
        self.play(
            FadeInFromDown(q2),
            q1.shift, 1.5 * UP,
        )
        self.play(FadeIn(formula, UP))
        self.play(
            GrowArrow(arrow),
            FadeIn(q3, LEFT)
        )
        self.wait()
