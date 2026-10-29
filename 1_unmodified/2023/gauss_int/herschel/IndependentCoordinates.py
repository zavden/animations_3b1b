# ==============================================================================
# Scene:      IndependentCoordinates
# Source:     videos/_2023/gauss_int/herschel.py (lines 218-283)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl IndependentCoordinates.py IndependentCoordinates -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class TwoDGaussianAsADistribution(InteractiveScene):
    n_points = 2000
    n_dots_per_moment = 10

    def construct(self):
        # Setup
        frame = self.frame
        plane = self.get_plane()
        plane.set_flat_stroke(False)
        self.add(plane)

        dartboard = self.get_dartboard(plane)
        dartboard.save_state()
        dartboard.set_opacity(0)
        self.add(dartboard)

        self.add_random_points_anim(plane)
        self.wait(10)
        self.play(Restore(dartboard))
        self.wait(10)

        # Graph
        def func(u, v, sigma=1):
            return np.exp(-(u**2 + v**2) / sigma**2) / sigma

        graphs = []
        for sigma in [0.8, 1.0, 0.6]:
            graph = ParametricSurface(lambda u, v: [u, v, func(u, v, sigma)], u_range=(-2, 2), v_range=(-2, 2))
            graph.match_width(plane.axes)
            graph.set_color(BLUE_E, 0.5)
            graph.move_to(plane.axes, IN)
            graph.always_sort_to_camera(self.camera)

            mesh = VGroup(*plane.background_lines.copy(), plane.faded_lines.copy())
            mesh.insert_n_curves(50)
            mesh.start = mesh.copy().set_opacity(0)
            mesh.save_state()
            mesh.saved_state.set_opacity(0)
            unit_size = plane.x_axis.get_unit_size()
            for submob in mesh.family_members_with_points():
                submob.set_points([
                    p + unit_size * func(*plane.p2c(p), sigma) * OUT
                    for p in submob.get_points()
                ])
                submob.set_stroke(
                    WHITE,
                    width=0.5 * submob.get_stroke_width(),
                    opacity=0.5 * submob.get_stroke_opacity()
                )
            mesh.shift(0.01 * OUT)
            graphs.append(Group(graph, mesh))

        graph1, graph2, graph3 = graphs

        # Test
        self.add(graph1)
        graph1[0].set_opacity(0)
        self.play(
            frame.animate.reorient(20, 70),
            graph1[0].animate.set_opacity(0.5),
            TransformFromCopy(graph1[1].start, graph1[1]),
            run_time=3
        )
        self.play(
            frame.animate.reorient(-20),
            run_time=7,
        )
        graph1.save_state()
        self.play(Transform(graph1, graph2), run_time=2)
        self.play(Transform(graph1, graph3), run_time=2)
        self.play(Restore(graph1), run_time=2)
        self.wait(2)

        self.play(
            FadeOut(graph1[0]),
            Restore(graph1[1]),
            frame.animate.reorient(0, 0),
            run_time=3,
        )

        # Radial symmetry
        blob = Circle(radius=0.2)
        blob.set_stroke(TEAL, 2)
        blob.set_fill(TEAL, 0.5)
        blob.move_to(plane.c2p(0.5, 0.5))

        arrow = FillArrow(ORIGIN, DL)
        arrow.next_to(blob, UR, buff=0)
        arrow.set_fill(RED, 1)
        arrow.set_backstroke(width=2)

        radial_line = DashedLine(plane.c2p(0, 0), blob.get_center(), dash_length=0.025)
        radial_line.set_stroke(TEAL, 2)

        self.play(
            dartboard.animate.set_opacity(0.2),
            DrawBorderThenFill(blob),
            GrowArrow(arrow)
        )
        self.wait()
        self.play(ShowCreation(radial_line))
        self.play(
            Rotate(blob, TAU, about_point=plane.get_origin(), run_time=6),
            Rotate(radial_line, TAU, about_point=plane.get_origin(), run_time=6),
            MaintainPositionRelativeTo(arrow, blob),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeOut, VGroup(blob, arrow, radial_line)),
            dartboard.animate.set_opacity(0.75)
        )
        self.play(
            self.frame.animate.set_gamma(-0.75 * PI),
            rate_func=there_and_back,
            run_time=6,
        )
        self.wait()

        # Ambient randomness
        self.wait(0.1 * self.n_points)

    def get_plane(self):
        plane = NumberPlane(
            (-2, 2), (-2, 2),
            background_line_style=dict(stroke_color=GREY, stroke_width=1, stroke_opacity=1)
        )
        plane.set_height(7)
        plane.to_edge(DOWN, buff=0.25)
        plane.add(Tex("x").next_to(plane.x_axis.get_right(), RIGHT, SMALL_BUFF))
        plane.add(Tex("y").next_to(plane.y_axis.get_top(), UP, SMALL_BUFF))
        return plane

    def get_dartboard(self, plane):
        dartboard = Dartboard()
        dartboard.match_height(plane.axes)
        dartboard.move_to(plane.axes)
        dartboard.set_opacity(0.75)
        return dartboard

    def add_random_points_anim(self, plane):
        coords = np.random.normal(0, 0.5, (self.n_points, 2))
        dots = Group(*(
            GlowDot(plane.c2p(x, y), glow_factor=4.0, radius=0.3)
            for x, y in coords
        ))

        anim = LaggedStart(*(
            FadeIn(dot, rate_func=there_and_back)
            for dot in dots
        ), lag_ratio=1 / self.n_dots_per_moment, run_time=self.n_points / self.n_dots_per_moment)

        anim_mob = turn_animation_into_updater(anim)
        self.add(anim_mob)


