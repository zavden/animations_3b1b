# ==============================================================================
# Scene:      StepFunctionSolutionFormla
# Source:     videos/_2019/diffyq/part4/staging.py (lines 1048-1082)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part2/wordy_scenes.py
#
# Run from this folder:
#     manimgl StepFunctionSolutionFormla.py StepFunctionSolutionFormla -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


# ----- From _2019/diffyq/part2/wordy_scenes.py -----

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



# ----- From _2019/diffyq/part4/staging.py -----

class StepFunctionSolutionFormla(WriteHeatEquationTemplate):
    CONFIG = {
        "tex_mobject_config": {
            "tex_to_color_map": {
                "{1}": WHITE,  # BLUE,
                "{3}": WHITE,  # GREEN,
                "{5}": WHITE,  # RED,
                "{7}": WHITE,  # YELLOW,
            },
        },
    }

    def construct(self):
        formula = OldTex(
            "T({x}, {t}) = ",
            "{4 \\over \\pi}",
            "\\left(",
            "{\\cos\\left({1}\\pi {x}\\right) \\over {1}}",
            "e^{-\\alpha {1}^2 {t} }",
            "-"
            "{\\cos\\left({3}\\pi {x}\\right) \\over {3}}",
            "e^{-\\alpha {3}^2 {t} }",
            "+",
            "{\\cos\\left({5}\\pi {x}\\right) \\over {5}}",
            "e^{-\\alpha {5}^2 {t} }",
            "- \\cdots",
            "\\right)",
            **self.tex_mobject_config,
        )

        formula.set_width(FRAME_WIDTH - 1)
        formula.to_edge(UP)

        self.play(FadeInFromDown(formula))
        self.wait()
