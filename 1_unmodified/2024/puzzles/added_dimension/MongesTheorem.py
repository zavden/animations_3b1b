# ==============================================================================
# Scene:      MongesTheorem
# Source:     videos/_2024/puzzles/added_dimension.py (lines 1987-2409)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MongesTheorem.py MongesTheorem -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class MongesTheorem(InteractiveScene):
    def construct(self):
        # Add circles
        circ1, circ2, circ3 = circles = self.get_initial_circles()

        self.play(LaggedStartMap(ShowCreation, circles, lag_ratio=0.5, run_time=2))
        self.wait()

        # Add tangents
        tangent_pairs = always_redraw(lambda: self.get_all_external_tangents(circles))
        intersection_dots = always_redraw(lambda: self.get_all_intersection_dots(tangent_pairs))

        dependents = Group(tangent_pairs, intersection_dots)
        dependents.suspend_updating()

        for tangents, dot, circle_pair in zip(tangent_pairs, intersection_dots, it.combinations(circles, 2)):
            c1, c2 = (c.copy() for c in circle_pair)
            self.play(*map(GrowFromCenter, tangents), run_time=1.5)
            self.play(
                LaggedStart(
                    c1.animate.scale(0, about_point=dot.get_center()),
                    c2.animate.scale(0, about_point=dot.get_center()),
                    FadeIn(dot),
                    lag_ratio=0.2,
                )
            )
            self.remove(c1, c2)
            self.wait()

        # Manipuate the circles
        dependents.resume_updating()
        circles.save_state()
        self.add(*dependents)

        self.add(*circles)
        self.wait(note="Play with circle positions. Be careful!")

        # Show the line between them
        monge_line = Line()
        monge_line.f_always.put_start_and_end_on(
            intersection_dots[0].get_center,
            intersection_dots[2].get_center,
        )
        monge_line.always.set_length(100)
        monge_line.set_stroke(WHITE, 3)
        monge_line.suspend_updating()

        self.play(GrowFromCenter(monge_line))
        self.wait()

        # Manipulate again
        monge_line.resume_updating()
        self.add(*circles)
        self.wait(30, note="Play with circle positions. Be careful!")
        self.play(Restore(circles), self.frame.animate.to_default_state(), run_time=3)

        dependents.suspend_updating()
        self.play(FadeOut(monge_line))
        self.wait()

        # Setup spheres and tangent groups
        plane = NumberPlane((-8, 8), (-8, 8))
        plane.background_lines.set_stroke(GREY, 1)
        plane.faded_lines.set_stroke(GREY, 1, 0.25)
        plane.axes.set_stroke(GREY, 1)

        spheres = self.get_spheres(circles)
        tangent_groups = always_redraw(lambda: self.get_tangent_groups(circles))

        tangent_groups.suspend_updating()

        # Show spheres
        frame = self.frame
        self.wait()
        self.play(
            frame.animate.reorient(-11, 69, 0),
            FadeIn(plane),
            FadeIn(spheres, lag_ratio=0.25),
            run_time=4
        )
        self.wait()

        # Reposition
        self.play(self.frame.animate.reorient(-41, 72, 0), run_time=5)

        # Show various external tangents
        self.play(
            frame.animate.reorient(-67, 76, 0),
            LaggedStartMap(GrowFromCenter, tangent_groups[2], lag_ratio=0.1),
            spheres[0].animate.set_opacity(0.05),
            run_time=3
        )
        self.wait(10, note="Emphasize how it's formed")

        self.play(
            frame.animate.reorient(-105, 46, 0),
            LaggedStartMap(GrowFromCenter, tangent_groups[1], lag_ratio=0.1),
            spheres[0].animate.set_opacity(0.5),
            spheres[1].animate.set_opacity(0.05),
            run_time=3
        )
        self.wait()
        self.play(
            frame.animate.reorient(-175, 51, 0, (1.2, 0.92, -0.26)),
            LaggedStartMap(GrowFromCenter, tangent_groups[0], lag_ratio=0.1),
            spheres[1].animate.set_opacity(0.5),
            spheres[2].animate.set_opacity(0.05),
            run_time=3
        )
        self.wait()
        self.play(
            frame.animate.reorient(-70, 59, 0, (0.22, 0.32, -1.5), 9.17),
            spheres[2].animate.set_opacity(0.5),
            run_time=6,
        )
        self.wait()

        # Show mutually tangent plane (Fudged, but it works)
        xy_plane = Square3D(resolution=(100, 100)).rotate(PI)
        xy_plane.set_color(BLUE_E, 0.35)
        xy_plane.replace(plane)

        inter_points = [dot.get_center() for dot in intersection_dots]
        blue_tip = self.get_cone_tips(circles[2:], angle=84 * DEGREES)[0]
        tangent_plane = self.get_plane_through_points([inter_points[2], inter_points[0], blue_tip])

        plane_lines = VGroup(
            tangent_groups[2][19].copy(),
            tangent_groups[0][31].copy(),
            tangent_groups[1][25].copy(),
        )
        plane_lines.set_stroke(width=4, opacity=1)

        self.play(
            frame.animate.reorient(-50, 74, 0, (0.22, 0.32, -1.5), 9.17),
            ShowCreation(tangent_plane, time_span=(0, 2)),
            run_time=6,
        )
        self.wait()
        self.play(
            frame.animate.reorient(-77, 63, 0, (0.22, 0.32, -1.5), 9.17),
            FadeOut(tangent_groups),
            run_time=4
        )
        for line in plane_lines:
            self.play(ShowCreation(line, run_time=2))
            self.wait()

        self.add(xy_plane, tangent_plane, plane_lines)
        self.play(ShowCreation(xy_plane, time_span=(0, 2)))
        self.wait()
        self.play(ShowCreation(monge_line, suspend_mobject_updating=True))
        self.wait()

        # Move circles to problem position
        self.play(
            FadeOut(xy_plane),
            FadeOut(tangent_plane),
            FadeOut(plane_lines),
            self.frame.animate.to_default_state(),
            run_time=2
        )

        dependents.resume_updating()
        self.add(dependents)
        self.play(
            circles[1].animate.move_to(2 * LEFT),
            circles[0].animate.move_to(0.2 * UP),
            circles[2].animate.move_to(3 * RIGHT),
            run_time=3
        )
        dependents.suspend_updating()
        self.wait()

        # Show the outside plane
        angle = abs(tangent_pairs[2][0].get_angle())
        partial_tangent_plane = xy_plane.copy()
        pivot_point = intersection_dots[2].get_center()
        partial_tangent_plane.rotate(angle, axis=DOWN, about_point=pivot_point)
        partial_tangent_plane.set_height(5, stretch=True)
        partial_tangent_plane.set_color(GREY_C, 0.5)
        partial_tangent_plane.set_shading(0.25, 0.25, 0.25)

        self.add(partial_tangent_plane)
        self.play(ShowCreation(partial_tangent_plane))
        self.wait()
        self.play(self.frame.animate.reorient(27, 75, 0))
        self.play(
            Rotating(partial_tangent_plane, PI / 2, axis=RIGHT, about_point=pivot_point),
            run_time=8,
            rate_func=there_and_back,
        )
        self.wait()
        self.play(
            FadeOut(partial_tangent_plane),
            self.frame.animate.to_default_state(),
            run_time=3
        )
        dependents.resume_updating()
        self.add(dependents)
        self.play(circles[0].animate.move_to(2 * UP), run_time=3)
        dependents.suspend_updating()

        # Show the cones
        cones = self.get_cones(circles)

        def upadte_cone_positions(cones):
            for cone, circle in zip(cones, circles):
                cone.match_width(circle)
                cone.move_to(circle, IN)

        self.play(
            self.frame.animate.reorient(-74, 72, 0, (-1.2, 0.14, -0.2), 8.00),
            run_time=3
        )
        spheres.clear_updaters()
        self.play(ReplacementTransform(spheres, cones, lag_ratio=0.5, run_time=2))
        self.wait()

        # Show the center of similarity
        def get_tip_lines():
            result = VGroup()
            for i, j, k in [(2, 2, 2), (1, 2, 1), (0, 1, 0)]:
                line = Line(intersection_dots[i].get_center(), cones[j].get_zenith())
                line.match_color(tangent_pairs[k][0])
                line.scale(2, about_point=line.get_start())
                result.add(line)
            return result
        tip_lines = always_redraw(get_tip_lines)
        tip_lines.suspend_updating()

        self.play(ShowCreation(tip_lines[0]))
        self.play(self.frame.animate.reorient(-1, 83, 0, (-1.2, 0.14, -0.2)), run_time=3)
        self.wait()

        cone_ghost = cones[2].copy().set_opacity(0.5)
        cone_ghost.deactivate_depth_test()
        self.add(cones, cone_ghost)
        self.play(FadeIn(cone_ghost))
        for x in range(2):
            self.play(
                cone_ghost.animate.scale(1e-2, about_point=intersection_dots[2].get_center()),
                run_time=8,
                rate_func=there_and_back
            )
            self.wait()
            self.play(self.frame.animate.reorient(0, 7, 0, (-1.92, 0.22, 0.0)), run_time=3)
        self.play(
            FadeOut(cone_ghost),
            self.frame.animate.reorient(-129, 75, 0, (-1.92, 0.22, 0.0)),
            run_time=4
        )
        self.play(ShowCreation(tip_lines[1:], lag_ratio=0.5, run_time=2))
        self.wait()

        # Add plane
        plane = always_redraw(lambda: self.get_plane_through_points([
            intersection_dots[2].get_center(),
            intersection_dots[0].get_center(),
            cones[2].get_zenith()
        ]))
        plane.suspend_updating()

        self.play(
            ShowCreation(plane),
            self.frame.animate.reorient(-74, 66, 0, (-1.92, 0.22, 0.0)),
            run_time=4
        )

        # Move the circles all about
        dependents.add(tip_lines, plane)
        dependents.resume_updating()
        cones.add_updater(upadte_cone_positions)
        self.add(cones, dependents)

        self.play(circles[0].animate.move_to(0.2 * UP), run_time=3)
        dependents.suspend_updating()
        self.play(self.frame.animate.reorient(-173, 69, 0, (-1.36, 0.7, 1.01), 7.14), run_time=10)
        self.wait(note="Reorient")
        dependents.resume_updating()
        self.play(
            circles[0].animate.move_to(2 * UP),
            self.frame.animate.reorient(-122, 54, 0, (-1.54, 0.75, 0.38), 8.65),
            run_time=4
        )
        self.manipulate_circle_positions(circles)
        dependents.suspend_updating()

    def get_initial_circles(self):
        centers = [[-3, 3, 0], [-6, -1.5, 0], [3, -1.5, 0]]
        colors = [RED, GREEN, BLUE]
        radii = [1, 2, 4]
        circles = VGroup(
            Circle(radius=radius).move_to(center).set_color(color)
            for radius, center, color in zip(radii, centers, colors)
        )
        circles.scale(0.5)
        circles.to_edge(RIGHT, buff=LARGE_BUFF)
        return circles

    def get_plane_through_points(self, points, color=GREY_B, opacity=0.5):
        v1 = points[1] - points[0]
        v2 = points[2] - points[0]
        perp = normalize(cross(v2, v1))
        vert_angle = math.acos(perp[2])

        plane = Square3D(resolution=(100, 100))
        plane.set_width(get_norm(v1))
        plane.move_to(ORIGIN, DL)
        plane.rotate(angle_of_vector(v1), about_point=ORIGIN)
        plane.rotate(PI - vert_angle, axis=v1, about_point=ORIGIN)
        plane.shift(points[0])
        plane.scale(2, about_point=points[0])

        plane.set_color(color, opacity=opacity)

        return plane

    def get_cones(self, circles, angle=90 * DEGREES):
        cones = Group()
        for circle in circles:
            radius = circle.get_width() / 2
            cone = Cone(radius=radius, height=radius / math.tan(angle / 2))
            cone.move_to(circle, IN)
            cone.set_color(circle.get_color())
            cone.set_opacity(0.5)
            cone.always_sort_to_camera(self.camera)
            cones.add(cone)
        return cones

    def get_cone_tips(self, circles, angle=90 * DEGREES):
        points = []
        for circle in circles:
            radius = circle.get_width() / 2
            height = radius / math.tan(angle / 2)
            point = circle.get_center() + height * OUT
            points.append(point)
        return points

    def get_spheres(self, circles, opacity=0.5):
        spheres = Group()
        for circle in circles:
            sphere = Sphere(radius=circle.get_radius())
            sphere.set_color(circle.get_color(), opacity)
            sphere.circle = circle
            sphere.always_sort_to_camera(self.camera)
            sphere.always.match_width(circle)
            sphere.always.move_to(circle)
            spheres.add(sphere)
        return spheres

    def get_tangent_groups(self, circles, n_lines=24):
        tangent_groups = VGroup()
        for circ1, circ2 in it.combinations(circles, 2):
            tangent_pair = self.get_external_tangents(circ1, circ2)
            point = self.get_intersection(*tangent_pair)
            axis = circ2.get_center() - circ1.get_center()
            group = VGroup()
            for angle in np.arange(0, PI, PI / n_lines):
                group.add(*tangent_pair.copy().rotate(angle, axis=axis, about_point=point))
            for line in group:
                line.shift(point - line.get_start())
            group.set_stroke(width=1, opacity=0.5)
            tangent_groups.add(group)
        return tangent_groups

    def get_all_intersection_dots(self, line_pairs):
        return Group(
            GlowDot(self.get_intersection(*pair))
            for pair in line_pairs
        )

    def get_all_external_tangents(self, circles, **kwargs):
        return VGroup(
            self.get_external_tangents(circ1, circ2)
            for circ1, circ2 in it.combinations(circles, 2)
        )

    def get_external_tangents(self, circle1, circle2, length=100, color=None):
        c1 = circle1.get_center()
        c2 = circle2.get_center()
        r1 = circle1.get_radius()
        r2 = circle2.get_radius()

        if get_norm(c1 - c2) <= max(r1, r2):
            return VectorizedPoint().replicate(2)

        # Distance to intersection of external tangents
        L1 = get_norm(c1 - c2) / (1 - r2 / r1)
        intersection = c1 + L1 * normalize(c2 - c1)
        theta = math.asin(r1 / L1)

        line1 = Line(c1, c2)
        line1.insert_n_curves(20)
        line1.rotate(theta, about_point=intersection)
        line1.set_length(length)
        line2 = line1.copy().rotate(PI, axis=(c2 - c1), about_point=intersection)

        result = VGroup(line1, line2)
        if color is None:
            color = interpolate_color(circle1.get_color(), circle2.get_color(), 0.5)
        result.set_stroke(color, width=2)
        return result

    def get_intersection(self, line1, line2):
        try:
            return line_intersection(
                line1.get_start_and_end(),
                line2.get_start_and_end(),
            )
        except Exception:
            return midpoint(line1.get_end(), line2.get_end())

    def manipulate_circle_positions(self, circles):
        circ1, circ2, circ3 = circles
        # Example
        self.play(circ2.animate.shift(LEFT), run_time=2)
        self.play(circ2.animate.scale(0.75), run_time=2)
        self.play(circ1.animate.scale(0.5).shift(0.2 * DOWN), run_time=2)
        self.play(circ3.animate.scale(0.7).shift(0.2 * DOWN), run_time=4)
        self.wait()
        self.play(Restore(circles), run_time=3)
        self.wait()
