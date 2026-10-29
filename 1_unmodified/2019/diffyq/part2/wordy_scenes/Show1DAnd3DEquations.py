# ==============================================================================
# Scene:      Show1DAnd3DEquations
# Source:     videos/_2019/diffyq/part2/wordy_scenes.py (lines 435-480)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Show1DAnd3DEquations.py Show1DAnd3DEquations -w -m --fps 15
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


class Show1DAnd3DEquations(WriteHeatEquationTemplate):
    def construct(self):
        d1_group = self.get_d1_group()
        d3_group = self.get_d3_group()
        d1_words, d1_equation = d1_group
        d3_words, d3_equation = d3_group

        groups = VGroup(d1_group, d3_group)
        for group in groups:
            group.arrange(DOWN, buff=MED_LARGE_BUFF)
        groups.arrange(RIGHT, buff=1.5)
        groups.to_edge(UP)

        d3_rhs = d3_equation[9:-2]
        d3_brace = Brace(d3_rhs, DOWN)
        nabla_words = OldTexText("Sometimes written as")
        nabla_words.match_width(d3_brace)
        nabla_words.next_to(d3_brace, DOWN)
        nabla_exp = OldTex(
            "\\nabla^2 {T}",
            **self.tex_mobject_config,
        )
        nabla_exp.next_to(nabla_words, DOWN)
        # nabla_group = VGroup(nabla_words, nabla_exp)

        d1_group.save_state()
        d1_group.center().to_edge(UP)

        self.play(
            Write(d1_words),
            FadeIn(d1_equation, UP),
            run_time=1,
        )
        self.wait(2)
        self.play(
            Restore(d1_group),
            FadeIn(d3_group, LEFT)
        )
        self.wait()
        self.play(
            GrowFromCenter(d3_brace),
            Write(nabla_words),
            TransformFromCopy(d3_rhs, nabla_exp),
            run_time=1,
        )
        self.wait()
