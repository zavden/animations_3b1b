# ==============================================================================
# Scene:      KochZoom
# Source:     videos/_2024/inscribed_rect/loops.py (lines 2984-2992)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/inscribed_rect/helpers.py
#
# Run from this folder:
#     manimgl KochZoom.py KochZoom -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
from typing import TYPE_CHECKING


# ----- From _2024/inscribed_rect/helpers.py -----

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3, Vect4


def get_example_loop(index=1, stroke_color=WHITE, stroke_width=3, width=5):
    result = SVGMobject(f"example_loop{index}").family_members_with_points()[0]
    result.set_width(width)
    result.set_stroke(stroke_color, stroke_width)
    return result


def get_special_dot(
    color=YELLOW,
    radius=0.05,
    glow_radius_multiple=3,
    glow_factor=1.5
):
    return Group(
        TrueDot(radius=radius).make_3d(),
        GlowDot(radius=radius * glow_radius_multiple, glow_factor=glow_factor)
    ).set_color(color)


def smooth_index(lst: list, real_index: float):
    N = len(lst)
    scaled_index = real_index * (N - 1)
    int_index = int(scaled_index)
    residue = scaled_index % 1
    if int_index >= N - 1:
        return lst[-1]
    return interpolate(lst[int_index], lst[int_index + 1], residue)


def get_quick_loop_func(loop: VMobject, n_samples=501):
    samples = np.array(list(map(loop.pfp, np.linspace(0, 1, n_samples))))

    def func(x):
        return smooth_index(samples, x)

    return func


def get_surface_func(loop_func: Callable[[float], Vect3]):
    def func(u, v):
        point1 = loop_func(u)
        point2 = loop_func(v)
        midpoint = mid(point1, point2)
        dist = get_norm(point1 - point2)
        return (*midpoint[:2], dist)
    return func


def get_half_parametric_func(func):
    def half_func(u, v):
        return func(u * v, v)
    return half_func


def find_rectangle(
    loop_func: Callable[[float], Vect3],
    initial_condition: Vect4 = np.arange(0, 1, 0.25),
    target_angle: float = 60 * DEGREES,
    initial_param_range: float = 1.0,
    n_samples_per_range: int = 10,
    n_refinements: int = 4,
    return_cost = False
) -> Vect4:
    """
    Returns an numpy array of 4 elements, between 0 and 1, such that 
    entering them into loop_func approximately gives a rectangle.
    """
    params = initial_condition.copy()
    param_range = initial_param_range
    min_cost = np.inf

    for _ in range(n_refinements):
        param_groups = [
            np.linspace(x - param_range / 2, x + param_range / 2, n_samples_per_range) % 1
            for x in params
        ]
        sample_groups = [
            np.array([loop_func(x) for x in param_group])
            for param_group in param_groups
        ]

        min_cost = np.inf
        best_idx_group = None
        for idx_group in it.product(*4 * [range(n_samples_per_range)]):
            a, b, c, d = [sg[i] for sg, i in zip(sample_groups, idx_group)]
            ac_dist = get_dist(a, c)
            mid_dist_ratio = get_dist(midpoint(a, c), midpoint(b, d)) / ac_dist
            dist_dist_ratio = abs(ac_dist - get_dist(b, d)) / ac_dist
            angle = abs(angle_between_vectors(c - a, d - b))
            if angle > PI / 2:
                angle = PI - angle
            cost = mid_dist_ratio + dist_dist_ratio + abs(angle - target_angle) / TAU
            if cost < min_cost:
                best_idx_group = idx_group
                min_cost = cost
        params = [pg[i] for pg, i in zip(param_groups, best_idx_group)]

        param_range /= n_samples_per_range

    if return_cost:
        return params, min_cost
    else:
        return params



# ----- From _2024/inscribed_rect/loops.py -----

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3, Vect4


