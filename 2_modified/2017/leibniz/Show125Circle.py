# ==============================================================================
# Scene:      Show125Circle
# Source:     videos/_2017/leibniz.py (lines 2943-2978)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl Show125Circle.py Show125Circle -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - radius_squared is never defined in the original (NameError also in Cairo); 25 = 3^2+4^2 = 5^2+0^2, the circle through coords_list
#   - ask_about_two is only defined in the subclass SummarizeCountingRule (AttributeError also in Cairo); drop the call here
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


# CHANGE: radius_squared is never defined in the original (NameError also in Cairo); 25 = 3^2+4^2 = 5^2+0^2, the circle through coords_list
class ThreeOutputsAsLatticePoints(LatticePointScene):
    CONFIG = {
        "radius_squared" : 25,
        "coords_list" : [(3, 4), (5, 0), (3, -4)],
        "dot_radius" : 0.1,
        "colors" : [YELLOW, GREEN, PINK, MAROON_B],
    }
    def construct(self):
        self.add_circle()
        self.add_dots_and_labels()

    def add_circle(self):
        radius = np.sqrt(self.radius_squared)
        circle = self.get_circle(radius)
        radial_line, root_label = self.get_radial_line_with_label(radius)
        self.add(radial_line, root_label, circle)
        self.add_foreground_mobject(root_label)

    def add_dots_and_labels(self):
        dots = VGroup(*[
            Dot(
                self.plane.coords_to_point(*coords),
                radius = self.dot_radius, 
                color = self.colors[0],
            )
            for coords in self.coords_list
        ])
        labels = VGroup()
        for x, y in self.coords_list:
            if y == 0:
                y_str = ""
                vect = DOWN+RIGHT
            elif y > 1:
                y_str = "+%di"%y
                vect = UP+RIGHT
            else:
                y_str = "%di"%y
                vect = DOWN+RIGHT
            label = OldTex("%d%s"%(x, y_str))
            label.add_background_rectangle()
            point = self.plane.coords_to_point(x, y)
            label.next_to(point, vect)
            labels.add(label)

        for dot, label in zip(dots, labels):
            self.play(
                FadeIn(label),
                DrawBorderThenFill(
                    dot, 
                    stroke_color = PINK,
                    stroke_width = 4
                )
            )
        self.wait(2)

        self.original_dots = dots


class ThreeOutputsAsLatticePointsContinued(ThreeOutputsAsLatticePoints):
    def construct(self):
        self.force_skipping()
        ThreeOutputsAsLatticePoints.construct(self)
        self.revert_to_original_skipping_status()

        self.show_multiplication_by_units()

    def show_multiplication_by_units(self):
        original_dots = self.original_dots
        lines = VGroup()
        for dot in original_dots:
            line = Line(self.plane_center, dot.get_center())
            line.set_stroke(dot.get_color(), 6)
            lines.add(line)
            dot.add(line)
        words_group = VGroup(*[
            OldTexText("Multiply by $%s$"%s)
            for s in ("1", "i", "-1", "-i")
        ])
        for words, color in zip(words_group, self.colors):
            words.add_background_rectangle()
            words.set_color(color)
        words_group.arrange(DOWN, aligned_edge = LEFT)
        words_group.to_corner(UP+LEFT, buff = MED_SMALL_BUFF)
        angles = [np.pi/2, np.pi, -np.pi/2]

        self.play(
            FadeIn(words_group[0]),
            *list(map(ShowCreation, lines))
        )
        for words, angle, color in zip(words_group[1:], angles, self.colors[1:]):
            self.play(FadeIn(words))
            dots_copy = original_dots.copy()
            self.play(
                dots_copy.rotate, angle,
                dots_copy.set_color, color,
                path_arc = angle
            )
            self.wait()
        self.wait(2)


class Show125Circle(ThreeOutputsAsLatticePointsContinued):
    CONFIG = {
        "radius_squared" : 125,
        "coords_list" : [(2, 11), (10, 5), (10, -5), (2, -11)],
        "y_radius" : 15,
    }
    def construct(self):
        self.draw_circle()
        self.add_dots_and_labels()
        # CHANGE: ask_about_two is only defined in the subclass SummarizeCountingRule (AttributeError also in Cairo); drop the call here
        self.show_multiplication_by_units()

    def draw_circle(self):
        self.plane.scale(2)
        radius = np.sqrt(self.radius_squared)
        circle = self.get_circle(radius)
        radial_line, root_label = self.get_radial_line_with_label(radius)

        self.play(
            Write(root_label),
            ShowCreation(radial_line)
        )
        self.add_foreground_mobject(root_label)
        self.play(
            Rotating(
                radial_line, 
                rate_func = smooth, 
                about_point = self.plane_center
            ),
            ShowCreation(circle),
            run_time = 2,
        )
        group = VGroup(
            self.plane, radial_line, circle, root_label
        )
        self.play(group.scale, 0.5)
