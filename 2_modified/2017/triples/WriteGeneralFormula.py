# ==============================================================================
# Scene:      WriteGeneralFormula
# Source:     videos/_2017/triples.py (lines 1323-1515)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WriteGeneralFormula.py WriteGeneralFormula -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - complex_string is not importable here: str(z) without the parentheses (what the 3feb helper returned)
# ==============================================================================

from manim_imports_ext import *

U_COLOR = GREEN


V_COLOR = RED


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


class WriteGeneralFormula(GeneralExample):
    CONFIG = {
        "plane_center" : 2*RIGHT,
        "x_label_range" : [],
        "y_label_range" : [],
        "unit_size" : 0.7,
        "number" : complex(2, 1),
    }
    def construct(self):
        self.add_plane()
        self.show_squaring()
        self.expand_square()
        self.draw_triangle()
        self.show_uv_to_triples()

    def show_squaring(self):
        self.force_skipping()
        self.square_point()
        dot = self.example_dot
        old_label = self.example_label
        line = self.example_line
        square_dot = self.square_dot
        old_square_label = self.square_label
        square_line = self.square_line
        z_to_z_squared = self.z_to_z_squared
        arrow = self.z_to_z_squared_arrow
        result_length_label = self.result_length_label
        self.clear()
        self.add(self.plane, self.plane.coordinate_labels)
        self.revert_to_original_skipping_status()

        label = OldTex("u+vi")
        label.move_to(old_label, LEFT)
        label.add_background_rectangle()
        square_label = OldTex("(u+vi)^2")
        square_label.move_to(old_square_label, LEFT)
        square_label.add_background_rectangle()

        self.add(label, dot, line)
        self.play(
            ShowCreation(arrow),
            FadeIn(z_to_z_squared)
        )
        self.play(*[
            ReplacementTransform(
                start.copy(), target,
                run_time = 1.5,
                path_arc = np.pi/2
            )
            for start, target in [
                (dot, square_dot),
                (line, square_line),
                (label, square_label),
            ]
        ])

        self.example_label = label
        self.square_label = square_label

    def expand_square(self):
        rect = Rectangle(
            height = 2.5, width = 7,
            stroke_width = 0,
            fill_color = BLACK,
            fill_opacity = 0.8,
        )
        rect.to_corner(UP+LEFT, buff = 0)
        top_line = OldTex("(u+vi)(u+vi)")
        for i in 1, 7:
            top_line[i].set_color(U_COLOR)
            top_line[i+2].set_color(V_COLOR)
        top_line.next_to(rect.get_top(), DOWN)
        second_line = OldTex(
            "\\big(", "u^2 - v^2", "\\big)", "+",
            "\\big(", "2uv", "\\big)", "i"
        )
        for i, j in (1, 0), (5, 1):
            second_line[i][j].set_color(U_COLOR)
        for i, j in (1, 3), (5, 2):
            second_line[i][j].set_color(V_COLOR)
        second_line.next_to(top_line, DOWN, MED_LARGE_BUFF)
        real_part = second_line[1]
        imag_part = second_line[5]
        for part in real_part, imag_part:
            part.add_to_back(BackgroundRectangle(part))

        z = self.number**2
        square_point = self.plane.number_to_point(z)
        zero_point = self.plane.number_to_point(0)
        real_part_point = self.plane.number_to_point(z.real)
        real_part_line = Line(zero_point, real_part_point)
        imag_part_line = Line(real_part_point, square_point)
        for line in real_part_line, imag_part_line:
            line.set_color(self.square_color)


        self.play(*list(map(FadeIn, [rect, top_line, second_line])))
        self.wait()
        self.play(
            real_part.copy().next_to, real_part_line.copy(), 
                DOWN, SMALL_BUFF,
            ShowCreation(real_part_line)
        )
        self.wait()
        self.play(
            FadeOut(VGroup(
                self.example_label, self.example_dot, self.example_line,
                self.z_to_z_squared, self.z_to_z_squared_arrow
            )),
            imag_part.copy().next_to, imag_part_line.copy(), 
                RIGHT, SMALL_BUFF,
            ShowCreation(imag_part_line)
        )
        self.wait()

        self.corner_rect = rect

    def draw_triangle(self):
        hyp_length = OldTex("u", "^2", "+", "v", "^2")
        hyp_length.set_color_by_tex("u", U_COLOR)
        hyp_length.set_color_by_tex("v", V_COLOR)
        hyp_length.add_background_rectangle()
        line = self.square_line
        hyp_length.next_to(line.get_center(), UP, SMALL_BUFF)
        hyp_length.rotate(
            line.get_angle(),
            about_point = line.get_center()
        )
        triangle = Polygon(
            ORIGIN, RIGHT, RIGHT+UP,
            stroke_width = 0,
            fill_color = MAROON_B,
            fill_opacity = 0.5,
        )
        triangle.replace(line, stretch = True)

        self.play(Write(hyp_length))
        self.wait()
        self.play(FadeIn(triangle))
        self.wait()

    def show_uv_to_triples(self):
        rect = self.corner_rect.copy()
        rect.stretch_to_fit_height(FRAME_HEIGHT)
        rect.move_to(self.corner_rect.get_bottom(), UP)

        h_line = Line(rect.get_left(), rect.get_right())
        h_line.next_to(rect.get_top(), DOWN, LARGE_BUFF)
        v_line = Line(rect.get_top(), rect.get_bottom())
        v_line.shift(1.3*LEFT)
        uv_title = OldTex("(u, v)")
        triple_title = OldTex("(u^2 - v^2, 2uv, u^2 + v^2)")
        uv_title.scale(0.75)
        triple_title.scale(0.75)
        uv_title.next_to(
            h_line.point_from_proportion(1./6), 
            UP, SMALL_BUFF
        )
        triple_title.next_to(
            h_line.point_from_proportion(2./3),
            UP, SMALL_BUFF
        )

        pairs = [(2, 1), (3, 2), (4, 1), (4, 3), (5, 2), (5, 4)]
        pair_mobs = VGroup()
        triple_mobs = VGroup()
        for u, v in pairs:
            a, b, c = u**2 - v**2, 2*u*v, u**2 + v**2
            pair_mob = OldTex("(", str(u), ",", str(v), ")")
            pair_mob.set_color_by_tex(str(u), U_COLOR)
            pair_mob.set_color_by_tex(str(v), V_COLOR)
            triple_mob = OldTex("(%d, %d, %d)"%(a, b, c))
            pair_mobs.add(pair_mob)
            triple_mobs.add(triple_mob)
            pair_mob.scale(0.75)
            triple_mob.scale(0.75)
        pair_mobs.arrange(DOWN)
        pair_mobs.next_to(uv_title, DOWN, MED_LARGE_BUFF)
        triple_mobs.arrange(DOWN)
        triple_mobs.next_to(triple_title, DOWN, MED_LARGE_BUFF)

        self.play(*list(map(FadeIn, [
            rect, h_line, v_line, 
            uv_title, triple_title
        ])))
        self.play(*[
            LaggedStartMap(
                FadeIn, mob, 
                run_time = 5,
                lag_ratio = 0.2
            )
            for mob in (pair_mobs, triple_mobs)
        ])