class LoopScene(InteractiveScene):
    def get_dot_group(
        self,
        vect_tracker: ValueTracker,
        loop_func: Callable[[float], Vect3],
        colors=None,
        radius: float = 0.05,
        glow_factor: float = 1.5,
    ):
        n = len(vect_tracker.get_value())
        if colors is None:
            colors = [random_bright_color() for _ in range(n)]

        dots = Group(
            get_special_dot(color, radius=radius, glow_factor=glow_factor)
            for _, color in zip(range(n), it.cycle(colors))
        )

        def update_dots(dots):
            for dot, value in zip(dots, vect_tracker.get_value()):
                dot.move_to(loop_func(value))

        dots.add_updater(update_dots)
        return dots

    def get_movable_pair(
        self,
        uv_tracker: ValueTracker,
        loop_func: Callable[[float], Vect3],
        colors=[YELLOW, PINK],
        radius: float = 0.05,
        glow_factor: float = 1.5,
    ):
        return self.get_dot_group(uv_tracker, loop_func, colors, radius, glow_factor)

    def get_movable_quad(
        self,
        abcd_tracker: ValueTracker,
        loop_func: Callable[[float], Vect3],
        colors=[YELLOW, MAROON_B, PINK, RED],
        radius: float = 0.05,
        glow_factor: float = 1.5,
    ):
        return self.get_dot_group(abcd_tracker, loop_func, colors, radius, glow_factor)

    def get_connecting_line(self, dot_pair, stroke_color=TEAL_B, stroke_width=2):
        d1, d2 = dot_pair
        if stroke_color is None:
            stroke_color = average_color(d1.get_color(), d2.get_color())

        line = Line().set_stroke(stroke_color, stroke_width)
        line.f_always.put_start_and_end_on(d1.get_center, d2.get_center)
        return line

    def get_midpoint_dot(self, dot_pair, color=TEAL_B):
        dot = dot_pair[0].copy()
        dot.f_always.move_to(dot_pair.get_center)
        dot.set_color(color)
        return dot

    def get_dot_polygon(self, dots, stroke_color=BLUE, stroke_width=3):
        polygon = Polygon(LEFT, RIGHT)
        polygon.set_stroke(stroke_color, stroke_width)
        polygon.add_updater(lambda m: m.set_points_as_corners(
            [*(d.get_center() for d in dots), dots[0].get_center()]
        ))
        return polygon

    def get_dot_labels(self, dots, label_texs, direction=UL, buff=0):
        result = VGroup()
        for dot, tex in zip(dots, label_texs):
            label = Tex(tex)
            label.match_color(dot[0])
            label.set_backstroke(BLACK, 3)
            label.always.next_to(dot[0], direction, buff=buff)
            result.add(label)
        return result


