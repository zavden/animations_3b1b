# ==============================================================================
# Scene:      WriteHeatEquation
# Source:     videos/_2019/diffyq/part2/wordy_scenes.py (lines 352-410)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WriteHeatEquation.py WriteHeatEquation -w -m --fps 15
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


class WriteHeatEquation(WriteHeatEquationTemplate):
    def construct(self):
        title = OldTexText("The Heat Equation")
        title.to_edge(UP)

        equation = self.get_d1_equation()
        equation.next_to(title, DOWN)

        eq_i = equation.index_of_part_by_tex("=")
        dt_part = equation[:eq_i]
        dx_part = equation[eq_i + 3:]
        dt_rect = SurroundingRectangle(dt_part)
        dt_rect.set_stroke(YELLOW, 2)
        dx_rect = SurroundingRectangle(dx_part)
        dx_rect.set_stroke(GREEN, 2)

        two_outlines = equation.get_parts_by_tex("2").copy()
        two_outlines.set_stroke(YELLOW, 2)
        two_outlines.set_fill(opacity=0)

        to_be_explained = OldTexText(
            "To be explained shortly..."
        )
        to_be_explained.scale(0.7)
        to_be_explained.next_to(equation, RIGHT, MED_LARGE_BUFF)
        to_be_explained.fade(1)

        pde = OldTexText("Partial Differential Equation")
        pde.move_to(title)

        del_outlines = equation.get_parts_by_tex("\\partial").copy()
        del_outlines.set_stroke(YELLOW, 2)
        del_outlines.set_fill(opacity=0)

        self.play(
            FadeIn(title, 0.5 * DOWN),
            FadeIn(equation, 0.5 * UP),
        )
        self.wait()
        self.play(ShowCreation(dt_rect))
        self.wait()
        self.play(TransformFromCopy(dt_rect, dx_rect))
        self.play(ShowCreationThenDestruction(two_outlines))
        self.wait()
        self.play(Write(to_be_explained, run_time=1))
        self.wait(2)
        self.play(
            ShowCreationThenDestruction(
                del_outlines,
                lag_ratio=0.1,
            )
        )
        self.play(
            FadeOut(title, UP),
            FadeIn(pde, DOWN),
            FadeOut(dt_rect),
            FadeOut(dx_rect),
        )
        self.wait()
