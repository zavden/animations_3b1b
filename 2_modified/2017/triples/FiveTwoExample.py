# ==============================================================================
# Scene:      FiveTwoExample
# Source:     videos/_2017/triples.py (lines 1315-1321)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FiveTwoExample.py FiveTwoExample -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - complex_string is not importable here: str(z) without the parentheses (what the 3feb helper returned)
# ==============================================================================

from manim_imports_ext import *

def complex_string_with_i(z):
    if z.real == 0:
        return str(int(z.imag)) + "i"
    elif z.imag == 0:
        return str(int(z.real))
    # CHANGE: complex_string is not importable here: str(z) without the parentheses (what the 3feb helper returned)
    return "".join(c for c in str(z) if c not in "()").replace("j", "i")


class OneMoreExample(Scene):
    CONFIG = {
        "unit_size" : 0.5,
        "plane_center" : 3*LEFT + 3*DOWN,
        "dot_color" : YELLOW,
        "x_label_range" : list(range(-6, 25, 3)),
        "y_label_range" : list(range(3, 13, 3)),
    }
    def construct(self):
        self.add_plane()
        self.add_point()
        self.square_algebraically()
        self.plot_result()
        self.show_triangle()

    def add_plane(self):
        plane = ComplexPlane(
            unit_size = self.unit_size,
            center_point = self.plane_center,
            stroke_width = 2,
        )
        plane.axes.set_stroke(width = 4)
        coordinate_labels = VGroup()
        for x in self.x_label_range:
            if x == 0:
                continue
            coord = OldTex(str(x))
            coord.scale(0.75)
            coord.next_to(plane.coords_to_point(x, 0), DOWN, SMALL_BUFF)
            coord.add_background_rectangle()
            coordinate_labels.add(coord)
        for y in self.y_label_range:
            if y == 0:
                continue
            coord = OldTex("%di"%y)
            coord.scale(0.75)
            coord.next_to(plane.coords_to_point(0, y), LEFT, SMALL_BUFF)
            coord.add_background_rectangle()
            coordinate_labels.add(coord)
        self.add(plane, coordinate_labels)

        self.plane = plane
        self.plane.coordinate_labels = coordinate_labels

    def add_point(self):
        point = self.plane.coords_to_point(3, 2)
        dot = Dot(point, color = self.dot_color)
        line = Line(self.plane.get_center_point(), point)
        line.set_color(dot.get_color())
        number_label = OldTex("3+2i")
        number_label.add_background_rectangle()
        number_label.next_to(dot, RIGHT, SMALL_BUFF)
        distance_labels = VGroup() 
        for tex in "3^2 + 2^2", "13":
            pre_label = OldTex("\\sqrt{%s}"%tex)
            label = VGroup(
                BackgroundRectangle(pre_label),
                VGroup(*pre_label[:2]),
                VGroup(*pre_label[2:]),
            )
            label.scale(0.75)
            label.next_to(line.get_center(), UP, SMALL_BUFF)
            label.rotate(
                line.get_angle(),
                about_point = line.get_center()
            )
            distance_labels.add(label)

        self.play(
            FadeIn(number_label), 
            ShowCreation(line),
            DrawBorderThenFill(dot)
        )
        self.play(Write(distance_labels[0]))
        self.wait()
        self.play(ReplacementTransform(*distance_labels))
        self.wait()

        self.distance_label = distance_labels[1]
        self.line = line
        self.dot = dot
        self.number_label = number_label

    def square_algebraically(self):
        #Crazy hacky.  To anyone looking at this, for God's
        #sake, don't mimic this.
        rect = Rectangle(
            height = 3.5, width = 7,
            stroke_color = WHITE,
            stroke_width = 2,
            fill_color = BLACK,
            fill_opacity = 0.8
        )
        rect.to_corner(UP+RIGHT, buff = 0)
        number = self.number_label[1].copy()

        top_line = OldTex("(3+2i)", "(3+2i)")
        for part in top_line:
            for i, color in zip([1, 3], [BLUE, YELLOW]):
                part[i].set_color(color)
        second_line = OldTex(
            "\\big( 3^2 + (2i)^2 \\big) + " + \
            "\\big(3 \\cdot 2 + 2 \\cdot 3 \\big)i"
        )
        for i in 1, 12, 18:
            second_line[i].set_color(BLUE)
        for i in 5, 14, 16:
            second_line[i].set_color(YELLOW)
        second_line.scale(0.9)
        final_line = OldTex("5 + 12i")
        for i in 0, 2, 3:
            final_line[i].set_color(GREEN)
        lines = VGroup(top_line, second_line, final_line)
        lines.arrange(DOWN, buff = MED_LARGE_BUFF)
        lines.next_to(rect.get_top(), DOWN)
        minus = OldTex("-").scale(0.9)
        minus.move_to(second_line[3])

        self.play(
            FadeIn(rect),
            Transform(VGroup(number), top_line),
            run_time = 2
        )
        self.wait()

        index_alignment_lists = [
            [(0, 0, 0), (0, 1, 1), (1, 1, 2), (1, 5, 9)],
            [
                (0, 2, 3), (1, 3, 4), (0, 3, 5), 
                (0, 4, 6), (1, 4, 7), (1, 3, 8)
            ],
            [
                (0, 2, 10), (0, 0, 11), (0, 1, 12), 
                (1, 3, 13), (1, 3, 14), (1, 5, 19), 
                (0, 4, 20), (1, 4, 20),
            ],
            [
                (0, 2, 15), (0, 3, 16), 
                (1, 1, 17), (1, 1, 18),
            ],
        ]
        for index_alignment in index_alignment_lists[:2]:
            self.play(*[
                ReplacementTransform(
                    top_line[i][j].copy(), second_line[k],
                    run_time = 1.5
                )
                for i, j, k in index_alignment
            ])
            self.wait()
        self.play(
            Transform(second_line[3], minus),
            FadeOut(VGroup(*[
                second_line[i]
                for i in (4, 6, 7)
            ])),
            second_line[5].shift, 0.35*RIGHT,
        )
        self.play(VGroup(*second_line[:4]).shift, 0.55*RIGHT)
        self.wait()
        for index_alignment in index_alignment_lists[2:]:
            self.play(*[
                ReplacementTransform(
                    top_line[i][j].copy(), second_line[k],
                    run_time = 1.5
                )
                for i, j, k in index_alignment
            ])
            self.wait()
        self.play(FadeIn(final_line))
        self.wait()

        self.final_line = final_line

    def plot_result(self):
        result_label = self.final_line.copy()
        result_label.add_background_rectangle()

        point = self.plane.coords_to_point(5, 12)
        dot = Dot(point, color = GREEN)
        line = Line(self.plane.get_center_point(), point)
        line.set_color(dot.get_color())
        distance_label = OldTex("13")
        distance_label.add_background_rectangle()
        distance_label.next_to(line.get_center(), UP+LEFT, SMALL_BUFF)

        self.play(
            result_label.next_to, dot, UP+LEFT, SMALL_BUFF,
            Animation(self.final_line),
            DrawBorderThenFill(dot)
        )
        self.wait()
        self.play(*[
            ReplacementTransform(m1.copy(), m2)
            for m1, m2 in [
                (self.line, line), 
                (self.distance_label, distance_label)
            ]
        ])
        self.wait()

    def show_triangle(self):
        triangle = Polygon(*[
            self.plane.coords_to_point(x, y)
            for x, y in [(0, 0), (5, 0), (5, 12)]
        ])
        triangle.set_stroke(WHITE, 1)
        triangle.set_fill(BLUE, opacity = 0.75)

        self.play(
            FadeIn(triangle),
            Animation(VGroup(
                self.line, self.dot, 
                self.number_label[1], *self.distance_label[1:]
            )),
            run_time = 2
        )
        self.wait(2)