class IndependentCoordinates(TwoDGaussianAsADistribution):
    n_iterations = 20
    random_seed = 1

    def construct(self):
        frame = self.frame
        plane = self.get_plane()
        dartboard = self.get_dartboard(plane)
        dartboard.set_opacity(0.15)
        self.add(plane, dartboard)

        x_tip = ArrowTip(angle=90 * DEGREES).scale(0.5).set_color(BLUE)
        y_tip = ArrowTip(angle=0).scale(0.5).set_color(YELLOW)
        x_tip.move_to(plane.get_origin(), UP)
        y_tip.move_to(plane.get_origin(), RIGHT)
        for tip in x_tip, y_tip:
            tip.set_opacity(0)
            tip.save_state()

        for n in range(self.n_iterations):
            # Test
            x_tip.restore()
            y_tip.restore()

            # xs = np.random.normal(0, 1, 10)
            # ys = np.random.normal(0, 1, 10)
            # x = xs[-2]
            # y = ys[-2]
            x = np.random.normal(0, 0.5)
            y = np.random.normal(0, 0.5)

            if y < 0:
                x_tip.flip(RIGHT, about_point=plane.get_origin())
            if x < 0:
                y_tip.flip(UP, about_point=plane.get_origin())

            lines = VGroup(
                DashedLine(plane.c2p(x, 0), plane.c2p(x, y), dash_length=0.05),
                DashedLine(plane.c2p(0, y), plane.c2p(x, y), dash_length=0.05),
            )
            lines.set_stroke(WHITE, 2)

            dot = GlowDot().move_to(plane.c2p(x, y))

            self.play(LaggedStart(
                x_tip.animate.match_x(dot).set_opacity(1),
                y_tip.animate.match_y(dot).set_opacity(1),
                lag_ratio=0.5,
            ))
            self.play(
                *map(ShowCreation, lines),
                FadeIn(dot),
                run_time=0.5
            )
            self.wait(0.5)
            # self.play(UpdateFromAlphaFunc(x_tip, lambda m, a: m.match_x(
            #     plane.c2p(xs[integer_interpolate(0, len(xs) - 1, a)[0]], 0)
            # )))
            # self.play(UpdateFromAlphaFunc(y_tip, lambda m, a: m.match_y(
            #     plane.c2p(0, ys[integer_interpolate(0, len(ys) - 1, a)[0]])
            # )))
            # self.add(lines, dot)
            # self.wait()
            self.play(LaggedStartMap(FadeOut, Group(
                x_tip, y_tip, lines, dot
            )), run_time=1)
