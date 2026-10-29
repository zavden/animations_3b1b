# ==============================================================================
# Scene:      SphereSectorAnalysis
# Source:     videos/_2022/visual_proofs/lies.py (lines 627-851)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SphereSectorAnalysis.py SphereSectorAnalysis -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - ParametricCurve t_range=(0, dtheta) -> (0, dtheta, 0.01): requires 3 values
# ==============================================================================

from manim_imports_ext import *

EQUATOR_STYLE = dict(stroke_color=TEAL, stroke_width=2)


def get_sphere_slices(radius=1.0, n_slices=20):
    delta_theta = TAU / n_slices
    north_slices = Group(*(
        ParametricSurface(
            uv_func=lambda u, v: [
                radius * math.sin(v) * math.cos(u),
                radius * math.sin(v) * math.sin(u),
                radius * math.cos(v),
            ],
            u_range=[theta, theta + delta_theta],
            v_range=[0, PI / 2],
            resolution=(4, 25),
        )
        for theta in np.arange(0, TAU, delta_theta)
    ))
    north_slices.set_x(0)
    color_slices(north_slices)

    equator = Circle(**EQUATOR_STYLE)
    equator.insert_n_curves(100)
    equator.match_width(north_slices)
    equator.move_to(ORIGIN)
    equator.apply_depth_test()

    return Group(north_slices, get_south_slices(north_slices, dim=2), equator)


def color_slices(slices, colors=(BLUE_D, BLUE_E)):
    for slc, color in zip(slices, it.cycle([BLUE_D, BLUE_E])):
        slc.set_color(color)
    return slices


def get_south_slices(north_slices, dim):
    ss = north_slices.copy().stretch(-1, dim, about_point=ORIGIN)
    for slc in ss:
        slc.reverse_points()
    return ss


