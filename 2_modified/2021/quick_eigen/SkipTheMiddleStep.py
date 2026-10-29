# ==============================================================================
# Scene:      SkipTheMiddleStep
# Source:     videos/_2021/quick_eigen.py (lines 2676-2773)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SkipTheMiddleStep.py SkipTheMiddleStep -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - rate_function is called rate_func
# ==============================================================================

from manim_imports_ext import *

COL_COLORS = [MAROON_B, MAROON_C]


EIGEN_COLORS = [TEAL_A, TEAL_D]


MEAN_COLOR = BLUE_B


PROD_COLOR = BLUE_D


def det_path_anim(matrix, run_time=2):
    path = VMobject()
    path.set_points_smoothly([
        matrix.get_corner(UL),
        *[
            matrix.get_entries()[i].get_center()
            for i in [0, 3, 1, 2]
        ],
        matrix.get_corner(DL),
    ])
    path.set_stroke(BLUE, 3)

    # CHANGE: rate_function is called rate_func
    return VShowPassingFlash(path, time_width=1, run_time=run_time, rate_func=linear)


def get_diag_rects(matrix, color=MEAN_COLOR, off_diagonal=False):
    if off_diagonal:
        entries = matrix.get_entries()[1:3]
    else:
        entries = matrix.get_entries()[0::3]
    return VGroup(*(
        SurroundingRectangle(entry, buff=SMALL_BUFF, color=color)
        for entry in entries
    ))


class SkipTheMiddleStep(Scene):
    def construct(self):
        matrix = IntegerMatrix([[3, 1], [4, 1]])
        matrix.set_column_colors(*COL_COLORS)
        char_poly = OldTex(
            "\\lambda^2 - 4\\lambda - 1",
            tex_to_color_map={"\\lambda": EIGEN_COLORS[0]}
        )
        mp_formula = OldTex(
            "{2} \\pm \\sqrt{\\,{2}^2 - (-1)}",
            tex_to_color_map={
                "{2}": MEAN_COLOR,
                "(-1)": PROD_COLOR,
            }
        )

        group = VGroup(matrix, char_poly, mp_formula)
        group.arrange(RIGHT, buff=2)

        mat_label, char_poly_label, eigen_label = labels = VGroup(
            OldTexText("Matrix"),
            OldTexText("Characteristic\\\\polynomial"),
            OldTexText("Eigenvalues"),
        )
        for label, mob, color in zip(labels, group, [COL_COLORS[0], EIGEN_COLORS[0], MEAN_COLOR]):
            label.set_color(color)
            label.next_to(mob, DOWN, MED_LARGE_BUFF)
            label.align_to(labels[0], UP)

        arc = -90 * DEGREES
        arrows = VGroup(
            Arrow(matrix.get_corner(UR), char_poly.get_top(), path_arc=arc),
            Arrow(char_poly.get_top(), mp_formula.get_top(), path_arc=arc),
            Arrow(matrix.get_corner(UR), mp_formula.get_top(), path_arc=0.8 * arc),
        )
        arrows.shift(0.5 * UP)

        self.add(matrix, mat_label)
        self.play(
            DrawBorderThenFill(arrows[0]),
            GrowFromPoint(char_poly, matrix.get_top(), path_arc=arc),
            FadeTransform(mat_label.copy(), char_poly_label),
        )
        self.wait()
        self.play(
            DrawBorderThenFill(arrows[1]),
            TransformFromCopy(char_poly, mp_formula),
            FadeTransform(char_poly_label.copy(), eigen_label),
        )
        self.wait()
        self.play(
            VFadeInThenOut(get_diag_rects(matrix), run_time=2),
            LaggedStart(*(
                ShowCreationThenFadeOut(SurroundingRectangle(sm, buff=0.1, color=WHITE), run_time=2)
                for sm in mp_formula.get_parts_by_tex("{2}")
            ))
        )
        self.play(
            det_path_anim(matrix),
            ShowCreationThenFadeOut(SurroundingRectangle(
                mp_formula.get_parts_by_tex("(-1)"), buff=0.1, color=WHITE,
            ), run_time=2)
        )
        self.wait()
        self.play(
            Transform(arrows[0], arrows[2]),
            Transform(arrows[1], arrows[2]),
            VGroup(char_poly, char_poly_label).animate.set_opacity(0.15),
        )
        self.wait()

        #
        frame = self.camera.frame
        quad_form = OldTex(
            "{-b \\pm \\sqrt{\\,b^2 - 4ac} \\over 2a}",
            tex_to_color_map={
                "a": BLUE_B,
                "b": BLUE_C,
                "c": BLUE_D,
            }
        )
        words = OldTexText("Never could\\\\have worked!")
        group = VGroup(quad_form, words)
        group.arrange(RIGHT, buff=LARGE_BUFF)
        group.next_to(arrows, UP, LARGE_BUFF)
        cross = Cross(quad_form)
        cross.set_stroke(width=(1, 3, 3, 1))

        self.play(
            frame.animate.set_y(1),
            FadeIn(quad_form, DOWN),
        )
        self.wait()
        self.play(
            Write(words),
            ShowCreation(cross)
        )
        self.wait()
