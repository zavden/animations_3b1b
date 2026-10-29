# ==============================================================================
# Scene:      CountLatticePoints
# Source:     videos/_2017/leibniz.py (lines 717-900)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CountLatticePoints.py CountLatticePoints -w -m --fps 15
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


class CountLatticePoints(LatticePointScene):
    CONFIG = {
        "y_radius" : 11,
        "max_lattice_point_radius" : 10,
        "dot_radius" : 0.05,
        "example_coords" : (7, 5),
    }
    def construct(self):
        self.introduce_lattice_point()
        self.draw_lattice_points_in_circle()
        self.turn_points_int_units_of_area()
        self.write_pi_R_squared()
        self.allude_to_alternate_counting_method()


    def introduce_lattice_point(self):
        x, y = self.example_coords
        example_dot = Dot(
            self.plane.coords_to_point(x, y),
            color = self.dot_color,
            radius = 1.5*self.dot_radius,
        )
        label = OldTex(str(self.example_coords))
        label.add_background_rectangle()
        label.next_to(example_dot, UP+RIGHT, buff = 0)
        h_line = Line(
            ORIGIN, self.plane.coords_to_point(x, 0),
            color = GREEN
        )
        v_line = Line(
            h_line.get_end(), self.plane.coords_to_point(x, y),
            color = RED
        )
        lines = VGroup(h_line, v_line)

        dots = self.lattice_points.copy()
        random.shuffle(dots.submobjects)

        self.play(*[
            ApplyMethod(
                dot.set_fill, None, 0,
                run_time = 3,
                rate_func = squish_rate_func(
                    lambda t : 1 - there_and_back(t),
                    a, a + 0.5
                ),
                remover = True
            )
            for dot, a in zip(dots, np.linspace(0, 0.5, len(dots)))
        ])
        self.play(
            Write(label),
            ShowCreation(lines),
            DrawBorderThenFill(example_dot),
            run_time = 2,
        )
        self.wait(2)
        self.play(*list(map(FadeOut, [label, lines, example_dot])))

    def draw_lattice_points_in_circle(self):
        circle = self.get_circle()
        radius = Line(ORIGIN, circle.get_right())
        radius.set_color(RED)
        brace = Brace(radius, DOWN, buff = SMALL_BUFF)
        radius_label = brace.get_text(
            str(self.max_lattice_point_radius),
            buff = SMALL_BUFF
        )
        radius_label.add_background_rectangle()
        brace.add(radius_label)

        self.play(
            ShowCreation(circle),
            Rotating(radius, about_point = ORIGIN),
            run_time = 2,
            rate_func = smooth,
        )
        self.play(FadeIn(brace))
        self.add_foreground_mobject(brace)
        self.draw_lattice_points()
        self.wait()
        self.play(*list(map(FadeOut, [brace, radius])))

        self.circle = circle

    def turn_points_int_units_of_area(self):
        square = Square(fill_opacity = 0.9)
        unit_line = Line(
            self.plane.coords_to_point(0, 0),
            self.plane.coords_to_point(1, 0),
        )
        square.set_width(unit_line.get_width())
        squares = VGroup(*[
            square.copy().move_to(point)
            for point in self.lattice_points
        ])
        squares.set_color_by_gradient(BLUE_E, GREEN_E)
        squares.set_stroke(WHITE, 1)
        point_copies = self.lattice_points.copy()

        self.play(
            ReplacementTransform(
                point_copies, squares,
                run_time = 3,
                lag_ratio = 0.5,
            ),
            Animation(self.lattice_points)
        )
        self.wait()
        self.play(FadeOut(squares), Animation(self.lattice_points))

    def write_pi_R_squared(self):
        equations = VGroup(*[
            VGroup(
                OldTexText(
                    "\\# Lattice points\\\\",
                    "within radius ", R,
                    alignment = ""
                ),
                OldTex(
                    "\\approx \\pi", "(", R, ")^2"
                )
            ).arrange(RIGHT)
            for R in ("10", "1{,}000{,}000", "R")
        ])
        radius_10_eq, radius_million_eq, radius_R_eq = equations
        for eq in equations:
            for tex_mob in eq:
                tex_mob.set_color_by_tex("0", BLUE)
        radius_10_eq.to_corner(UP+LEFT)
        radius_million_eq.next_to(radius_10_eq, DOWN, LARGE_BUFF)
        radius_million_eq.to_edge(LEFT)
        brace = Brace(radius_million_eq, DOWN)
        brace.add(brace.get_text("More accurate"))
        brace.set_color(YELLOW)

        background = FullScreenFadeRectangle(opacity = 0.9)

        self.play(
            FadeIn(background),
            Write(radius_10_eq)
        )
        self.wait(2)
        self.play(ReplacementTransform(
            radius_10_eq.copy(),
            radius_million_eq
        ))
        self.play(FadeIn(brace))
        self.wait(3)

        self.radius_10_eq = radius_10_eq
        self.million_group = VGroup(radius_million_eq, brace)
        self.radius_R_eq = radius_R_eq

    def allude_to_alternate_counting_method(self):
        alt_count = OldTexText(
            "(...something else...)", "$R^2$", "=",
            arg_separator = ""
        )
        alt_count.to_corner(UP+LEFT)
        alt_count.set_color_by_tex("something", MAROON_B)
        self.radius_R_eq.next_to(alt_count, RIGHT)

        final_group = VGroup(
            alt_count.get_part_by_tex("something"),
            self.radius_R_eq[1].get_part_by_tex("pi"),
        ).copy()

        self.play(
            FadeOut(self.million_group),
            Write(alt_count),
            ReplacementTransform(
                self.radius_10_eq,
                self.radius_R_eq
            )
        )
        self.wait(2)
        self.play(
            final_group.arrange, RIGHT,
            final_group.next_to, ORIGIN, UP
        )
        rect = BackgroundRectangle(final_group)
        self.play(FadeIn(rect), Animation(final_group))
        self.wait(2)
