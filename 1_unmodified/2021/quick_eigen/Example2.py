# ==============================================================================
# Scene:      Example2
# Source:     videos/_2021/quick_eigen.py (lines 1713-1717)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Example2.py Example2 -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

COL_COLORS = [MAROON_B, MAROON_C]


MEAN_COLOR = BLUE_B


PROD_COLOR = BLUE_D


def get_diag_rects(matrix, color=MEAN_COLOR, off_diagonal=False):
    if off_diagonal:
        entries = matrix.get_entries()[1:3]
    else:
        entries = matrix.get_entries()[0::3]
    return VGroup(*(
        SurroundingRectangle(entry, buff=SMALL_BUFF, color=color)
        for entry in entries
    ))


class GeneralExample(Scene):
    matrix = [[3, 1], [4, 1]]

    def construct(self):
        mat = IntegerMatrix(self.matrix)
        mat.move_to(2 * LEFT)
        mat.set_column_colors(*COL_COLORS)

        matrix = np.array(self.matrix)
        a, b, c, d = matrix.flatten()

        mean = (a + d) / 2
        if (a + d) % 2 == 0:
            mean = int(mean)
        prod = a * d - b * c
        mean_str = "{" + str(mean) + "}"
        prod_str = "{" + str(prod) + "}"

        self.add(mat)
        self.wait()

        mean_eq = OldTex(f"m = {mean_str}", tex_to_color_map={"m": MEAN_COLOR, mean_str: MEAN_COLOR})
        mean_eq.next_to(mat, UP, LARGE_BUFF)
        diag_rects = get_diag_rects(mat)

        self.play(
            FadeIn(mean_eq[:2], 0.25 * UP)
        )
        self.play(LaggedStartMap(ShowCreation, diag_rects, lag_ratio=0.3, run_time=1))
        self.play(
            FadeTransform(diag_rects[0].copy(), mean_eq[2]),
            FadeTransform(diag_rects[1].copy(), mean_eq[2]),
        )
        self.play(FadeOut(diag_rects))

        last_part = "(" + prod_str + ")}" if prod < 0 else prod_str + "}"
        formula = OldTex(
            mean_str, "\\pm \\sqrt{\\,", mean_str, "^2 - ", last_part,
            font_size=60,
            tex_to_color_map={mean_str: MEAN_COLOR, prod_str: PROD_COLOR},
        )
        formula.next_to(mat, RIGHT, buff=1.5)

        self.play(
            Write(formula[1]),
            Write(formula[3]),
            FadeTransform(mean_eq[2].copy(), formula[0]),
            FadeTransform(mean_eq[2].copy(), formula[2]),
        )
        self.wait()

        # Product
        prod_eq = OldTex(
            f"p = {a * d} - {b * c} = {prod}",
            tex_to_color_map={
                str(prod): PROD_COLOR,
                str(a * d): COL_COLORS[0],
                str(b * c): COL_COLORS[0],
                "=": WHITE,
            }
        )
        prod_eq.move_to(mean_eq)

        self.play(
            FadeIn(prod_eq[:2]),
            mean_eq.animate.shift(UP),
        )
        self.play(
            FadeIn(prod_eq[2]),
            VFadeInThenOut(get_diag_rects(mat, color=YELLOW), run_time=1.5),
        )
        self.play(
            FadeIn(prod_eq[3:5]),
            VFadeInThenOut(get_diag_rects(mat, color=YELLOW, off_diagonal=True), run_time=1.5),
        )
        self.wait()
        self.play(Write(prod_eq[5:]))
        self.play(FadeTransform(prod_eq[-1].copy(), formula[4:]))
        self.wait()

        # Simplify
        line2 = OldTex(mean_str, "\\pm", "\\sqrt{\\,", str(mean**2 - prod), "}", font_size=60)
        if mean == 0:
            line2[0].scale(0, about_point=line2[1].get_left())
        line2[0].set_color(MEAN_COLOR)
        line2.next_to(formula, DOWN, buff=0.7, aligned_edge=LEFT)

        self.play(FadeTransform(formula.copy()[:4], line2))
        self.wait()

        line3 = self.get_final_simplification()
        if line3:
            line3.next_to(line2, DOWN, buff=0.7, aligned_edge=LEFT)
            self.play(FadeIn(line3, DOWN))
            self.wait()
            answer = line3[-1]
        else:
            answer = line2
        self.play(ShowCreation(SurroundingRectangle(answer)))
        self.wait()

    def get_final_simplification(self):
        return None


class Example2(GeneralExample):
    matrix = [[2, 7], [1, 8]]

    def get_final_simplification(self):
        return OldTex("5 \\pm 4", "=", "9,\\,1", font_size=60)