class GeneralExample(OneMoreExample):
    CONFIG = {
        "number" : complex(4, 1),
        "square_color" : MAROON_B,
        "result_label_vect" : UP+LEFT,
    }
    def construct(self):
        self.add_plane()
        self.square_point()

    def square_point(self):
        z = self.number
        z_point = self.plane.number_to_point(z)
        zero_point = self.plane.number_to_point(0)
        dot = Dot(z_point, color = self.dot_color)
        line = Line(zero_point, z_point)
        line.set_color(dot.get_color())
        label = OldTex(complex_string_with_i(z))
        label.add_background_rectangle()
        label.next_to(dot, RIGHT, SMALL_BUFF)

        square_point = self.plane.number_to_point(z**2)
        square_dot = Dot(square_point, color = self.square_color)
        square_line = Line(zero_point, square_point)
        square_line.set_color(square_dot.get_color())
        square_label = OldTex(complex_string_with_i(z**2))
        square_label.add_background_rectangle()
        square_label.next_to(square_dot, UP+RIGHT, SMALL_BUFF)
        result_length_label = OldTex(str(int(abs(z**2))))
        result_length_label.next_to(
            square_line.get_center(), self.result_label_vect
        )
        result_length_label.add_background_rectangle()

        arrow = Arrow(
            z_point, square_point, 
            # buff = SMALL_BUFF,
            path_arc = np.pi/2
        )
        arrow.set_color(WHITE)
        z_to_z_squared = OldTex("z", "\\to", "z^2")
        z_to_z_squared.set_color_by_tex("z", dot.get_color())
        z_to_z_squared.set_color_by_tex("z^2", square_dot.get_color())
        z_to_z_squared.next_to(
            arrow.point_from_proportion(0.5), 
            RIGHT, MED_SMALL_BUFF
        )
        z_to_z_squared.add_to_back(
            BackgroundRectangle(VGroup(
                z_to_z_squared[2][0],
                *z_to_z_squared[:-1]
            )),
            BackgroundRectangle(z_to_z_squared[2][1])
        )


        self.play(
            Write(label), 
            ShowCreation(line),
            DrawBorderThenFill(dot)
        )
        self.wait()
        self.play(
            ShowCreation(arrow),
            FadeIn(z_to_z_squared),
            Animation(label),
        )
        self.play(*[
            ReplacementTransform(
                start.copy(), target,
                path_arc = np.pi/2,
                run_time = 1.5
            )
            for start, target in [
                (dot, square_dot),
                (line, square_line),
                (label, square_label),
            ]
        ])
        self.wait()
        self.play(Write(result_length_label))
        self.wait()

        self.example_dot = dot
        self.example_label = label
        self.example_line = line
        self.square_dot = square_dot
        self.square_label = square_label
        self.square_line = square_line
        self.z_to_z_squared = z_to_z_squared
        self.z_to_z_squared_arrow = arrow
        self.result_length_label = result_length_label


class FiveTwoExample(GeneralExample):
    CONFIG = {
        "number" : complex(5, 2),
        "unit_size" : 0.25,
        "x_label_range" : list(range(-10, 40, 5)),
        "y_label_range" : list(range(0, 30, 5)),
    }
