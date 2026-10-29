# ==============================================================================
# Scene:      NonZeroDeterminantCase
# Source:     videos/_2018/cramer.py (lines 750-797)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl NonZeroDeterminantCase.py NonZeroDeterminantCase -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Cairo digest_config gave the LAST base (SetupSimpleSystemOfEquations) priority over the first (ShowZeroDeterminantCase) when merging CONFIG; here that is the non-singular matrix, while the Python MRO now picks the singular one
# ==============================================================================

from manim_imports_ext import *

X_COLOR = GREEN


Y_COLOR = RED


Z_COLOR = BLUE


OUTPUT_COLOR = YELLOW


INPUT_COLOR = MAROON_B


class LinearSystem(VGroup):
    CONFIG = {
        "matrix_config": {
            "element_to_mobject": Integer,
        },
        "dimensions": 3,
        "min_int": -9,
        "max_int": 10,
        "height": 4,
    }

    def __init__(self, matrix=None, output_vect=None, **kwargs):
        VGroup.__init__(self, **kwargs)
        if matrix is None:
            dim = self.dimensions
            matrix = np.random.randint(
                self.min_int,
                self.max_int,
                size=(dim, dim)
            )
        else:
            dim = len(matrix)
        self.matrix_mobject = Matrix(matrix, **self.matrix_config)
        self.equals = OldTex("=")
        self.equals.scale(1.5)

        colors = [X_COLOR, Y_COLOR, Z_COLOR][:dim]
        chars = ["x", "y", "z"][:dim]
        self.input_vect_mob = Matrix(np.array(chars))
        self.input_vect_mob.elements.set_color_by_gradient(*colors)

        if output_vect is None:
            output_vect = np.random.randint(
                self.min_int, self.max_int, size=(dim, 1))
        self.output_vect_mob = IntegerMatrix(output_vect)
        self.output_vect_mob.elements.set_color(OUTPUT_COLOR)

        for mob in self.matrix_mobject, self.input_vect_mob, self.output_vect_mob:
            mob.set_height(self.height)

        self.add(
            self.matrix_mobject,
            self.input_vect_mob,
            self.equals,
            self.output_vect_mob,
        )
        self.arrange(RIGHT, buff=SMALL_BUFF)