class ShowTheSurface(LoopScene):
    def construct(self):
        # Axes and plane
        frame = self.frame
        axes, plane = self.get_axes_and_plane()
        frame.set_height(6)

        # Curve
        loop = get_example_loop()
        loop_func = get_quick_loop_func(loop)
        self.play(ShowCreation(loop, run_time=2))

        # Pair of points
        uv_tracker = ValueTracker([0, 0.5])
        dots = self.get_movable_pair(uv_tracker, loop_func, radius=0.075)
        connecting_line = self.get_connecting_line(dots)
        midpoint_dot = self.get_midpoint_dot(dots)

        self.add(uv_tracker)
        self.add(dots)
        self.add(connecting_line)

        self.play(
            UpdateFromFunc(uv_tracker, lambda m: m.set_value(np.random.random(2))),
        )
        self.add(dots, connecting_line)
        self.play(uv_tracker.animate.set_value([0.8, 0.5]), run_time=3)

        # Add coordinates
        coords = Tex("(x, y)", font_size=36)
        coords.set_backstroke(BLACK, 3)
        coords.set_fill(WHITE, 1)

        midpoint_dot.update()
        coords.always.next_to(midpoint_dot, UR, buff=-0.1)

        self.play(
            Write(coords, suspend_mobject_updating=True),
            FadeIn(midpoint_dot, scale=0.5)
        )
        self.wait()
        self.play(Write(plane, lag_ratio=0.01, run_time=2, stroke_width=1))
        self.wait()

        # Show the distance
        brace = Brace(Line(LEFT, RIGHT).set_width(connecting_line.get_length()), DOWN, buff=SMALL_BUFF)
        brace.rotate(connecting_line.get_angle(), about_point=ORIGIN)
        brace.shift(connecting_line.get_center())
        brace.set_color(GREY_B)
        d_label = Tex("d", font_size=36)
        d_label.move_to(brace.get_center() + 0.4 * normalize(brace.get_center() - midpoint_dot.get_center()))

        self.play(GrowFromCenter(brace), Write(d_label))

        # 3d coords into the corner
        coords_3d = Tex("(x, y, d)", font_size=36)
        coords_3d.next_to(self.frame.get_corner(UR), DL, MED_SMALL_BUFF)

        self.play(
            TransformFromCopy(coords[:4], coords_3d[:4]),
            TransformFromCopy(d_label, coords_3d[4:6]),
            TransformFromCopy(coords[4:], coords_3d[6:]),
            run_time=2
        )

        # Into 3d
        z_line = self.get_z_line(dots)
        top_dot = self.get_top_dot(z_line)
        top_dot.update()
        top_dot_coords = coords_3d.copy()
        top_dot_coords.unfix_from_frame()
        top_dot_coords.rotate(90 * DEG, RIGHT)
        top_dot_coords.scale(0.75)
        top_dot_coords.next_to(top_dot, OUT + RIGHT, buff=-0.05)

        self.play(
            frame.animate.reorient(5, 79, 0, (0.4, 0.01, 1.41), 5.07),
            FadeIn(axes),
            ReplacementTransform(coords_3d, top_dot_coords),
            TransformFromCopy(midpoint_dot, top_dot, suspend_mobject_updating=True),
            run_time=3
        )
        self.play(
            frame.animate.reorient(-21, 84, 0, (0.4, 0.01, 1.41), 5.07),
            run_time=5
        )
        self.play(
            frame.animate.reorient(0, 18, 0, (0.41, -0.13, 1.34), 4.76),
            run_time=2
        )
        self.play(FlashAround(coords, run_time=2, time_width=1.5))
        self.play(
            TransformFromCopy(connecting_line, z_line, suspend_mobject_updating=True, time_span=(4, 6)),
            frame.animate.reorient(-38, 88, 0, (1.19, -0.11, 1.48), 3.94),
            run_time=6,
        )
        self.play(frame.animate.reorient(-4, 88, 0, (1.19, -0.11, 1.48), 3.94), run_time=5)
        self.wait()

        # Show another pair of points
        uv_tracker2 = ValueTracker([0.2, 0.4])
        dots2 = self.get_movable_pair(uv_tracker2, loop_func, colors=[RED, MAROON_B])
        connecting_line2 = self.get_connecting_line(dots2)
        z_line2 = self.get_z_line(dots2)
        top_dot2 = self.get_top_dot(z_line2)

        dot_group1 = Group(dots, connecting_line, midpoint_dot, z_line, top_dot)
        dot_group2 = Group(dots2, connecting_line2, z_line2, top_dot2)

        self.play(
            frame.animate.reorient(12, 78, 0, (-0.48, 0.08, 1.15), 5.27),
            LaggedStartMap(FadeIn, dot_group2),
            LaggedStartMap(FadeOut, Group(d_label, brace, coords, top_dot_coords)),
            run_time=4
        )
        self.play(uv_tracker2.animate.set_value([0.1, 0.2]), run_time=8)
        self.wait()
        nudge = 0.01
        for _ in range(3):
            self.play(
                uv_tracker.animate.increment_value(np.random.uniform(-nudge, nudge, 2)),
                uv_tracker2.animate.increment_value(np.random.uniform(-nudge, nudge, 2)),
                run_time=2,
                rate_func=lambda t: wiggle(t, 7),
            )
        self.wait()

        # Show pair collision
        # ic = np.random.random(4)
        # print(list(ic.round(2)))
        rect_params = find_rectangle(
            loop_func,
            initial_condition=[0.54, 0.59, 0.73, 0.31],
            n_refinements=5,
            target_angle=64 * DEG
        )
        self.play(
            frame.animate.reorient(-18, 67, 0, (0.11, 0.07, 0.75), 4.63),
            uv_tracker.animate.set_value(rect_params[0::2]),
            uv_tracker2.animate.set_value(rect_params[1::2]),
            run_time=12
        )
        self.wait()

        # Show the rectangle
        rect_points = [loop_func(x) for x in rect_params]
        rect = Polygon(*rect_points)
        rect.set_stroke(YELLOW, 5)
        z_group = Group(z_line, z_line2, top_dot, top_dot2)
        self.play(
            FadeOut(z_group),
            FadeOut(axes),
            frame.animate.reorient(0, 0, 0, ORIGIN, 4.75),
            run_time=4
        )
        self.play(
            ShowCreation(rect),
            loop.animate.set_stroke(width=2)
        )
        self.wait(2)
        self.play(
            FadeOut(rect),
            FadeIn(z_group),
            FadeIn(axes),
            frame.animate.reorient(22, 85, 0, (-0.33, 0.45, 1.52), 6.78),
            run_time=3
        )

        # Set them both in motion
        self.set_uv_tracker_in_motion(uv_tracker, velocity=(-0.05, 0.1))
        self.set_uv_tracker_in_motion(uv_tracker2, velocity=(-0.025, 0.07))
        frame.add_ambient_rotation()

        for dot in [top_dot, top_dot2]:
            tail = TracingTail(dot, time_traced=5, stroke_color=BLUE, stroke_width=(0, 5))
            traced_path = TracedPath(dot.get_center, stroke_color=BLUE, stroke_width=1)
            dot.paths = VGroup(traced_path, tail)
            self.add(dot.paths)
        self.wait(30)

        # Surface
        surface, mesh, surface_func = self.get_surface_info(loop_func, surface_resolution=(301, 301))

        top_dot.paths.clear_updaters()
        top_dot2.paths.clear_updaters()
        self.play(
            FadeIn(mesh),
            FadeIn(surface),
            FadeOut(top_dot.paths),
            FadeOut(top_dot2.paths),
            frame.animate.reorient(-29, 81, 0, (0.14, 0.39, 2.1), 6.47).set_anim_args(run_time=8),
        )
        self.wait(15)

        # Remove dot groups
        self.play(
            FadeOut(dot_group1),
            FadeOut(dot_group2),
        )
        uv_tracker.clear_updaters()
        uv_tracker2.clear_updaters()
        self.wait()

        # Show surface cross sections
        z_tracker = ValueTracker(surface.get_z(OUT))
        top_mesh = mesh.copy()
        top_mesh.set_stroke(width=0.5, opacity=0.1)

        cross_plane = Square3D()
        cross_plane.set_color(WHITE, 0.1)
        cross_plane.replace(plane)
        cross_plane.f_always.set_z(z_tracker.get_value)

        surface.f_always.set_clip_plane(lambda: IN, z_tracker.get_value)
        top_mesh.f_always.set_clip_plane(lambda: OUT, lambda: -z_tracker.get_value())

        self.play(
            surface.animate.set_opacity(1),
            mesh.animate.set_stroke(width=0, opacity=0),
        )
        self.add(top_mesh)
        self.play(FadeIn(cross_plane))
        self.play(
            z_tracker.animate.set_value(0.25),
            surface.animate.set_color(BLUE_E, 1),
            run_time=8
        )
        self.wait(3)

        # Add dots and show the intersection point
        target_z = surface_func(*rect_params[0::2])[2]
        uv_tracker.set_value(rect_params[0::2] + np.random.random(2) * 0.2)
        uv_tracker2.set_value(rect_params[1::2] + np.random.random(2) * -0.2)

        self.play(
            FadeIn(dot_group1),
            FadeIn(dot_group2),
            surface.animate.set_opacity(0.75)
        )
        frame.clear_updaters()
        self.play(
            uv_tracker.animate.set_value(rect_params[0::2]),
            uv_tracker2.animate.set_value(rect_params[1::2]),
            FadeOut(z_line2, time_span=(2.5, 3)),
            FadeOut(top_dot2, time_span=(2.5, 3)),
            frame.animate.reorient(-3, 49, 0, (0.76, 0.62, 0.49), 6.46),
            run_time=3
        )

        # Show the rectangle again
        abcd_tracker = ValueTracker(rect_params)
        uv_tracker.f_always.set_value(lambda: abcd_tracker.get_value()[0::2])
        uv_tracker2.f_always.set_value(lambda: abcd_tracker.get_value()[1::2])

        rect = Rectangle()
        rect.f_always.set_points_as_corners(lambda: list(map(loop_func, abcd_tracker.get_value())))
        rect.always.close_path()

        self.add(abcd_tracker)
        self.play(
            ShowCreation(rect, suspend_mobject_updating=True),
        )
        self.wait()

        # Raise the cross section up to point
        self.play(
            z_tracker.animate.set_value(target_z),
            frame.animate.reorient(-3, 47, 0, (0.27, 0.98, 0.85), 3.80),
            top_mesh.animate.set_stroke(opacity=0.01),
            run_time=7,
        )
        # self.wait(15)  # Comment on the intersection
        self.wait()

        # Animate changing rectangle
        traced_path = TracingTail(top_dot, stroke_color=WHITE, time_traced=5)

        self.add(traced_path)
        self.play(
            frame.animate.reorient(-3, 48, 0, (0.15, 0.76, 0.6), 5.26),
            run_time=4,
        )
        z_tracker.f_always.set_value(top_dot.get_z)
        self.animate_to_rectangle_with_angle(abcd_tracker, loop_func, 80 * DEGREES, n_samples=10, param_range_per_step=0.02)
        z_tracker.clear_updaters()
        self.play(frame.animate.reorient(0, 44, 0, (0.02, 0.63, 0.47), 7.67), run_time=5)
        self.remove(traced_path)

        # Multiple self intersection points
        for _ in range(5):
            new_rect_params = find_rectangle(
                loop_func,
                initial_condition=np.random.random(4),
                target_angle=np.random.uniform(30 * DEG, 90 * DEG),
            )
            new_z = get_dist(*map(loop_func, new_rect_params[::2]))
            self.play(
                abcd_tracker.animate.set_value(new_rect_params),
                z_tracker.animate.set_value(new_z),
            )
            self.wait()

        # Raise the ceiling in full
        self.play(
            frame.animate.reorient(-1, 48, 0, (0.29, 1.22, 1.26), 8.99),
            z_tracker.animate.set_value(surface.get_z(OUT)),
            FadeOut(rect),
            FadeOut(dot_group2),
            run_time=10,
        )
        self.wait()
        self.remove(abcd_tracker)
        uv_tracker.clear_updaters()
        self.play(
            z_tracker.animate.set_value(0.25),
            top_mesh.animate.set_stroke(opacity=0.1),
            frame.animate.reorient(-7, 78, 0, (0.31, 1.16, 0.94), 7.21),
            run_time=6
        )

        # Point out what happens near the edge
        glow_tracker = ValueTracker(dots[0][0].get_glow_factor())
        radius_tracker = ValueTracker(dots[0][0].get_radius())
        for dot in [*dots, top_dot]:
            for part in dot:
                part.f_always.set_glow_factor(glow_tracker.get_value)
                part.f_always.set_radius(radius_tracker.get_value)
        v = uv_tracker.get_value()[1]
        self.play(
            uv_tracker.animate.set_value([v + 0.01, v]),
            glow_tracker.animate.set_value(0.25),
            radius_tracker.animate.set_value(0.025),
            frame.animate.reorient(-7, 78, 0, (0.1, 1.02, 0.18), 3.80),
            FadeOut(midpoint_dot),
            run_time=5
        )
        self.play(uv_tracker.animate.set_value([0.26, 0.25]), run_time=6)
        self.wait()
        self.play(
            uv_tracker.animate.set_value([0.25, 0.25]),
            frame.animate.reorient(-7, 78, 0, (-0.15, 1.0, -0.07), 2.80),
            z_tracker.animate.set_value(0.01),
            run_time=7
        )
        self.play(frame.animate.reorient(2, 70, 0, (0.05, 1.06, 0.05), 4.29), run_time=10)
        self.wait()

    def get_axes_and_plane(
        self,
        x_range=(-3, 3),
        y_range=(-3, 3),
        z_range=(0, 5),
        depth=4,
    ):
        axes = ThreeDAxes(x_range, y_range, z_range)
        axes.set_depth(depth, stretch=True, about_edge=IN)
        axes.set_stroke(GREY_B, 1)

        plane = NumberPlane(x_range, y_range)
        plane.background_lines.set_stroke(BLUE, 1, 0.75)
        plane.faded_lines.set_stroke(BLUE, 0.5, 0.25)
        plane.axes.match_style(axes)
        plane.set_z_index(-1)
        return axes, plane

    def get_z_line(self, dot_pair, stroke_color=TEAL_B, stroke_width=2):
        z_line = Line(IN, OUT).set_stroke(stroke_color, stroke_width)

        def update_z_line(z_line):
            point1 = dot_pair[0].get_center()
            point2 = dot_pair[1].get_center()
            midpoint = mid(point1, point2)
            top = midpoint + get_norm(point1 - point2) * OUT
            z_line.put_start_and_end_on(midpoint, top)

        z_line.add_updater(update_z_line)
        z_line.update()
        return z_line

    def get_top_dot(self, z_line, color=BLUE, radius=0.05, glow_factor=1.0):
        top_dot = Group(
            TrueDot(radius=radius).make_3d(),
            GlowDot(radius=radius * 2, glow_factor=glow_factor)
        )
        top_dot.set_color(color)
        top_dot.f_always.move_to(z_line.get_end)
        return top_dot

    def set_uv_tracker_in_motion(self, uv_tracker, velocity=(-0.05, 0.1)):
        velocity = np.array(velocity)

        def update_uv_tracker(uv_tracker, dt):
            new_value = uv_tracker.get_value() + dt * velocity
            uv_tracker.set_value(new_value % 1)

        uv_tracker.add_updater(update_uv_tracker)
        return uv_tracker

    def animate_to_rectangle_with_angle(
        self, abcd_tracker, loop_func, target_angle,
        n_samples=5,
        run_time=5,
        param_range_per_step=0.1,
        n_samples_per_range=10,
        n_refinements=3,
    ):
        # Find the sample points
        points = list(map(loop_func, abcd_tracker.get_value()))
        curr_angle = abs(angle_between_vectors(points[2] - points[0], points[3] - points[1]))
        if curr_angle > PI / 2:
            curr_angle = PI - curr_angle

        rectangle_range = [abcd_tracker.get_value()]
        for angle in np.linspace(curr_angle, target_angle, n_samples + 1)[1:]:
            rectangle_range.append(find_rectangle(
                loop_func=loop_func,
                initial_condition=rectangle_range[-1],
                target_angle=angle,
                initial_param_range=param_range_per_step,
                n_samples_per_range=n_samples_per_range,
                n_refinements=n_refinements,
            ))
        rectangle_range = np.array(rectangle_range)

        self.play(
            UpdateFromAlphaFunc(abcd_tracker, lambda m, a: m.set_value(smooth_index(rectangle_range, a))),
            run_time=run_time
        )

    def get_surface_info(
        self,
        loop_func: Callable[[float], Vect3],
        surface_color=BLUE,
        surface_opacity=0.25,
        surface_resolution=(101, 101),
        mesh_color=WHITE,
        mesh_stroke_width=0.5,
        mesh_stroke_opacity=0.1,
        mesh_resolution=(101, 101),
    ):
        surface_func = get_surface_func(loop_func)

        surface = ParametricSurface(
            get_half_parametric_func(surface_func),
            resolution=surface_resolution,
        )
        surface.set_color(surface_color, surface_opacity)
        surface.always_sort_to_camera(self.camera)

        full_surface = ParametricSurface(surface_func)
        mesh = SurfaceMesh(full_surface, resolution=mesh_resolution, normal_nudge=0)
        mesh.set_stroke(WHITE, mesh_stroke_width, mesh_stroke_opacity)
        mesh.deactivate_depth_test()

        return surface, mesh, surface_func


