# ==============================================================================
# Scene:      TransformingAreasXCoord
# Source:     videos/_2018/cramer.py (lines 2017-2020)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TransformingAreasXCoord.py TransformingAreasXCoord -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

X_COLOR = GREEN


Y_COLOR = RED


INPUT_COLOR = MAROON_B


class TransformingAreasYCoord(LinearTransformationScene):
    CONFIG = {
        # Determines whether x-coordinate or y-coordinate is computed
        "index": 1,
        "matrix": [[2, -1], [0, 1]],
        "input_vect": [3, 2],
        "array_scale_factor": 0.7,
    }

    def construct(self):
        self.init_matrix()
        self.init_plane()
        self.show_coord_parallelogram()
        self.transform_space()
        self.solve_for_coord()

    def init_matrix(self):
        self.matrix = np.array(self.matrix)

    def init_plane(self):
        self.plane.set_stroke(width=2)

    def show_coord_parallelogram(self):
        index = self.index
        non_index = (index + 1) % 2

        input_vect = self.input_vect
        input_vect_mob = self.get_vector(input_vect, color=INPUT_COLOR)
        input_vect_label = Matrix(["x", "y"])
        input_vect_label.add_background_rectangle()
        input_vect_label.scale(self.array_scale_factor)
        self.set_input_vect_label_position(input_vect_mob, input_vect_label)

        mystery_words = OldTexText("Mystery input vector")
        mystery_words.next_to(input_vect_label, RIGHT)
        mystery_words.add_background_rectangle()

        # Add basis vector labels
        basis_labels = self.basis_labels = VGroup()
        basis_vectors = self.basis_vectors
        chars = ["\\imath", "\\jmath"]
        directions = ["right", "left"]
        for basis, char, direction in zip(basis_vectors, chars, directions):
            label = self.get_vector_label(
                basis, "\\mathbf{\\hat{%s}}" % char,
                direction=direction
            )
            self.basis_labels.add(label)

        ip = self.get_input_parallelogram(input_vect_mob)
        area_arrow_direction = 1.5 * DOWN + RIGHT if self.index == 0 else DR
        area_arrow = Vector(
            area_arrow_direction, color=WHITE,
            rectangular_stem_width=0.025,
            tip_length=0.2,
        )
        area_arrow.shift(ip.get_center() - area_arrow.get_end() + SMALL_BUFF * DL)
        area_words = OldTex(
            "\\text{Area}", "=", "1", "\\times",
            ["x", "y"][index]
        )
        area_words.next_to(
            area_arrow.get_start(), UL, SMALL_BUFF,
            submobject_to_align=area_words[0]
        )
        area_words.set_color_by_tex_to_color_map({
            "Area": YELLOW,
            "x": X_COLOR,
            "y": Y_COLOR,
        })
        area_words.rect = BackgroundRectangle(area_words)

        origin = self.plane.coords_to_point(0, 0)
        unit_brace = Brace(
            Line(origin, basis_vectors[non_index].get_end()),
            [DOWN, LEFT][non_index],
            buff=SMALL_BUFF
        )
        one = unit_brace.get_tex("1")
        one.add_background_rectangle()
        coord_brace = self.get_parallelogram_braces(ip)[index]

        self.add(input_vect_mob, input_vect_label)
        self.add(basis_labels)

        self.play(
            FadeIn(ip),
            Animation(VGroup(basis_vectors, input_vect_mob))
        )
        self.play(
            ShowCreationThenDestruction(SurroundingRectangle(basis_labels[non_index])),
            GrowArrow(self.basis_vectors[non_index].copy(), remover=True)
        )
        self.play(
            ShowCreationThenDestruction(SurroundingRectangle(input_vect_label)),
            GrowArrow(input_vect_mob.copy(), remover=True),
        )
        self.wait()
        self.play(
            FadeIn(area_words.rect),
            Write(area_words[:2]),
            GrowArrow(area_arrow),
        )
        self.wait()
        self.play(
            FadeOut(basis_labels),
            GrowFromCenter(unit_brace),
            FadeIn(one),
            FadeIn(area_words[2])
        )
        self.wait()
        self.play(
            GrowFromCenter(coord_brace),
            FadeIn(coord_brace.label),
            FadeIn(area_words[3:]),
        )
        self.wait()
        self.play(
            area_words.rect.stretch_to_fit_width,
            area_words[:3].get_width() + SMALL_BUFF, {"about_edge": LEFT},
            FadeOut(area_words[2:4]),
            area_words[4].shift,
            (area_words[2].get_left()[0] - area_words[4].get_left()[0]) * RIGHT,
            Animation(area_words[:2]),
        )
        area_words.remove(*area_words[2:4])
        self.wait()

        # Run with me
        morty = Mortimer(height=2).flip()
        morty.to_corner(DL)
        randy = Randolph(height=2, color=BLUE_C).flip()
        randy.move_to(4 * RIGHT)
        randy.to_edge(DOWN)
        self.play(FadeIn(randy))
        self.play(randy.change, "confused", ip)
        self.play(Blink(randy), FadeIn(morty))
        self.play(
            PiCreatureSays(morty, "Run with \\\\ me here...", look_at=randy.eyes),
            randy.look_at, morty.eyes,
        )
        self.play(Blink(morty))
        self.play(FadeOut(VGroup(morty, morty.bubble, morty.bubble.content, randy)))

        # Signed area
        signed = OldTexText("Signed")
        signed.match_color(area_words[0])
        signed.next_to(area_words, LEFT)

        brace_group = VGroup(coord_brace, coord_brace.label)

        def update_brace_group(brace_group):
            new_brace = self.get_parallelogram_braces(ip)[index]
            new_group = VGroup(new_brace, new_brace.label)
            Transform(brace_group, new_group).update(1)

        area_words.add_to_back(signed)
        self.play(
            area_words.rect.stretch_to_fit_width, area_words.get_width(),
            {"about_edge": RIGHT},
            Write(signed),
            Animation(area_words),
        )
        self.play(
            UpdateFromFunc(
                ip, lambda m: Transform(m, self.get_input_parallelogram(input_vect_mob)).update(1)
            ),
            input_vect_mob.rotate, np.pi, {"about_point": origin},
            Animation(self.basis_vectors),
            UpdateFromFunc(brace_group, update_brace_group),
            UpdateFromFunc(
                input_vect_label,
                lambda ivl: self.set_input_vect_label_position(input_vect_mob, ivl)
            ),
            MaintainPositionRelativeTo(area_arrow, ip),
            MaintainPositionRelativeTo(area_words.rect, area_arrow),
            MaintainPositionRelativeTo(area_words, area_arrow),
            run_time=9,
            rate_func=there_and_back_with_pause,
        )

        # Fade out unneeded bits
        self.play(LaggedStartMap(FadeOut, VGroup(
            unit_brace, one, coord_brace, coord_brace.label,
        )))

        self.input_parallelogram = ip
        self.area_words = area_words
        self.area_arrow = area_arrow
        self.input_vect_mob = input_vect_mob
        self.input_vect_label = input_vect_label

    def transform_space(self):
        matrix = self.matrix
        ip = self.input_parallelogram
        area_words = self.area_words
        area_arrow = self.area_arrow
        input_vect_mob = self.input_vect_mob
        input_vect_label = self.input_vect_label
        basis_vectors = self.basis_vectors
        index = self.index
        non_index = (index + 1) % 2

        apply_words = OldTexText("Apply")
        apply_words.add_background_rectangle()
        matrix_mobject = IntegerMatrix(self.matrix)
        matrix_mobject.set_column_colors(X_COLOR, Y_COLOR)
        matrix_mobject.add_background_rectangle()
        matrix_mobject.next_to(apply_words, RIGHT)
        matrix_brace = Brace(matrix_mobject, DOWN, buff=SMALL_BUFF)
        matrix_label = matrix_brace.get_tex("A")
        matrix_label.add_background_rectangle()
        apply_group = VGroup(apply_words, matrix_mobject, matrix_brace, matrix_label)
        apply_group.to_corner(UL, buff=MED_SMALL_BUFF)

        area_scale_words = OldTexText("All areas get scaled by", "$\\det(A)$")
        area_scale_words.scale(1.5)
        area_scale_words.move_to(2 * DOWN)
        area_scale_words.add_background_rectangle()

        blobs = VGroup(
            Circle(radius=0.5).move_to(2 * LEFT + UP),
            Square(side_length=1).rotate(TAU / 12).move_to(2 * UP + 0.5 * RIGHT),
            OldTex("\\pi").scale(3).move_to(3 * RIGHT)
        )
        blobs.set_stroke(YELLOW, 3)
        blobs.set_fill(YELLOW, 0.3)

        # Initial transform
        self.add_transformable_mobject(ip)
        self.add(self.basis_vectors)
        self.add_vector(input_vect_mob, animate=False)
        self.play(
            Write(apply_words), FadeIn(matrix_mobject),
            GrowFromCenter(matrix_brace), Write(matrix_label),
        )
        self.add_foreground_mobjects(apply_group)
        self.play(*list(map(FadeOut, [
            area_words.rect, area_words, area_arrow, input_vect_label,
        ])))
        self.apply_matrix(matrix)
        self.wait(2)
        self.apply_inverse(matrix, run_time=0)

        # Show many areas
        self.play(
            LaggedStartMap(DrawBorderThenFill, blobs),
            Write(area_scale_words)
        )
        self.add_transformable_mobject(blobs)
        self.add_foreground_mobject(area_scale_words)
        self.apply_matrix(matrix)

        # Ask about parallelogram
        ip_copy = ip.copy()
        ip_copy.set_stroke(BLACK, 4)
        ip_copy.set_fill(BLACK, 0)

        q_marks = OldTex("???")
        q_marks.scale(1.5)
        q_marks.rect = BackgroundRectangle(q_marks)
        q_marks_group = VGroup(q_marks, q_marks.rect)
        q_marks_group.rotate(input_vect_mob.get_angle())
        q_marks_group.move_to(ip)

        column_mobs = VGroup()
        for i, vect in zip(list(range(2)), [DOWN, LEFT]):
            column = matrix_mobject.deepcopy().mob_matrix[:, i]
            column_mob = MobjectMatrix(column)
            column_mob.scale(self.array_scale_factor)
            column_mob.next_to(basis_vectors[i].get_end(), vect)
            column_mob.add_background_rectangle()
            column_mobs.add(column_mob)
        column_mob = column_mobs[non_index]

        transformed_input_vect_label = VGroup(input_vect_label.copy())
        transformed_input_vect_label.add_to_back(matrix_label.copy())
        transformed_input_vect_label.arrange(RIGHT, buff=SMALL_BUFF)
        transformed_input_vect_label.next_to(input_vect_mob.get_end(), UP)

        self.play(
            ShowPassingFlash(ip_copy),
            FadeIn(q_marks.rect),
            Animation(ip),
            Animation(basis_vectors),
            Animation(input_vect_mob),
            Write(q_marks),
            LaggedStartMap(FadeOut, blobs),
        )
        self.transformable_mobjects.remove(blobs)
        self.play(
            FadeIn(column_mob.background_rectangle),
            ReplacementTransform(
                matrix_mobject.brackets.copy(), column_mob.brackets
            ),
            ReplacementTransform(
                VGroup(*matrix_mobject.mob_matrix[:, non_index]).copy(),
                column_mob.elements
            ),
        )
        self.wait()
        self.play(
            ReplacementTransform(matrix_label.copy(), transformed_input_vect_label[0]),
            FadeIn(transformed_input_vect_label[1])
        )
        self.wait(2)

        # Back to input state
        self.remove(q_marks.rect)
        self.apply_inverse(matrix, added_anims=[
            FadeOut(q_marks),
            FadeOut(transformed_input_vect_label),
            FadeOut(column_mob),
            FadeIn(area_words.rect),
            FadeIn(area_words),
            FadeIn(area_arrow),
        ])
        self.wait(2)

        # Show how parallelogram scales by det(A)
        self.apply_matrix(matrix, added_anims=[
            UpdateFromFunc(
                area_arrow,
                lambda a: a.put_start_and_end_on(
                    area_arrow.get_start(), ip.get_center() + SMALL_BUFF * DL
                )
            ),
            Animation(area_words.rect),
            Animation(area_words),
        ])

        det_A = area_scale_words.get_part_by_tex("det").copy()
        det_A.generate_target()
        det_A.target.scale(1.0 / 1.5)
        det_A.target.next_to(
            area_words[1:3], RIGHT, SMALL_BUFF,
            aligned_edge=DOWN,
            submobject_to_align=det_A.target[0]
        )
        coord = area_words[-1]
        coord.generate_target()
        coord.target.next_to(det_A.target, RIGHT, SMALL_BUFF)

        self.play(
            area_words.rect.match_width, VGroup(area_words, coord.target),
            {"stretch": True, "about_edge": LEFT},
            Animation(area_words),
            MoveToTarget(det_A),
            MoveToTarget(coord),
        )
        self.wait(2)
        area_words.submobjects.insert(-1, det_A)

        self.area_scale_words = area_scale_words
        self.apply_group = apply_group

    def solve_for_coord(self):
        apply_group = self.apply_group
        area_words = self.area_words.copy()
        index = self.index
        non_index = (index + 1) % 2

        # Setup rearrangement
        signed, area, equals, det, coord = area_words
        for part in area_words:
            part.add_background_rectangle()
            part.generate_target()
        apply_word, matrix_mobject, matrix_brace, matrix_label = apply_group

        h_line = Line(LEFT, RIGHT).match_width(det)
        frac = VGroup(area.target, h_line, det.target)
        frac.arrange(DOWN)
        coord_equation = VGroup(coord.target, equals.target, frac)
        equals.target.next_to(coord.target, RIGHT)
        frac.next_to(equals.target, RIGHT, submobject_to_align=h_line)
        coord_equation.next_to(ORIGIN, DOWN, buff=1.2)
        coord_equation.to_edge(LEFT)

        output_vect = np.dot(self.matrix, self.input_vect)
        new_matrix = np.array(self.matrix)
        new_matrix[:, self.index] = output_vect

        # Setup rhs
        frac_matrix_height = 1.5
        matrix_mobject_copy = matrix_mobject.copy()
        matrix_mobject_copy.set_height(frac_matrix_height)
        denom_det_text = get_det_text(matrix_mobject_copy)
        top_matrix_mobject = IntegerMatrix(new_matrix)
        top_matrix_mobject.set_height(frac_matrix_height)
        top_matrix_mobject.set_column_colors(X_COLOR, Y_COLOR)
        VGroup(*top_matrix_mobject.mob_matrix[:, self.index]).set_color(MAROON_B)
        top_matrix_mobject.add_background_rectangle()
        num_det_text = get_det_text(top_matrix_mobject)
        rhs_h_line = Line(LEFT, RIGHT)
        rhs_h_line.match_width(num_det_text)
        rhs = VGroup(
            VGroup(num_det_text, top_matrix_mobject),
            rhs_h_line,
            VGroup(matrix_mobject_copy, denom_det_text)
        )
        rhs.arrange(DOWN, buff=SMALL_BUFF)
        rhs_equals = OldTex("=")
        rhs_equals.next_to(h_line, RIGHT)
        rhs.next_to(rhs_equals, submobject_to_align=rhs_h_line)

        # Setup linear system
        output_vect_label = IntegerMatrix(output_vect)
        output_vect_label.elements.match_color(self.input_vect_mob)
        output_vect_label.scale(self.array_scale_factor)
        output_vect_label.add_background_rectangle()
        self.set_input_vect_label_position(self.input_vect_mob, output_vect_label)

        matrix_mobject.generate_target()
        system_input = Matrix(["x", "y"])
        system_input.add_background_rectangle()
        system_output = output_vect_label.copy()
        system_output.generate_target()
        system_eq = OldTex("=")
        for array in system_input, system_output.target:
            array.match_height(matrix_mobject.target)
        system = VGroup(
            matrix_mobject.target,
            system_input, system_eq, system_output.target
        )
        system.arrange(RIGHT, buff=SMALL_BUFF)
        system.to_corner(UL)

        # Rearrange
        self.play(
            FadeOut(self.area_scale_words),
            ShowCreation(h_line),
            *list(map(MoveToTarget, area_words[1:])),
            run_time=3
        )
        self.wait()
        self.play(
            ReplacementTransform(matrix_mobject.copy(), matrix_mobject_copy),
            Write(rhs_equals),
            Write(denom_det_text),
            ShowCreation(rhs_h_line)
        )
        self.wait(2)

        # Show output coord
        self.play(
            FadeIn(output_vect_label.background_rectangle),
            ReplacementTransform(
                self.input_vect_mob.copy(),
                output_vect_label.elements,
            ),
            Write(output_vect_label.brackets),
        )
        self.wait()
        self.play(
            FadeOut(apply_word),
            MoveToTarget(matrix_mobject),
            MaintainPositionRelativeTo(matrix_brace, matrix_mobject),
            MaintainPositionRelativeTo(matrix_label, matrix_mobject),
        )
        self.play(
            FadeIn(system_input),
            FadeIn(system_eq),
            MoveToTarget(system_output),
            area_words.rect.stretch_to_fit_width, self.area_words[1:].get_width(),
            {"about_edge": RIGHT},
            Animation(self.area_words[1:]),
            FadeOut(self.area_words[0]),
        )
        self.wait()
        replaced_column = VGroup(*top_matrix_mobject.mob_matrix[:, self.index])
        replaced_column.set_fill(opacity=0)
        self.play(
            ReplacementTransform(matrix_mobject_copy.copy(), top_matrix_mobject),
            ReplacementTransform(denom_det_text.copy(), num_det_text),
        )
        self.wiggle_vector(self.basis_vectors[non_index])
        self.wait()
        self.wiggle_vector(self.input_vect_mob)
        self.remove(replaced_column)
        self.play(
            Transform(
                output_vect_label.elements.copy(),
                replaced_column.copy().set_fill(opacity=1),
                remover=True
            )
        )
        replaced_column.set_fill(opacity=1)
        self.wait()

        # Circle equation
        equation = VGroup(
            area_words[1:], h_line,
            rhs_equals, rhs,
        )
        equation_rect = SurroundingRectangle(equation)
        equation_rect.set_stroke(YELLOW, 3)
        equation_rect.set_fill(BLACK, 0.9)

        self.play(
            DrawBorderThenFill(equation_rect),
            Animation(equation)
        )
        self.wait()

    # Helpers

    def get_input_parallelogram(self, input_vect_mob):
        input_vect = np.array(self.plane.point_to_coords(input_vect_mob.get_end()))
        matrix = self.matrix
        dim = matrix.shape[0]
        # Transofmration from unit square to input parallelogram
        square_to_ip = self.square_to_ip = np.identity(dim)
        square_to_ip[:, self.index] = np.array(input_vect)

        ip = self.get_unit_square()
        ip.apply_matrix(self.square_to_ip)
        if input_vect[self.index] < 0:
            ip.set_color(GOLD)

        return ip

    def get_parallelogram_braces(self, input_parallelogram):
        braces = VGroup(*[
            Brace(
                input_parallelogram, vect,
                buff=SMALL_BUFF,
                min_num_quads=3,
                max_num_quads=3,
            )
            for vect in (DOWN, RIGHT)
        ])
        for brace, tex, color in zip(braces, "xy", [X_COLOR, Y_COLOR]):
            brace.label = brace.get_tex(tex, buff=SMALL_BUFF)
            brace.label.add_background_rectangle()
            brace.label.set_color(color)
        return braces

    def set_input_vect_label_position(self, input_vect_mob, input_vect_label):
        direction = np.sign(input_vect_mob.get_vector())
        input_vect_label.next_to(input_vect_mob.get_end(), direction, buff=SMALL_BUFF)
        return input_vect_label

    def wiggle_vector(self, vector_mob):
        self.play(
            Rotate(
                vector_mob, 15 * DEGREES,
                about_point=ORIGIN,
                rate_func=wiggle,
            )
        )


class TransformingAreasXCoord(TransformingAreasYCoord):
    CONFIG = {
        "index": 0,
    }
