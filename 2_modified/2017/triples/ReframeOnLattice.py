# ==============================================================================
# Scene:      ReframeOnLattice
# Source:     videos/_2017/triples.py (lines 485-951)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ReframeOnLattice.py ReframeOnLattice -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - unit_size is a read-only property of GL planes; these two assignments were only bookkeeping on the target (unused afterwards)
# ==============================================================================

from manim_imports_ext import *

class ReframeOnLattice(PiCreatureScene):
    CONFIG = {
        "initial_plane_center" : 3*LEFT + DOWN,
        "new_plane_center" : ORIGIN,
        "initial_unit_size" : 0.5,
        "new_unit_size" : 0.8,
        "dot_radius" : 0.075,
        "dot_color" : YELLOW,
    }
    def construct(self):
        self.remove(self.pi_creature)
        self.add_plane()
        self.wander_over_lattice_points()
        self.show_whole_distance_examples()
        self.resize_plane()
        self.show_root_example()
        self.view_as_complex_number()
        self.mention_squaring_it()
        self.work_out_square_algebraically()
        self.walk_through_square_geometrically()

    def add_plane(self):
        plane = ComplexPlane(
            center_point = self.initial_plane_center,
            unit_size = self.initial_unit_size,
            stroke_width = 2,
            secondary_line_ratio = 0,
        )
        plane.axes.set_stroke(width = 4)
        plane.coordinate_labels = VGroup()
        for x in range(-8, 20, 2):
            if x == 0:
                continue
            label = OldTex(str(x))
            label.scale(0.5)
            label.add_background_rectangle(opacity = 1)
            label.next_to(plane.coords_to_point(x, 0), DOWN, SMALL_BUFF)
            plane.coordinate_labels.add(label)

        self.add(plane, plane.coordinate_labels)
        self.plane = plane

    def wander_over_lattice_points(self):
        initial_examples = [(5, 3), (6, 8), (2, 7)]
        integer_distance_examples = [(3, 4), (12, 5), (15, 8)]
        dot_tuple_groups = VGroup()
        for x, y in initial_examples + integer_distance_examples:
            dot = Dot(
                self.plane.coords_to_point(x, y),
                color = self.dot_color,
                radius = self.dot_radius,
            )
            tuple_mob = OldTex("(", str(x), ",", str(y), ")")
            tuple_mob.add_background_rectangle()
            tuple_mob.next_to(dot, UP+RIGHT, buff = 0)
            dot_tuple_groups.add(VGroup(dot, tuple_mob))
        dot_tuple_group = dot_tuple_groups[0]
        final_group = dot_tuple_groups[-len(integer_distance_examples)]

        all_dots = self.get_all_plane_dots()

        self.play(Write(dot_tuple_group, run_time = 2))
        self.wait()
        for new_group in dot_tuple_groups[1:len(initial_examples)]:
            self.play(Transform(dot_tuple_group, new_group))
            self.wait()
        self.play(LaggedStartMap(
            FadeIn, all_dots,
            rate_func = there_and_back,
            run_time = 3,
            lag_ratio = 0.2,
        ))
        self.wait()
        self.play(ReplacementTransform(
            dot_tuple_group, final_group
        ))

        self.integer_distance_dot_tuple_groups = VGroup(
            *dot_tuple_groups[len(initial_examples):]
        )

    def show_whole_distance_examples(self):
        dot_tuple_groups = self.integer_distance_dot_tuple_groups
        for dot_tuple_group in dot_tuple_groups:
            dot, tuple_mob = dot_tuple_group
            p0 = self.plane.get_center_point()
            p1 = dot.get_center()
            triangle = Polygon(
                p0, p1[0]*RIGHT + p0[1]*UP, p1,
                stroke_width = 0,
                fill_color = BLUE,
                fill_opacity = 0.75,
            )
            line = Line(p0, p1, color = dot.get_color())
            a, b = self.plane.point_to_coords(p1)
            c = int(np.sqrt(a**2 + b**2))
            hyp_label = OldTex(str(c))
            hyp_label.add_background_rectangle()
            hyp_label.next_to(
                triangle.get_center(), UP+LEFT, buff = SMALL_BUFF
            )
            line.add(hyp_label)

            dot_tuple_group.triangle = triangle
            dot_tuple_group.line = line

        group = dot_tuple_groups[0]

        self.play(Write(group.line))
        self.play(FadeIn(group.triangle), Animation(group.line))
        self.wait(2)
        for new_group in dot_tuple_groups[1:]:
            self.play(
                Transform(group, new_group),
                Transform(group.triangle, new_group.triangle),
                Transform(group.line, new_group.line),
            )
            self.wait(2)
        self.play(*list(map(FadeOut, [group, group.triangle, group.line])))

    def resize_plane(self):
        new_plane = ComplexPlane(
            plane_center = self.new_plane_center,
            unit_size = self.new_unit_size,
            y_radius = 8,
            x_radius = 11,
            stroke_width = 2,
            secondary_line_ratio = 0,
        )
        new_plane.axes.set_stroke(width = 4)
        self.plane.generate_target()
        # CHANGE: unit_size is a read-only property of GL planes; these two assignments were only bookkeeping on the target (unused afterwards)
        self.plane.target.shift(
            new_plane.coords_to_point(0, 0) - \
            self.plane.target.coords_to_point(0, 0)
        )
        self.plane.target.scale(
            self.new_unit_size / self.initial_unit_size
        )
        coordinate_labels = self.plane.coordinate_labels
        for coord in coordinate_labels:
            x = int(coord.get_tex())
            coord.generate_target()
            coord.target.scale(1.5)
            coord.target.next_to(
                new_plane.coords_to_point(x, 0),
                DOWN, buff = SMALL_BUFF
            )


        self.play(
            MoveToTarget(self.plane),
            *list(map(MoveToTarget, self.plane.coordinate_labels)),
            run_time = 2
        )
        self.remove(self.plane)
        self.plane = new_plane
        self.plane.coordinate_labels = coordinate_labels 
        self.add(self.plane, coordinate_labels)
        self.wait()

    def show_root_example(self):
        x, y = (2, 1)
        point = self.plane.coords_to_point(x, y)
        dot = Dot(
            point,
            color = self.dot_color,
            radius = self.dot_radius
        )
        tuple_label = OldTex(str((x, y)))
        tuple_label.add_background_rectangle()
        tuple_label.next_to(dot, RIGHT, SMALL_BUFF)
        line = Line(self.plane.get_center_point(), point)
        line.set_color(dot.get_color())
        distance_labels = VGroup()
        for tex in "2^2 + 1^2", "5":
            pre_label = OldTex("\\sqrt{%s}"%tex)
            rect = BackgroundRectangle(pre_label)
            label = VGroup(
                rect,
                VGroup(*pre_label[:2]),
                VGroup(*pre_label[2:]),
            )
            label.scale(0.8)
            label.next_to(line.get_center(), UP, SMALL_BUFF)
            label.rotate(
                line.get_angle(),
                about_point = line.get_center()
            )
            distance_labels.add(label)

        self.play(
            ShowCreation(line),
            DrawBorderThenFill(
                dot,
                stroke_width = 3,
                stroke_color = PINK
            )
        )
        self.play(Write(tuple_label))
        self.wait()
        self.play(FadeIn(distance_labels[0]))
        self.wait(2)
        self.play(Transform(*distance_labels))
        self.wait(2)

        self.distance_label = distance_labels[0]
        self.example_dot = dot
        self.example_line = line
        self.example_tuple_label = tuple_label

    def view_as_complex_number(self):
        imag_coords = VGroup()
        for y in range(-4, 5, 2):
            if y == 0:
                continue
            label = OldTex("%di"%y)
            label.add_background_rectangle()
            label.scale(0.75)
            label.next_to(
                self.plane.coords_to_point(0, y),
                LEFT, SMALL_BUFF
            )
            imag_coords.add(label)
        tuple_label = self.example_tuple_label
        new_label = OldTex("2+i")
        new_label.add_background_rectangle()
        new_label.next_to(
            self.example_dot,
            DOWN+RIGHT, buff = 0,
        )

        self.play(Write(imag_coords))
        self.wait()
        self.play(FadeOut(tuple_label))
        self.play(FadeIn(new_label))
        self.wait(2)

        self.example_label = new_label
        self.plane.coordinate_labels.add(*imag_coords)

    def mention_squaring_it(self):
        morty = self.pi_creature
        arrow = Arrow(
            self.plane.coords_to_point(2, 1),
            self.plane.coords_to_point(3, 4),
            path_arc = np.pi/3,
            color = MAROON_B
        )
        square_label = OldTex("z \\to z^2")
        square_label.set_color(arrow.get_color())
        square_label.add_background_rectangle()
        square_label.next_to(
            arrow.point_from_proportion(0.5), 
            RIGHT, buff = SMALL_BUFF
        )

        self.play(FadeIn(morty))
        self.play(
            PiCreatureSays(
                morty, "Try squaring \\\\ it!",
                target_mode = "hooray",
                bubble_config = {"width" : 4, "height" : 3},
            )
        )
        self.play(
            ShowCreation(arrow),
            Write(square_label)
        )
        self.wait()
        self.play(RemovePiCreatureBubble(
            morty, target_mode = "pondering",
            look_at = self.example_label
        ))

    def work_out_square_algebraically(self):
        rect = Rectangle(
            height = 3.5, width = 6.5,
            stroke_width = 0,
            fill_color = BLACK,
            fill_opacity = 0.8
        )
        rect.to_corner(UP+LEFT, buff = 0)
        top_line = OldTex("(2+i)", "(2+i)")
        top_line.next_to(rect.get_top(), DOWN)
        second_line = OldTex(
            "2^2 + 2i + 2i + i^2"
        )
        second_line.next_to(top_line, DOWN, MED_LARGE_BUFF)
        final_line = OldTex("3 + 4i")
        final_line.next_to(second_line, DOWN, MED_LARGE_BUFF)

        result_dot = Dot(
            self.plane.coords_to_point(3, 4),
            color = MAROON_B,
            radius = self.dot_radius
        )

        self.play(
            FadeIn(rect),
            ReplacementTransform(
                VGroup(self.example_label[1].copy()),
                top_line
            ),
            run_time = 2
        )
        self.wait()

        #From top line to second line
        index_alignment_lists = [
            [(0, 1, 0), (1, 1, 1)],
            [(0, 2, 2), (0, 1, 3), (1, 3, 4)],
            [(0, 2, 5), (1, 1, 6), (0, 3, 7)],
            [(0, 2, 8), (0, 3, 9), (1, 3, 10)],
        ]
        for index_alignment in index_alignment_lists:
            self.play(*[
                ReplacementTransform(
                    top_line[i][j].copy(), second_line[k],
                )
                for i, j, k in index_alignment
            ])
        self.wait(2)

        #From second line to final line
        index_alignment_lists = [
            [(0, 0), (1, 0), (9, 0), (10, 0)],
            [(2, 1), (3, 2), (4, 3), (6, 2), (7, 3)],
        ]
        for index_alignment in index_alignment_lists:
            self.play(*[
                ReplacementTransform(
                    second_line[i].copy(), final_line[j],
                    run_time = 1.5
                )
                for i, j in index_alignment
            ])
            self.wait()

        #Move result to appropriate place
        result_label = final_line.copy()
        result_label.add_background_rectangle()
        self.play(
            result_label.next_to, result_dot, UP+RIGHT, SMALL_BUFF,
            Animation(final_line),
            run_time = 2,
        )
        self.play(DrawBorderThenFill(
            result_dot,
            stroke_width = 4,
            stroke_color = PINK
        ))
        self.wait(2)

    def walk_through_square_geometrically(self):
        line = self.example_line
        dot = self.example_dot
        example_label = self.example_label
        distance_label = self.distance_label

        alt_line = line.copy().set_color(RED)
        arc = Arc(
            angle = line.get_angle(),
            radius = 0.7,
            color = WHITE
        )
        double_arc = Arc(
            angle = 2*line.get_angle(),
            radius = 0.8,
            color = RED,
        )
        theta = OldTex("\\theta")
        two_theta = OldTex("2\\theta")
        for tex_mob, arc_mob in (theta, arc), (two_theta, double_arc):
            tex_mob.scale(0.75)
            tex_mob.add_background_rectangle()
            point = arc_mob.point_from_proportion(0.5)
            tex_mob.move_to(point)
            tex_mob.shift(tex_mob.get_width()*point/get_norm(point))


        self.play(self.pi_creature.change, "happy", arc)
        self.play(ShowCreation(alt_line))
        self.play(ShowCreation(line))
        self.remove(alt_line)
        self.wait()
        self.play(
            ShowCreation(arc),
            Write(theta)
        )
        self.wait()
        self.play(Indicate(distance_label))
        self.wait()

        #Multiply full plane under everything
        everything = VGroup(*self.get_top_level_mobjects())
        everything.remove(self.plane)
        self.plane.save_state()
        ghost_plane = self.plane.copy().fade()
        method_args_list = [
            (self.plane.rotate, (line.get_angle(),)),
            (self.plane.scale, (np.sqrt(5),)),
            (self.plane.restore, ()),
        ]
        for method, args in method_args_list:
            self.play(
                Animation(ghost_plane),
                ApplyMethod(method, *args),
                Animation(everything),
                run_time = 1.5
            )
            self.wait()

        #Multiply number by itself
        ghost_arc = arc.copy().fade()
        ghost_line = line.copy().fade()
        ghots_dot = dot.copy().fade()
        self.add(ghost_arc, ghost_line, ghots_dot)

        self.play(
            VGroup(
                line, dot, distance_label,
            ).rotate, line.get_angle(),
            Transform(arc, double_arc),
            Transform(theta, two_theta),
        )
        self.wait()
        five = distance_label[2]
        distance_label.remove(five)
        for mob in five, line, dot:
            mob.generate_target()
        line.target.scale(np.sqrt(5))
        five.target.shift(line.target.get_center()-line.get_center())
        dot.target.move_to(line.target.get_end())
        self.play(
            FadeOut(distance_label),
            *list(map(MoveToTarget, [five, line, dot])),
            run_time = 2
        )
        self.wait(2)

    ####

    def get_all_plane_dots(self):
        x_min, y_min = list(map(int, self.plane.point_to_coords(
            FRAME_X_RADIUS*LEFT + FRAME_Y_RADIUS*DOWN
        )))
        x_max, y_max = list(map(int, self.plane.point_to_coords(
            FRAME_X_RADIUS*RIGHT + FRAME_Y_RADIUS*UP
        )))
        result = VGroup(*[
            Dot(
                self.plane.coords_to_point(x, y),
                radius = self.dot_radius,
                color = self.dot_color,
            )
            for x in range(int(x_min), int(x_max)+1)
            for y in range(int(y_min), int(y_max)+1)
        ])
        result.sort(lambda p : np.dot(p, UP+RIGHT))
        return result

    def create_pi_creature(self):
        morty = Mortimer().flip()
        morty.to_corner(DOWN+LEFT, buff = MED_SMALL_BUFF)
        return morty
