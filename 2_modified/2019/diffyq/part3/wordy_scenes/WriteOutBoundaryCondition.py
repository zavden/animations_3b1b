# ==============================================================================
# Scene:      WriteOutBoundaryCondition
# Source:     videos/_2019/diffyq/part3/wordy_scenes.py (lines 709-762)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part2/wordy_scenes.py
#
# Run from this folder:
#     manimgl WriteOutBoundaryCondition.py WriteOutBoundaryCondition -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use CairoImageMobject to keep Cairo's default height and pixel reading, without changing other years.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's height (2) and the pixel_array reading through a local adapter.
from cairo_compat import CairoImageMobject as ImageMobject


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


class FlatAtBoundaryWords(Scene):
    def construct(self):
        words = self.get_bc_words()
        self.play(Write(words))
        self.wait()

    def get_bc_words(self):
        return OldTexText(
            "Flat at boundary\\\\"
            "for all", "${t}$", "$> 0$",
        )


class WriteOutBoundaryCondition(FlatAtBoundaryWords, ThreeConstraints, MovingCameraScene):
    def construct(self):
        self.force_skipping()
        ThreeConstraints.construct(self)
        self.revert_to_original_skipping_status()

        self.add_ic()
        self.write_bc_words()
        self.write_bc_equation()

    def add_ic(self):
        image = ImageMobject("temp_initial_condition_example")
        image.set_width(3)
        border = SurroundingRectangle(image, buff=SMALL_BUFF)
        border.shift(SMALL_BUFF * UP)
        border.set_stroke(WHITE, 2)
        group = Group(image, border)
        group.next_to(self.items[2], DOWN)
        self.add(group)

    def write_bc_words(self):
        bc_paren = self.bc_paren
        bc_words = self.get_bc_words()
        bc_words.match_width(self.items[1][1])
        bc_words.move_to(bc_paren, UP)
        bc_words.set_color_by_tex("{t}", YELLOW)

        self.play(ShowCreationThenFadeAround(
            VGroup(self.items[0], self.pde)
        ))
        self.play(
            FadeOut(bc_paren, UP),
            FadeIn(bc_words, DOWN),
        )
        self.wait()

        self.bc_words = bc_words

    def write_bc_equation(self):
        bc_words = self.bc_words

        equation = OldTex(
            "{\\partial {T} \\over \\partial {x}}(0, {t}) = ",
            "{\\partial {T} \\over \\partial {x}}(L, {t}) = ",
            "0",
            **self.tex_mobject_config,
        )
        equation.next_to(bc_words, DOWN, MED_LARGE_BUFF)

        self.play(
            self.camera_frame.shift, 0.8 * DOWN,
        )
        self.play(FadeIn(equation, UP))
        self.wait()
