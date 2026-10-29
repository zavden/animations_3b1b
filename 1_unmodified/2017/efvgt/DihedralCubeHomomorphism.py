# ==============================================================================
# Scene:      DihedralCubeHomomorphism
# Source:     videos/_2017/efvgt.py (lines 2738-2804)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DihedralCubeHomomorphism.py DihedralCubeHomomorphism -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SymmetriesOfSquare(ThreeDScene):
    CONFIG = {
        "square_config" : {
            "side_length" : 2,
            "stroke_width" : 0,
            "fill_color" : BLUE,
            "fill_opacity" : 0.75,
        },
        "dashed_line_config" : {},
    }
    def construct(self):
        self.add_title()
        self.ask_about_square_symmetry()
        self.talk_through_90_degree_rotation()
        self.talk_through_vertical_flip()
        self.confused_by_lack_of_labels()
        self.add_labels()
        self.show_full_group()
        self.show_top_actions()
        self.show_bottom_actions()
        self.name_dihedral_group()

    def add_title(self):
        title = OldTexText("Groups", "$\\leftrightarrow$", "Symmetry")
        title.to_edge(UP)

        for index in 0, 2:
            self.play(Write(title[index], run_time = 1))
        self.play(GrowFromCenter(title[1]))
        self.wait()

        self.title = title

    def ask_about_square_symmetry(self):
        brace = Brace(self.title[-1])
        q_marks = brace.get_text("???")

        self.square = Square(**self.square_config)

        self.play(DrawBorderThenFill(self.square))
        self.play(GrowFromCenter(brace), Write(q_marks))
        self.rotate_square()
        self.wait()
        for axis in UP, UP+RIGHT:
            self.flip_square(axis)
            self.wait()
        self.rotate_square(-np.pi)
        self.wait()
        self.play(*list(map(FadeOut, [brace, q_marks])))

    def talk_through_90_degree_rotation(self):
        arcs = self.get_rotation_arcs(self.square, np.pi/2)

        self.play(*list(map(ShowCreation, arcs)))
        self.wait()
        self.rotate_square(np.pi/2, run_time = 2)
        self.wait()
        self.play(FadeOut(arcs))
        self.wait()

    def talk_through_vertical_flip(self):
        self.flip_square(UP, run_time = 2)
        self.wait()

    def confused_by_lack_of_labels(self):
        randy = Randolph(mode = "confused")
        randy.next_to(self.square, LEFT, buff = LARGE_BUFF)
        randy.to_edge(DOWN)
        self.play(FadeIn(randy))
        for axis in OUT, RIGHT, UP:
            self.rotate_square(
                angle = np.pi, axis = axis,
                added_anims = [randy.look_at, self.square.get_points()[0]]
            )
        self.play(Blink(randy))
        self.wait()

        self.randy = randy

    def add_labels(self):
        self.add_randy_to_square(self.square)

        self.play(
            FadeIn(self.square.randy),
            self.randy.change_mode, "happy",
            self.randy.look_at, self.square.randy.eyes
        )
        self.play(Blink(self.randy))
        self.play(FadeOut(self.randy))

        self.wait()

    def show_full_group(self):
        new_title = OldTexText("Group", "of", "symmetries")
        new_title.move_to(self.title)

        all_squares = VGroup(*[
            self.square.copy().scale(0.5)
            for x in range(8)
        ])
        all_squares.arrange(RIGHT, buff = LARGE_BUFF)

        top_squares = VGroup(*all_squares[:4])
        bottom_squares = VGroup(*all_squares[4:])
        bottom_squares.next_to(top_squares, DOWN, buff = LARGE_BUFF)

        all_squares.set_width(FRAME_WIDTH-2*LARGE_BUFF)
        all_squares.center()
        all_squares.to_edge(DOWN, buff = LARGE_BUFF)

        self.play(ReplacementTransform(self.square, all_squares[0]))
        self.play(ReplacementTransform(self.title, new_title))
        self.title = new_title
        self.play(*[
            ApplyMethod(mob.set_color, GREY)
            for mob in self.title[1:]
        ])

        for square, angle in zip(all_squares[1:4], [np.pi/2, np.pi, -np.pi/2]):
            arcs = self.get_rotation_arcs(square, angle, MED_SMALL_BUFF)
            self.play(*list(map(FadeIn, [square, arcs])))
            square.rotation_kwargs = {"angle" : angle}
            self.rotate_square(square = square, **square.rotation_kwargs)
            square.add(arcs)

        for square, axis in zip(bottom_squares, [RIGHT, RIGHT+UP, UP, UP+LEFT]):
            axis_line = self.get_axis_line(square, axis)
            self.play(FadeIn(square))
            self.play(ShowCreation(axis_line))
            square.rotation_kwargs = {"angle" : np.pi, "axis" : axis}
            self.rotate_square(square = square, **square.rotation_kwargs)
            square.add(axis_line)
        self.wait()

        self.all_squares = all_squares

    def show_top_actions(self):
        all_squares = self.all_squares

        self.play(Indicate(all_squares[0]))
        self.wait()

        self.play(*[
            Rotate(
                square,
                rate_func = lambda t : -there_and_back(t),
                run_time = 3,
                about_point = square.get_center(),
                **square.rotation_kwargs
            )
            for square in all_squares[1:4]
        ])
        self.wait()

    def show_bottom_actions(self):
        for square in self.all_squares[4:]:
            self.rotate_square(
                square = square,
                rate_func = there_and_back,
                run_time = 2,
                **square.rotation_kwargs
            )
        self.wait()

    def name_dihedral_group(self):
        new_title = OldTexText(
            "``Dihedral group'' of order 8"
        )
        new_title.to_edge(UP)

        self.play(FadeOut(self.title))
        self.play(FadeIn(new_title))
        self.wait()

    ##########

    def rotate_square(
        self, 
        angle = np.pi/2, 
        axis = OUT, 
        square = None, 
        show_axis = False,
        added_anims = None,
        **kwargs
        ):
        if square is None:
            assert hasattr(self, "square")
            square = self.square
        added_anims = added_anims or []
        rotation = Rotate(
            square, 
            angle = angle, 
            axis = axis, 
            about_point = square.get_center(),
            **kwargs
        )
        if hasattr(square, "labels"):
            for label in rotation.target_mobject.labels:
                label.rotate(-angle, axis)

        if show_axis:
            axis_line = self.get_axis_line(square, axis)
            self.play(
                ShowCreation(axis_line),
                Animation(square)
            )
        self.play(rotation, *added_anims)
        if show_axis:
            self.play(
                FadeOut(axis_line),
                Animation(square)
            )

    def flip_square(self, axis = UP, **kwargs):
        self.rotate_square(
            angle = np.pi, 
            axis = axis,
            show_axis = True,
            **kwargs
        )

    def get_rotation_arcs(self, square, angle, angle_buff = SMALL_BUFF):
        square_radius = get_norm(
            square.get_points()[0] - square.get_center()
        )
        arc = Arc(
            radius = square_radius + SMALL_BUFF,
            start_angle = np.pi/4 + np.sign(angle)*angle_buff,
            angle = angle - np.sign(angle)*2*angle_buff,
            color = YELLOW
        )
        arc.add_tip()
        if abs(angle) < 3*np.pi/4:
            angle_multiple_range = list(range(1, 4))
        else:
            angle_multiple_range = [2]
        arcs = VGroup(arc, *[
            arc.copy().rotate(i*np.pi/2)
            for i in angle_multiple_range
        ])
        arcs.move_to(square[0])

        return arcs

    def get_axis_line(self, square, axis):
        axis_line = DashedLine(2*axis, -2*axis, **self.dashed_line_config)
        axis_line.replace(square, dim_to_match = np.argmax(np.abs(axis)))
        axis_line.scale(1.2)
        return axis_line

    def add_labels_and_dots(self, square):
        labels = VGroup()
        dots = VGroup()
        for tex, vertex in zip("ABCD", square.get_anchors()):
            label = OldTex(tex)
            label.add_background_rectangle()
            label.next_to(vertex, vertex-square.get_center(), SMALL_BUFF)
            labels.add(label)
            dot = Dot(vertex, color = WHITE)
            dots.add(dot)
        square.add(labels, dots)
        square.labels = labels
        square.dots = dots

    def add_randy_to_square(self, square, mode = "pondering"):
        randy = Randolph(mode = mode)
        randy.set_height(0.75*square.get_height())
        randy.move_to(square)
        square.add(randy)
        square.randy = randy


