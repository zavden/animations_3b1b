# ==============================================================================
# Scene:      PauliMatricesWithCharacteristicPolynomial
# Source:     videos/_2021/quick_eigen.py (lines 2071-2296)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PauliMatricesWithCharacteristicPolynomial.py PauliMatricesWithCharacteristicPolynomial -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - rate_function is called rate_func
#   - Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
#   - Matrix no longer has element_to_mobject_config; it is now element_config
#   - Matrix's h_buff is now the gap between elements (before, the distance between centers, 1.5): with 1.5 the matrix came out too wide and 'p = -1' was stuck to the edge
#   - Matrix's h_buff is no longer the distance between centers (2.0) but the gap between elements; with 2.0 the matrix went off the screen on the left
# ==============================================================================

from manim_imports_ext import *

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


class PauliMatrices(Scene):
    def construct(self):
        self.camera.frame.focal_distance = 20

        # Matrices
        colors = [RED, GREEN, BLUE]
        lhss, matrices = self.get_lhss_and_matrices(colors)

        self.add(lhss)
        self.play(LaggedStartMap(FadeIn, matrices, shift=0.25 * RIGHT, lag_ratio=0.3, run_time=2))
        self.wait()

        # Title
        title = Text("Pauli spin matrices")
        title.next_to(group, RIGHT, buff=1.25)
        self.play(Write(title, run_time=2))
        self.wait()

        # Axes
        axes = ThreeDAxes(
            (-2, 2), (-2, 2), (-2, 2),
            axis_config={"include_tip": False}
        )
        axes.set_flat_stroke(False)
        axes.rotate(20 * DEGREES, OUT)
        axes.rotate(70 * DEGREES, LEFT)
        axes.set_height(1.7)
        axes.labels = VGroup(*(
            OldTex(ch, font_size=24).next_to(axis.get_end(), vect, buff=SMALL_BUFF)
            for ch, axis, vect in zip("xyz", axes.get_axes(), [RIGHT, UP, UP])
        ))
        axes.add(axes.labels)
        axes.set_stroke(background=True)

        axes_copies = VGroup()
        for i, matrix, color, (v1, v2) in zip(it.count(), matrices, colors, [(UP, DOWN), (LEFT, RIGHT), (RIGHT, RIGHT)]):
            ac = axes.deepcopy()
            ac.labels.set_fill(GREY_C, 1)
            ac.labels[i].set_fill(color, 1)
            axis = ac.get_axes()[i]
            vp1, vm1 = (
                # CHANGE: Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
                FillArrow(axis.n2p(0), axis.n2p(n), buff=0.05, fill_color=color, thickness=0.05)
                for n in (2, -2)
            )
            for vector, tex, v in [(vp1, "+1", v1), (vm1, "-1", v2)]:
                vector.add(OldTex(tex, font_size=24).next_to(vector, v, buff=0.05))
            ac.add(vp1, vm1)
            ac.next_to(matrix, RIGHT, buff=LARGE_BUFF)
            axes_copies.add(ac)

        acx, acy, acz = axes_copies

        self.play(
            FadeOut(title),
            Write(acx, stroke_width=0.5),
        )
        self.wait()
        self.play(TransformFromCopy(acx, acy))
        self.wait()
        self.play(TransformFromCopy(acy, acz))
        self.wait()
        self.play(LaggedStartMap(FadeOut, axes_copies, shift=0.25 * DOWN, run_time=1, lag_ratio=0.3))

        # Compute means
        means_rects = VGroup(*(
            get_diag_rects(matrix)
            for matrix in matrices
        ))
        mean_eqs = VGroup(*(
            OldTex("m = 0", tex_to_color_map={"m": MEAN_COLOR, "0": WHITE}).next_to(matrix, RIGHT, buff=MED_LARGE_BUFF)
            for matrix in matrices
        ))

        kw = {
            "tex_to_color_map": {
                "0": MEAN_COLOR,
                "{p}": PROD_COLOR,
            }
        }
        forms = VGroup(*(
            OldTex("0 \\pm \\sqrt{\\,0^2 - {p}}", **kw).next_to(matrix, RIGHT).to_edge(RIGHT)
            for matrix in matrices
        ))
        simple_forms = VGroup(*(
            OldTex("\\pm \\sqrt{-{p}}", **kw).move_to(form, LEFT)
            for form in forms
        ))

        for me, mr, form in zip(mean_eqs, means_rects, forms):
            self.play(
                FadeIn(mr),
                Write(me[:2], run_time=1),
            )
            self.play(
                TransformFromCopy(mr, me[2], run_time=0.7)
            )
        self.wait()
        self.play(
            LaggedStart(*(
                FadeIn(VGroup(form[1], form[3], form[4]))
                for form in forms
            ), lag_ratio=0.2),
            LaggedStart(*(
                TransformFromCopy(me.get_parts_by_tex("0"), form.get_parts_by_tex("0"))
                for me, form in zip(mean_eqs, forms)
            ), lag_ratio=0.2),
        )
        self.wait()
        self.play(LaggedStart(*(
            TransformMatchingShapes(form, simple_form)
            for form, simple_form in zip(forms, simple_forms)
        )))
        self.wait()

        # Products
        prod_eqs = VGroup(*(
            OldTex("p = -1", tex_to_color_map={"p": PROD_COLOR, "-1": WHITE}).next_to(
                matrix, RIGHT, buff=MED_LARGE_BUFF
            ).shift(0.5 * DOWN)
            for matrix in matrices
        ))

        self.play(
            mean_eqs.animate.shift(0.5 * UP),
            LaggedStart(*(FadeIn(pe[:2]) for pe in prod_eqs)),
            FadeOut(means_rects)
        )
        self.play(LaggedStart(*(det_path_anim(matrix) for matrix in matrices), lag_ratio=0.2))

        for matrix, pe in zip(matrices, prod_eqs):
            r1 = get_diag_rects(matrix)
            r2 = get_diag_rects(matrix, off_diagonal=True)
            VGroup(r1, r2).set_color(YELLOW)
            self.play(FadeIn(r1))
            self.play(FadeOut(r1), FadeIn(r2), FadeIn(pe[2]))
            self.play(FadeOut(r2))
            self.wait()

        final_forms = VGroup(*(
            OldTex("= \\pm 1").move_to(sf.get_center(), LEFT)
            for sf in simple_forms
        ))

        self.play(
            LaggedStart(*(
                FadeTransform(pe[2].copy(), ff)
                for pe, ff in zip(prod_eqs, final_forms)
            ), lag_ratio=0.3),
            LaggedStart(*(
                sf.animate.next_to(ff, LEFT)
                for sf, ff in zip(simple_forms, final_forms)
            ))
        )
        self.wait()

        # Bring back axes
        axes_copies.shift(2 * RIGHT)
        self.play(
            FadeOut(simple_forms), FadeOut(final_forms),
            FadeIn(acx),
        )
        self.play(FadeIn(acy))
        self.play(FadeIn(acz))
        self.wait()

    def get_lhss_and_matrices(self, colors):
        lhss = VGroup(*(OldTex(f"\\sigma_{c} = ") for c in "xyz"))
        kw = {"h_buff": 0.7, "v_buff": 0.7}
        matrices = VGroup(
            Matrix([["0", "1"], ["1", "0"]], **kw),
            Matrix([["0", "-i"], ["i", "0"]], **kw),
            Matrix([["1", "0"], ["0", "-1"]], **kw),
        )
        lhss.set_submobject_colors_by_gradient(*colors)
        lhss.arrange(DOWN, buff=2.5)
        for lhs, matrix in zip(lhss, matrices):
            matrix.set_height(1.5)
            matrix.next_to(lhs, RIGHT)

        group = VGroup(lhss, matrices)
        group.move_to(2 * LEFT)
        return group