class TrackTheAngle(ShowTheSurface):
    initial_uv = [0.55, 0.75]
    second_uv = [0.6, 0.66]
    limiting_uv = [0.659, 0.66]

    def construct(self):
        # Initial setup
        frame = self.frame
        frame.set_height(6.5)
        frame.set_x(1.5)
        loop, pair_group = self.setup_loop()
        uv_tracker, dots, connecting_line = pair_group
        uv_tracker.set_value(self.initial_uv)
        pair_group.update()

        self.remove(pair_group)

        # Show smoothness
        x_tracker = ValueTracker(0.5)
        get_x = x_tracker.get_value
        dx = 1e-3
        line = Line(LEFT, RIGHT)
        line.set_stroke(TEAL, 4)
        line.f_always.put_start_and_end_on(
            lambda: loop.quick_point_from_proportion(get_x()),
            lambda: loop.quick_point_from_proportion(get_x() + dx)
        )
        line.always.set_length(3)

        self.add(line)
        self.play(x_tracker.animate.set_value(0.9), run_time=10)

        # Temp
        x_tracker.set_value(0)
        self.play(x_tracker.animate.set_value(0.99), run_time=25, rate_func=linear)

        # Angle label
        angle_label = self.get_angle_label(connecting_line)
        theta_label = always_redraw(lambda: self.get_theta_label(connecting_line))

        self.play(
            VFadeIn(theta_label, suspend_mobject_updating=True),
            VFadeIn(angle_label, suspend_mobject_updating=True),
            FadeOut(line),
            FadeIn(pair_group),
            loop.animate.set_stroke(WHITE, 1, 0.5)
        )

        # Move points
        self.play(
            uv_tracker.animate.set_value(self.second_uv),
            run_time=4
        )
        self.play(
            uv_tracker.animate.set_value(self.limiting_uv),
            run_time=15,
            rate_func=bezier([0, 0, 1, 1, 1, 1, 1, 1, 1]),
        )

    def setup_loop(self):
        # Setup (fairly heavily copied from above)
        axes, plane = self.get_axes_and_plane()
        plane.fade(0.5)
        self.add(plane)

        loop = self.get_loop()
        loop.set_height(5.5).center()
        loop_func = loop.quick_point_from_proportion
        self.add(loop)

        uv_tracker = ValueTracker([0, 0.5])
        dots = self.get_movable_pair(uv_tracker, loop_func, radius=0.075)
        connecting_line = self.get_connecting_line(dots)
        connecting_line.always.set_length(20)
        pair_group = Group(uv_tracker, dots, connecting_line)
        pair_group.update()

        self.add(pair_group)

        return loop, pair_group

    def get_loop(self):
        return get_example_loop(4)

    def get_angle_label(self, line):
        label = Tex(R"\theta = 100.0^\circ")
        label.next_to(self.frame.get_corner(UR), DL)
        angle = label.make_number_changeable("100.0", edge_to_fix=RIGHT)
        angle.f_always.set_value(lambda: (line.get_angle() % PI) / DEG)
        return label

    def get_theta_label(self, line):
        h_line = Line(ORIGIN, RIGHT)
        line_center = line.get_center()
        h_line.move_to(line_center, LEFT)
        angle = line.get_angle() % PI
        arc = Arc(0, angle, radius=0.25, arc_center=line_center)
        theta = Tex(R"\theta", font_size=36)
        try:
            arc_center = arc.pfp(0.5)
        except Exception:
            arc_center = arc.get_center()
        theta.move_to(arc_center + 0.8 * (arc_center - line_center))
        return VGroup(h_line, arc, theta)


