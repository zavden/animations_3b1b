# ==============================================================================
# Scene:      IntroduceTriples
# Source:     videos/_2017/triples.py (lines 20-121)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IntroduceTriples.py IntroduceTriples -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

A_COLOR = BLUE


B_COLOR = GREEN


C_COLOR = YELLOW


SIDE_COLORS = [A_COLOR, B_COLOR, C_COLOR]


class IntroduceTriples(TeacherStudentsScene):
    def construct(self):
        title = OldTex("a", "^2", "+", "b", "^2", "=", "c", "^2")
        for color, char in zip(SIDE_COLORS, "abc"):
            title.set_color_by_tex(char, color)
        title.to_corner(UP + RIGHT)

        triples = [
            (3, 4, 5), 
            (5, 12, 13),
            (8, 15, 17),
            (7, 24, 25),
        ]

        self.add(title)
        for a, b, c in triples:
            triangle = Polygon(
                ORIGIN, a*RIGHT, a*RIGHT+b*UP,
                stroke_width = 0,
                fill_color = WHITE,
                fill_opacity = 0.5
            )
            hyp_line = Line(ORIGIN, a*RIGHT+b*UP)
            elbow = VMobject()
            elbow.set_points_as_corners([LEFT, LEFT+UP, UP])
            elbow.set_width(0.2*triangle.get_width())
            elbow.move_to(triangle, DOWN+RIGHT)
            triangle.add(elbow)

            square = Square(side_length = 1)
            square_groups = VGroup()
            for n, color in zip([a, b, c], SIDE_COLORS):
                square_group = VGroup(*[
                    square.copy().shift(x*RIGHT + y*UP)
                    for x in range(n)
                    for y in range(n)
                ])
                square_group.set_stroke(color, width = 3)
                square_group.set_fill(color, opacity = 0.5)
                square_groups.add(square_group)
            a_square, b_square, c_square = square_groups
            a_square.move_to(triangle.get_bottom(), UP)
            b_square.move_to(triangle.get_right(), LEFT)
            c_square.move_to(hyp_line.get_center(), DOWN)
            c_square.rotate(
                hyp_line.get_angle(),
                about_point = hyp_line.get_center()
            )
            if c in [5, 13, 25]:
                if c == 5:
                    keys = list(range(0, 5, 2))
                elif c == 13:
                    keys = list(range(0, 13, 3))
                elif c == 25:
                    keys = list(range(0, 25, 4))
                i_list = [i for i in range(c**2) if (i%c) in keys and (i//c) in keys]
            else:
                i_list = list(range(a**2))
            not_i_list = list(filter(
                lambda i : i not in i_list,
                list(range(c**2)),
            ))
            c_square_parts = [
                VGroup(*[c_square[i] for i in i_list]),
                VGroup(*[c_square[i] for i in not_i_list]),
            ]
            full_group = VGroup(triangle, square_groups)
            full_group.set_height(4)
            full_group.center()
            full_group.to_edge(UP)

            equation = OldTex(
                str(a), "^2", "+", str(b), "^2", "=", str(c), "^2"
            )
            for num, color in zip([a, b, c], SIDE_COLORS):
                equation.set_color_by_tex(str(num), color)
            equation.next_to(title, DOWN, MED_LARGE_BUFF)
            equation.shift_onto_screen()
            
            self.play(
                FadeIn(triangle),
                self.teacher.change_mode, "raise_right_hand"
            )
            self.play(LaggedStartMap(FadeIn, a_square))
            self.play_student_changes(
                *["pondering"]*3,
                look_at = triangle,
                added_anims = [LaggedStartMap(FadeIn, b_square)]
            )
            self.play(self.teacher.change_mode, "happy")
            for start, target in zip([a_square, b_square], c_square_parts):
                mover = start.copy().set_fill(opacity = 0)
                target.set_color(start.get_color())
                self.play(ReplacementTransform(
                    mover, target,
                    run_time = 2,
                    path_arc = np.pi/2
                ))
            self.play(Write(equation))
            self.play(c_square.set_color, C_COLOR)
            self.wait()
            self.play(*list(map(FadeOut, [full_group, equation])))
