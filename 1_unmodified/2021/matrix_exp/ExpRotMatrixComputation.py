# ==============================================================================
# Scene:      ExpRotMatrixComputation
# Source:     videos/_2021/matrix_exp.py (lines 3798-4023)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExpRotMatrixComputation.py ExpRotMatrixComputation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_matrix_exponential(matrix, height=1.5, scalar_tex="t", **matrix_config):
    elem = matrix[0][0]
    if isinstance(elem, str):
        mat_class = Matrix
    elif isinstance(elem, int) or isinstance(elem, np.int64):
        mat_class = IntegerMatrix
    else:
        mat_class = DecimalMatrix

    matrix = mat_class(matrix, **matrix_config)
    base = OldTex("e")
    base.set_height(0.4 * height)
    matrix.set_height(0.6 * height)
    matrix.move_to(base.get_corner(UR), DL)
    result = VGroup(base, matrix)
    if scalar_tex:
        scalar = OldTex(scalar_tex)
        scalar.set_height(0.7 * base.get_height())
        scalar.next_to(matrix, RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
        result.add(scalar)
    return result


class ExpRotMatrixComputation(Scene):
    def construct(self):
        # Plug Mt into series
        mat_exp = get_matrix_exponential([[0, -1], [1, 0]])
        mat_exp.to_corner(UL)
        mat_exp[1].set_color(TEAL)

        equation = OldTex(
            "e^X", ":=", "X^0 + X^1 + \\frac{1}{2} X^2 + \\frac{1}{6} X^3 + \\cdots + \\frac{1}{n!} X^n + \\cdots",
            isolate=["X", "+"],
        )
        equation.set_width(FRAME_WIDTH - 1)
        equation.to_edge(UP)
        self.add(equation)

        rhs_tex = "{t}^0 X^0 + {t}^1 X^1 + \\frac{1}{2} {t}^2 X^2 + \\frac{1}{6} {t}^3 X^3 + \\cdots + \\frac{1}{n!} {t}^n X^n + \\cdots"
        mat_tex = "\\left[ \\begin{array}{cc} 0 & -1 \\\\ 1 & 0 \\end{array} \\right]"
        mat_rhs = OldTex(
            rhs_tex.replace("X", mat_tex),
            tex_to_color_map={mat_tex: TEAL},
            isolate=["{t}", "+"],
        )
        mat_rhs.scale(0.5)
        mat_equals = OldTex("=")

        mat_exp.match_height(mat_rhs)
        mat_equation = VGroup(mat_exp, mat_equals, mat_rhs)
        mat_equation.arrange(RIGHT)
        mat_exp.align_to(mat_rhs, DOWN)
        mat_equation.set_width(FRAME_WIDTH - 1)
        mat_equation.next_to(equation, DOWN, LARGE_BUFF)

        self.wait()
        self.play(LaggedStart(
            FadeTransform(equation[:2].copy(), mat_equation[0]),
            FadeTransform(equation[2].copy(), mat_equation[1]),
            *(
                FadeTransform(equation[i].copy(), mat_equation[2][j])
                for i, j in zip(
                    # Christ...
                    [3, 4, 3, 4, 5, 6, 7, 6, 7, 8, 9, 10, 11, 10, 11, 12, 13, 14, 15, 14, 15, 16, 17, 18, 19, 20, 21, 20, 21, 22, 23],
                    it.count()
                )
            ),
            run_time=2,
            lag_ratio=0.02
        ))
        self.wait()

        # Show first few powers
        new_eq = mat_equation.copy()
        new_eq.shift(1.5 * DOWN)

        kw = {"bracket_h_buff": 0.25}
        m0 = IntegerMatrix([[1, 0], [0, 1]], **kw)
        m1 = IntegerMatrix([[0, -1], [1, 0]], **kw)
        m2 = IntegerMatrix([[-1, 0], [0, -1]], **kw)
        m3 = IntegerMatrix([[0, 1], [-1, 0]], **kw)
        mat_powers = VGroup(m0, m1, m2, m3)
        mat_powers.set_submobject_colors_by_gradient(BLUE, GREEN, RED)

        indices = [2, 7, 13, 19]
        for mat_power, index in zip(mat_powers, indices):
            mat_power.replace(new_eq[2][index], dim_to_match=0)
            mat_power.source = mat_equation[2][index:index + 2]
            new_eq[2][index: index + 2].set_opacity(0)

        self.play(LaggedStart(
            TransformFromCopy(mat_equation[0], new_eq[0]),
            TransformFromCopy(mat_equation[1], new_eq[1]),
            *(
                TransformFromCopy(mat_equation[2][i], new_eq[2][i])
                for i in range(21)
                if i not in indices and i - 1 not in indices
            ),
            lag_ratio=0.01
        ))

        rect = SurroundingRectangle(mat_powers[0].source, buff=0.05)
        rect.set_stroke(width=0)
        for mat_power in mat_powers:
            self.play(rect.animate.become(SurroundingRectangle(mat_power.source, buff=0.05)), run_time=0.5)
            self.play(FadeTransform(mat_power.source.copy(), mat_power))
            self.wait(0.5)
        self.wait()
        self.play(rect.animate.move_to(mat_equation[2][27:29]))

        # Show cycling pattern
        rows = VGroup()
        for i in range(2):
            row = VGroup()
            for j in range(4):
                mat_power_copy = mat_powers[j].deepcopy()
                power = str(4 * (i + 1) + j)
                coef = OldTex("+\\frac{1}{" + power + "!} t^{" + power + "}")
                coef.match_height(mat_equation[2][10])
                coef.next_to(mat_power_copy, LEFT, SMALL_BUFF)
                row.add(coef, mat_power_copy)
            row.shift(1.1 * (i + 1) * DOWN)
            rows.add(row)
        dots = OldTex("+ \\cdots", font_size=24)
        dots.next_to(rows, DOWN, aligned_edge=LEFT)

        for row in rows:
            for coef, mp in zip(row[0::2], row[1::2]):
                new_rect = SurroundingRectangle(mp, buff=0.05)
                self.add(coef, mp, new_rect)
                self.wait(0.5)
                self.remove(new_rect)
        self.play(Write(dots))
        self.wait()

        # Setup for new rhs
        lhs = mat_equation[:2]
        self.play(
            lhs.animate.scale(2).to_corner(UL).shift(DOWN),
            FadeOut(VGroup(mat_equation[2], rect, equation))
        )

        # Show massive rhs
        rhs = Matrix(
            [
                [
                    "1 - \\frac{t^2}{2!} + \\frac{t^4}{4!} - \\frac{t^6}{6!} + \\cdots",
                    "-t + \\frac{t^3}{3!} - \\frac{t^5}{5!} + \\frac{t^7}{7!} - \\cdots",
                ],
                [
                    "t - \\frac{t^3}{3!} + \\frac{t^5}{5!} - \\frac{t^7}{7!} + \\cdots",
                    "1 - \\frac{t^2}{2!} + \\frac{t^4}{4!} - \\frac{t^6}{6!} + \\cdots",
                ],
            ],
            h_buff=6,
            v_buff=2,
        )
        rhs.set_width(10)
        rhs.next_to(lhs, RIGHT)

        power_entry_rects = VGroup(*(VGroup() for x in range(4)))
        for group in [mat_powers, rows[0][1::2], rows[1][1::2]]:
            for mat_power in group:
                for i, entry in enumerate(mat_power.get_entries()):
                    rect = SurroundingRectangle(entry, buff=0.05)
                    rect.set_stroke(YELLOW, 2)
                    power_entry_rects[i].add(rect)

        self.play(Write(rhs.get_brackets()))

        last_per = power_entry_rects[0].copy()
        last_per.set_opacity(0)
        last_rect = VMobject()
        for entry, per in zip(rhs.get_entries(), power_entry_rects):
            rect = VGroup(SurroundingRectangle(entry, stroke_width=1))
            self.play(
                ReplacementTransform(last_per, per),
                FadeIn(entry),
                FadeIn(rect),
                FadeOut(last_rect),
            )
            self.wait()
            last_per = per
            last_rect = rect
        self.play(FadeOut(last_per), FadeOut(last_rect))
        self.wait()

        # Show collapse to trig functions
        low_terms = VGroup(new_eq[2][:21], mat_powers, rows, dots)

        new_lhs = lhs.copy()
        new_lhs.next_to(rhs, DOWN, LARGE_BUFF)
        new_lhs.align_to(lhs, LEFT)
        final_result = Matrix(
            [["\\cos(t)", "-\\sin(t)"], ["\\sin(t)", "\\cos(t)"]],
            h_buff=2.0
        )
        final_result.next_to(new_lhs, RIGHT)

        anims = []
        colors = [BLUE_B, BLUE_D, BLUE_D, BLUE_B]
        for color, entry1, entry2 in zip(colors, rhs.get_entries(), final_result.get_entries()):
            anims.append(entry1.animate.set_color(color))
            entry2.set_color(color)

        self.play(
            *anims,
            FadeOut(low_terms, shift=2 * DOWN),
            ReplacementTransform(new_eq[:2], new_lhs),
            TransformFromCopy(rhs.get_brackets(), final_result.get_brackets()),
        )
        self.wait()
        last_rects = VGroup()
        for entry1, entry2 in zip(rhs.get_entries(), final_result.get_entries()):
            rect1 = SurroundingRectangle(entry1, stroke_width=1)
            rect2 = SurroundingRectangle(entry2, stroke_width=1)
            self.play(
                FadeIn(rect1),
                FadeIn(rect2),
                FadeIn(entry2),
                FadeOut(last_rects),
            )
            last_rects = VGroup(rect1, rect2)
        self.play(FadeOut(last_rects))
        self.wait()

        # Ask question
        question = OldTexText("What transformation\\\\is this?")
        question.next_to(final_result, RIGHT, buff=1.5)
        question.shift_onto_screen()
        arrow = Arrow(question, final_result, buff=SMALL_BUFF)

        self.play(
            FadeIn(question, shift=0.5 * RIGHT),
            GrowArrow(arrow)
        )
        self.wait()

        # Highlight result
        high_eq = VGroup(lhs, rhs)
        low_eq = VGroup(new_lhs, final_result)

        self.play(LaggedStart(
            FadeOut(high_eq, UP),
            FadeOut(VGroup(question, arrow)),
            low_eq.animate.center().to_edge(UP),
            lag_ratio=0.05
        ))
        self.wait()
