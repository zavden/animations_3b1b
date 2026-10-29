# ==============================================================================
# Scene:      ThreeConstraints
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 91-162)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part2/wordy_scenes.py
#
# Run from this folder:
#     manimgl ThreeConstraints.py ThreeConstraints -w -m --fps 15
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

class ThreeConstraints(WriteHeatEquationTemplate):
    def construct(self):
        self.cross_out_solving()
        self.show_three_conditions()

    def cross_out_solving(self):
        equation = self.get_d1_equation()
        words = OldTexText("Solve this equation")
        words.to_edge(UP)
        equation.next_to(words, DOWN)
        cross = Cross(words)

        self.add(words, equation)
        self.wait()
        self.play(ShowCreation(cross))
        self.wait()

        self.equation = equation
        self.to_remove = VGroup(words, cross)

    def show_three_conditions(self):
        equation = self.equation
        to_remove = self.to_remove

        title = OldTex(
            "\\text{Constraints }"
            "T({x}, {t})"
            "\\text{ must satisfy:}",
            **self.tex_mobject_config
        )
        title.to_edge(UP)

        items = VGroup(
            OldTexText("1)", "The PDE"),
            OldTexText("2)", "Boundary condition"),
            OldTexText("3)", "Initial condition"),
        )
        items.scale(0.7)
        items.arrange(RIGHT, buff=LARGE_BUFF)
        items.set_width(FRAME_WIDTH - 2)
        items.next_to(title, DOWN, LARGE_BUFF)
        items[1].set_color(MAROON_B)
        items[2].set_color(RED)

        bc_paren = OldTexText("(Explained soon)")
        bc_paren.scale(0.7)
        bc_paren.next_to(items[1], DOWN)

        self.play(
            FadeInFromDown(title),
            FadeOut(to_remove, UP),
            equation.scale, 0.6,
            equation.next_to, items[0], DOWN,
            equation.shift_onto_screen,
            LaggedStartMap(FadeIn, [
                items[0],
                items[1][0],
                items[2][0],
            ])
        )
        self.wait()
        self.play(Write(items[1][1]))
        bc_paren.match_y(equation)
        self.play(FadeIn(bc_paren, UP))
        self.wait(2)
        self.play(Write(items[2][1]))
        self.wait(2)

        self.title = title
        self.items = items
        self.pde = equation
        self.bc_paren = bc_paren