class SetupSimpleSystemOfEquations(LinearTransformationScene):
    CONFIG = {
        "matrix": [[3, 2], [-1, 2]],
        "output_vect": [-4, -2],
        "quit_before_final_transformation": False,
        "array_scale_factor": 0.75,
        "compare_to_big_system": True,
        "transition_to_geometric_view": True,
    }

    def construct(self):
        self.remove_grid()
        self.introduce_system()
        self.from_system_to_matrix()
        self.show_geometry()

    def remove_grid(self):
        self.clear()

    def introduce_system(self):
        system = self.system = self.get_system(self.matrix, self.output_vect)
        dim = len(self.matrix)
        big_dim = 7  # Big system size
        big_matrix = np.random.randint(-9, 10, size=(big_dim, big_dim))
        big_output_vect = np.random.randint(-9, 10, size=big_dim)
        big_matrix[:dim, :dim] = self.matrix
        big_output_vect[:dim] = self.output_vect
        big_system = self.get_system(big_matrix, big_output_vect)

        unknown_circles = VGroup(*[
            Circle(color=YELLOW).replace(term).scale(1.5)
            for term in system.unknowns
        ])
        unknown_circles.set_stroke(YELLOW, 2)
        for circle in unknown_circles:
            circle.save_state()
            circle.scale(5)
            circle.fade(1)
        row_rects = VGroup(*list(map(SurroundingRectangle, system)))
        row_rects.set_stroke(BLUE, 2)

        self.add(system)
        self.wait()
        self.play(LaggedStartMap(
            ApplyMethod, unknown_circles,
            lambda m: (m.restore,),
            lag_ratio=0.7
        ))
        self.play(FadeOut(unknown_circles))
        self.play(LaggedStartMap(ShowCreation, row_rects,
                              run_time=1, lag_ratio=0.8))
        self.play(FadeOut(row_rects))
        self.wait()
        if self.compare_to_big_system:
            self.remove(system)
            self.play(ReplacementTransform(system.copy(), big_system))
            self.wait(2)
            # Oh yeah, super readable line...
            cutoff = 3 * dim - 1
            self.play(*[
                ReplacementTransform(big_system[i][:cutoff], system[i][:cutoff])
                for i in range(dim)
            ] + [
                ReplacementTransform(big_system[i][-2:], system[i][-2:])
                for i in range(dim)
            ] + [
                FadeOut(big_system[i][start:end])
                for i in range(big_dim)
                for start in [cutoff if i < dim else 0]
                for end in [-2 if i < dim else len(big_system[i])]
            ])
            self.remove(big_system, system)
            self.add(system)

    def from_system_to_matrix(self):
        # dim = len(self.matrix)
        system_in_lines = self.system
        matrix_system = self.matrix_system = LinearSystem(
            self.matrix, self.output_vect, height=2
        )
        matrix_system.center()

        corner_rect = self.corner_rect = SurroundingRectangle(
            matrix_system, buff=MED_SMALL_BUFF
        )
        corner_rect.set_stroke(width=0)
        corner_rect.set_fill(BLACK, opacity=0.8)
        corner_rect.set_height(2)
        corner_rect.to_corner(UL, buff=0)

        self.play(system_in_lines.to_edge, UP)
        system_in_lines_copy = system_in_lines.deepcopy()
        self.play(
            ReplacementTransform(
                VGroup(*list(map(VGroup, system_in_lines_copy.matrix_elements))),
                matrix_system.matrix_mobject.elements,
            ),
            Write(matrix_system.matrix_mobject.brackets),
            Write(matrix_system.output_vect_mob.brackets),
            Write(matrix_system.input_vect_mob.brackets),
            Write(matrix_system.equals)
        )
        self.play(ReplacementTransform(
            VGroup(*list(map(VGroup, system_in_lines_copy.output_vect_elements))),
            matrix_system.output_vect_mob.elements,
        ))
        self.play(*[
            ReplacementTransform(uk, elem)
            for uk, elem in zip(
                system_in_lines_copy.unknowns,
                it.cycle(matrix_system.input_vect_mob.elements)
            )
        ])
        self.wait()
        if self.transition_to_geometric_view:
            self.play(
                Write(self.background_plane),
                Write(self.plane),
                FadeOut(system_in_lines),
                FadeIn(corner_rect),
                matrix_system.set_height, corner_rect.get_height() - MED_LARGE_BUFF,
                matrix_system.move_to, corner_rect,
            )
            self.play(*list(map(GrowArrow, self.basis_vectors)))

            self.add_foreground_mobject(corner_rect)
            self.add_foreground_mobject(matrix_system)

    def show_geometry(self):
        system = self.matrix_system
        matrix_mobject = system.matrix_mobject
        columns = VGroup(*[
            VGroup(*matrix_mobject.mob_matrix[:, i])
            for i in (0, 1)
        ])

        matrix = np.array(self.matrix)
        first_half_matrix = np.identity(matrix.shape[0])
        first_half_matrix[:, 0] = matrix[:, 0]
        second_half_matrix = np.dot(
            matrix,
            np.linalg.inv(first_half_matrix),
        )

        scale_factor = self.array_scale_factor

        column_mobs = VGroup()
        for i in 0, 1:
            column_mob = IntegerMatrix(matrix[:, i])
            column_mob.elements.set_color([X_COLOR, Y_COLOR][i])
            column_mob.scale(scale_factor)
            column_mob.next_to(
                self.plane.coords_to_point(*matrix[:, i]), RIGHT)
            column_mob.add_to_back(BackgroundRectangle(column_mob))
            column_mobs.add(column_mob)

        output_vect_mob = self.get_vector(self.output_vect, color=OUTPUT_COLOR)
        output_vect_label = system.output_vect_mob.deepcopy()
        output_vect_label.add_to_back(BackgroundRectangle(output_vect_label))
        output_vect_label.generate_target()
        output_vect_label.target.scale(scale_factor)
        output_vect_label.target.next_to(
            output_vect_mob.get_end(), LEFT, SMALL_BUFF)

        input_vect = np.dot(np.linalg.inv(self.matrix), self.output_vect)
        input_vect_mob = self.get_vector(input_vect, color=INPUT_COLOR)
        q_marks = OldTex("????")
        q_marks.set_color_by_gradient(INPUT_COLOR, OUTPUT_COLOR)
        q_marks.next_to(input_vect_mob.get_end(), DOWN, SMALL_BUFF)
        q_marks_rect = SurroundingRectangle(q_marks, color=WHITE)

        # Show output vector
        self.play(
            GrowArrow(output_vect_mob),
            MoveToTarget(output_vect_label),
        )
        self.add_foreground_mobjects(output_vect_mob, output_vect_label)
        self.wait()

        # Show columns
        for column, color in zip(columns, [X_COLOR, Y_COLOR]):
            rect = SurroundingRectangle(column, color=WHITE)
            self.play(
                column.set_color, color,
                system.input_vect_mob.elements.set_color, WHITE,
                ShowPassingFlash(rect),
            )
        matrices = [first_half_matrix, second_half_matrix]
        for column, column_mob, m in zip(columns, column_mobs, matrices):
            column_mob.save_state()
            column_mob[0].scale(0).move_to(matrix_mobject)
            column_mob.elements.become(column)
            column_mob.brackets.become(matrix_mobject.brackets)
            self.add_foreground_mobject(column_mob)
            self.apply_matrix(m, added_anims=[
                ApplyMethod(column_mob.restore, path_arc=90 * DEGREES)
            ])
        self.wait()

        # Do inverse transformation to reveal input
        self.remove_foreground_mobjects(column_mobs)
        self.apply_inverse(self.matrix, run_time=1, added_anims=[
            ReplacementTransform(output_vect_mob.copy(), input_vect_mob),
            ReplacementTransform(output_vect_label.elements.copy(), q_marks),
            FadeOut(column_mobs)
        ])
        self.play(ShowPassingFlash(q_marks_rect))
        self.wait(2)
        if not self.quit_before_final_transformation:
            self.apply_matrix(self.matrix, added_anims=[
                FadeOut(q_marks),
                ReplacementTransform(input_vect_mob, output_vect_mob),
                FadeIn(column_mobs),
            ])
            self.wait()

        self.q_marks = q_marks
        self.input_vect_mob = input_vect_mob
        self.output_vect_mob = output_vect_mob
        self.output_vect_label = output_vect_label
        self.column_mobs = column_mobs

    # Helpers

    def get_system(self, matrix, output_vect):
        if len(matrix) <= 3:
            chars = "xyzwv"
        else:
            chars = ["x_%d" % d for d in range(len(matrix))]
        colors = [
            color
            for i, color in zip(
                list(range(len(matrix))),
                it.cycle([X_COLOR, Y_COLOR, Z_COLOR, YELLOW, MAROON_B, TEAL])
            )
        ]
        system = VGroup()
        system.matrix_elements = VGroup()
        system.output_vect_elements = VGroup()
        system.unknowns = VGroup()
        for row, num in zip(matrix, output_vect):
            args = []
            for i in range(len(row)):
                if i + 1 == len(row):
                    sign = "="
                elif row[i + 1] < 0:
                    sign = "-"
                else:
                    sign = "+"
                args += [str(abs(row[i])), chars[i], sign]
            args.append(str(num))
            line = OldTex(*args)
            line.set_color_by_tex_to_color_map(dict([
                (char, color)
                for char, color in zip(chars, colors)
            ]))
            system.add(line)
            system.matrix_elements.add(*line[0:-1:3])
            system.unknowns.add(*line[1:-1:3])
            system.output_vect_elements.add(line[-1])

        system.output_vect_elements.set_color(OUTPUT_COLOR)
        system.arrange(
            DOWN,
            buff=0.75,
            index_of_submobject_to_align=-2
        )
        return system


