# ==============================================================================
# Scene:      PauliMatrices
# Source:     videos/_2021/quick_eigen.py (lines 1732-1913)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PauliMatrices.py PauliMatrices -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - rate_function is called rate_func
#   - 'group' was not defined (an error in the original); it is taken from the value that get_lhss_and_matrices returns
#   - Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
# ==============================================================================

from manim_imports_ext import *

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
        # CHANGE: 'group' was not defined (an error in the original); it is taken from the value that get_lhss_and_matrices returns
        lhss, matrices = group = self.get_lhss_and_matrices(colors)

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
