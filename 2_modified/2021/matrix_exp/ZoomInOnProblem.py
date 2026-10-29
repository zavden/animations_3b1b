# ==============================================================================
# Scene:      ZoomInOnProblem
# Source:     videos/_2021/matrix_exp.py (lines 137-226)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ZoomInOnProblem.py ZoomInOnProblem -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - OldTex/OldTexText with {{ }}: manimgl removed that convention (Apr 2021) and no longer splits the text into parts; the double braces are removed and isolate=[...] is passed with the same pieces.
#
# Placeholder assets (not Grant's originals):
#   - Placeholder mat_exp_exercise.png (16:9 book page) in _lib/assets/raster_images/ (make_matrix_exp_assets.py)
# ==============================================================================

from manim_imports_ext import *

class ZoomInOnProblem(Scene):
    def construct(self):
        # Highlight problem
        image = ImageMobject("mat_exp_exercise.png")
        image.set_height(FRAME_HEIGHT)

        prob_rect = Rectangle(3.25, 0.35)
        prob_rect.move_to([-2.5, -2.5, 0])
        prob_rect.set_stroke(BLUE, 2)

        examples_rect = Rectangle(2.0, 0.8)
        examples_rect.move_to([01.8, 2.8, 0.0])
        examples_rect.set_stroke(YELLOW, 3)
        answer_rect = Rectangle(3.0, 2.0)
        answer_rect.move_to(examples_rect, UR)
        answer_rect.shift(0.1 * RIGHT)

        full_rect = FullScreenRectangle()
        full_rect.flip()
        full_rect.set_fill(BLACK, opacity=0.6)
        full_rect.append_vectorized_mobject(prob_rect)
        full_rect2 = full_rect.copy()
        full_rect3 = full_rect.copy()
        full_rect.append_vectorized_mobject(examples_rect.copy().scale(1e-6))
        full_rect2.append_vectorized_mobject(examples_rect)
        full_rect3.append_vectorized_mobject(answer_rect)

        self.add(image)

        # Write problem
        # CHANGE: OldTex no longer splits on {{ }} (convention removed from manimgl in Apr 2021); they are removed and isolate=[...] is used with the same pieces
        problem = OldTexText(
            "Compute the matrix $e^{At}$\\\\if the matrix A has the form...",
            isolate=["matrix A", "matrix", "$e^{At}$"],
        )
        problem.to_corner(UL)
        problem.set_stroke(BLACK, 5, background=True)
        prob_arrow = Arrow(prob_rect, problem)
        prob_arrow.set_fill(BLUE)
        mat_underline = Underline(problem.get_part_by_tex("matrix"))
        mat_underline.set_color(YELLOW)

        self.play(
            ShowCreation(prob_rect),
            FadeIn(full_rect),
            FadeTransform(prob_rect.copy(), problem),
            GrowArrow(prob_arrow),
        )
        self.wait()
        for part in ["e^{At}", "matrix A"]:
            self.play(FlashAround(problem.get_part_by_tex(part), run_time=2, time_width=4))
            self.wait()
        self.play(ShowCreation(mat_underline))
        self.wait()
        mat_underline.rotate(PI)
        self.play(Uncreate(mat_underline))
        self.wait()

        # Show inputs
        examples_label = OldTexText("Various matrices to\\\\plug in for $A$", font_size=40)
        examples_label.next_to(examples_rect)

        lhs = OldTex("A = ", font_size=96)
        lhs.set_stroke(BLACK, 5, background=True)

        matrices = VGroup(
            IntegerMatrix([[1, 0], [0, 2]]),
            IntegerMatrix([[0, 1], [0, 0]]),
            IntegerMatrix([[0, 1], [-1, 0]]),
            IntegerMatrix([[0, 1, 0], [0, 0, 1], [0, 0, 0]]),
        )
        eq = VGroup(lhs, matrices[-1])
        eq.arrange(RIGHT)
        eq.next_to(examples_rect, DOWN, LARGE_BUFF, aligned_edge=LEFT)
        eq.shift_onto_screen()
        for matrix in matrices:
            matrix.move_to(matrices[-1], LEFT)
            matrix.set_stroke(BLACK, 5, background=True)

        self.play(
            Transform(full_rect, full_rect2)
        )
        self.play(
            ShowCreation(examples_rect),
            FadeIn(examples_label),
            FadeIn(lhs),
            FadeIn(matrices[0]),
        )
        self.wait()
        for m1, m2 in zip(matrices, matrices[1:]):
            self.play(FadeTransform(m1, m2))
            self.wait()