class ShowZeroDeterminantCase(LinearTransformationScene):
    CONFIG = {
        "show_basis_vectors": True,
        "matrix": [[3, -2.0], [1, -2.0 / 3]],
        "tex_scale_factor": 1.25,
        "det_eq_symbol": "=",
    }

    def construct(self):
        self.add_equation()
        self.show_det_zero()

    def add_equation(self):
        equation = self.equation = OldTex(
            "A", "\\vec{\\textbf{x}}", "=", "\\vec{\\textbf{v}}"
        )
        equation.scale(self.tex_scale_factor)
        equation.set_color_by_tex("{x}", INPUT_COLOR)
        equation.set_color_by_tex("{v}", OUTPUT_COLOR)
        equation.add_background_rectangle()
        equation.to_corner(UL)
        self.add(equation)
        self.add_foreground_mobject(equation)

    def show_det_zero(self):
        matrix = self.matrix

        # vect_in_span = [2, 2.0 / 3]
        vect_in_span = [2, 2.0 / 3]
        vect_off_span = [1, 2]
        vect_in_span_mob = self.get_vector(vect_in_span, color=OUTPUT_COLOR)
        vect_off_span_mob = self.get_vector(vect_off_span, color=OUTPUT_COLOR)

        for vect_mob in vect_in_span_mob, vect_off_span_mob:
            circle = Circle(color=WHITE, radius=0.15, stroke_width=2)
            circle.move_to(vect_mob.get_end())
            vect_mob.circle = circle

        vect_off_span_words = OldTexText("No input lands here")
        vect_off_span_words.next_to(vect_off_span_mob.circle, UP)
        vect_off_span_words.add_background_rectangle()

        vect_in_span_words = OldTexText("Many inputs lands here")
        vect_in_span_words.next_to(vect_in_span_mob.circle, DR)
        vect_in_span_words.shift_onto_screen()
        vect_in_span_words.add_background_rectangle()

        moving_group = VGroup(self.plane, self.basis_vectors)
        moving_group.save_state()

        solution = np.dot(np.linalg.pinv(matrix), vect_in_span)
        import sympy
        null_space_basis = np.array(sympy.Matrix(matrix).nullspace())
        null_space_basis = null_space_basis.flatten().astype(float)
        solution_vectors = VGroup(*[
            self.get_vector(
                solution + x * null_space_basis,
                rectangular_stem_width=0.025,
                tip_length=0.2,
            )
            for x in np.linspace(-4, 4, 20)
        ])
        solution_vectors.set_color_by_gradient(YELLOW, MAROON_B)

        self.apply_matrix(matrix, path_arc=0)
        self.wait()
        self.show_det_equation()
        self.wait()

        # Mention zero determinants
        self.play(GrowArrow(vect_off_span_mob))
        self.play(
            ShowCreation(vect_off_span_mob.circle),
            Write(vect_off_span_words),
        )
        self.wait()
        self.play(
            FadeOut(vect_off_span_mob.circle),
            ReplacementTransform(vect_off_span_mob, vect_in_span_mob),
            ReplacementTransform(vect_off_span_words, vect_in_span_words),
            ReplacementTransform(vect_off_span_mob.circle,
                                 vect_in_span_mob.circle),
        )
        self.wait(2)
        self.play(
            FadeOut(vect_in_span_words),
            FadeOut(vect_in_span_mob.circle),
            ApplyMethod(moving_group.restore, run_time=2),
            ReplacementTransform(
                VGroup(vect_in_span_mob),
                solution_vectors,
                run_time=2,
            ),
        )
        self.wait()

    # Helpers

    def show_det_equation(self):
        equation = self.equation
        det_equation = OldTex(
            "\\det(", "A", ")", self.det_eq_symbol, "0"
        )
        det_equation.scale(self.tex_scale_factor)
        det_equation.next_to(
            equation, DOWN, buff=MED_LARGE_BUFF, aligned_edge=LEFT)
        det_rect = BackgroundRectangle(det_equation)
        self.play(
            FadeIn(det_rect),
            Write(det_equation[0]),
            ReplacementTransform(
                equation.get_part_by_tex("A").copy(),
                det_equation.get_part_by_tex("A").copy(),
            ),
            Write(det_equation[2:]),
        )
        self.add_foreground_mobject(det_rect, det_equation)


