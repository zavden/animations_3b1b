# ==============================================================================
# Scene:      Example1
# Source:     videos/_2021/quick_eigen.py (lines 1423-1592)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Example1.py Example1 -w -m --fps 15
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


class Example1(TeacherStudentsScene):
    def construct(self):
        # Show matrix
        mat = IntegerMatrix([[3, 1], [4, 1]])
        mat.set_column_colors(*COL_COLORS)
        mat.move_to(self.hold_up_spot, DOWN)

        self.play(
            self.teacher.change("raise_right_hand", mat),
            FadeIn(mat.get_brackets(), UP)
        )
        self.play(
            Write(mat.get_entries(), lag_ratio=0.1, run_time=2),
            self.change_students("pondering", "pondering", "thinking", look_at=mat)
        )
        self.wait()

        bubble = ThoughtBubble(height=4, width=7)
        bubble.pin_to(self.students[2])
        self.play(
            self.students[2].change("tease", bubble),
            Write(bubble)
        )
        self.wait(3)

        # Write formula
        shift_vect = 5 * LEFT
        arrow = Vector(0.75 * RIGHT)
        arrow.next_to(mat, RIGHT)
        formula = OldTex(
            "\\lambda_1, \\, \\lambda_2 = {2} \\pm \\sqrt{\\,{2}^2 - (-1)}",
            tex_to_color_map={
                "\\lambda_1": EIGEN_COLORS[0],
                "\\lambda_2": EIGEN_COLORS[1],
                "(-1)": PROD_COLOR,
                "{2}": MEAN_COLOR,
            }
        )
        formula.next_to(arrow, RIGHT)
        VGroup(formula, arrow).shift(shift_vect)

        twos = formula.get_parts_by_tex("{2}")
        min1 = formula.get_part_by_tex("(-1)")
        m_rects = VGroup(*(SurroundingRectangle(two, buff=0) for two in twos))
        m_rects.set_stroke(MEAN_COLOR)
        p_rect = SurroundingRectangle(min1, buff=0)
        p_rect.set_stroke(PROD_COLOR)
        form_rects = VGroup(m_rects, p_rect)
        VGroup(twos, min1).set_opacity(0)

        self.play(
            FadeOut(bubble),
            mat.animate.shift(shift_vect),
            FadeIn(arrow, shift_vect),
            FadeIn(formula),
            FadeIn(form_rects),
            self.change_students("pondering", "pondering", "pondering", look_at=ORIGIN)
        )
        self.play(
            self.teacher.change("tease", formula),
            *(pi.animate.look_at(formula) for pi in self.students),
        )
        self.wait()

        # Show mean
        m_eq = OldTex("m", "=", "2", tex_to_color_map={"m": MEAN_COLOR, "2": MEAN_COLOR})
        m_eq.next_to(mat, UP, LARGE_BUFF)
        t2c = {
            "\\lambda_1": EIGEN_COLORS[0],
            "\\lambda_2": EIGEN_COLORS[1],
            "{m}": MEAN_COLOR,
            "{p}": PROD_COLOR,
            "=": WHITE,
        }
        diag_rects = VGroup(*(SurroundingRectangle(mat.get_entries()[i]) for i in [0, 3]))
        diag_rects.set_stroke(MEAN_COLOR)
        two_rect = SurroundingRectangle(m_eq[2])
        two_rect.set_stroke(MEAN_COLOR)

        self.play(
            Write(m_eq[:2]),
            *(pi.animate.look_at(m_eq) for pi in self.pi_creatures)
        )
        self.play(
            ShowCreation(diag_rects),
            self.teacher.change("tease", diag_rects),
            *(pi.animate.look_at(diag_rects) for pi in self.students),
        )
        self.wait()
        self.play(
            FadeTransform(diag_rects[0].copy(), m_eq[2], remover=True),
            FadeTransform(diag_rects[1].copy(), m_eq[2], remover=True),
            *(pi.animate.look_at(two_rect) for pi in self.pi_creatures),
        )
        self.wait(2)

        self.remove(twos, min1)
        VGroup(twos, min1).set_opacity(1)
        for i in (0, 1):
            self.play(
                TransformFromCopy(m_eq[2], twos[i]),
                FadeOut(m_rects[i]),
                self.teacher.change("raise_right_hand", twos),
                *(pi.change("thinking", twos) for pi in self.students)
            )
        self.wait()

        # Show product
        prod_eq = OldTex(
            # "\\lambda_1 \\lambda_2 =",
            "{p} = {3} - {4} = -1",
            tex_to_color_map={
                "{3}": COL_COLORS[0],
                "{4}": COL_COLORS[0],
                **t2c
            }
        )
        prod_eq.next_to(mat, UP, LARGE_BUFF)
        prod_eq.set_x(mat.get_center()[0], LEFT)

        lhs = prod_eq[:1]

        self.play(
            m_eq.animate.scale(0.7).next_to(mat, LEFT).to_edge(LEFT),
            FadeIn(lhs),
            FadeOut(diag_rects),
            self.teacher.change("happy"),
            self.change_students("erm", "hesitant", "thinking", look_at=prod_eq)
        )
        self.play(det_path_anim(mat, run_time=1))
        self.play(
            FadeIn(prod_eq[1]),
            FadeTransform(mat.get_entries()[0].copy(), prod_eq[2]),
            FadeTransform(mat.get_entries()[3].copy(), prod_eq[2]),
            VFadeInThenOut(VGroup(*(SurroundingRectangle(e) for e in mat.get_entries()[0::3]))),
            self.teacher.change("coin_flip_1"),
        )
        self.play(
            FadeIn(prod_eq[3]),
            FadeTransform(mat.get_entries()[1].copy(), prod_eq[4]),
            FadeTransform(mat.get_entries()[2].copy(), prod_eq[4]),
            VFadeInThenOut(VGroup(*(SurroundingRectangle(e) for e in mat.get_entries()[1:3]))),
        )
        self.wait()
        self.play(
            Write(prod_eq[-2:]),
            self.change_students("tease", "tease", "happy", look_at=prod_eq.get_right()),
        )
        self.play(
            FadeOut(p_rect),
            FadeTransform(prod_eq[-1].copy(), min1),
            self.teacher.change("raise_left_hand", min1),
            *(pi.animate.look_at(min1) for pi in self.students)
        )
        self.wait()
        self.play(
            prod_eq.animate.scale(0.7).next_to(m_eq, UP).to_edge(LEFT)
        )
        self.wait(2)

        # Final answer
        rhs = OldTex("2\\pm\\sqrt{5}")
        rhs.move_to(formula[4], LEFT)

        self.play(
            self.teacher.change("tease", rhs),
            TransformMatchingShapes(formula[4:6].copy(), rhs),
            formula[4:].animate.shift(UP),
        )
        self.wait()
