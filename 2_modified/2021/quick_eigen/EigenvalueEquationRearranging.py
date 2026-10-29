# ==============================================================================
# Scene:      EigenvalueEquationRearranging
# Source:     videos/_2021/quick_eigen.py (lines 395-479)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl EigenvalueEquationRearranging.py EigenvalueEquationRearranging -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
# ==============================================================================

from manim_imports_ext import *

EIGEN_COLORS = [TEAL_A, TEAL_D]


class EigenvalueEquationRearranging(Scene):
    def construct(self):
        v_tex = "\\vec{\\textbf{v}}"
        zero_tex = "\\vec{\\textbf{0}}"
        kw = {
            "tex_to_color_map": {
                "A": BLUE,
                "\\lambda": EIGEN_COLORS[1],
                v_tex: YELLOW,
                "=": WHITE,
            }
        }
        lines = VGroup(
            OldTex("A", v_tex, "=", "\\lambda ", v_tex, **kw),
            OldTex("A", v_tex, "=", "\\lambda ", " I ", v_tex, **kw),
            OldTex("A", v_tex, "-", "\\lambda ", " I ", v_tex, "=", zero_tex, **kw),
            OldTex("(A", "-", "\\lambda ", "I)", v_tex, "=", zero_tex, **kw),
            OldTex("\\text{det}", "(A", "-", "\\lambda ", "I)", "=", "0", **kw),
        )
        for line in lines:
            line.shift(-line.get_part_by_tex("=").get_center())

        mat_prod_brace = Brace(lines[0][:2])
        mat_prod_label = Text("Matrix product", color=BLUE, font_size=24)
        mat_prod_label.next_to(mat_prod_brace, DOWN, SMALL_BUFF, aligned_edge=RIGHT)
        scalar_prod_brace = Brace(lines[0][3:5])
        scalar_prod_label = Text("Scalar product", color=EIGEN_COLORS[1], font_size=24)
        scalar_prod_label.next_to(scalar_prod_brace, DOWN, SMALL_BUFF, aligned_edge=LEFT)

        self.add(lines[0])
        self.play(
            LaggedStart(
                GrowFromCenter(mat_prod_brace),
                GrowFromCenter(scalar_prod_brace),
                lag_ratio=0.3
            ),
            LaggedStart(
                FadeIn(mat_prod_label, 0.25 * DOWN),
                FadeIn(scalar_prod_label, 0.25 * DOWN),
                lag_ratio=0.3
            )
        )
        self.wait()

        id_brace = Brace(lines[1].get_part_by_tex("I"))
        id_label = Text("Identity matrix", font_size=24)
        id_label.next_to(id_brace, DOWN, SMALL_BUFF, aligned_edge=LEFT)

        self.play(
            TransformMatchingTex(lines[0], lines[1]),
            ReplacementTransform(scalar_prod_brace, id_brace),
            FadeTransform(scalar_prod_label, id_label),
            VGroup(mat_prod_label, mat_prod_brace).animate.shift(lines[1].get_left() - lines[0].get_left()),
        )
        self.wait()

        for shift_value, line in zip(it.count(1), lines[2:5]):
            line.shift(shift_value * 0.75 * DOWN)

        self.play(
            TransformMatchingTex(lines[1].copy(), lines[2], path_arc=-45 * DEGREES),
            FadeOut(VGroup(mat_prod_label, mat_prod_brace, id_brace, id_label), 0.5 * DOWN)
        )
        self.wait()
        self.play(
            TransformMatchingShapes(lines[2].copy(), lines[3]),
        )
        self.wait()

        v_part = lines[3].get_part_by_tex(v_tex)
        nz_label = Text("Non-zero vector", color=YELLOW, font_size=24)
        nz_label.next_to(v_part, DR, MED_LARGE_BUFF)
        # CHANGE: Arrow(thickness=...) with the old scale (0.05 = thin) ends up invisible; _lib's FillArrow converts the thickness
        arrow = FillArrow(nz_label.get_corner(UL), v_part, fill_color=YELLOW, buff=0.1, thickness=0.025)

        self.play(
            Write(nz_label, run_time=2),
            GrowArrow(arrow)
        )
        self.wait()
        self.play(
            TransformMatchingShapes(lines[3].copy(), lines[4]),
            FadeOut(nz_label),
            FadeOut(arrow),
        )
        self.wait()