class SphereSectorAnalysis(Scene):
    n_slices = 20

    def construct(self):
        # Setup
        radius = 2.0
        frame = self.camera.frame
        frame.reorient(10, 60)

        axes = ThreeDAxes()
        axes.insert_n_curves(20)
        axes.set_stroke(GREY_B, 1)
        axes.apply_depth_test()

        sphere = Sphere(radius=radius)
        mesh = SurfaceMesh(sphere, resolution=(self.n_slices + 1, 3))
        mesh.set_stroke(BLUE_E, 1)
        slices = get_sphere_slices(radius=radius, n_slices=self.n_slices)
        slices[2].scale(1.007)
        slices.rotate(-90 * DEGREES, OUT)

        self.add(axes)
        self.add(slices, mesh)
        self.play(
            ShowCreation(slices, lag_ratio=0.05),
            frame.animate.reorient(-10, 70),
            run_time=2,
        )
        self.add(slices, mesh)
        self.wait()

        # Isolate one slice
        self.play(
            slices[0][1:].animate.set_opacity(0.1),
            slices[1].animate.set_opacity(0.1),
        )
        self.wait()

        # Preview varying width
        dtheta = TAU / self.n_slices
        phi_tracker = ValueTracker(45 * DEGREES)
        get_phi = phi_tracker.get_value

        def get_width_line():
            return ParametricCurve(
                lambda t: radius * np.array([
                    math.sin(t) * math.sin(get_phi()),
                    -math.cos(t) * math.sin(get_phi()),
                    math.cos(get_phi()),
                ]),
                # CHANGE: t_range requires (min, max, step)
                t_range=(0, dtheta, 0.01),
                stroke_color=RED,
                stroke_width=2,
            )

        width_line = get_width_line()
        width_label = Text("Width", color=RED)
        width_label.rotate(90 * DEGREES, RIGHT)
        width_label.set_stroke(BLACK, 1, background=True)
        width_label.add_updater(lambda m: m.next_to(width_line, OUT, buff=SMALL_BUFF).set_width(1.5 * width_line.get_width() + 1e-2))

        self.play(ShowCreation(width_line), Write(width_label))
        self.wait()
        width_line.add_updater(lambda m: m.match_points(get_width_line()))
        for angle in 0, PI / 2, 0:
            self.play(phi_tracker.animate.set_value(angle), run_time=2)
        self.play(FadeOut(width_label))
        self.wait()

        # Reorient
        slices.generate_target()
        mesh.generate_target()
        for mob in slices, mesh:
            for submob in mob.target.family_members_with_points():
                if submob.get_x() < -0.1:
                    submob.set_opacity(0)

        self.add(slices, width_line)
        self.play(
            frame.animate.reorient(-65, 65),
            MoveToTarget(slices),
            MoveToTarget(mesh),
            slices[2].animate.set_stroke(width=0),
            run_time=2,
        )
        frame.add_updater(lambda f, dt: f.increment_theta(0.01 * dt))

        # Show phi angle
        def get_sphere_point():
            return radius * (math.cos(get_phi()) * OUT + math.sin(get_phi()) * DOWN)

        def get_radial_line():
            return Line(
                ORIGIN, get_sphere_point(),
                stroke_color=YELLOW,
                stroke_width=2,
            )

        phi_label = OldTex("\\phi", font_size=30)

        def get_angle_label():
            arc = Arc(start_angle=90 * DEGREES, angle=-get_phi(), radius=0.5, n_components=8)
            arc.set_stroke(WHITE, 2)
            arc.set_fill(opacity=0)
            label = phi_label.copy()
            label.next_to(arc.pfp(0.5), UP, buff=SMALL_BUFF)
            result = VGroup(arc, label)
            result.rotate(90 * DEGREES, RIGHT, about_point=ORIGIN)
            result.rotate(90 * DEGREES, IN, about_point=ORIGIN)
            return result

        def get_lat_line_radius():
            point = get_sphere_point()
            return Line(point[2] * OUT, point, stroke_color=PINK, stroke_width=2)

        def get_lat_line():
            result = Circle(radius=radius * math.sin(get_phi()))
            result.set_stroke(RED, 1, opacity=0.5)
            result.set_z(get_sphere_point()[2])
            return result

        radial_line = get_radial_line()
        radial_line.add_updater(lambda m: m.match_points(get_radial_line()))
        angle_label = get_angle_label()
        angle_label[0].add_updater(lambda m: m.match_points(get_angle_label()[0]).set_stroke(WHITE, 2).set_fill(opacity=0))
        angle_label[1].add_updater(lambda m: m.move_to(get_angle_label()[1]))
        lat_line_radius = get_lat_line_radius()
        lat_line_radius.add_updater(lambda m: m.match_points(get_lat_line_radius()))
        lat_line_label = OldTex("R\\sin(\\phi)", font_size=24)
        lat_line_label.rotate(90 * DEGREES, RIGHT).rotate(90 * DEGREES, IN)
        lat_line_label.next_to(lat_line_radius, OUT, SMALL_BUFF)

        self.play(ShowCreation(radial_line))
        self.play(
            phi_tracker.animate.set_value(30 * DEGREES),
            UpdateFromAlphaFunc(angle_label, lambda m, a: m.update().set_opacity(a)),
        )
        self.wait()
        self.play(
            phi_tracker.animate.set_value(75 * DEGREES),
            run_time=3,
        )
        self.play(phi_tracker.animate.set_value(45 * DEGREES), run_time=2)
        self.wait()

        lat_line_label.add_updater(lambda m: m.next_to(lat_line_radius, OUT, SMALL_BUFF))
        self.play(
            ShowCreation(lat_line_radius),
            Write(lat_line_label)
        )
        self.wait()

        lat_line = get_lat_line()
        lat_line.add_updater(lambda m: m.match_points(get_lat_line()))
        self.play(ShowCreation(lat_line))
        self.wait()

        # Show delta theta
        brace = Brace(Line(ORIGIN, radius * dtheta * RIGHT), UP, buff=SMALL_BUFF)
        delta_theta = OldTex("\\Delta \\theta", font_size=36)
        delta_theta.next_to(brace, UP, buff=SMALL_BUFF)
        dt_label = VGroup(brace, delta_theta)
        dt_label.rotate(90 * DEGREES, RIGHT)
        dt_label.next_to(radius * DOWN, OUT, buff=0)
        dt_label.rotate(0.5 * dtheta, OUT, about_point=ORIGIN)

        self.play(Write(dt_label), frame.animate.set_theta(-30 * DEGREES))
        self.wait()

        # Exact formula
        formula1 = OldTex("2\\pi", " R \\sin(\\phi)", "\\cdot", "{\\Delta \\theta", " \\over 2\\pi}")
        formula2 = OldTex("R \\sin(\\phi)", "\\cdot", "\\Delta \\theta")
        for formula in formula1, formula2:
            formula.to_corner(UR)
            formula.fix_in_frame()

        self.play(Write(formula1))
        self.wait()
        self.play(
            FadeTransform(formula1[1], formula2[0]),
            FadeTransform(formula1[2], formula2[1]),
            FadeTransform(formula1[3], formula2[2]),
            FadeOut(formula1[0]),
            FadeOut(formula1[4:]),
        )
        self.wait()

        # Graph
        axes = Axes(
            (0, PI, PI / 4),
            (0, 1, 1 / 2),
            height=1,
            width=PI,
        )
        axes.y_axis.add(Text("Wedge width", font_size=24, color=RED).next_to(axes.c2p(0, 1), LEFT))
        axes.x_axis.add(OldTex("\\pi / 2", font_size=24).next_to(axes.c2p(PI / 2, 0), DOWN))
        axes.x_axis.add(OldTex("\\pi", font_size=24).next_to(axes.c2p(PI, 0), DOWN))
        axes.x_axis.add(OldTex("\\phi", font_size=24).next_to(axes.c2p(PI, 0), UR, buff=SMALL_BUFF))
        axes.to_corner(UL)
        axes.fix_in_frame()
        graph = axes.get_graph(lambda x: math.sin(x), x_range=[0, PI / 2])
        graph.set_stroke(RED, 2)
        graph.fix_in_frame()
        dot = Dot()
        dot.scale(0.25)
        dot.fix_in_frame()

        self.play(FadeIn(axes), frame.animate.set_theta(-50 * DEGREES))
        self.wait()
        self.play(phi_tracker.animate.set_value(0))
        self.wait()
        graph_copy = graph.copy()
        self.play(
            phi_tracker.animate.set_value(90 * DEGREES),
            ShowCreation(graph),
            UpdateFromAlphaFunc(dot, lambda d, a: d.move_to(graph_copy.pfp(a))),
            run_time=6,
        )
        self.wait()
        self.play(
            phi_tracker.animate.set_value(45 * DEGREES),
            UpdateFromAlphaFunc(dot, lambda d, a: d.move_to(graph.pfp(1 - 0.5 * a))),
            run_time=3,
        )
        self.wait()
