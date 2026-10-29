# ==============================================================================
# Scene:      TwoDBoxExample
# Source:     videos/_2017/highD.py (lines 1535-1717)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TwoDBoxExample.py TwoDBoxExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class TwoDBoxExample(Scene):
    def setup(self):
        scale_factor = 1.7
        self.plane = NumberPlane()
        self.plane.scale(scale_factor)
        self.plane.add_coordinates()
        self.plane.axes.set_color(GREY)
        self.add(self.plane)

    def construct(self):
        self.add_box()
        self.label_corner_coordinates()
        self.add_corner_circles()
        self.add_center_circle()
        self.compute_radius()

    def add_box(self):
        box = Square(color = RED, stroke_width = 6)
        line = Line(
            self.plane.coords_to_point(-1, -1),
            self.plane.coords_to_point(1, 1),
        )
        box.replace(line, stretch = True)
        self.play(ShowCreation(box))
        self.wait()

    def label_corner_coordinates(self):
        corner_dots = VGroup()
        coords_group = VGroup()
        for x, y in it.product(*[[1, -1]]*2):
            point = self.plane.coords_to_point(x, y)
            dot = Dot(point, color = WHITE)
            coords = OldTex("(%d, %d)"%(x, y))
            coords.add_background_rectangle()
            coords.next_to(point, point, SMALL_BUFF)
            corner_dots.add(dot)
            coords_group.add(coords)

            self.play(
                ShowCreation(dot),
                Write(coords, run_time = 1)
            )

        self.add_foreground_mobjects(coords_group)
        self.corner_dots = corner_dots
        self.coords_group = coords_group

    def add_corner_circles(self):
        line = Line(
            self.plane.coords_to_point(-1, 0),
            self.plane.coords_to_point(1, 0),
        )
        circle = Circle(color = YELLOW)
        circle.replace(line, dim_to_match = 0)
        circles = VGroup(*[
            circle.copy().move_to(dot)
            for dot in self.corner_dots
        ])

        radius = Line(ORIGIN, self.plane.coords_to_point(1, 0))
        radius.set_stroke(GREY, 6)
        radius.rotate(-np.pi/4)
        c0_center = circles[0].get_center()
        radius.shift(c0_center)
        r_equals_1 = OldTex("r = 1")
        r_equals_1.add_background_rectangle()
        r_equals_1.next_to(
            radius.point_from_proportion(0.75),
            UP+RIGHT, SMALL_BUFF
        )

        self.play(LaggedStartMap(ShowCreation, circles))
        self.play(
            ShowCreation(radius),
            Write(r_equals_1)
        )
        for angle in -np.pi/4, -np.pi/2, 3*np.pi/4:
            self.play(Rotating(
                radius, about_point = c0_center,
                radians = angle,
                run_time = 1,
                rate_func = smooth,
            ))
            self.wait(0.5)
        self.play(*list(map(FadeOut, [radius, r_equals_1])))
        self.wait()

        self.corner_radius = radius
        self.corner_circles = circles

    def add_center_circle(self):
        r = np.sqrt(2) - 1
        radius = Line(ORIGIN, self.plane.coords_to_point(r, 0))
        radius.set_stroke(WHITE)
        circle = Circle(color = GREEN)
        circle.replace(
            VGroup(radius, radius.copy().rotate(np.pi)),
            dim_to_match = 0
        )
        radius.rotate(np.pi/4)
        r_equals_q = OldTex("r", "= ???")
        r_equals_q[1].add_background_rectangle()
        r_equals_q.next_to(radius, RIGHT, buff = -SMALL_BUFF)

        self.play(GrowFromCenter(circle, run_time = 2))
        self.play(circle.scale, 1.2, rate_func = wiggle)
        self.play(ShowCreation(radius))
        self.play(Write(r_equals_q))
        self.wait(2)
        self.play(FadeOut(r_equals_q[1]))

        self.inner_radius = radius
        self.inner_circle = circle
        self.inner_r = r_equals_q[0]

    def compute_radius(self):
        triangle = Polygon(
            ORIGIN, 
            self.plane.coords_to_point(1, 0),
            self.plane.coords_to_point(1, 1),
            fill_color = BLUE,
            fill_opacity = 0.5,
            stroke_width = 6,
            stroke_color = WHITE,
        )
        bottom_one = OldTex("1")
        bottom_one.next_to(triangle.get_bottom(), UP, SMALL_BUFF)
        bottom_one.shift(MED_SMALL_BUFF*RIGHT)
        side_one = OldTex("1")
        side_one.next_to(triangle, RIGHT)
        sqrt_1_plus_1 = OldTex("\\sqrt", "{1^2 + 1^2}")
        sqrt_2 = OldTex("\\sqrt", "{2}")
        for sqrt in sqrt_1_plus_1, sqrt_2:
            sqrt.add_background_rectangle()
            sqrt.next_to(ORIGIN, UP, SMALL_BUFF)
            sqrt.rotate(np.pi/4)
            sqrt.shift(triangle.get_center())

        root_2_value = OldTex("\\sqrt{2} \\approx 1.414")
        root_2_value.to_corner(UP+RIGHT)
        root_2_value.add_background_rectangle()
        root_2_minus_1_value = OldTex(
            "\\sqrt{2} - 1 \\approx 0.414"
        )
        root_2_minus_1_value.next_to(root_2_value, DOWN)
        root_2_minus_1_value.to_edge(RIGHT)
        root_2_minus_1_value.add_background_rectangle()

        corner_radius = self.corner_radius
        c0_center = self.corner_circles[0].get_center()
        corner_radius.rotate(-np.pi/2, about_point = c0_center)

        rhs = OldTex("=", "\\sqrt", "{2}", "-1")
        rhs.next_to(self.inner_r, RIGHT, SMALL_BUFF, DOWN)
        rhs.shift(0.5*SMALL_BUFF*DOWN)
        sqrt_2_target = VGroup(*rhs[1:3])
        rhs.add_background_rectangle()

        self.play(
            FadeIn(triangle),
            Write(VGroup(bottom_one, side_one, sqrt_1_plus_1))
        )
        self.wait(2)
        self.play(ReplacementTransform(sqrt_1_plus_1, sqrt_2))
        self.play(
            Write(root_2_value, run_time = 1),
            *list(map(FadeOut, [bottom_one, side_one]))
        )
        self.wait()
        self.play(ShowCreation(corner_radius))
        self.play(Rotating(
            corner_radius, about_point = c0_center,
            run_time = 2,
            rate_func = smooth
        ))
        self.play(FadeOut(triangle), Animation(corner_radius))
        self.wait()
        self.play(
            Write(rhs),
            Transform(sqrt_2, sqrt_2_target),
        )
        self.play(Write(root_2_minus_1_value))
        self.wait(2)