class PauliMatricesWithCharacteristicPolynomial(PauliMatrices):
    def construct(self):
        # Set up determinants
        colors = [RED, GREEN, BLUE]
        lhss, matrices = group = self.get_lhss_and_matrices(colors)
        group.to_edge(LEFT)

        kw = {
            # CHANGE: Matrix no longer has element_to_mobject_config; it is now element_config
            "element_config": {
                "tex_to_color_map": {
                    "-\\lambda": EIGEN_COLORS[1],
                }
            },
            "v_buff": 0.7,
            "h_buff": 1.3,
        }
        new_matrices = VGroup(
            Matrix([["-\\lambda", "1"], ["1", "-\\lambda"]], **kw),
            Matrix([["-\\lambda", "-i"], ["i", "-\\lambda"]], **kw),
            Matrix([["1 -\\lambda", "0"], ["0", "-1 -\\lambda"]], **kw),
        )
        arrows = VGroup()
        det_terms = VGroup()
        for mat, new_mat in zip(matrices, new_matrices):
            mat.set_height(1.0, about_edge=LEFT)
            new_mat.replace(mat, dim_to_match=1)
            new_mat.shift(3.75 * RIGHT)

            parens = OldTex("()", font_size=60)[0]
            parens.match_height(new_mat, stretch=True)
            parens[0].next_to(new_mat, LEFT, buff=0.1)
            parens[1].next_to(new_mat, RIGHT, buff=0.1)
            det = Text("det", font_size=30)
            det.next_to(parens, LEFT, SMALL_BUFF)

            det_terms.add(VGroup(det, parens, new_mat))
            arrows.add(Arrow(mat, det, buff=0.2))

        self.add(lhss, matrices)
        self.wait()
        self.play(
            LaggedStart(*(
                TransformMatchingShapes(mat.copy(), det_term)
                for mat, det_term in zip(matrices, det_terms)
            ), lag_ratio=0.8),
            LaggedStartMap(GrowArrow, arrows, lag_ratio=0.8),
        )
        self.wait()

        # Polynomials
        kw = {"tex_to_color_map": {
            "\\lambda": EIGEN_COLORS[1],
            "=": WHITE,
        }}
        rhss = VGroup(
            OldTex("= \\lambda^2 - 1 = 0", **kw),
            OldTex("= \\lambda^2 - 1 = 0", **kw),
            OldTex("= (1 - \\lambda)(-1 - \\lambda) = 0", **kw),
        )

        lpm1s = VGroup()
        for rhs, det_term in zip(rhss, det_terms):
            rhs.next_to(det_term, RIGHT, SMALL_BUFF, submobject_to_align=rhs[0])
            self.play(LaggedStart(
                det_path_anim(det_term[-1]),
                TransformMatchingShapes(det_term[-1].get_entries().copy(), rhs),
                lag_ratio=0.5
            ))
            if rhs is rhss[-1]:
                continue

            self.play(FlashUnder(rhs))
            self.wait()
            lpm1 = OldTex("\\lambda = \\pm 1", **kw)
            lpm1.next_to(rhs, DOWN, buff=0.75)
            lpm1s.add(lpm1)
            self.play(TransformMatchingShapes(rhs[1:4].copy(), lpm1))
            self.wait()

        # Comment on last
        rect = SurroundingRectangle(matrices[2])
        words = Text("Already diagonal!", font_size=24)
        words.next_to(rect, UP)
        words.set_color(YELLOW)
        diag_rects = get_diag_rects(matrices[2], color=EIGEN_COLORS[1])

        self.play(FadeInFromLarge(rect))
        self.play(Write(words, run_time=1))
        self.wait()
        self.play(ShowCreation(diag_rects))
        self.wait()

        self.play(LaggedStartMap(FadeOut, VGroup(
            *arrows, *det_terms, *rhss, *lpm1s,
            rect, words, diag_rects,
        )))

        # Show combinations
        colors = [YELLOW_B, YELLOW_C, YELLOW_D]

        def get_combo(triplet):
            group = VGroup(
                OldTex("a"), triplet[0].copy(), OldTex("+"),
                OldTex("b"), triplet[1].copy(), OldTex("+"),
                OldTex("c"), triplet[2].copy()
            )
            group.arrange(RIGHT, buff=0.15)
            group[3].align_to(group[0], DOWN)
            group[6].align_to(group[0], DOWN)
            group.set_color(WHITE)
            group[0::3].set_submobject_colors_by_gradient(*colors)
            return group

        true_lhss = VGroup(*(lhs[0][:2] for lhs in lhss))
        row1 = get_combo(true_lhss)
        row1[1::3].shift(0.06 * DOWN)
        row2 = get_combo(matrices)
        rows = VGroup(row1, row2)
        rows.arrange(DOWN, buff=LARGE_BUFF)
        rows.to_corner(UR, buff=LARGE_BUFF)

        kw = {"tex_to_color_map": {
            "a": colors[0],
            "b": colors[1],
            "c": colors[2],
            "\\lambda": EIGEN_COLORS[1],
        }}
        normalized_eq = OldTex("\\left(a^2 + b^2 + c^2 = 1\\right)", **kw)
        normalized_eq.next_to(row2, DOWN, LARGE_BUFF)
        normalized_eq.to_edge(DOWN)

        full_mat = Matrix(
            [
                ["c", "a - bi"],
                ["a + bi", "-c"],
            ],
            # CHANGE: Matrix no longer has element_to_mobject_config; it is now element_config
            # CHANGE: Matrix's h_buff is now the gap between elements (before, the distance between centers, 1.5): with 1.5 the matrix came out too wide and 'p = -1' was stuck to the edge
            element_config=kw,
            h_buff=0.5
        )
        full_mat.next_to(row2, DOWN, LARGE_BUFF)

        self.play(TransformMatchingShapes(true_lhss.copy(), row1))
        self.wait()
        self.play(FadeTransformPieces(row1.copy(), row2))
        self.wait()
        self.play(TransformMatchingShapes(row2.copy(), full_mat))
        self.wait()  # Let some physics happen
        self.play(TransformMatchingShapes(row2[0::3].copy(), normalized_eq))
        self.wait()

        # Talk about eigen computations
        self.play(FadeOut(lhss), FadeOut(matrices))

        randy = Randolph()
        randy.set_height(2)
        randy.next_to(full_mat, LEFT).to_edge(DOWN)
        randy.set_opacity(0)
        diag_rects = get_diag_rects(full_mat)
        bubble = ThoughtBubble(height=2, width=2)
        bubble.pin_to(randy)
        m_eq = OldTex("m = 0", tex_to_color_map={"m": MEAN_COLOR})
        p_eq = OldTex("p = ??", tex_to_color_map={"p": PROD_COLOR})
        bubble.position_mobject_inside(m_eq)
        bubble.position_mobject_inside(p_eq)

        p_eq2 = OldTex("p = -1", tex_to_color_map={"p": PROD_COLOR})
        p_eq2.next_to(full_mat, RIGHT, aligned_edge=DOWN)

        self.play(
            VFadeIn(randy),
            randy.animate.set_opacity(1).change("hesitant", full_mat)
        )
        self.play(ShowCreation(diag_rects))
        self.play(
            Write(bubble),
            Write(m_eq),
            randy.change("pondering", bubble)
        )
        self.play(randy.change("thinking", bubble))
        self.play(Blink(randy))
        self.wait()
        self.play(
            FadeIn(p_eq, 0.25 * UP),
            m_eq.animate.next_to(full_mat, RIGHT, aligned_edge=UP),
            randy.change("hesitant", full_mat),
            FadeOut(diag_rects),
        )
        self.play(det_path_anim(full_mat))
        self.play(Blink(randy))
        self.wait()
        self.play(
            FadeOut(bubble),
            randy.change("tease", p_eq2),
            Transform(p_eq, p_eq2),
        )
        self.play(Blink(randy))
        self.wait()

        # Characteristic polynomial
        mod_mat = Matrix(
            [
                ["c - \\lambda", "a - bi"],
                ["a + bi", "-c - \\lambda"],
            ],
            # CHANGE: Matrix's h_buff is no longer the distance between centers (2.0) but the gap between elements; with 2.0 the matrix went off the screen on the left
            element_config=kw,
            h_buff=0.5
        )
        parens = OldTex("(", ")")
        parens.stretch(2, 1)
        parens.match_height(mod_mat)
        parens[0].next_to(mod_mat, LEFT, SMALL_BUFF)
        parens[1].next_to(mod_mat, RIGHT, SMALL_BUFF)
        det = Text("det")
        det.next_to(parens, LEFT, SMALL_BUFF)
        char_poly = VGroup(det, parens, mod_mat)
        char_poly.next_to(randy, UL)

        self.play(
            TransformMatchingShapes(full_mat.copy(), char_poly, run_time=2),
            randy.change("raise_left_hand", char_poly),
        )
        self.play(randy.change("horrified", char_poly))
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change("tired"))
        self.wait()
