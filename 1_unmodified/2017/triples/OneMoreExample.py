# ==============================================================================
# Scene:      OneMoreExample
# Source:     videos/_2017/triples.py (lines 959-1176)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl OneMoreExample.py OneMoreExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

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