class GroupOfCubeSymmetries(ThreeDScene):
    CONFIG = {
        "cube_opacity" : 0.5,
        "cube_colors" : [BLUE],
        "put_randy_on_cube" : True,
    }
    def construct(self):
        title = OldTexText("Group of cube symmetries")
        title.to_edge(UP)
        self.add(title)

        cube = self.get_cube()

        face_centers = [face.get_center() for face in cube[0:7:2]]
        angle_axis_pairs = list(zip(3*[np.pi/2], face_centers))
        for i in range(3):
            ones = np.ones(3)
            ones[i] = -1
            axis = np.dot(ones, face_centers)
            angle_axis_pairs.append((2*np.pi/3, axis))

        for angle, axis in angle_axis_pairs:
            self.play(Rotate(
                cube, angle = angle, axis = axis,
                run_time = 2
            ))
            self.wait()

    def get_cube(self):
        cube = Cube(fill_opacity = self.cube_opacity)
        cube.set_color_by_gradient(*self.cube_colors)
        if self.put_randy_on_cube:
            randy = Randolph(mode = "pondering")
            # randy.pupils.shift(0.01*OUT)
            # randy.add(randy.pupils.copy().shift(0.02*IN))
            # for submob in randy.get_family():
            #     submob.part_of_three_d_mobject = True
            randy.scale(0.5)
            face = cube[1]
            randy.move_to(face)
            face.add(randy)
        pose_matrix = self.get_pose_matrix()
        cube.apply_function(
            lambda p : np.dot(p, pose_matrix.T),
            maintain_smoothness = False
        )
        return cube

    def get_pose_matrix(self):
        return np.dot(
            rotation_matrix(np.pi/8, UP),
            rotation_matrix(np.pi/24, RIGHT)
        )


