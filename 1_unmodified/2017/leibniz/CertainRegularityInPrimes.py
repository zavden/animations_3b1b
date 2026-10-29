# ==============================================================================
# Scene:      CertainRegularityInPrimes
# Source:     videos/_2017/leibniz.py (lines 441-492)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CertainRegularityInPrimes.py CertainRegularityInPrimes -w -m --fps 15
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


class CertainRegularityInPrimes(LatticePointScene):
    CONFIG = {
        "y_radius" : 8,
        "x_radius" : 20,
        "max_lattice_point_radius" : 8,
        "plane_center" : 2.5*RIGHT,
        "primes" : [5, 13, 17, 29, 37, 41, 53],
        "include_pi_formula" : True,
    }
    def construct(self):
        if self.include_pi_formula:
            self.add_pi_formula()
        self.walk_through_primes()

    def add_pi_formula(self):
        formula = OldTex(
            "\\frac{\\pi}{4}", "=",
            "1", "-", "\\frac{1}{3}",
            "+", "\\frac{1}{5}", "-", "\\frac{1}{7}",
            "+\\cdots"
        )
        formula.set_color_by_tex("pi", YELLOW)
        formula.add_background_rectangle()
        formula.to_corner(UP+LEFT, buff = MED_SMALL_BUFF)
        self.add_foreground_mobject(formula)

    def walk_through_primes(self):
        primes = self.primes
        lines_and_labels = [
            self.get_radial_line_with_label(np.sqrt(p))
            for p in primes
        ]
        lines, labels = list(zip(*lines_and_labels))
        circles = [
            self.get_circle(np.sqrt(p))
            for p in primes
        ]
        dots_list = [
            self.get_lattice_points_on_r_squared_circle(p)
            for p in primes
        ]
        groups = [
            VGroup(*mobs)
            for mobs in zip(lines, labels, circles, dots_list)
        ]

        curr_group = groups[0]
        self.play(Write(curr_group, run_time = 2))
        self.wait()
        for group in groups[1:]:
            self.play(Transform(curr_group, group))
            self.wait(2)