class TrackTheAngleForFractal(TrackTheAngle):
    def get_loop(self, n_iters=7):
        triangle = Triangle()
        triangle.set_height(4)
        a, b, c = triangle.get_vertices()
        snowflake = VMobject().set_points_as_corners(np.vstack([
            self.get_koch_line_points(a, c, n_iters),
            self.get_koch_line_points(c, b, n_iters),
            self.get_koch_line_points(b, a, n_iters),
        ]))
        snowflake.set_stroke(WHITE, 1)

        return snowflake

    def get_koch_line_points(self, start, end, n_iters=7):
        """
        Return points for a Koch snowflake portion,
        not including the end
        """
        a, b, c, d = np.linspace(start, end, 4)
        tip = b + rotate_vector(c - b, 60 * DEG)
        if n_iters == 0:
            return np.array([a, b, tip, c])
        return np.vstack([
            self.get_koch_line_points(a, b, n_iters - 1),
            self.get_koch_line_points(b, tip, n_iters - 1),
            self.get_koch_line_points(tip, c, n_iters - 1),
            self.get_koch_line_points(c, d, n_iters - 1),
        ])


class KochZoom(TrackTheAngleForFractal):
    def construct(self):
        snowflake = self.get_loop(9)
        self.add(snowflake)
        self.play(
            self.frame.animate.reorient(0, 0, 0, (-1.12, 1.0, 0.0), 0.23),
            rate_func=bezier([0, 0, 1, 1, 1, 1, 1, 1]),
            run_time=10
        )
