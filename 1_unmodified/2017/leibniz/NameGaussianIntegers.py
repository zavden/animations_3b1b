# ==============================================================================
# Scene:      NameGaussianIntegers
# Source:     videos/_2017/leibniz.py (lines 1717-1867)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl NameGaussianIntegers.py NameGaussianIntegers -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class LatticePointScene(Scene):
    CONFIG = {
        "y_radius" : 6,
        "x_radius" : None,
        "plane_center" : ORIGIN,
        "max_lattice_point_radius" : 6,
        "dot_radius" : 0.075,
        "secondary_line_ratio" : 0,
        "plane_color" : BLUE_E,
        "dot_color" : YELLOW,
        "dot_drawing_stroke_color" : PINK,
        "circle_color" : MAROON_D,
        "radial_line_color" : RED,
    }
    def setup(self):
        if self.x_radius is None:
            self.x_radius = self.y_radius*FRAME_X_RADIUS/FRAME_Y_RADIUS
        plane = ComplexPlane(
            y_radius = self.y_radius,
            x_radius = self.x_radius,
            secondary_line_ratio = self.secondary_line_ratio,
            radius = self.plane_color
        )
        plane.set_height(FRAME_HEIGHT)
        plane.shift(self.plane_center)
        self.add(plane)
        self.plane = plane

        self.setup_lattice_points()

    def setup_lattice_points(self):
        M = self.max_lattice_point_radius
        int_range = list(range(-M, M+1))
        self.lattice_points = VGroup()
        for x, y in it.product(*[int_range]*2):
            r_squared = x**2 + y**2
            if r_squared > M**2:
                continue
            dot = Dot(
                self.plane.coords_to_point(x, y),
                color = self.dot_color,
                radius = self.dot_radius,
            )
            dot.r_squared = r_squared
            self.lattice_points.add(dot)
        self.lattice_points.sort(
            lambda p : get_norm(p - self.plane_center)
        )

    def get_circle(self, radius = None, color = None):
        if radius is None:
            radius = self.max_lattice_point_radius
        if color is None:
            color = self.circle_color
        radius *= self.plane.get_space_unit_to_y_unit()
        circle = Circle(
            color = color,
            radius = radius,
        )
        circle.move_to(self.plane.get_center())
        return circle

    def get_radial_line_with_label(self, radius = None, color = None):
        if radius is None:
            radius = self.max_lattice_point_radius
        if color is None:
            color = self.radial_line_color
        radial_line = Line(
            self.plane_center,
            self.plane.coords_to_point(radius, 0),
            color = color
        )
        r_squared = int(np.round(radius**2))
        root_label = OldTex("\\sqrt{%d}"%r_squared)
        root_label.add_background_rectangle()
        root_label.next_to(radial_line, UP, SMALL_BUFF)

        return radial_line, root_label

    def get_lattice_points_on_r_squared_circle(self, r_squared):
        points = VGroup(*[dot for dot in self.lattice_points if dot.r_squared == r_squared])
        points.sort(
            lambda p : angle_of_vector(p-self.plane_center)%(2*np.pi)
        )
        return points

    def draw_lattice_points(self, points = None, run_time = 4):
        if points is None:
            points = self.lattice_points
        self.play(*[
            DrawBorderThenFill(
                dot,
                stroke_width = 4,
                stroke_color = self.dot_drawing_stroke_color,
                run_time = run_time,
                rate_func = squish_rate_func(
                    double_smooth, a, a + 0.25
                ),
            )
            for dot, a in zip(
                points, 
                np.linspace(0, 0.75, len(points))
            )
        ])

    def add_axis_labels(self, spacing = 2):
        x_max = int(self.plane.point_to_coords(FRAME_X_RADIUS*RIGHT)[0])
        y_max = int(self.plane.point_to_coords(FRAME_Y_RADIUS*UP)[1])
        x_range = list(range(spacing, x_max, spacing))
        y_range = list(range(spacing, y_max, spacing))
        for r in x_range, y_range:
            r += [-n for n in r]
        tick = Line(ORIGIN, MED_SMALL_BUFF*UP)
        x_ticks = VGroup(*[
            tick.copy().move_to(self.plane.coords_to_point(x, 0))
            for x in x_range
        ])
        tick.rotate(-np.pi/2)
        y_ticks = VGroup(*[
            tick.copy().move_to(self.plane.coords_to_point(0, y))
            for y in y_range
        ])
        x_labels = VGroup(*[
            OldTex(str(x))
            for x in x_range
        ])
        y_labels = VGroup(*[
            OldTex(str(y) + "i")
            for y in y_range
        ])

        for labels, ticks in (x_labels, x_ticks), (y_labels, y_ticks):
            labels.scale(0.6)
            for tex_mob, tick in zip(labels, ticks):
                tex_mob.add_background_rectangle()
                tex_mob.next_to(
                    tick,
                    tick.get_start() - tick.get_end(),
                    SMALL_BUFF
                )
        self.add(x_ticks, y_ticks, x_labels, y_labels)
        digest_locals(self, [
            "x_ticks", "y_ticks",
            "x_labels", "y_labels",
        ])

    def point_to_int_coords(self, point):
        x, y = self.plane.point_to_coords(point)[:2]
        return (int(np.round(x)), int(np.round(y)))

    def dot_to_int_coords(self, dot):
        return self.point_to_int_coords(dot.get_center())


