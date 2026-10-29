# ==============================================================================
# Scene:      ExoticExponentsWithEBase
# Source:     videos/_2021/matrix_exp.py (lines 3596-3719)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExoticExponentsWithEBase.py ExoticExponentsWithEBase -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Matrix/DecimalMatrix: `element_to_mobject_config` no longer exists: Matrix uses `element_config`; DecimalMatrix uses `num_decimal_places=` and `decimal_config=`.
# ==============================================================================

from manim_imports_ext import *

def get_matrix_exponential(matrix, height=1.5, scalar_tex="t", **matrix_config):
    elem = matrix[0][0]
    if isinstance(elem, str):
        mat_class = Matrix
    elif isinstance(elem, int) or isinstance(elem, np.int64):
        mat_class = IntegerMatrix
    else:
        mat_class = DecimalMatrix

    matrix = mat_class(matrix, **matrix_config)
    base = OldTex("e")
    base.set_height(0.4 * height)
    matrix.set_height(0.6 * height)
    matrix.move_to(base.get_corner(UR), DL)
    result = VGroup(base, matrix)
    if scalar_tex:
        scalar = OldTex(scalar_tex)
        scalar.set_height(0.7 * base.get_height())
        scalar.next_to(matrix, RIGHT, buff=SMALL_BUFF, aligned_edge=DOWN)
        result.add(scalar)
    return result


def get_2d_equation(matrix=[["a", "b"], ["c", "d"]]):
    deriv = OldTex("d \\over dt", tex_to_color_map={"t": GREY_B})
    vect = Matrix(
        [["x(t)"], ["y(t)"]],
        bracket_h_buff=SMALL_BUFF,
        bracket_v_buff=SMALL_BUFF,
        # CHANGE: element_to_mobject_config no longer exists in Matrix/DecimalMatrix (see element_config / decimal_config)
        element_config={
            "tex_to_color_map": {"t": GREY_B},
            "isolate": ["(", ")"]
        }
    )
    deriv.match_height(vect)
    equals = OldTex("=")
    matrix_mob = Matrix(matrix, h_buff=0.8)
    matrix_mob.set_color(TEAL)
    matrix_mob.match_height(vect)
    equation = VGroup(deriv, vect, equals, matrix_mob, vect.deepcopy())
    equation.arrange(RIGHT)
    return equation


class ExoticExponentsWithEBase(Scene):
    def construct(self):
        # Write exotic exponents
        exps = VGroup(
            OldTex("e", "^{it}"),
            get_matrix_exponential([[3, 1], [4, 1]]),
            OldTex("e", "^{((i + j + k) / \\sqrt{3})t}"),
            OldTex("e", "^{\\left(\\frac{\\partial}{\\partial x}\\right)t}"),
        )
        for i in (0, 2, 3):
            exps[i][0].scale(1.25)
            exps[i][0].move_to(exps[i][1:].get_corner(DL), UR)
        exps[1].scale(exps[0][0].get_height() / exps[1][0].get_height())
        exps.arrange(DOWN, buff=LARGE_BUFF, aligned_edge=LEFT)

        labels = VGroup(
            Text("Complex numbers", font_size=30),
            Text("Matrices", font_size=30),
            Text("Quaternions", font_size=30),
            Text("Operators", font_size=30),
        )
        labels.set_submobject_colors_by_gradient(BLUE_B, BLUE_C)
        for label, exp in zip(labels, exps):
            label.move_to(exp, DL)
            label.align_to(labels[0], LEFT)
        labels.set_x(-2)

        exps.set_x(labels.get_right()[0] + 3)

        arrow = Arrow(labels.get_corner(UL), labels.get_corner(DL), buff=0)
        arrow.shift(0.5 * LEFT)
        arrow.set_color(TEAL)
        exotic_label = OldTexText("More\\\\exotic\\\\exponents", alignment="")
        exotic_label.next_to(arrow, LEFT)
        VGroup(arrow, exotic_label).set_opacity(0)

        e_mobs = VGroup()
        for label, exp in zip(labels, exps):
            e_mobs.add(exp[0])
            self.play(
                FadeIn(label),
                FadeIn(exp[0]),
                GrowFromPoint(exp[1:], exp[0].get_center()),
                exotic_label.animate.set_opacity(1),
                arrow.animate.set_opacity(1),
            )
        self.wait()
        self.play(LaggedStart(*(
            FlashAround(e, buff=0.05, time_width=3, run_time=2)
            for e in e_mobs
        ), lag_ratio=0.1))
        self.wait()

        # Analytic number theory exception
        zeta = OldTex("\\sum_{n = 1}^\\infty \\frac{1}{n^s}")
        zeta.move_to(exps[0], LEFT)

        self.play(
            FadeOut(exps[0]),
            FadeIn(zeta),
        )
        self.wait()
        self.play(
            FadeOut(zeta),
            FadeIn(exps[0]),
        )
        self.wait()

        # Other bases
        n_mob_groups = VGroup()
        for n in ["2", "5", "\\pi", "1{,}729"]:
            n_mobs = VGroup()
            for e_mob in e_mobs:
                n_mob = OldTex(n)
                n_mob.match_height(e_mob)
                n_mob.scale(1.2)
                n_mob.move_to(e_mob, UR)
                n_mob.shift(0.025 * DL)
                n_mobs.add(n_mob)
            n_mob_groups.add(n_mobs)
        for color, group in zip([YELLOW, GREEN_B, RED, MAROON_B], n_mob_groups):
            group.set_color(color)
        last_group = e_mobs
        for group in [*n_mob_groups, e_mobs]:
            self.play(
                LaggedStartMap(FadeOut, last_group, lag_ratio=0.2),
                LaggedStartMap(FadeIn, group, lag_ratio=0.2),
                run_time=1.5,
            )
            self.wait()
            last_group = group

        # Show which equations are solved.
        equations = VGroup(
            OldTex("\\frac{dz}{dt}(t) = i \\cdot z(t)"),
            get_2d_equation([["3", "1"], ["4", "1"]]),
            OldTex("\\frac{dq}{dt}(t) = \\frac{i + j + k}{ \\sqrt{3} } \\cdot q(t)"),
            OldTex("{\\partial \\over \\partial t}f(x, t) = {\\partial \\over \\partial x}f(x, t)"),
        )
        for eq, exp in zip(equations, exps):
            eq.match_height(exp)
            eq.move_to(exp, DL)
            eq.align_to(equations[0], LEFT)

        equations.to_edge(RIGHT)

        self.play(
            FadeOut(arrow, 3 * LEFT),
            FadeOut(exotic_label, 3 * LEFT),
            VGroup(labels, exps).animate.to_edge(LEFT),
            LaggedStartMap(FadeIn, equations, run_time=3, lag_ratio=0.5)
        )
        self.wait()
        self.play(
            VGroup(
                labels[0], labels[2:],
                exps[0], exps[2:],
                equations[0], equations[2:]
            ).animate.set_opacity(0.3),
            equations[1].animate.scale(1.5, about_edge=RIGHT),
            exps[1].animate.scale(1.5),
            labels[1].animate.scale(1.5, about_edge=LEFT),
        )
        self.wait()
