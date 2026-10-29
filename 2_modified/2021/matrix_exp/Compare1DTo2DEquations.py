# ==============================================================================
# Scene:      Compare1DTo2DEquations
# Source:     videos/_2021/matrix_exp.py (lines 3238-3290)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Compare1DTo2DEquations.py Compare1DTo2DEquations -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Matrix/DecimalMatrix: `element_to_mobject_config` no longer exists: Matrix uses `element_config`; DecimalMatrix uses `num_decimal_places=` and `decimal_config=`.
#   - TransformMatchingShapes(..., fade_transform_mismatches=True): the argument no longer exists (fading out the unmatched pieces is all it does today); it is removed.
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


def get_1d_equation(r="r"):
    return OldTex(
        "{d \\over d{t}} x({t}) = {" + r + "} \\cdot x({t})",
        tex_to_color_map={
            "{t}": GREY_B,
            "{" + r + "}": BLUE,
            "=": WHITE,
        }
    )


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


class Compare1DTo2DEquations(Scene):
    def construct(self):
        eq1d = get_1d_equation()
        eq2d = get_2d_equation()
        eq1d.match_height(eq2d)

        equations = VGroup(eq1d, eq2d)
        equations.arrange(DOWN, buff=2.0)
        equations.to_edge(LEFT, buff=1.0)

        solutions = VGroup(
            OldTex("e^{rt}", tex_to_color_map={"r": BLUE}),
            get_matrix_exponential(
                [["a", "b"], ["c", "d"]],
                h_buff=0.75,
                v_buff=0.5,
                bracket_h_buff=0.25,
            )
        )
        solutions[1][1].set_color(TEAL)
        solutions[0].scale(2)
        arrows = VGroup()
        for eq, sol in zip(equations, solutions):
            sol.next_to(eq[-1], RIGHT, index_of_submobject_to_align=0)
            sol.set_x(4)
            arrows.add(Arrow(eq, sol[0], buff=0.5))

        sol0, sol1 = solutions
        sol0.save_state()
        sol0.center()
        self.add(sol0)
        self.wait()
        self.play(
            Restore(sol0),
            TransformFromCopy(Arrow(eq1d, sol0, fill_opacity=0), arrows[0]),
            FadeIn(eq1d),
        )
        self.wait(2)
        self.play(
            # CHANGE: TransformMatchingShapes no longer has fade_transform_mismatches (unmatched pieces always fade out); it is removed
            TransformMatchingShapes(sol0.copy(), sol1),
        )
        self.wait()
        self.play(
            TransformFromCopy(*arrows),
            LaggedStart(*(
                FadeTransform(m1.copy(), m2)
                for m1, m2 in zip(
                    [eq1d[:2], eq1d[2:5], eq1d[5], eq1d[6], eq1d[7:]],
                    eq2d
                )
            ), lag_ratio=0.05)
        )
        self.wait()