class NameGaussianIntegers(LatticePointScene):
    CONFIG = {
        "max_lattice_point_radius" : 15,
        "dot_radius" : 0.05,
        "plane_center" : 2*LEFT,
        "x_radius" : 15,
    }
    def construct(self):
        self.add_axis_labels()
        self.add_a_plus_bi()
        self.draw_lattice_points()
        self.add_name()
        self.restrict_to_one_circle()
        self.show_question_algebraically()

    def add_a_plus_bi(self):
        label = OldTex(
            "a", "+", "b", "i"
        )
        a = label.get_part_by_tex("a")
        b = label.get_part_by_tex("b")
        a.set_color(GREEN)
        b.set_color(RED)
        label.add_background_rectangle()
        label.to_corner(UP+RIGHT)
        integers = OldTexText("Integers")
        integers.next_to(label, DOWN, LARGE_BUFF)
        integers.add_background_rectangle()
        arrows = VGroup(*[
            Arrow(integers.get_top(), mob, tip_length = 0.15)
            for mob in (a, b)
        ])
        self.add_foreground_mobjects(label, integers, arrows)

        self.a_plus_bi = label
        self.integers_label = VGroup(integers, arrows)

    def add_name(self):
        gauss_name = OldTexText(
            "Carl Friedrich Gauss"
        )
        gauss_name.add_background_rectangle()
        gauss_name.next_to(ORIGIN, UP, MED_LARGE_BUFF)
        gauss_name.to_edge(LEFT)

        gaussian_integers = OldTexText("``Gaussian integers'': ")
        gaussian_integers.scale(0.9)
        gaussian_integers.next_to(self.a_plus_bi, LEFT)
        gaussian_integers.add_background_rectangle()

        self.play(FadeIn(gaussian_integers))
        self.add_foreground_mobject(gaussian_integers)
        self.play(FadeIn(
            gauss_name,
            run_time = 2,
            lag_ratio = 0.5
        ))
        self.wait(3)
        self.play(FadeOut(gauss_name))

        self.gaussian_integers = gaussian_integers

    def restrict_to_one_circle(self):
        dots = self.get_lattice_points_on_r_squared_circle(25).copy()
        for dot in dots:
            dot.scale(2)
        circle = self.get_circle(5)
        radius, root_label = self.get_radial_line_with_label(5)

        self.play(
            FadeOut(self.lattice_points),
            ShowCreation(circle),
            Rotating(
                radius, 
                run_time = 1, rate_func = smooth,
                about_point = self.plane_center
            ),
            *list(map(GrowFromCenter, dots))
        )
        self.play(Write(root_label))
        self.wait()

        self.circle_dots = dots

    def show_question_algebraically(self):
        for i, dot in enumerate(self.circle_dots):
            x, y = self.dot_to_int_coords(dot)
            x_str = str(x)
            y_str = str(y) if y >= 0 else "(%d)"%y
            label = OldTex(x_str, "+", y_str, "i")
            label.scale(0.8)
            label.next_to(
                dot, 
                dot.get_center()-self.plane_center + SMALL_BUFF*(UP+RIGHT),
                buff = 0,
            )
            label.add_background_rectangle()
            dot.label = label

            equation = OldTex(
                "25 = "
                "(", x_str, "+", y_str, "i", ")",
                "(", x_str, "-", y_str, "i", ")",
            )
            equation.scale(0.9)
            equation.add_background_rectangle()
            equation.to_corner(UP + RIGHT)
            dot.equation = equation

            for mob in label, equation:
                mob.set_color_by_tex(x_str, GREEN, substring = False)
                mob.set_color_by_tex(y_str, RED, substring = False)

            dot.line_pair = VGroup(*[
                Line(
                    self.plane_center,
                    self.plane.coords_to_point(x, u*y),
                    color = PINK,
                )
                for u in (1, -1)
            ])
            dot.conjugate_dot = self.circle_dots[-i]

        self.play(*list(map(FadeOut, [
            self.a_plus_bi, self.integers_label,
            self.gaussian_integers,
        ])))

        last_dot = None
        for dot in self.circle_dots:
            anims = [
                dot.set_color, PINK,
                dot.conjugate_dot.set_color, PINK,
            ]
            if last_dot is None:
                anims += [
                    FadeIn(dot.equation),
                    FadeIn(dot.label),
                ]
                anims += list(map(ShowCreation, dot.line_pair))
            else:
                anims += [
                    last_dot.set_color, self.dot_color,
                    last_dot.conjugate_dot.set_color, self.dot_color,
                    ReplacementTransform(last_dot.equation, dot.equation),
                    ReplacementTransform(last_dot.label, dot.label),
                    ReplacementTransform(last_dot.line_pair, dot.line_pair),
                ]
            self.play(*anims)
            self.wait()
            last_dot = dot