class DihedralCubeHomomorphism(GroupOfCubeSymmetries, SymmetriesOfSquare):
    def construct(self):
        angle_axis_pairs = [
            (np.pi/2, OUT),
            (np.pi, RIGHT),
            (np.pi, OUT),
            (np.pi, UP+RIGHT),
            (-np.pi/2, OUT),
            (np.pi, UP+LEFT),
        ]
        angle_axis_pairs *= 3

        title = OldTexText(
            "``", "Homo", "morph", "ism", "''", 
            arg_separator = ""
        )
        homo_brace = Brace(title[1], UP, buff = SMALL_BUFF)
        homo_def = homo_brace.get_text("same")
        morph_brace = Brace(title[2], UP, buff = SMALL_BUFF)
        morph_def = morph_brace.get_text("shape", buff = SMALL_BUFF)
        def_group = VGroup(
            homo_brace, homo_def, 
            morph_brace, morph_def
        )
        VGroup(title, def_group).to_edge(UP)
        homo_group = VGroup(title[1], homo_brace, homo_def)
        morph_group = VGroup(title[2], morph_brace, morph_def)

        equation = OldTex("f(X \\circ Y) = f(X) \\circ f(Y)")
        equation.next_to(title, DOWN)

        self.add(title, equation)

        arrow = Arrow(LEFT, RIGHT)
        cube = self.get_cube()
        cube.next_to(arrow, RIGHT)
        pose_matrix = self.get_pose_matrix()

        square = self.square = Square(**self.square_config)
        self.add_randy_to_square(square)
        square.next_to(arrow, LEFT)

        VGroup(square, arrow, cube).next_to(
            equation, DOWN, buff = MED_LARGE_BUFF
        )

        self.add(square, cube)
        self.play(ShowCreation(arrow))
        for i, (angle, raw_axis) in enumerate(angle_axis_pairs):
            posed_axis = np.dot(raw_axis, pose_matrix.T)
            self.play(*[
                Rotate(
                    mob, angle = angle, axis = axis, 
                    in_place = True,
                    run_time = abs(angle/(np.pi/2))
                )
                for mob, axis in [(square, raw_axis), (cube, posed_axis)]
            ])
            self.wait()
            if i == 2:
                for group, color in (homo_group, YELLOW), (morph_group, BLUE):
                    part, remainder = group[0], VGroup(*group[1:])
                    remainder.set_color(color)
                    self.play(
                        part.set_color, color,
                        FadeIn(remainder)
                    )
