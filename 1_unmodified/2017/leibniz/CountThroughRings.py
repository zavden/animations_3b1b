# ==============================================================================
# Scene:      CountThroughRings
# Source:     videos/_2017/leibniz.py (lines 913-1165)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CountThroughRings.py CountThroughRings -w -m --fps 15
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


class CountThroughRings(LatticePointScene):
    CONFIG = {
        "example_coords" : (3, 2),
        "num_rings_to_show_explicitly" : 7,
        "x_radius" : 15,

        "plane_center" : 2*RIGHT,
        "max_lattice_point_radius" : 5,
    }
    def construct(self):
        self.add_lattice_points()
        self.preview_rings()
        self.isolate_single_ring()
        self.show_specific_lattice_point_distance()
        self.count_through_rings()

    def add_lattice_points(self):
        big_circle = self.get_circle()
        self.add(big_circle)
        self.add(self.lattice_points)
        self.big_circle = big_circle

    def preview_rings(self):
        radii = list(set([
            np.sqrt(p.r_squared) for p in self.lattice_points
        ]))
        radii.sort()
        circles = VGroup(*[
            self.get_circle(radius = r)
            for r in radii
        ])
        circles.set_stroke(width = 2)
    
        self.add_foreground_mobject(self.lattice_points)
        self.play(FadeIn(circles))
        self.play(LaggedStartMap(
            ApplyMethod,
            circles,
            arg_creator = lambda m : (m.set_stroke, PINK, 4),
            rate_func = there_and_back,
        ))
        self.wait()
        self.remove_foreground_mobject(self.lattice_points)

        digest_locals(self, ["circles", "radii"])

    def isolate_single_ring(self):
        x, y = self.example_coords
        example_circle = self.circles[
            self.radii.index(np.sqrt(x**2 + y**2))
        ]
        self.circles.remove(example_circle)
        points_on_example_circle = self.get_lattice_points_on_r_squared_circle(
            x**2 + y**2
        ).copy()

        self.play(
            FadeOut(self.circles),
            self.lattice_points.set_fill, GREY, 0.5,
            Animation(points_on_example_circle)
        )
        self.wait()

        digest_locals(self, ["points_on_example_circle", "example_circle"])

    def show_specific_lattice_point_distance(self):
        x, y = self.example_coords
        dot = Dot(
            self.plane.coords_to_point(x, y),
            color = self.dot_color,
            radius = self.dot_radius
        )
        label = OldTex("(a, b)")
        num_label = OldTex(str(self.example_coords))
        for mob in label, num_label:
            mob.add_background_rectangle()
            mob.next_to(dot, UP + RIGHT, SMALL_BUFF)
        a, b = label[1][1].copy(), label[1][3].copy()

        x_spot = self.plane.coords_to_point(x, 0)
        radial_line = Line(self.plane_center, dot)
        h_line = Line(self.plane_center, x_spot)
        h_line.set_color(GREEN)
        v_line = Line(x_spot, dot)
        v_line.set_color(RED)

        distance = OldTex("\\sqrt{a^2 + b^2}")
        distance_num = OldTex("\\sqrt{%d}"%(x**2 + y**2))
        for mob in distance, distance_num:
            mob.scale(0.75)
            mob.add_background_rectangle()
            mob.next_to(radial_line.get_center(), UP, SMALL_BUFF)
            mob.rotate(
                radial_line.get_angle(),
                about_point = mob.get_bottom()
            )

        self.play(Write(label))
        self.play(
            ApplyMethod(a.next_to, h_line, DOWN, SMALL_BUFF),
            ApplyMethod(b.next_to, v_line, RIGHT, SMALL_BUFF),
            ShowCreation(h_line),
            ShowCreation(v_line),
        )
        self.play(ShowCreation(radial_line))
        self.play(Write(distance))
        self.wait(2)

        a_num, b_num = [
            OldTex(str(coord))[0]
            for coord in self.example_coords
        ]
        a_num.move_to(a, UP)
        b_num.move_to(b, LEFT)
        self.play(
            Transform(label, num_label),
            Transform(a, a_num),
            Transform(b, b_num),
        )
        self.wait()
        self.play(Transform(distance, distance_num))
        self.wait(3)
        self.play(*list(map(FadeOut, [
            self.example_circle, self.points_on_example_circle,
            distance, a, b,
            radial_line, h_line, v_line,
            label
        ])))

    def count_through_rings(self):
        counts = [
            len(self.get_lattice_points_on_r_squared_circle(N))
            for N in range(self.max_lattice_point_radius**2 + 1)
        ]
        left_list = VGroup(*[
            OldTex(
                "\\sqrt{%d} \\Rightarrow"%n, str(count)
            )
            for n, count in zip(
                list(range(self.num_rings_to_show_explicitly)),
                counts
            )
        ])
        left_counts = VGroup()
        left_roots = VGroup()
        for mob in left_list:
            mob[1].set_color(YELLOW)
            left_counts.add(VGroup(mob[1]))
            mob.add_background_rectangle()
            left_roots.add(VGroup(mob[0], mob[1][0]))

        left_list.arrange(
            DOWN,
            buff = MED_LARGE_BUFF,
            aligned_edge = LEFT,
        )
        left_list.to_corner(UP + LEFT)

        top_list = VGroup(*[
            OldTex("%d, "%count)
            for count in counts
        ])
        top_list.set_color(YELLOW)
        top_list.arrange(RIGHT, aligned_edge = DOWN)
        top_list.set_width(FRAME_WIDTH - MED_LARGE_BUFF)
        top_list.to_edge(UP, buff = SMALL_BUFF)
        top_rect = BackgroundRectangle(top_list)

        for r_squared, count_mob, root in zip(it.count(), left_counts, left_roots):
            self.show_ring_count(
                r_squared,
                count_mob,
                added_anims = [FadeIn(root)]
            )
            self.wait(2)
        self.play(
            FadeOut(left_roots),
            FadeIn(top_rect),
            *[
                ReplacementTransform(
                    lc, VGroup(tc),
                    path_arc = np.pi/2
                )
                for lc, tc in zip(left_counts, top_list)
            ]
        )
        for r_squared in range(len(left_counts), self.max_lattice_point_radius**2 + 1):
            self.show_ring_count(
                r_squared, top_list[r_squared],
            )
        self.wait(3)


    def show_ring_count(
        self, radius_squared, target,
        added_anims = None,        
        run_time = 1
        ):
        added_anims = added_anims or []
        radius = np.sqrt(radius_squared)
        points = self.get_lattice_points_on_r_squared_circle(radius_squared)
        points.save_state()
        circle = self.get_circle(radius)
        radial_line = Line(
            self.plane_center, self.plane.coords_to_point(radius, 0),
            color = RED
        )
        root = OldTex("\\sqrt{%d}"%radius_squared)
        root.add_background_rectangle()
        root.set_width(
            min(0.7*radial_line.get_width(), root.get_width())
        )
        root.next_to(radial_line, DOWN, SMALL_BUFF)
        if not hasattr(self, "little_circle"):
            self.little_circle = circle
        if not hasattr(self, "radial_line"):
            self.radial_line = radial_line
        if not hasattr(self, "root"):
            self.root = root
        if hasattr(self, "last_points"):
            added_anims += [self.last_points.restore]
        self.last_points = points

        if radius_squared == 0:
            points.set_fill(YELLOW, 1)
            self.play(
                DrawBorderThenFill(points, stroke_color = PINK),
                *added_anims,
                run_time = run_time
            )
            self.play(ReplacementTransform(
                points.copy(), target
            ))
            return
        points.set_fill(YELLOW, 1)
        self.play(
            Transform(self.little_circle, circle),
            Transform(self.radial_line, radial_line),
            Transform(self.root, root),
            DrawBorderThenFill(
                points, 
                stroke_width = 4,
                stroke_color = PINK,
            ),
            *added_anims,
            run_time = run_time
        )
        self.wait(run_time)
        if len(points) > 0:
            mover = points.copy()  
        else:
            mover = VectorizedPoint(self.plane_center)
        self.play(ReplacementTransform(mover, target, run_time = run_time))
