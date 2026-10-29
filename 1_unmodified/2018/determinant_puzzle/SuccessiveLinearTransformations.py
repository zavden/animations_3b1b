# ==============================================================================
# Scene:      SuccessiveLinearTransformations
# Source:     videos/_2018/determinant_puzzle.py (lines 159-283)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SuccessiveLinearTransformations.py SuccessiveLinearTransformations -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SuccessiveLinearTransformations(LinearTransformationScene):
    CONFIG = {
        "matrix_2": [[3, -1], [0, 1]],
        "matrix_1": [[2, 3], [-1. / 3, 2]],
    }

    def construct(self):
        self.create_product_and_inverse()
        self.scale_area_successively()
        self.apply_transformations_successively()
        self.scale_area_successively(
            "\\det(M_2)", "\\det(M_1)", "\\det(M_1 M_2)",
            reset=False
        )
        # self.show_det_as_scaling_factor()

    def create_product_and_inverse(self):
        self.matrix_product = np.dot(self.matrix_1, self.matrix_2)
        self.matrix_product_inverse = np.linalg.inv(self.matrix_product)

    def scale_area_successively(self, tex2="3", tex1="5", tex_prod="15", reset=True):
        self.add_unit_square()
        t1 = "$%s \\, \\cdot $" % tex1
        t2 = "$%s \\, \\cdot $" % tex2
        t3 = "Area"
        areas = VGroup(
            OldTexText("", "", t3),
            OldTexText("", t2, t3),
            OldTexText(t1, t2, t3),
        )
        areas.scale(0.8)
        areas.move_to(self.square)
        area = areas[0]
        self.add_moving_mobject(area, areas[1])

        self.play(
            FadeIn(self.square),
            Write(area),
            Animation(self.basis_vectors)
        )
        self.apply_matrix(self.matrix_2)
        self.wait()
        self.add_moving_mobject(area, areas[2])
        self.apply_matrix(self.matrix_1)
        self.wait()

        product = VGroup(area[:2])
        brace = Brace(product, DOWN, buff=SMALL_BUFF)
        brace_tex = brace.get_tex(tex_prod, buff=SMALL_BUFF)
        brace_tex.scale(0.8, about_edge=UP)

        self.play(
            GrowFromCenter(brace),
            Write(brace_tex)
        )
        self.wait()
        if reset:
            self.play(
                FadeOut(VGroup(self.square, area, brace, brace_tex)),
                Animation(self.plane),
                Animation(self.basis_vectors)
            )
            self.transformable_mobjects.remove(self.square)
            self.moving_mobjects = []
            self.reset_plane()
        self.wait()

    def apply_transformations_successively(self):
        M1, M2, all_space = expression = OldTex(
            "M_1", "M_2", "\\text{(All 2d space)}"
        )
        expression.set_color_by_tex_to_color_map({
            "M_1": TEAL,
            "M_2": PINK,
        })
        expression.shift(FRAME_WIDTH * LEFT / 4)
        expression.to_edge(UP)
        for part in expression:
            part.add_background_rectangle()
            part.background_rectangle.stretch(1.05, 0)
        M1.save_state()
        M1.move_to(ORIGIN)
        M1.fade(1)

        # Apply one after the other
        self.play(
            FocusOn(M2, run_time=1),
            FadeIn(VGroup(M2, all_space))
        )
        self.add_foreground_mobjects(M2, all_space)
        self.apply_matrix(self.matrix_2)
        self.wait()
        self.play(M1.restore)
        self.add_foreground_mobjects(M1)
        self.apply_matrix(self.matrix_1)
        self.wait()

        # Show full composition
        rp, lp = parens = OldTex("()")
        matrices = VGroup(M1, M2)
        matrices.generate_target()
        parens.match_height(matrices)
        lp.move_to(matrices, RIGHT)
        matrices.target.next_to(lp, LEFT, SMALL_BUFF)
        rp.next_to(matrices.target, LEFT, SMALL_BUFF)

        self.reset_plane()
        self.play(
            MoveToTarget(matrices),
            *list(map(GrowFromCenter, parens))
        )
        self.apply_matrix(self.matrix_product)
        self.wait()
        self.reset_plane()

    def show_det_as_scaling_factor(self):
        pass

    ###

    def reset_plane(self):
        plane_and_bases = VGroup(self.plane, self.basis_vectors)
        self.play(FadeOut(plane_and_bases))
        self.apply_matrix(self.matrix_product_inverse, run_time=0)
        self.play(FadeIn(plane_and_bases))
