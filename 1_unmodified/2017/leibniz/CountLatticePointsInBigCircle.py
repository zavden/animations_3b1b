# ==============================================================================
# Scene:      CountLatticePointsInBigCircle
# Source:     videos/_2017/leibniz.py (lines 4069-4228)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CountLatticePointsInBigCircle.py CountLatticePointsInBigCircle -w -m --fps 15
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


class CountLatticePointsInBigCircle(LatticePointScene):
    CONFIG = {
        "y_radius" : 2*11,
        "max_lattice_point_radius" : 10,
        "dot_radius" : 0.05
    }
    def construct(self):
        self.resize_plane()
        self.introduce_points()
        self.show_rings()
        self.ignore_center_dot()

    def resize_plane(self):
        self.plane.set_stroke(width = 2)
        self.plane.scale(2)
        self.lattice_points.scale(2)
        for point in self.lattice_points:
            point.scale(0.5)

    def introduce_points(self):
        circle = self.get_circle(radius = self.max_lattice_point_radius)
        radius = Line(ORIGIN, circle.get_right())
        radius.set_color(RED)
        R = OldTex("R").next_to(radius, UP)
        R_rect = BackgroundRectangle(R)
        R_group = VGroup(R_rect, R)
        pi_R_squared = OldTex("\\pi", "R", "^2")
        pi_R_squared.next_to(ORIGIN, UP)
        pi_R_squared.to_edge(RIGHT)
        pi_R_squared_rect = BackgroundRectangle(pi_R_squared)
        pi_R_squared_group = VGroup(pi_R_squared_rect, pi_R_squared)

        self.play(*list(map(FadeIn, [circle, radius, R_group])))
        self.add_foreground_mobject(R_group)
        self.draw_lattice_points()
        self.wait()
        self.play(
            FadeOut(R_rect),
            FadeIn(pi_R_squared_rect),
            ReplacementTransform(R, pi_R_squared.get_part_by_tex("R")),
            Write(VGroup(*[
                part for part in pi_R_squared
                if part is not pi_R_squared.get_part_by_tex("R")
            ]))
        )
        self.remove(R_group)
        self.add_foreground_mobject(pi_R_squared_group)
        self.wait()

        self.circle = circle
        self.radius = radius

    def show_rings(self):
        N_range = list(range(self.max_lattice_point_radius**2))
        rings = VGroup(*[
            self.get_circle(radius = np.sqrt(N))
            for N in N_range
        ])
        rings.set_color_by_gradient(TEAL, GREEN)
        rings.set_stroke(width = 2)
        dot_groups = VGroup(*[
            self.get_lattice_points_on_r_squared_circle(N)
            for N in N_range
        ])
        radicals = self.get_radicals()

        self.play(
            LaggedStartMap(FadeIn, rings),
            Animation(self.lattice_points),
            LaggedStartMap(FadeIn, radicals),
            run_time = 3
        )
        self.add_foreground_mobject(radicals)
        self.play(
            LaggedStartMap(
                ApplyMethod,
                dot_groups,
                lambda m : (m.set_stroke, PINK, 5),
                rate_func = there_and_back,
                run_time = 4,
                lag_ratio = 0.1,
            ),
        )
        self.wait()

        self.rings = rings

    def ignore_center_dot(self):
        center_dot = self.lattice_points[0]
        circle = Circle(color = RED)
        circle.replace(center_dot)
        circle.scale(2)
        arrow = Arrow(ORIGIN, UP+RIGHT, color = RED)
        arrow.next_to(circle, DOWN+LEFT, SMALL_BUFF)
        new_max = 2*self.max_lattice_point_radius
        new_dots = VGroup(*[
            Dot(
                self.plane.coords_to_point(x, y),
                color = self.dot_color,
                radius = self.dot_radius,
            )
            for x in range(-new_max, new_max+1)
            for y in range(-new_max, new_max+1)
            if (x**2 + y**2) > self.max_lattice_point_radius**2
            if (x**2 + y**2) < new_max**2
        ])
        new_dots.sort(get_norm)

        self.play(*list(map(ShowCreation, [circle, arrow])))
        self.play(*list(map(FadeOut, [circle, arrow])))
        self.play(FadeOut(center_dot))
        self.lattice_points.remove(center_dot)
        self.wait()
        self.play(*[
            ApplyMethod(m.scale, 0.5)
            for m in [
                self.plane,
                self.circle,
                self.radius,
                self.rings,
                self.lattice_points
            ]
        ])
        new_dots.scale(0.5)
        self.play(FadeOut(self.rings))
        self.play(
            ApplyMethod(
                VGroup(self.circle, self.radius).scale, 2,
                rate_func=linear,
            ),
            LaggedStartMap(
                DrawBorderThenFill,
                new_dots,
                stroke_width = 4,
                stroke_color = PINK,
                lag_ratio = 0.2,
            ),
            run_time = 4,
        )
        self.wait(2)

    #####

    @staticmethod
    def get_radicals():
        radicals = VGroup(*[
            OldTex("\\sqrt{%d}"%N)
            for N in range(1, 13)
        ])
        radicals.add(
            OldTex("\\vdots"),
            OldTex("\\sqrt{R^2}")
        )
        radicals.arrange(DOWN, buff = MED_SMALL_BUFF)
        radicals.set_height(FRAME_HEIGHT - MED_LARGE_BUFF)
        radicals.to_edge(DOWN, buff = MED_SMALL_BUFF)
        radicals.to_edge(LEFT)
        for radical in radicals:
            radical.add_background_rectangle()
        return radicals
