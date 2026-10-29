# ==============================================================================
# Scene:      SolutionsToMatrixEquation
# Source:     videos/_2021/matrix_exp.py (lines 3744-3745)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SolutionsToMatrixEquation.py SolutionsToMatrixEquation -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - VectorField/StreamLines are imported from legacy_arrow_vector_field (arrow API with func(x, y) and step_multiple, from before Sept 2024).
#   - Vector(..., thickness=X) -> thickness=X / Arrow.tickness_multiplier: same thickness scale change.
#   - Matrix/DecimalMatrix: `element_to_mobject_config` no longer exists: Matrix uses `element_config`; DecimalMatrix uses `num_decimal_places=` and `decimal_config=`.
# ==============================================================================

from manim_imports_ext import *
# CHANGE: VectorField/StreamLines with manimgl's arrow API from before Sept 2024 (see _lib/legacy_arrow_vector_field.py)
from legacy_arrow_vector_field import VectorField, StreamLines

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


class From2DTo1D(Scene):
    show_solution = False

    def construct(self):
        # (Setup vector equation)
        equation = get_2d_equation()
        equation.center()
        equation.to_edge(UP, buff=1.0)
        deriv, vect_sym, equals, matrix_mob, vect_sym2 = equation

        vect_sym.save_state()

        # (Setup plane)
        plane = NumberPlane(
            x_range=(-4, 4),
            y_range=(-2, 2),
            height=4,
            width=8,
        )
        plane.to_edge(DOWN)

        point = Point(plane.c2p(2, 0.5))
        vector = Arrow(plane.get_origin(), point.get_location(), buff=0)
        vector.set_color(YELLOW)

        # Show vector
        vect_sym.set_x(0)
        static_vect_sym = vect_sym.deepcopy()
        for entry in static_vect_sym.get_entries():
            entry[1:].set_opacity(0)
            entry[:1].move_to(entry)
        static_vect_sym.get_brackets().space_out_submobjects(0.7)
        vector.save_state()
        vector.put_start_and_end_on(
            static_vect_sym.get_corner(DL),
            static_vect_sym.get_corner(UR),
        )
        vector.set_opacity(0)

        self.add(plane, static_vect_sym)
        self.play(Restore(vector))
        self.wait()

        # Changing with time
        matrix = np.array([[0.5, -3], [1, -0.5]])

        def func(x, y):
            return 0.2 * np.dot([x, y], matrix.T)

        move_points_along_vector_field(point, func, plane)
        vector.add_updater(lambda m: m.put_start_and_end_on(
            plane.get_origin(), point.get_location(),
        ))
        # CHANGE: Vector(thickness=...): thickness in scene units; the current Arrow multiplies it by Arrow.tickness_multiplier
        deriv_vector = Vector(fill_color=RED, thickness=0.03 / Arrow.tickness_multiplier)
        deriv_vector.add_updater(
            lambda m: m.put_start_and_end_on(
                plane.get_origin(),
                plane.c2p(*func(*plane.p2c(point.get_location()))),
            ).shift(vector.get_vector())
        )

        self.add(point)
        self.play(ReplacementTransform(static_vect_sym, vect_sym))
        self.wait(3)

        # Show matrix equation
        deriv_underline = Underline(VGroup(deriv, vect_sym.saved_state))
        deriv_underline.set_stroke(RED, 3)
        alt_line = deriv_underline.deepcopy()

        self.play(
            Restore(vect_sym),
            FadeIn(deriv),
        )
        self.wait()
        self.play(
            ShowCreation(deriv_underline),
        )
        self.play(
            VFadeIn(deriv_vector, rate_func=squish_rate_func(smooth, 0.8, 1.0)),
            UpdateFromAlphaFunc(
                alt_line,
                lambda m, a: m.put_start_and_end_on(
                    interpolate(deriv_underline.get_start(), deriv_vector.get_start(), a),
                    interpolate(deriv_underline.get_end(), deriv_vector.get_end(), a),
                ),
                remover=True,
            ),
        )
        self.wait(4)

        self.play(
            LaggedStartMap(FadeIn, equation[2:4], shift=RIGHT, lag_ratio=0.3),
            TransformFromCopy(
                equation[1], equation[4], path_arc=-45 * DEGREES,
                run_time=2,
                rate_func=squish_rate_func(smooth, 0.3, 1.0)
            )
        )
        self.wait(8)

        # Highlight equation
        deriv_rect = SurroundingRectangle(equation[:2])
        deriv_rect.set_stroke(RED, 2)
        rhs_rect = SurroundingRectangle(equation[-1])
        rhs_rect.set_stroke(YELLOW, 2)

        self.play(ShowCreation(deriv_rect))
        self.wait()
        self.play(ReplacementTransform(deriv_rect, rhs_rect, path_arc=-45 * DEGREES))

        # Draw vector field
        vector_field = VectorField(
            func, plane,
            magnitude_range=(0, 1.2),
            opacity=0.5,
            vector_config={"thickness": 0.02}
        )
        vector_field.sort(lambda p: get_norm(p - plane.get_origin()))

        self.add(vector_field, deriv_vector, vector)
        VGroup(vector, deriv_vector).set_stroke(BLACK, 5, background=True)
        self.play(
            FadeOut(rhs_rect),
            LaggedStartMap(GrowArrow, vector_field, lag_ratio=0)
        )
        self.wait(14)

        # flow_lines = AnimatedStreamLines(StreamLines(func, plane, step_multiple=0.25))
        # self.add(flow_lines)
        # self.wait(4)
        # self.play(VFadeOut(flow_lines))

        # self.wait(10)

        # Show solution
        equation.add(deriv_underline)
        mat_exp = get_matrix_exponential(
            [["a", "b"], ["c", "d"]],
            h_buff=0.75,
            v_buff=0.75,
        )
        mat_exp[1].set_color(TEAL)
        if self.show_solution:
            equation.generate_target()
            equation.target.to_edge(LEFT)
            implies = OldTex("\\Rightarrow")
            implies.next_to(equation.target, RIGHT)
            solution = VGroup(
                equation[1].copy(),
                OldTex("="),
                mat_exp,
                Matrix(
                    [["x(0)"], ["y(0)"]],
                    bracket_h_buff=SMALL_BUFF,
                    bracket_v_buff=SMALL_BUFF,
                )
            )
            solution[2].match_height(solution[0])
            solution[3].match_height(solution[0])
            solution.arrange(RIGHT, buff=MED_SMALL_BUFF)
            solution.next_to(implies, RIGHT, MED_LARGE_BUFF)
            solution.align_to(equation[1], DOWN)
            solution_rect = SurroundingRectangle(solution, buff=MED_SMALL_BUFF)

            self.play(
                MoveToTarget(equation),
            )
            self.play(LaggedStart(
                Write(implies),
                ShowCreation(solution_rect),
                TransformFromCopy(equation[4], solution[0], path_arc=30 * DEGREES),
            ))
            self.wait()
            self.play(LaggedStart(
                TransformFromCopy(equation[3], solution[2][1]),
                FadeIn(solution[2][0]),
                FadeIn(solution[2][2]),
                FadeIn(solution[1]),
                FadeIn(solution[3]),
                lag_ratio=0.1,
            ))
            self.wait(10)
            return
        else:
            # Show relation with matrix exp
            mat_exp.move_to(equation[0], DOWN)
            mat_exp.to_edge(RIGHT, buff=LARGE_BUFF)
            equation.generate_target()
            equation.target.to_edge(LEFT, buff=LARGE_BUFF)
            arrow1 = Arrow(equation.target.get_corner(UR), mat_exp.get_corner(UL), path_arc=-45 * DEGREES)
            arrow2 = Arrow(mat_exp.get_corner(DL), equation.target.get_corner(DR), path_arc=-45 * DEGREES)
            arrow1.shift(0.2 * RIGHT)

            self.play(MoveToTarget(equation))
            self.play(
                FadeIn(mat_exp[0::2]),
                TransformFromCopy(equation[3], mat_exp[1]),
                Write(arrow1, run_time=1),
            )
            self.wait(4)
            self.play(Write(arrow2, run_time=2))
            self.wait(4)

            normal_exp = OldTex("e^{rt}")[0]
            normal_exp.set_height(1.0)
            normal_exp[1].set_color(BLUE)
            normal_exp.move_to(mat_exp)
            self.play(
                FadeTransformPieces(mat_exp, normal_exp),
                FadeOut(VGroup(arrow1, arrow2))
            )
            self.wait(2)

        # Transition to 1D
        max_x = 50
        mult = 50
        number_line = NumberLine((0, max_x), width=max_x)
        number_line.add_numbers()
        number_line.move_to(plane)
        number_line.to_edge(LEFT)
        nl = number_line
        nl2 = NumberLine((0, mult * max_x, mult), width=max_x)
        nl2.add_numbers()
        nl2.set_width(nl.get_width() * mult)
        nl2.shift(nl.n2p(0) - nl2.n2p(0))
        nl2.set_opacity(0)
        nl.add(nl2)

        new_equation = OldTex(
            "{d \\over dt}", "x(t)", "=", "r \\cdot ", "x(t)",
        )
        new_equation[0][3].set_color(GREY_B)
        new_equation[1][2].set_color(GREY_B)
        new_equation[4][2].set_color(GREY_B)
        new_equation[3][0].set_color(BLUE)
        new_equation.match_height(equation)
        new_equation.move_to(equation)

        self.remove(point)
        vector.clear_updaters()
        deriv_vector.clear_updaters()

        self.remove(vector_field)
        plane.add(vector_field)
        self.add(number_line, deriv_vector, vector)
        self.play(
            normal_exp.animate.scale(0.5).to_corner(UR),
            # Plane to number line
            vector.animate.put_start_and_end_on(nl.n2p(0), nl.n2p(1)),
            deriv_vector.animate.put_start_and_end_on(nl.n2p(1), nl.n2p(1.5)),
            plane.animate.shift(nl.n2p(0) - plane.get_origin()).set_opacity(0),
            FadeIn(number_line, rate_func=squish_rate_func(smooth, 0.5, 1)),
            # Equation
            TransformMatchingShapes(equation[0], new_equation[0]),
            Transform(equation[1].get_entries()[0], new_equation[1]),
            FadeTransform(equation[2], new_equation[2]),
            FadeTransform(equation[3], new_equation[3]),
            FadeTransform(equation[4].get_entries()[0], new_equation[4]),
            FadeOut(equation[1].get_brackets()),
            FadeOut(equation[1].get_entries()[1]),
            FadeOut(equation[4].get_brackets()),
            FadeOut(equation[4].get_entries()[1]),
            FadeOut(deriv_underline),
            run_time=2,
        )

        vt = ValueTracker(1)
        vt.add_updater(lambda m, dt: m.increment_value(0.2 * dt * m.get_value()))

        vector.add_updater(lambda m: m.put_start_and_end_on(nl.n2p(0), nl.n2p(vt.get_value())))
        deriv_vector.add_updater(lambda m: m.set_width(0.5 * vector.get_width()).move_to(vector.get_right(), LEFT))

        self.add(vt)
        self.wait(11)
        self.play(
            number_line.animate.scale(0.3, about_point=nl.n2p(0)),
        )
        self.wait(4)
        number_line.generate_target()
        number_line.target.scale(0.1, about_point=nl.n2p(0)),
        number_line.target[-1].set_opacity(1)
        self.play(
            MoveToTarget(number_line)
        )
        self.wait(11)
        self.play(number_line.animate.scale(0.2, about_point=nl.n2p(0)))
        self.wait(10)


class SolutionsToMatrixEquation(From2DTo1D):
    show_solution = True
