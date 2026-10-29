# ==============================================================================
# Scene:      Matrices
# Source:     videos/_2021/shadows.py (lines 1797-1850)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Matrices.py Matrices -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Matrices(Scene):
    def construct(self):
        self.add(FullScreenRectangle())

        kw = {
            "v_buff": 0.7,
            "bracket_v_buff": 0.15,
            "bracket_h_buff": 0.15,
        }
        matrices = VGroup(
            Matrix([["v_1", "w_1"], ["v_2", "w_2"], ["v_3", "w_3"]], h_buff=1.0, **kw),
            Matrix([["1", "0", "0"], ["0", "1", "0"]], h_buff=0.6, **kw),
        )
        matrices.set_color(GREY_A)
        matrices[0].set_column_colors(GREEN, RED)
        matrices.arrange(LEFT, buff=SMALL_BUFF)
        matrices.scale(0.5)
        mat_product = matrices[:2].copy()

        vectors = VGroup(
            Matrix([["x_0"], ["y_0"]], **kw),
            Matrix([["x_1"], ["y_1"], ["z_1"]], **kw),
            Matrix([["x_2"], ["y_2"]], **kw),
        )

        for vect, x in zip(vectors, [-6, 0, 6]):
            vect.set_x(x)
            vect.set_y(2.5)

        arrows = VGroup(
            Arrow(vectors[0], vectors[1]),
            Arrow(vectors[1], vectors[2]),
            Arrow(vectors[0], vectors[2]),
        )

        for mat, arrow in zip((*matrices[:2], mat_product), arrows):
            mat.next_to(arrow, UP, SMALL_BUFF)

        # Animations
        self.add(vectors[0])
        for i in range(2):
            self.play(
                FadeTransform(vectors[i].copy(), vectors[i + 1]),
                ShowCreation(arrows[i]),
                FadeIn(matrices[i], 0.5 * RIGHT)
            )
            self.wait()

        self.play(
            Transform(arrows[0], arrows[2]),
            Transform(arrows[1], arrows[2]),
            Transform(matrices, mat_product),
            FadeOut(vectors[1], scale=0),
        )
