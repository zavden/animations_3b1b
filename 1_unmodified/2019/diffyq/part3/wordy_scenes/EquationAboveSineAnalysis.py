# ==============================================================================
# Scene:      EquationAboveSineAnalysis
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 281-334)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part2/wordy_scenes.py
#
# Run from this folder:
#     manimgl EquationAboveSineAnalysis.py EquationAboveSineAnalysis -w -m --fps 15
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



# ----- From _2019/diffyq/part3/wordy_scenes.py -----

class EquationAboveSineAnalysis(WriteHeatEquationTemplate):
    def construct(self):
        equation = self.get_d1_equation()
        equation.to_edge(UP)
        equation.shift(2 * LEFT)
        eq_index = equation.index_of_part_by_tex("=")
        lhs = equation[:eq_index]
        eq = equation[eq_index]
        rhs = equation[eq_index + 1:]
        t_terms = equation.get_parts_by_tex("{t}")[1:]
        t_terms.save_state()
        zeros = VGroup(*[
            OldTex("0").replace(t, dim_to_match=1)
            for t in t_terms
        ])
        zeros.align_to(t_terms, DOWN)
        new_rhs = OldTex(
            "=", "-\\alpha \\cdot {T}", "({x}, 0)",
            **self.tex_mobject_config
        )
        # new_rhs.move_to(equation.get_right())
        # new_rhs.next_to(equation, DOWN, MED_LARGE_BUFF)
        # new_rhs.align_to(eq, LEFT)
        new_rhs.next_to(equation, RIGHT)
        new_rhs.shift(SMALL_BUFF * DOWN)

        self.add(equation)
        self.play(ShowCreationThenFadeAround(rhs))
        self.wait()
        self.play(
            FadeOut(t_terms, UP),
            FadeIn(zeros, DOWN),
        )
        t_terms.fade(1)
        self.wait()
        self.play(
            # VGroup(equation, zeros).next_to,
            # new_rhs, LEFT,
            FadeIn(new_rhs),
        )
        self.wait()
        self.play(
            VGroup(
                lhs[6:],
                eq,
                rhs,
                new_rhs[0],
                new_rhs[-3:],
                zeros,
            ).fade, 0.5,
        )
        self.play(ShowCreationThenFadeAround(lhs[:6]))
        self.play(ShowCreationThenFadeAround(new_rhs[1:-3]))
        self.wait()
