# ==============================================================================
# Scene:      ReferernceSpheresFelixView
# Source:     videos/_2018/quaternions.py (lines 4123-4154)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ReferernceSpheresFelixView.py ReferernceSpheresFelixView -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def stereo_project_point(point, axis=0, r=1, max_norm=10000):
    point = fdiv(point * r, point[axis] + r)
    point[axis] = 0
    norm = get_norm(point)
    if norm > max_norm:
        point *= max_norm / norm
    return point


def stereo_project(mobject, axis=0, r=1, outer_r=10, **kwargs):
    epsilon = 1
    for submob in mobject.family_members_with_points():
        points = submob.get_points()
        n = len(points)
        for i in range(n):
            if points[i, axis] == -r:
                js = it.chain(
                    range(i + 1, n),
                    range(i - 1, -1, -1)
                )
                for j in js:
                    if points[j, axis] == -r:
                        continue
                    else:
                        vect = points[j] - points[i]
                        points[i] += epsilon * vect
                        break
        submob.apply_function(
            lambda p: stereo_project_point(p, axis, r, **kwargs)
        )

        # If all points are outside a certain range, this
        # shouldn't be displayed
        norms = np.apply_along_axis(get_norm, 1, submob.get_points())
        if np.all(norms > outer_r):
            # TODO, instead set opacity?
            # submob.get_points()[:, :] = 0
            submob.set_fill(opacity=0)
            submob.set_stroke(opacity=0)

    return mobject


class Felix(PiCreature):
    CONFIG = {
        "color": GREEN_D
    }


class CheckeredCircle(Circle):
    CONFIG = {
        "n_pieces": 16,
        "colors": [BLUE_E, BLUE_C],
        "stroke_width": 5,
    }

    def __init__(self, **kwargs):
        Circle.__init__(self, **kwargs)
        pieces = self.get_pieces(self.n_pieces)
        self.set_points(np.zeros((0, 3)))
        self.add(*pieces)
        n_colors = len(self.colors)
        for i, color in enumerate(self.colors):
            self[i::n_colors].set_color(color)


class StereoProjectedSphere(Sphere):
    CONFIG = {
        "stereo_project_config": {
            "axis": 2,
        },
        "max_r": 32,
        "max_width": FRAME_WIDTH,
        "max_height": FRAME_WIDTH,
        "max_depth": FRAME_WIDTH,
        "radius": 1,
    }

    def __init__(self, rotation_matrix=None, **kwargs):
        digest_config(self, kwargs)
        if rotation_matrix is None:
            rotation_matrix = np.identity(3)
        self.rotation_matrix = rotation_matrix

        self.stereo_project_config["r"] = self.radius
        ParametricSurface.__init__(
            self, self.post_projection_func, **kwargs
        )
        self.submobjects.sort(
            key=lambda m: -m.get_width()
        )
        self.fade_far_out_submobjects()

    def post_projection_func(self, u, v):
        point = self.radius * Sphere.func(self, u, v)
        rot_point = np.dot(point, self.rotation_matrix.T)
        result = stereo_project_point(
            rot_point, **self.stereo_project_config
        )
        epsilon = 1e-4
        if np.any(np.abs(result) == np.inf) or np.any(np.isnan(result)):
            return self.func(u + epsilon, v)
        return result

    def fade_far_out_submobjects(self, **kwargs):
        max_r = kwargs.get("max_r", self.max_r)
        max_width = kwargs.get("max_width", self.max_width)
        max_height = kwargs.get("max_height", self.max_height)
        max_depth = kwargs.get("max_depth", self.max_depth)
        for submob in self.submobjects:
            violations = [
                np.any(np.apply_along_axis(get_norm, 1, submob.get_anchors()) > max_r),
                submob.get_width() > max_width,
                submob.get_height() > max_height,
                submob.get_depth() > max_depth
            ]
            if any(violations):
                # self.remove(submob)
                submob.fade(1)
        return self


