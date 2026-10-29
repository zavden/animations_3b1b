# ==============================================================================
# Scene:      ComplexEquation
# Source:     videos/_2021/matrix_exp.py (lines 4793-4893)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ComplexEquation.py ComplexEquation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ComplexEquation(Scene):
    def construct(self):
        # Equation
        equation = OldTex(
            """
            \\frac{d}{d{t} } \\Big[ x(t) + {i}y(t)\\Big] =
            {i} \\cdot \\Big[ x(t) + {i}y(t) \\Big]
            """,
            tex_to_color_map={
                "x": BLUE_B,
                "y": BLUE_D,
                "{t}": GREY_B,
                "=": WHITE,
                "\\cdot": WHITE,
                "{i}": RED,
            }
        )
        equation.move_to(2 * UP)

        braces = VGroup(*(
            Brace(equation[i:j], UP, buff=SMALL_BUFF)
            for i, j in [(2, 8), (11, 17)]
        ))
        braces.set_fill(GREY_A, 1)
        for brace in braces:
            brace.zt = OldTex("z(t)", tex_to_color_map={"z": BLUE, "t": GREY_B})
            brace.zt.next_to(brace, UP, SMALL_BUFF)

        self.add(equation)
        self.play(
            *(GrowFromCenter(b) for b in braces),
            *(FadeIn(b.zt, 0.25 * UP) for b in braces)
        )
        self.wait()

        # Show romeo and juilet
        x_part = equation.get_part_by_tex("x")
        y_part = equation.get_part_by_tex("y")

        juliet_label = OldTexText("Juliet's love", font_size=30)
        juliet_label.next_to(x_part, DOWN, LARGE_BUFF)
        romeo_label = OldTexText("Romeo's love", font_size=30)
        romeo_label.next_to(y_part, DOWN, LARGE_BUFF)
        juliet_label.align_to(romeo_label, DOWN)
        VGroup(juliet_label, romeo_label).space_out_submobjects(1.5)

        juliet_arrow = Arrow(x_part, juliet_label, buff=0.1, fill_color=BLUE_B)
        romeo_arrow = Arrow(y_part, romeo_label, buff=0.1, fill_color=BLUE_D)

        self.play(
            GrowArrow(juliet_arrow),
            FadeIn(juliet_label),
        )
        self.play(
            GrowArrow(romeo_arrow),
            FadeIn(romeo_label),
        )
        self.wait()

        # Describe i
        i_part = equation.get_parts_by_tex("{i}")[1]
        i_label = OldTexText("90-degree rotation", font_size=30)
        i_label.set_color(RED)
        i_label.next_to(romeo_label, RIGHT, MED_LARGE_BUFF, aligned_edge=DOWN)
        i_arrow = Arrow(i_part, i_label, fill_color=RED)

        self.play(
            GrowArrow(i_arrow),
            FadeIn(i_label, DR),
        )
        self.wait()

        all_labels = VGroup(romeo_label, juliet_label, i_label)

        # Show solution
        solution = OldTex(
            "z(t) = e^{it} z_0",
            tex_to_color_map={
                "i": RED,
                "t": GREY_B,
                "z": BLUE,
                "=": WHITE,
            }
        )
        solution.scale(1.5)
        solution.next_to(all_labels, DOWN, LARGE_BUFF)
        solution[8:].set_color(BLUE_D)

        self.play(
            TransformFromCopy(braces[0].zt, solution[:4]),
            Write(solution[4]),
        )
        self.play(
            Write(solution[5]),
            TransformFromCopy(equation[9], solution[6]),
            Write(solution[7]),
        )
        self.play(
            FadeIn(solution[8:], 0.1 * DOWN)
        )
        self.wait()
