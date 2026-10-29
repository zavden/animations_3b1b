# ==============================================================================
# Scene:      OutlineThreeFacts
# Source:     videos/_2021/quick_eigen.py (lines 694-1013)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OutlineThreeFacts.py OutlineThreeFacts -w -m --fps 15
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


class OutlineThreeFacts(Scene):
    def construct(self):
        # Matrix to lambdas
        mat = Matrix([["a", "b"], ["c", "d"]], v_buff=0.8, h_buff=0.8)
        mat.set_column_colors(COL_COLORS[0], COL_COLORS[1])

        lambdas = OldTex("\\lambda_1", "\\,,\\,", "\\lambda_2")
        lambdas[0].set_color(EIGEN_COLORS[0])
        lambdas[2].set_color(EIGEN_COLORS[1])
        arrow = Vector(1.5 * RIGHT)
        group = VGroup(mat, arrow, lambdas)
        group.arrange(RIGHT)
        arrow_label = Text("Quick?", font_size=24)
        arrow_label.next_to(arrow, UP, buff=0)

        self.add(mat)
        self.play(
            GrowArrow(arrow),
            Write(arrow_label, run_time=1),
            LaggedStart(*(
                AnimationGroup(*(
                    Transform(entry, lambdas[i])
                    for entry in mat.get_entries().deepcopy()
                ))
                for i in [0, 2]
            ), lag_ratio=0.3),
            FadeIn(lambdas[1]),
        )
        self.clear()
        self.add(group, arrow_label)
        self.wait()

        # Three steps
        indices = VGroup(*(Text(str(i) + ")", font_size=48) for i in range(1, 4)))
        indices.set_color(GREY_B)
        indices.arrange(DOWN, aligned_edge=LEFT, buff=2)
        indices.to_edge(LEFT)

        group.generate_target()
        group.target[1].rotate(-90 * DEGREES)
        group.target[1].scale(0.5)
        group.target.arrange(DOWN)
        group.target.to_corner(DR)

        self.play(
            LaggedStartMap(FadeIn, indices, shift=0.25 * UP, lag_ratio=0.3),
            FadeOut(arrow_label),
            MoveToTarget(group),
        )
        self.wait()

        # Trace
        tr_mat = mat.deepcopy()
        tr = OldTex("\\text{tr}", "\\Big(", "\\Big)", font_size=60)
        tr[1:].match_height(tr_mat, stretch=True)
        tr.set_submobjects([*tr[:-1], tr_mat, tr[-1]])
        tr.arrange(RIGHT, buff=SMALL_BUFF)
        tr.next_to(indices[0], RIGHT, MED_LARGE_BUFF)

        tr_rects = VGroup(
            SurroundingRectangle(tr_mat.get_entries()[0]),
            SurroundingRectangle(tr_mat.get_entries()[3]),
        )
        tr_rects.set_color(BLUE_C)
        moving_tr_rects = tr_rects.copy()
        moving_tr_rects.generate_target()

        tex_kw = {
            "tex_to_color_map": {
                "a": COL_COLORS[0],
                "b": COL_COLORS[1],
                "c": COL_COLORS[0],
                "d": COL_COLORS[1],
                "=": WHITE,
                "\\lambda_1": EIGEN_COLORS[0],
                "\\lambda_2": EIGEN_COLORS[1],
            }
        }
        tr_rhs = OldTex("= a + d = \\lambda_1 + \\lambda_2", **tex_kw)
        tr_rhs.next_to(tr, RIGHT)

        for term, rect in zip(tr_rhs[1:4:2], moving_tr_rects.target):
            rect.move_to(term)

        self.play(
            TransformFromCopy(mat, tr_mat),
            Write(VGroup(*tr[:2], tr[-1])),
        )
        self.play(LaggedStart(*map(ShowCreation, tr_rects)))
        tr.add(tr_rects)
        self.play(
            MoveToTarget(moving_tr_rects),
            TransformFromCopy(tr_mat.get_entries()[0], tr_rhs.get_part_by_tex("a")),
            TransformFromCopy(tr_mat.get_entries()[3], tr_rhs.get_part_by_tex("d")),
            FadeIn(tr_rhs[0:4:2]),
        )
        self.play(FadeOut(moving_tr_rects))
        self.wait()
        self.play(
            TransformMatchingShapes(lambdas.copy(), tr_rhs[4:]),
        )
        self.wait()

        # Mean of eigenvalues
        half = OldTex("1 \\over 2")
        half.move_to(tr, LEFT)
        tr.generate_target()
        tr.target.next_to(half, RIGHT, SMALL_BUFF)
        new_tr_rhs = OldTex("= {a + d \\over 2} = {\\lambda_1 + \\lambda_2 \\over 2}", **tex_kw)
        new_tr_rhs.next_to(tr.target, RIGHT)

        self.play(
            GrowFromCenter(half),
            MoveToTarget(tr),
            TransformMatchingShapes(tr_rhs, new_tr_rhs),
        )
        self.wait()

        # Determinant
        det_mat = mat.deepcopy()
        det = OldTex("\\text{det}", "\\Big(", "\\Big)", font_size=60)
        det[1:].match_height(det_mat, stretch=True)
        det.set_submobjects([*det[:-1], det_mat, det[-1]])
        det.arrange(RIGHT, buff=SMALL_BUFF)
        det.next_to(indices[1], RIGHT, MED_LARGE_BUFF)

        det_rhs = OldTex("= ad - bc = \\lambda_1 \\lambda_2", **tex_kw)
        det_rhs.next_to(det, RIGHT)
        self.play(
            TransformFromCopy(mat, det_mat),
            Write(VGroup(*det[:2], det[-1])),
        )

        self.play(
            det_path_anim(det_mat),
            LaggedStart(
                Animation(Mobject(), remover=True),
                FadeIn(det_rhs[:3]),
                FadeIn(det_rhs[3:6]),
                lag_ratio=0.7,
            )
        )
        self.wait()
        self.play(
            TransformMatchingShapes(lambdas.copy(), det_rhs[6:])
        )
        self.wait()

        # Mean and product
        eq_m = OldTexText("=", " $m$", "\\quad (mean)")
        eq_m[1].set_color(MEAN_COLOR)
        eq_m.next_to(new_tr_rhs, RIGHT)
        eq_p = OldTexText("=", " $p$", "\\quad (product)")
        eq_p[1].set_color(PROD_COLOR)
        eq_p.next_to(det_rhs, RIGHT)

        form_lhs = lambdas.copy()
        form_rhs = OldTex("= {m} \\pm \\sqrt{\\,{m}^2 - {p}}", tex_to_color_map={"{m}": MEAN_COLOR, "{p}": PROD_COLOR})
        form_lhs.next_to(indices[2], RIGHT)
        form_rhs.next_to(form_lhs, RIGHT)

        third_point_placeholder = Text("(We'll get to this...)", font_size=30)
        third_point_placeholder.set_fill(GREY_C)
        third_point_placeholder.next_to(indices[2], RIGHT, MED_LARGE_BUFF)

        form = VGroup(indices[2], form_lhs, form_rhs)
        rect = SurroundingRectangle(VGroup(form), buff=MED_SMALL_BUFF)

        randy = Randolph(height=2)
        randy.next_to(rect, RIGHT)
        randy.to_edge(DOWN)

        self.play(
            FadeIn(third_point_placeholder),
            VFadeIn(randy),
            randy.change("erm", third_point_placeholder)
        )
        self.play(Blink(randy))
        self.wait()
        self.play(
            randy.change("thinking", eq_m),
            Write(eq_m)
        )
        self.play(
            randy.animate.look_at(eq_p),
            Write(eq_p),
            mat.animate.set_height(1, about_edge=DOWN)
        )
        self.play(Blink(randy))
        self.wait()

        # Example matrix
        ex_mat = IntegerMatrix([[8, 4], [2, 6]])
        ex_mat.set_height(1.25)
        ex_mat.set_column_colors(COL_COLORS[0], COL_COLORS[1])
        ex_mat.next_to(randy, RIGHT, aligned_edge=UP)

        kw = {"tex_to_color_map": {"m": MEAN_COLOR, "p": PROD_COLOR, "=": WHITE, "-": WHITE}}
        m_eq = OldTex("m = 7", **kw)
        p_eq1 = OldTex("p = 48 - 8", **kw)
        p_eq2 = OldTex("p = 40", **kw)

        for mob in (m_eq, p_eq1, p_eq2):
            mob.next_to(ex_mat, RIGHT, buff=MED_LARGE_BUFF)
        m_eq.shift(0.5 * UP)
        VGroup(p_eq1, p_eq2).shift(0.5 * DOWN)

        diag_rects = VGroup(
            SurroundingRectangle(ex_mat.get_entries()[0]),
            SurroundingRectangle(ex_mat.get_entries()[3]),
        )
        off_diag_rects = VGroup(
            SurroundingRectangle(ex_mat.get_entries()[1]),
            SurroundingRectangle(ex_mat.get_entries()[2]),
        )
        diag_rects.set_color(PROD_COLOR)
        off_diag_rects.set_color(PROD_COLOR)
        mean_rect = SurroundingRectangle(m_eq[2])
        mean_rect.set_color(MEAN_COLOR)

        tr_rect = SurroundingRectangle(VGroup(indices[0], tr, eq_m)).set_stroke(MEAN_COLOR)
        det_rect = SurroundingRectangle(VGroup(indices[1], det, eq_p)).set_stroke(PROD_COLOR)

        self.play(
            randy.change("raise_right_hand", ex_mat),
            FadeIn(ex_mat, RIGHT),
            FadeOut(group, RIGHT),
        )
        self.play(Blink(randy))
        self.wait()

        self.play(FadeIn(tr_rect), randy.change("pondering", tr_rhs))
        self.play(
            Write(m_eq[:2]),
            LaggedStartMap(ShowCreation, diag_rects, lag_ratio=0.5, run_time=1),
            randy.animate.look_at(m_eq),
        )
        self.wait()
        self.remove(diag_rects)
        self.play(
            TransformFromCopy(diag_rects, mean_rect),
            FadeTransform(ex_mat.get_entries()[0].copy(), m_eq[2]),
            FadeTransform(ex_mat.get_entries()[3].copy(), m_eq[2]),
        )
        self.play(Blink(randy))
        self.wait()

        self.play(FadeOut(tr_rect), FadeIn(det_rect), randy.animate.look_at(tr_rhs))
        self.play(
            Write(p_eq1[:2]),
            randy.change("hesitant", p_eq1),
            FadeOut(mean_rect),
        )

        self.play(det_path_anim(ex_mat))
        self.wait()
        self.play(
            FadeIn(diag_rects),
            FadeIn(p_eq1[2]),
        )
        self.play(
            FadeOut(diag_rects),
            FadeIn(off_diag_rects),
            FadeIn(p_eq1[3:]),
        )
        self.play(
            FadeOut(off_diag_rects),
        )
        self.play(
            randy.change("tease", p_eq2),
            FadeOut(p_eq1),
            FadeIn(p_eq2),
        )
        self.play(FadeOut(det_rect))
        self.wait()

        # Let other stuff happen up top
        full_rect = FullScreenFadeRectangle()
        full_rect.set_fill(BLACK, 1)

        ex = VGroup(ex_mat, m_eq, p_eq2)

        self.add(full_rect, randy, ex)
        self.play(
            FadeIn(full_rect),
            randy.change("pondering", ORIGIN)
        )
        for x in range(10):
            if random.random() < 0.5:
                self.play(Blink(randy))
            else:
                self.wait()

        # Show final formula
        ex_rect = SurroundingRectangle(ex, buff=0.35)
        ex_rect.set_stroke(GREY_A)
        ex_rect.set_fill(interpolate_color(GREY_E, BLACK, 0.25))
        ex_rect.set_opacity(0)
        ex_group = VGroup(ex_rect, ex)
        ex_group.generate_target()
        ex_group.target.set_height(1.5)
        ex_group.target.to_corner(DR)
        ex_group.target[0].set_opacity(1)

        self.play(
            FadeOut(full_rect),
            FadeOut(randy),
            MoveToTarget(ex_group)
        )

        self.play(
            FadeIn(form_lhs, 0.25 * UP),
            FadeOut(third_point_placeholder, 0.25 * UP)
        )
        self.play(TransformMatchingShapes(
            VGroup(m_eq[0], p_eq2[0]).copy(),
            form_rhs,
        ))
        self.play(ShowCreation(rect))
        self.wait()