class IntroduceFelix(PiCreatureScene, SpecialThreeDScene):
    def setup(self):
        PiCreatureScene.setup(self)
        SpecialThreeDScene.setup(self)

    def construct(self):
        self.introduce_felix()
        self.add_plane()
        self.show_in_three_d()

    def introduce_felix(self):
        felix = self.felix = self.pi_creature

        arrow = Vector(DL, color=WHITE)
        arrow.next_to(felix, UR)

        label = OldTexText("Felix the Flatlander")
        label.next_to(arrow.get_start(), UP)

        self.add(felix)
        self.play(
            felix.change, "wave_1", label,
            Write(label),
            GrowArrow(arrow),
        )
        self.play(Blink(felix))
        self.play(felix.change, "thinking", label)

        self.to_fade = VGroup(label, arrow)

    def add_plane(self):
        plane = NumberPlane(y_radius=10)
        axes = self.get_axes()
        to_fade = self.to_fade
        felix = self.felix

        self.add(axes, plane, felix)
        self.play(
            ShowCreation(axes),
            ShowCreation(plane),
            FadeOut(to_fade),
        )
        self.wait()

        self.plane = plane
        self.axes = axes

    def show_in_three_d(self):
        felix = self.pi_creature
        plane = self.plane
        axes = self.axes

        # back_plane = Rectangle().replace(plane, stretch=True)
        # back_plane.shade_in_3d = True
        # back_plane.set_fill(GREY_B, opacity=0.5)
        # back_plane.set_sheen(1, UL)
        # back_plane.shift(SMALL_BUFF * IN)
        # back_plane.set_stroke(width=0)
        # back_plane = ParametricSurface(
        #     lambda u, v: u * RIGHT + v * UP
        # )
        # back_plane.replace(plane, stretch=True)
        # back_plane.set_stroke(width=0)
        # back_plane.set_fill(GREY_B, opacity=0.5)

        sphere = self.get_sphere()
        # sphere.set_fill(BLUE_E, 0.5)

        self.move_camera(
            phi=70 * DEGREES,
            theta=-110 * DEGREES,
            added_anims=[FadeOut(plane)],
            run_time=2
        )
        self.begin_ambient_camera_rotation()
        self.add(axes, sphere)
        self.play(
            Write(sphere),
            felix.change, "confused"
        )
        self.wait()

        axis_angle_pairs = [
            (RIGHT, 90 * DEGREES),
            (OUT, 45 * DEGREES),
            (UR + OUT, 120 * DEGREES),
            (RIGHT, 90 * DEGREES),
        ]
        for axis, angle in axis_angle_pairs:
            self.play(Rotate(
                sphere, angle=angle, axis=axis,
                run_time=2,
            ))
        self.wait(2)

    #
    def create_pi_creature(self):
        return Felix().move_to(4 * LEFT + 2 * DOWN)


