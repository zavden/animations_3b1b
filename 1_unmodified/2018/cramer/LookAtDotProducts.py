# ==============================================================================
# Scene:      LookAtDotProducts
# Source:     videos/_2018/cramer.py (lines 912-1127)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl LookAtDotProducts.py LookAtDotProducts -w -m --fps 15
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


class LookAtDotProducts(SetupSimpleSystemOfEquations):
    CONFIG = {
        "quit_before_final_transformation": True,
        "equation_scale_factor": 0.7,
    }

    def construct(self):
        self.force_skipping()
        super(LookAtDotProducts, self).construct()
        self.revert_to_original_skipping_status()

        self.remove_corner_system()
        self.show_dot_products()

    def remove_corner_system(self):
        to_remove = [self.corner_rect, self.matrix_system]
        self.remove_foreground_mobjects(*to_remove)
        self.remove(*to_remove)

        q_marks = self.q_marks
        input_vect_mob = self.input_vect_mob

        equations = self.equations = VGroup()
        for i in 0, 1:
            basis = [0, 0]
            basis[i] = 1
            equation = VGroup(
                Matrix(["x", "y"]),
                OldTex("\\cdot"),
                IntegerMatrix(basis),
                OldTex("="),
                OldTex(["x", "y"][i]),
            )
            for part in equation:
                if isinstance(part, Matrix):
                    part.scale(self.array_scale_factor)
            equation[2].elements.set_color([X_COLOR, Y_COLOR][i])
            equation.arrange(RIGHT, buff=SMALL_BUFF)
            equation.scale(self.equation_scale_factor)
            equations.add(equation)
        equations.arrange(DOWN, buff=MED_LARGE_BUFF)
        equations.to_corner(UL)
        corner_rect = self.corner_rect = BackgroundRectangle(
            equations, opacity=0.8)
        self.resize_corner_rect_to_mobjet(corner_rect, equations)
        corner_rect.save_state()
        self.resize_corner_rect_to_mobjet(corner_rect, equations[0])

        xy_vect_mob = Matrix(["x", "y"], include_background_rectangle=True)
        xy_vect_mob.scale(self.array_scale_factor)
        xy_vect_mob.next_to(input_vect_mob.get_end(), DOWN, SMALL_BUFF)
        q_marks.add_background_rectangle()
        q_marks.next_to(xy_vect_mob, RIGHT)

        origin = self.plane.coords_to_point(0, 0)
        input_vect_end = input_vect_mob.get_end()
        x_point = (input_vect_end - origin)[0] * RIGHT + origin
        y_point = (input_vect_end - origin)[1] * UP + origin
        v_dashed_line = DashedLine(input_vect_end, x_point)
        h_dashed_line = DashedLine(input_vect_end, y_point)

        h_brace = Brace(Line(x_point, origin), UP, buff=SMALL_BUFF)
        v_brace = Brace(Line(y_point, origin), RIGHT, buff=SMALL_BUFF)

        self.add(xy_vect_mob)
        self.wait()
        self.play(
            FadeIn(corner_rect),
            FadeIn(equations[0][:-1]),
            ShowCreation(v_dashed_line),
            GrowFromCenter(h_brace),
        )
        self.play(
            ReplacementTransform(h_brace.copy(), equations[0][-1])
        )
        self.wait()
        self.play(
            corner_rect.restore,
            Animation(equations[0]),
            FadeIn(equations[1]),
        )
        self.wait()
        self.play(
            ReplacementTransform(equations[1][-1].copy(), v_brace),
            ShowCreation(h_dashed_line),
            GrowFromCenter(v_brace)
        )
        self.wait()

        self.to_fade = VGroup(
            h_dashed_line, v_dashed_line,
            h_brace, v_brace,
            xy_vect_mob, q_marks,
        )

    def show_dot_products(self):
        moving_equations = self.equations.copy()
        transformed_equations = VGroup()
        implications = VGroup()
        transformed_input_rects = VGroup()
        transformed_basis_rects = VGroup()
        for equation in moving_equations:
            equation.generate_target()
            xy_vect, dot, basis, equals, coord = equation.target
            T1, lp1, rp1 = OldTex("T", "(", ")")
            lp1.scale(1, about_edge=LEFT)
            rp1.scale(1, about_edge=LEFT)
            for paren in lp1, rp1:
                paren.stretch_to_fit_height(equation.get_height())
            T2, lp2, rp2 = T1.copy(), lp1.copy(), rp1.copy()
            transformed_equation = VGroup(
                T1, lp1, xy_vect, rp1, dot,
                T2, lp2, basis, rp2, equals,
                coord
            )
            transformed_equation.arrange(RIGHT, buff=SMALL_BUFF)
            # transformed_equation.scale(self.equation_scale_factor)

            implies = OldTex("\\Rightarrow").scale(1.2)
            implies.next_to(equation, RIGHT)
            implies.set_color(BLUE)

            transformed_equation.next_to(implies, RIGHT)
            implications.add(implies)

            transformed_input_rects.add(SurroundingRectangle(
                transformed_equation[:4],
                color=OUTPUT_COLOR
            ))
            transformed_basis_rects.add(SurroundingRectangle(
                transformed_equation[5:5 + 4],
                color=basis.elements.get_color()
            ))

            for mob in [implies]:
                mob.add(OldTex("?").next_to(mob, UP, SMALL_BUFF))

            transformed_equation.parts_to_write = VGroup(
                T1, lp1, rp1, T2, lp2, rp2
            )

            transformed_equations.add(transformed_equation)

        corner_rect = self.corner_rect
        corner_rect.generate_target()
        group = VGroup(self.equations, transformed_equations)
        self.resize_corner_rect_to_mobjet(corner_rect.target, group)

        for array in [self.output_vect_label] + list(self.column_mobs):
            array.rect = SurroundingRectangle(array)
            array.rect.match_color(array.elements)

        self.play(
            MoveToTarget(corner_rect),
            Animation(self.equations),
            FadeOut(self.to_fade),
            LaggedStartMap(Write, implications),
        )
        self.remove(self.input_vect_mob)
        self.apply_matrix(self.matrix, added_anims=[
            Animation(VGroup(corner_rect, self.equations, implications)),
            MoveToTarget(moving_equations[0]),
            LaggedStartMap(FadeIn, transformed_equations[0].parts_to_write),
            FadeIn(self.column_mobs),
            ReplacementTransform(
                self.input_vect_mob.copy(), self.output_vect_mob)
        ])
        self.play(
            MoveToTarget(moving_equations[1]),
            LaggedStartMap(FadeIn, transformed_equations[1].parts_to_write),
            path_arc=-30 * DEGREES,
            run_time=2
        )
        self.wait()

        # Show rectangles
        self.play(
            LaggedStartMap(ShowCreation, transformed_input_rects, lag_ratio=0.8),
            ShowCreation(self.output_vect_label.rect),
        )
        for tbr, column_mob in zip(transformed_basis_rects, self.column_mobs):
            self.play(
                ShowCreation(tbr),
                ShowCreation(column_mob.rect),
            )
        self.wait()
        self.play(FadeOut(VGroup(
            transformed_input_rects,
            transformed_basis_rects,
            self.output_vect_label.rect,
            *[cm.rect for cm in self.column_mobs]
        )))

        # These computations assume plane is centered at ORIGIN
        output_vect = self.output_vect_mob.get_end()
        c1 = self.basis_vectors[0].get_end()
        c2 = self.basis_vectors[1].get_end()
        x_point = c1 * np.dot(output_vect, c1) / (get_norm(c1)**2)
        y_point = c2 * np.dot(output_vect, c2) / (get_norm(c2)**2)

        dashed_line_to_x = DashedLine(self.output_vect_mob.get_end(), x_point)
        dashed_line_to_y = DashedLine(self.output_vect_mob.get_end(), y_point)

        self.play(ShowCreation(dashed_line_to_x))
        self.play(ShowCreation(dashed_line_to_y))
        self.wait()

    # Helpers

    def resize_corner_rect_to_mobjet(self, rect, mobject):
        rect.stretch_to_fit_width(
            mobject.get_width() + MED_LARGE_BUFF + SMALL_BUFF)
        rect.stretch_to_fit_height(
            mobject.get_height() + MED_LARGE_BUFF + SMALL_BUFF)
        rect.to_corner(UL, buff=0)
        return rect
