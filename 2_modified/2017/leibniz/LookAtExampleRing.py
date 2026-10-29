# ==============================================================================
# Scene:      LookAtExampleRing
# Source:     videos/_2017/leibniz.py (lines 1167-1316)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LookAtExampleRing.py LookAtExampleRing -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - zip is an iterator in Python 3
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


class LookAtExampleRing(LatticePointScene):
    CONFIG = {
        "dot_radius" : 0.1,
        "plane_center" : 2*LEFT,
        "x_radius" : 17,
        "y_radius" : 7,
    }
    def construct(self):
        self.analyze_25()
        self.analyze_11()

    def analyze_25(self):
        x_color = GREEN
        y_color = RED
        circle = self.get_circle(radius = 5)
        points = self.get_lattice_points_on_r_squared_circle(25)
        radius, root_label = self.get_radial_line_with_label(5)
        coords_list = [(5, 0), (4, 3), (3, 4), (0, 5), (-3, 4), (-4, 3)]
        labels = [
            OldTex("(", str(x), ",", str(y), ")")
            for x, y in coords_list
        ]
        for label in labels:
            label.x = label[1]
            label.y = label[3]
            label.x.set_color(x_color)
            label.y.set_color(y_color)
            label.add_background_rectangle()

        for label, point in zip(labels, points):
            x_coord = (point.get_center() - self.plane_center)[0]
            vect = UP+RIGHT if x_coord >= 0 else UP+LEFT
            label.next_to(point, vect, SMALL_BUFF)
            label.point = point

        def special_str(n):
            return "(%d)"%n if n < 0 else str(n)

        sums_of_squares = [
            OldTex(
                special_str(x), "^2", "+", 
                special_str(y), "^2", "= 25"
            )
            for x, y in coords_list
        ]
        for tex_mob in sums_of_squares:
            tex_mob.x = tex_mob[0]
            tex_mob.y = tex_mob[3]
            tex_mob.x.set_color(x_color)
            tex_mob.y.set_color(y_color)
            tex_mob.add_background_rectangle()
            tex_mob.to_corner(UP+RIGHT)

        self.play(
            ShowCreation(radius),
            Write(root_label)
        )
        self.play(
            ShowCreation(circle),
            Rotating(
                radius, 
                about_point = self.plane_center,
                rate_func = smooth, 
            ),
            FadeIn(points, lag_ratio = 0.5),
            run_time = 2,
        )
        self.wait()

        curr_label = labels[0]
        curr_sum_of_squares = sums_of_squares[0]
        self.play(
            Write(curr_label),
            curr_label.point.set_color, PINK
        )
        x, y = curr_label.x.copy(), curr_label.y.copy()
        self.play(
            Transform(x, curr_sum_of_squares.x),
            Transform(y, curr_sum_of_squares.y),
        )
        self.play(
            Write(curr_sum_of_squares),
            Animation(VGroup(x, y))
        )
        self.remove(x, y)
        self.wait()

        # CHANGE: zip is an iterator in Python 3
        for label, sum_of_squares in list(zip(labels, sums_of_squares))[1:]:
            self.play(
                ReplacementTransform(curr_label, label),
                label.point.set_color, PINK,
                curr_label.point.set_color, self.dot_color
            )
            curr_label = label
            self.play(
                ReplacementTransform(
                    curr_sum_of_squares, sum_of_squares
                )
            )
            curr_sum_of_squares = sum_of_squares
            self.wait()

        points.save_state()
        points.generate_target()
        for i, point in enumerate(points.target):
            point.move_to(
                self.plane.coords_to_point(i%3, i//3)
            )
        points.target.next_to(circle, RIGHT)

        self.play(MoveToTarget(
            points, 
            run_time = 2,
        ))
        self.wait()
        self.play(points.restore, run_time = 2)
        self.wait()
        self.play(*list(map(FadeOut, [
            curr_label, curr_sum_of_squares, 
            circle, points,
            radius, root_label
        ])))

    def analyze_11(self):
        R = np.sqrt(11)
        circle = self.get_circle(radius = R)
        radius, root_label = self.get_radial_line_with_label(R)
        equation = OldTex("11 \\ne ", "a", "^2", "+", "b", "^2")
        equation.set_color_by_tex("a", GREEN)
        equation.set_color_by_tex("b", RED)
        equation.add_background_rectangle()
        equation.to_corner(UP+RIGHT)

        self.play(
            Write(root_label),
            ShowCreation(radius),
            run_time = 1
        )
        self.play(
            ShowCreation(circle),
            Rotating(
                radius, 
                about_point = self.plane_center,
                rate_func = smooth, 
            ),
            run_time = 2,
        )
        self.wait()
        self.play(Write(equation))
        self.wait(3)