class SphereExamplePointsDecimal(Scene):
    CONFIG = {
        "point_rotation_angle_axis_pairs": [
            (45 * DEGREES, DOWN),
            (120 * DEGREES, OUT),
            (35 * DEGREES, rotate_vector(RIGHT, 30 * DEGREES)),
            (90 * DEGREES, IN),
        ]
    }

    def construct(self):
        decimals = VGroup(*[
            DecimalNumber(
                0,
                num_decimal_places=3,
                color=color,
                include_sign=True,
                edge_to_fix=RIGHT,
            )
            for color in [YELLOW, GREEN, RED]
        ])
        number_label = VGroup(
            decimals[0], OldTex("+"),
            decimals[1], OldTex("i"), OldTex("+"),
            decimals[2], OldTex("j"),
        )
        number_label.arrange(RIGHT, buff=SMALL_BUFF)
        number_label.to_corner(UL)

        point = VectorizedPoint(OUT)

        def generate_decimal_updater(decimal, index):
            shifted_i = (index - 1) % 3
            decimal.add_updater(lambda d: d.set_value(
                point.get_location()[shifted_i]
            ))
            return decimal

        for i, decimal in enumerate(decimals):
            self.add(generate_decimal_updater(decimal, i))

        decimal_braces = VGroup()
        for decimal, char in zip(decimals, "wxy"):
            brace = Brace(decimal, DOWN, buff=SMALL_BUFF)
            label = brace.get_tex(char, buff=SMALL_BUFF)
            label.match_color(decimal)
            brace.add(label)
            decimal_braces.add(brace)

        equation = OldTex(
            "w^2 + x^2 + y^2 = 1",
            tex_to_color_map={
                "w": YELLOW,
                "x": GREEN,
                "y": RED,
            }
        )
        equation.next_to(decimal_braces, DOWN, MED_LARGE_BUFF)

        self.add(number_label)
        self.add(decimal_braces)
        self.add(equation)

        pairs = self.point_rotation_angle_axis_pairs
        for angle, axis in pairs:
            self.play(
                Rotate(point, angle, axis=axis, about_point=ORIGIN),
                run_time=2
            )
            self.wait()