# CHANGE: Cairo digest_config gave the LAST base (SetupSimpleSystemOfEquations) priority over the first (ShowZeroDeterminantCase) when merging CONFIG; here that is the non-singular matrix, while the Python MRO now picks the singular one
class NonZeroDeterminantCase(ShowZeroDeterminantCase, SetupSimpleSystemOfEquations):
    CONFIG = {
        "det_eq_symbol": "\\neq",
        "matrix": [[3, 2], [-1, 2]],
    }

    def construct(self):
        self.add_equation()
        self.show_det_equation()

        output_vect = self.output_vect
        matrix = self.matrix
        input_vect = np.dot(np.linalg.inv(matrix), output_vect)

        input_vect_mob = self.get_vector(input_vect, color=INPUT_COLOR)
        output_vect_mob = self.get_vector(output_vect, color=OUTPUT_COLOR)

        input_vect_label = OldTexText("Input")
        input_vect_label.next_to(input_vect_mob.get_end(), DOWN, SMALL_BUFF)
        input_vect_label.match_color(input_vect_mob)
        output_vect_label = OldTexText("Output")
        output_vect_label.next_to(output_vect_mob.get_end(), DOWN, SMALL_BUFF)
        output_vect_label.match_color(output_vect_mob)
        for label in input_vect_label, output_vect_label:
            label.scale(1.25, about_edge=UP)
            label.add_background_rectangle()

        self.apply_matrix(matrix)
        self.wait()
        self.apply_inverse(matrix)
        self.wait()
        self.play(
            GrowArrow(input_vect_mob),
            Write(input_vect_label),
            run_time=1
        )
        self.wait()
        self.remove(input_vect_mob, input_vect_label)
        self.apply_matrix(matrix, added_anims=[
            ReplacementTransform(input_vect_mob.copy(), output_vect_mob),
            ReplacementTransform(input_vect_label.copy(), output_vect_label),
        ], run_time=2)
        self.wait()
        self.remove(output_vect_mob, output_vect_label)
        self.apply_inverse(matrix, added_anims=[
            ReplacementTransform(output_vect_mob.copy(), input_vect_mob),
            ReplacementTransform(output_vect_label.copy(), input_vect_label),
        ], run_time=2)
        self.wait()
