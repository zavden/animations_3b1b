# ==============================================================================
# Scene:      DihedralGroupStructure
# Source:     videos/_2017/efvgt.py (lines 1033-1155)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DihedralGroupStructure.py DihedralGroupStructure -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def normalize(vect):
    norm = get_norm(vect)
    if norm == 0:
        return OUT
    else:
        return vect/norm


def get_composite_rotation_angle_and_axis(angles, axes):
    angle1, axis1 = 0, OUT
    for angle2, axis2 in zip(angles, axes):
        ## Figure out what (angle3, axis3) is the same 
        ## as first applying (angle1, axis1), then (angle2, axis2)
        axis2 = normalize(axis2)
        dot = np.dot(axis2, axis1)
        cross = np.cross(axis2, axis1)
        angle3 = 2*np.arccos(
            np.cos(angle2/2)*np.cos(angle1/2) - \
            np.sin(angle2/2)*np.sin(angle1/2)*dot
        )
        axis3 = (
            np.sin(angle2/2)*np.cos(angle1/2)*axis2 + \
            np.cos(angle2/2)*np.sin(angle1/2)*axis1 + \
            np.sin(angle2/2)*np.sin(angle1/2)*cross
        )
        axis3 = normalize(axis3)
        angle1, axis1 = angle3, axis3

    if angle1 > np.pi:
        angle1 -= 2*np.pi
    return angle1, axis1


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


class DihedralGroupStructure(SymmetriesOfSquare):
    CONFIG = {
        "dashed_line_config" : {
            "dash_length" : 0.1
        },
        "filed_sum_scale_factor" : 0.4,
        "num_rows" : 5,
    }
    def construct(self):
        angle_axis_pairs = [
            (np.pi/2, OUT),
            (np.pi, OUT),
            (-np.pi/2, OUT),
            # (np.pi, RIGHT),
            # (np.pi, UP+RIGHT),
            (np.pi, UP),
            (np.pi, UP+LEFT),
        ]
        pair_pairs = list(it.product(*[angle_axis_pairs]*2))
        random.shuffle(pair_pairs)
        for pair_pair in pair_pairs[:4]:
            sum_expression = self.demonstrate_sum(pair_pair)
            self.file_away_sum(sum_expression)
        for pair_pair in pair_pairs[4:]:
            should_skip_animations = self.skip_animations
            self.skip_animations = True
            sum_expression = self.demonstrate_sum(pair_pair)
            self.file_away_sum(sum_expression)
            self.skip_animations = should_skip_animations
            self.play(FadeIn(sum_expression))
        self.wait(3)


    def demonstrate_sum(self, angle_axis_pairs):
        angle_axis_pairs = list(angle_axis_pairs) + [
            get_composite_rotation_angle_and_axis(
                *list(zip(*angle_axis_pairs))
            )
        ]

        prototype_square = Square(**self.square_config)
        prototype_square.flip(RIGHT)
        self.add_randy_to_square(prototype_square)

        # self.add_labels_and_dots(prototype_square)
        prototype_square.scale(0.7)
        expression = s1, plus, s2, equals, s3 = VGroup(
            prototype_square, OldTex("+").scale(2), 
            prototype_square.copy(), OldTex("=").scale(2),
            prototype_square.copy()
        )

        final_expression = VGroup()
        for square, (angle, axis) in zip([s1, s2, s3], angle_axis_pairs):
            if np.cos(angle) > 0.5:
                square.action_illustration = VectorizedPoint()
            elif np.argmax(np.abs(axis)) == 2: ##Axis is in z direction
                square.action_illustration = self.get_rotation_arcs(
                    square, angle
                )
            else:
                square.action_illustration = self.get_axis_line(
                    square, axis
                )
            square.add(square.action_illustration)
            final_expression.add(square.action_illustration)
            square.rotation_kwargs = {
                "square" : square,
                "angle" : angle,
                "axis" : axis,
            }
        expression.arrange()
        expression.set_width(FRAME_X_RADIUS+1)
        expression.to_edge(RIGHT, buff = SMALL_BUFF)
        for square in s1, s2, s3:
            square.remove(square.action_illustration)

        self.play(FadeIn(s1))
        self.play(*list(map(ShowCreation, s1.action_illustration)))
        self.rotate_square(**s1.rotation_kwargs)

        s1_copy = s1.copy()
        self.play(
            # FadeIn(s2),
            s1_copy.move_to, s2,
            Write(plus)
        )
        Transform(s2, s1_copy).update(1)
        self.remove(s1_copy)
        self.add(s2)
        self.play(*list(map(ShowCreation, s2.action_illustration)))
        self.rotate_square(**s2.rotation_kwargs)

        self.play(
            Write(equals),
            FadeIn(s3)
        )
        self.play(*list(map(ShowCreation, s3.action_illustration)))
        self.rotate_square(**s3.rotation_kwargs)
        self.wait()
        final_expression.add(*expression)

        return final_expression

    def file_away_sum(self, sum_expression):
        if not hasattr(self, "num_sum_expressions"):
            self.num_sum_expressions = 0
        target = sum_expression.copy()
        target.scale(self.filed_sum_scale_factor)
        y_index = self.num_sum_expressions%self.num_rows
        y_prop = float(y_index)/(self.num_rows-1)
        y = interpolate(FRAME_Y_RADIUS-LARGE_BUFF, -FRAME_Y_RADIUS+LARGE_BUFF, y_prop)
        x_index = self.num_sum_expressions//self.num_rows
        x_spacing = FRAME_WIDTH/3
        x = (x_index-1)*x_spacing

        target.move_to(x*RIGHT + y*UP)

        self.play(Transform(sum_expression, target))
        self.wait()

        self.num_sum_expressions += 1
        self.last_sum_expression = sum_expression