class TwoDStereographicProjection(IntroduceFelix):
    CONFIG = {
        "camera_config": {
            "exponential_projection": False,
        },
        "sphere_sample_point_u_range": np.arange(
            0, PI, PI / 16,
        ),
        "sphere_sample_point_v_range": np.arange(
            0, TAU, TAU / 16,
        ),
        "n_sample_rotation_cycles": 2,
        "lift_labels": True,
    }

    def construct(self):
        self.add_parts()
        self.talk_through_sphere()
        self.draw_projection_lines()
        self.show_point_at_infinity()
        self.show_a_few_rotations()

    def add_parts(self, run_time=1):
        felix = self.felix = self.pi_creature
        felix.shift(1.5 * DL)
        axes = self.axes = self.get_axes()
        sphere = self.sphere = self.get_sphere()

        c2p = axes.coords_to_point
        labels = self.labels = VGroup(
            OldTex("i").next_to(c2p(1, 0, 0), DR, SMALL_BUFF),
            OldTex("-i").next_to(c2p(-1, 0, 0), DL, SMALL_BUFF),
            OldTex("j").next_to(c2p(0, 1, 0), UL, SMALL_BUFF),
            OldTex("-j").next_to(c2p(0, -1, 0), DL, SMALL_BUFF),
            OldTex("1").rotate(
                90 * DEGREES, RIGHT,
            ).next_to(c2p(0, 0, 1), RIGHT + OUT, SMALL_BUFF),
            OldTex("-1").rotate(
                90 * DEGREES, RIGHT,
            ).next_to(c2p(0, 0, -1), RIGHT + IN, SMALL_BUFF),
        )
        if self.lift_labels:
            for sm in labels[:4].family_members_with_points():
                sm.add(VectorizedPoint(
                    0.25 * DOWN + 0.25 * OUT
                ))
        labels.set_stroke(width=0, background=True)
        for submob in labels.get_family():
            submob.shade_in_3d = True

        self.add(felix, axes, sphere, labels)
        self.move_camera(
            **self.get_default_camera_position(),
            run_time=run_time
        )
        self.begin_ambient_camera_rotation(rate=0.01)
        self.play(
            felix.change, "pondering", sphere,
            run_time=run_time,
        )

    def talk_through_sphere(self):
        point = VectorizedPoint(OUT)
        arrow = Vector(IN, shade_in_3d=True)
        arrow.set_fill(PINK)
        arrow.set_stroke(BLACK, 1)

        def get_dot():
            dot = Sphere(radius=0.05, u_max=PI / 2)
            dot.set_fill(PINK)
            dot.set_stroke(width=0)
            dot.move_to(2.05 * OUT)
            dot.apply_matrix(
                z_to_vector(normalize(point.get_location())),
                about_point=ORIGIN
            )
            return dot

        dot = get_dot()
        dot.add_updater(
            lambda d: d.become(get_dot())
        )

        def update_arrow(arrow):
            target_point = 2.1 * point.get_location()
            rot_matrix = np.dot(
                z_to_vector(normalize(target_point)),
                np.linalg.inv(
                    z_to_vector(normalize(-arrow.get_vector()))
                )
            )
            arrow.apply_matrix(rot_matrix)
            arrow.shift(target_point - arrow.get_end())
            return arrow
        arrow.add_updater(update_arrow)

        self.add(self.sphere, dot, arrow)
        pairs = SphereExamplePointsDecimal.CONFIG.get(
            "point_rotation_angle_axis_pairs"
        )
        for angle, axis in pairs:
            self.play(
                Rotate(point, angle, axis=axis, about_point=ORIGIN),
                run_time=2
            )
            self.wait()
        self.play(FadeOut(dot), FadeOut(arrow))

    def draw_projection_lines(self):
        sphere = self.sphere
        axes = self.axes
        radius = sphere.get_width() / 2

        neg_one_point = axes.coords_to_point(0, 0, -1)
        neg_one_dot = Dot(
            neg_one_point,
            color=YELLOW,
            shade_in_3d=True
        )

        xy_plane = StereoProjectedSphere(
            u_max=15 * PI / 16,
            **self.sphere_config
        )
        xy_plane.set_fill(WHITE, 0.25)
        xy_plane.set_stroke(width=0)

        point_mob = VectorizedPoint(2 * OUT)
        point_mob.add_updater(
            lambda m: m.move_to(radius * normalize(m.get_center()))
        )
        point_mob.move_to([1, -1, 1])
        point_mob.update(0)

        def get_projection_line(sphere_point):
            to_sphere = Line(neg_one_point, sphere_point)
            to_plane = Line(
                sphere_point,
                self.project_point(sphere_point)
            )
            line = VGroup(to_sphere, to_plane)
            line.set_stroke(YELLOW, 3)
            for submob in line:
                submob.shade_in_3d = True
            return line

        def get_sphere_dot(sphere_point):
            dot = Dot()
            dot.set_shade_in_3d(True)
            dot.set_fill(PINK)
            dot.shift(OUT)
            dot.apply_matrix(
                z_to_vector(sphere_point),
                about_point=ORIGIN,
            )
            dot.move_to(1.01 * sphere_point)
            dot.add(VectorizedPoint(5 * sphere_point))
            return dot

        def get_projection_dot(sphere_point):
            projection = self.project_point(sphere_point)
            dot = Dot(projection, shade_in_3d=True)
            dot.add(VectorizedPoint(dot.get_center() + 0.1 * OUT))
            dot.set_fill(WHITE)
            return dot

        point = point_mob.get_location()
        dot = get_sphere_dot(point)
        line = get_projection_line(point)
        projection_dot = get_projection_dot(point)

        sample_points = [
            radius * sphere.func(u, v)
            for u in self.sphere_sample_point_u_range
            for v in self.sphere_sample_point_v_range
        ]

        lines = VGroup(*[get_projection_line(p) for p in sample_points])
        lines.set_stroke(width=1)
        north_lines = lines[:len(lines) // 2]
        south_lines = lines[len(lines) // 2:]

        self.add(xy_plane, sphere)
        self.play(Write(xy_plane))
        self.wait(2)
        self.play(sphere.set_fill, BLUE_E, 0.5)
        self.play(FadeInFromLarge(dot))
        self.play(
            FadeIn(neg_one_dot),
            ShowCreation(line),
        )
        self.wait(2)
        self.play(ReplacementTransform(
            dot.copy(), projection_dot
        ))

        def get_point():
            return 2 * normalize(point_mob.get_location())

        dot.add_updater(
            lambda d: d.become(get_sphere_dot(get_point()))
        )
        line.add_updater(
            lambda l: l.become(get_projection_line(get_point()))
        )
        projection_dot.add_updater(
            lambda d: d.become(get_projection_dot(get_point()))
        )

        self.play(
            point_mob.move_to,
            radius * normalize(np.array([1, -1, -1])),
            run_time=3
        )
        self.move_camera(
            theta=-150 * DEGREES,
            run_time=3
        )
        self.add(axes, sphere, xy_plane, dot, line)
        for point in np.array([-2, 1, -0.5]), np.array([-0.01, -0.01, 1]):
            self.play(
                point_mob.move_to,
                radius * normalize(point),
                run_time=3
            )
        self.wait(2)

        # Project norther hemisphere
        north_hemisphere = self.get_sphere()
        n = len(north_hemisphere)
        north_hemisphere.remove(*north_hemisphere[n // 2:])
        north_hemisphere.generate_target()
        self.project_mobject(north_hemisphere.target)
        north_hemisphere.set_fill(opacity=0.8)

        self.play(
            LaggedStartMap(ShowCreation, north_lines),
            FadeIn(north_hemisphere)
        )
        self.play(
            MoveToTarget(north_hemisphere),
            run_time=3,
            rate_func=lambda t: smooth(0.99 * t)
        )
        self.play(FadeOut(north_lines))
        self.wait(2)

        # Unit circle
        circle = Sphere(
            radius=2.01,
            u_min=PI / 2 - 0.01,
            u_max=PI / 2 + 0.01,
            resolution=(1, 24),
        )
        for submob in circle:
            submob.add(VectorizedPoint(1.5 * submob.get_center()))
        circle.set_fill(YELLOW)
        circle_path = Circle(radius=2)
        circle_path.rotate(-90 * DEGREES)

        self.play(FadeInFromLarge(circle))
        self.play(point_mob.move_to, circle_path.get_points()[0])
        self.play(MoveAlongPath(point_mob, circle_path, run_time=6))
        self.move_camera(
            phi=0,
            theta=-90 * DEGREES,
            rate_func=there_and_back_with_pause,
            run_time=6,
        )
        self.play(point_mob.move_to, OUT)
        self.wait()

        # Southern hemisphere
        south_hemisphere = self.get_sphere()
        n = len(south_hemisphere)
        south_hemisphere.remove(*south_hemisphere[:n // 2])
        south_hemisphere.remove(
            *south_hemisphere[-sphere.get_resolution()[1]:]
        )
        south_hemisphere.generate_target()
        self.project_mobject(south_hemisphere.target)
        south_hemisphere.set_fill(opacity=0.8)
        south_hemisphere.target[-sphere.get_resolution()[1] // 2:].set_fill(
            opacity=0
        )

        self.play(
            LaggedStartMap(ShowCreation, south_lines),
            FadeIn(south_hemisphere)
        )
        self.play(
            MoveToTarget(south_hemisphere),
            FadeOut(south_lines),
            FadeOut(xy_plane),
            run_time=3,
            rate_func=lambda t: smooth(0.99 * t)
        )
        self.wait(3)

        self.projected_sphere = VGroup(
            north_hemisphere,
            south_hemisphere,
        )
        self.equator = circle
        self.point_mob = point_mob

    def show_point_at_infinity(self):
        points = list(compass_directions(
            12, start_vect=rotate_vector(RIGHT, 3.25 * DEGREES)
        ))
        points.pop(7)
        points.pop(2)
        arrows = VGroup(*[
            Arrow(6 * p, 11 * p)
            for p in points
        ])
        arrows.set_fill(RED)
        arrows.set_stroke(RED, 5)
        neg_ones = VGroup(*[
            OldTex("-1").next_to(arrow.get_start(), -p)
            for p, arrow in zip(points, arrows)
        ])
        neg_ones.set_stroke(width=0, background=True)

        sphere_arcs = VGroup()
        for angle in np.arange(0, TAU, TAU / 12):
            arc = Arc(PI, radius=2)
            arc.set_stroke(RED)
            arc.rotate(PI / 2, axis=DOWN, about_point=ORIGIN)
            arc.rotate(angle, axis=OUT, about_point=ORIGIN)
            sphere_arcs.add(arc)
        sphere_arcs.set_stroke(RED)

        self.play(
            LaggedStartMap(GrowArrow, arrows),
            LaggedStartMap(Write, neg_ones)
        )
        self.wait(3)
        self.play(
            FadeOut(self.projected_sphere),
            FadeOut(arrows),
            FadeOut(neg_ones),
        )
        for x in range(2):
            self.play(
                ShowCreationThenDestruction(
                    sphere_arcs,
                    lag_ratio=0,
                    run_time=3,
                )
            )

    def show_a_few_rotations(self):
        sphere = self.sphere
        felix = self.felix
        point_mob = self.point_mob
        point_mob.add_updater(
            lambda m: m.move_to(sphere.get_all_points()[0])
        )
        coord_point_mobs = VGroup(
            VectorizedPoint(RIGHT),
            VectorizedPoint(UP),
            VectorizedPoint(OUT),
        )
        for pm in coord_point_mobs:
            pm.shade_in_3d = True

        def get_rot_matrix():
            return np.array([
                pm.get_location()
                for pm in coord_point_mobs
            ]).T

        def get_projected_sphere():
            result = StereoProjectedSphere(
                get_rot_matrix(),
                max_r=10,
                **self.sphere_config,
            )
            result.set_fill(opacity=0.2)
            result.fade_far_out_submobjects(max_r=32)
            for submob in result:
                if submob.get_center()[1] < -11:
                    submob.fade(1)
            return result

        projected_sphere = get_projected_sphere()
        projected_sphere.add_updater(
            lambda m: m.become(get_projected_sphere())
        )

        def get_projected_equator():
            equator = CheckeredCircle(
                n_pieces=24,
                radius=2,
            )
            for submob in equator.get_family():
                submob.shade_in_3d = True
            equator.set_stroke(YELLOW, 5)
            equator.apply_matrix(get_rot_matrix())
            self.project_mobject(equator)
            return equator

        projected_equator = get_projected_equator()
        projected_equator.add_updater(
            lambda m: m.become(get_projected_equator())
        )

        self.add(sphere, projected_sphere)
        self.move_camera(phi=60 * DEGREES)
        self.play(
            sphere.set_fill_by_checkerboard,
            BLUE_E, BLUE_D, {"opacity": 0.8},
            FadeIn(projected_sphere)
        )
        sphere.add(coord_point_mobs)
        sphere.add(self.equator)
        self.add(projected_equator)
        pairs = self.get_sample_rotation_angle_axis_pairs()
        for x in range(self.n_sample_rotation_cycles):
            for angle, axis in pairs:
                self.play(
                    Rotate(
                        sphere, angle=angle, axis=axis,
                        about_point=ORIGIN,
                        run_time=3,
                    ),
                    felix.change, "confused",
                )
                self.wait()

        self.projected_sphere = projected_sphere

    #
    def project_mobject(self, mobject):
        return stereo_project(mobject, axis=2, r=2, outer_r=20)

    def project_point(self, point):
        return stereo_project_point(point, axis=2, r=2)

    def get_sample_rotation_angle_axis_pairs(self):
        return SphereExamplePointsDecimal.CONFIG.get(
            "point_rotation_angle_axis_pairs"
        )


class ShowRotationsJustWithReferenceCircles(TwoDStereographicProjection):
    CONFIG = {
        "flat_view": False,
    }

    def construct(self):
        self.add_parts(run_time=1)
        self.begin_ambient_camera_rotation(rate=0.03)
        self.edit_parts()
        self.show_1i_circle()
        self.show_1j_circle()
        self.show_random_circle()
        self.show_rotations()

    def edit_parts(self):
        sphere = self.sphere
        axes = self.axes
        axes.set_stroke(width=1)
        xy_plane = StereoProjectedSphere(u_max=15 * PI / 16)
        xy_plane.set_fill(WHITE, 0.2)
        xy_plane.set_stroke(width=0, opacity=0)

        self.add(xy_plane, sphere)
        self.play(
            FadeIn(xy_plane),
            sphere.set_fill, BLUE_E, {"opacity": 0.2},
            sphere.set_stroke, {"width": 0.1, "opacity": 0.5}
        )

    def show_1i_circle(self):
        axes = self.axes

        circle = self.get_circle(GREEN_E, GREEN)
        circle.rotate(TAU / 4, RIGHT)
        circle.rotate(TAU / 4, DOWN)

        projected = self.get_projected_circle(circle)

        labels = VGroup(*map(Tex, ["0", "2i", "3i"]))
        labels.set_shade_in_3d(True)
        if self.flat_view:
            labels.fade(1)
        for label, x in zip(labels, [0, 2, 3]):
            label.next_to(
                axes.coords_to_point(x, 0, 0), DR, SMALL_BUFF
            )

        self.play(ShowCreation(circle, run_time=3))
        self.wait()
        self.play(ReplacementTransform(
            circle.copy(), projected,
            run_time=3
        ))
        # self.axes.x_axis.pieces.set_stroke(width=0)
        self.wait(7)
        self.move_camera(
            phi=60 * DEGREES,
        )
        self.play(
            LaggedStartMap(
                FadeInFrom, labels,
                lambda m: (m, UP)
            )
        )
        self.wait(2)
        self.play(FadeOut(labels))

        self.one_i_circle = circle
        self.projected_one_i_circle = projected

    def show_1j_circle(self):
        circle = self.get_circle(RED_E, RED)
        circle.rotate(TAU / 4, DOWN)

        projected = self.get_projected_circle(circle)

        self.move_camera(theta=-170 * DEGREES)
        self.play(ShowCreation(circle, run_time=3))
        self.wait()
        self.play(ReplacementTransform(
            circle.copy(), projected, run_time=3
        ))
        # self.axes.y_axis.pieces.set_stroke(width=0)
        self.wait(3)

        self.one_j_circle = circle
        self.projected_one_j_circle = projected

    def show_random_circle(self):
        sphere = self.sphere

        circle = self.get_circle(BLUE_E, BLUE)
        circle.set_width(2 * sphere.radius * np.sin(30 * DEGREES))
        circle.shift(sphere.radius * np.cos(30 * DEGREES) * OUT)
        circle.rotate(150 * DEGREES, UP, about_point=ORIGIN)

        projected = self.get_projected_circle(circle)

        self.play(ShowCreation(circle, run_time=2))
        self.wait()
        self.play(ReplacementTransform(
            circle.copy(), projected,
            run_time=2
        ))
        self.wait(3)
        self.play(
            FadeOut(circle),
            FadeOut(projected),
        )

    def show_rotations(self):
        sphere = self.sphere
        c1i = self.one_i_circle
        pc1i = self.projected_one_i_circle
        c1j = self.one_j_circle
        pc1j = self.projected_one_j_circle
        cij = self.get_circle(YELLOW_E, YELLOW)
        pcij = self.get_projected_circle(cij)

        circles = VGroup(c1i, c1j, cij)
        x_axis = self.axes.x_axis
        y_axis = self.axes.y_axis

        arrow = Arrow(
            2 * RIGHT, 2 * UP,
            buff=SMALL_BUFF,
            path_arc=PI,
        )
        arrow.set_stroke(GREY_B, 3)
        arrow.tip.set_fill(GREY_B)
        arrows = VGroup(arrow, *[
            arrow.copy().rotate(angle, about_point=ORIGIN)
            for angle in np.arange(TAU / 4, TAU, TAU / 4)
        ])
        arrows.rotate(TAU / 4, RIGHT, about_point=ORIGIN)
        arrows.rotate(TAU / 2, OUT, about_point=ORIGIN)
        arrows.rotate(TAU / 4, UP, about_point=ORIGIN)
        arrows.space_out_submobjects(1.2)

        self.play(FadeInFromLarge(cij))
        sphere.add(circles)

        pc1i.add_updater(
            lambda c: c.become(self.get_projected_circle(c1i))
        )
        pc1j.add_updater(
            lambda c: c.become(self.get_projected_circle(c1j))
        )
        pcij.add_updater(
            lambda c: c.become(self.get_projected_circle(cij))
        )
        self.add(pcij)

        # About j-axis
        self.play(ShowCreation(arrows, run_time=3, rate_func=linear))
        self.wait(3)
        for x in range(2):
            y_axis.pieces.set_stroke(width=1)
            self.play(
                Rotate(sphere, 90 * DEGREES, axis=UP),
                run_time=4,
            )
            y_axis.pieces.set_stroke(width=0)
            self.wait(2)

        # About i axis
        self.move_camera(theta=-45 * DEGREES)
        self.play(Rotate(arrows, TAU / 4, axis=OUT))
        self.wait(2)
        for x in range(2):
            x_axis.pieces.set_stroke(width=1)
            self.play(
                Rotate(sphere, -90 * DEGREES, axis=RIGHT),
                run_time=4,
            )
            x_axis.pieces.set_stroke(width=0)
            self.wait(2)
        self.wait(2)

        # About real axis
        self.move_camera(
            theta=-135 * DEGREES,
            added_anims=[FadeOut(arrows)]
        )
        self.ambient_camera_rotation.rate = 0.01
        for x in range(2):
            x_axis.pieces.set_stroke(width=1)
            y_axis.pieces.set_stroke(width=1)
            self.play(
                Rotate(sphere, 90 * DEGREES, axis=OUT),
                run_time=4,
            )
            # x_axis.pieces.set_stroke(width=0)
            # y_axis.pieces.set_stroke(width=0)
            self.wait(2)

    #
    def get_circle(self, *colors):
        sphere = self.sphere
        circle = CheckeredCircle(colors=colors, n_pieces=48)
        circle.set_shade_in_3d(True)
        circle.match_width(sphere)
        if self.flat_view:
            circle[::2].fade(1)

        return circle

    def get_projected_circle(self, circle):
        result = circle.deepcopy()
        self.project_mobject(result)
        result[::2].fade(1)
        for sm in result:
            if sm.get_width() > FRAME_WIDTH:
                sm.fade(1)
            if sm.get_height() > FRAME_HEIGHT:
                sm.fade(1)
        return result


class ReferernceSpheresFelixView(ShowRotationsJustWithReferenceCircles):
    CONFIG = {
        "flat_view": True,
        "lift_labels": False,
    }

    def add_parts(self, **kwargs):
        ShowRotationsJustWithReferenceCircles.add_parts(self, **kwargs)
        one = OldTex("1")
        one.next_to(ORIGIN, DR, SMALL_BUFF)
        self.add(one)

    def get_default_camera_position(self):
        return {}

    def move_camera(self, **kwargs):
        kwargs["phi"] = 0
        kwargs["theta"] = -90 * DEGREES
        ShowRotationsJustWithReferenceCircles.move_camera(self, **kwargs)

    def begin_ambient_camera_rotation(self, rate):
        self.ambient_camera_rotation = VectorizedPoint()

    def capture_mobjects_in_camera(self, mobjects, **kwargs):
        mobs_on_xy = [
            sm
            for sm in self.camera.extract_mobject_family_members(
                mobjects, only_those_with_points=True
            )
            if abs(sm.get_center()[2]) < 0.001
        ]
        return Scene.capture_mobjects_in_camera(self, mobs_on_xy, **kwargs)
