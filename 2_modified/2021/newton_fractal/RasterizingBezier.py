# ==============================================================================
# Scene:      RasterizingBezier
# Source:     videos/_2021/newton_fractal.py (lines 644-912)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RasterizingBezier.py RasterizingBezier -w -m --fps 15
#
# Placeholder assets (not Grant's originals):
#   - _lib/assets/svg_images/bezier_example.svg (synthetic Bézier curve; generator _lib/assets/generated/2021/newton_fractal/make_newton_fractal_assets.py)
# ==============================================================================

from manim_imports_ext import *

class RasterizingBezier(Scene):
    def construct(self):
        # Add curve and pixels
        self.add(FullScreenRectangle())

        curve = SVGMobject("bezier_example")[0]
        curve.set_width(FRAME_WIDTH - 3)
        curve.set_stroke(WHITE, width=1.0)
        curve.set_fill(opacity=0)
        curve.to_edge(DOWN, buff=1)
        curve.insert_n_curves(10)  # To better uniformize it

        thick_curve = curve.copy()
        thick_curve.set_stroke(YELLOW, 30.0)
        thick_curve.reverse_points()

        pixels = Square().get_grid(90 // 2, 160 // 2, buff=0, fill_rows_first=False)
        pixels.set_height(FRAME_HEIGHT)
        pixels.set_stroke(WHITE, width=0.25)

        # I fully recognize the irony is implementing this without
        # solving polynomials, but I'm happy to be inificient on runtime
        # to just code up the quickest thing I can think of.
        samples = np.array([curve.pfp(x) for x in np.linspace(0, 1, 100)])
        sw_tracker = ValueTracker(0.15)
        get_sw = sw_tracker.get_value

        for pixel in pixels:
            diffs = samples - pixel.get_center()
            dists = np.apply_along_axis(lambda p: np.dot(p, p), 1, diffs)
            index = np.argmin(dists)
            if index == 0 or index == len(samples) - 1:
                pixel.dist = np.infty
            else:
                pixel.dist = dists[index]

        def update_pixels(pixels):
            for pixel in pixels:
                pixel.set_fill(
                    YELLOW,
                    0.5 * clip(10 * (get_sw() - pixel.dist), 0, 1)
                )

        update_pixels(pixels)

        fake_pixels = pixels.copy()
        fake_pixels.set_stroke(width=0)
        fake_pixels.set_fill(GREY_E, 1)

        self.add(thick_curve)
        self.wait()
        self.add(fake_pixels, pixels)
        self.play(
            FadeIn(fake_pixels),
            ShowCreation(pixels),
            lag_ratio=10 / len(pixels),
            run_time=4
        )
        self.remove(thick_curve)
        self.wait()

        # Pixel
        pixel = pixels[725].deepcopy()
        pixel.set_fill(opacity=0)
        label = OldTexText("Pixel $\\vec{\\textbf{p}}$")
        label.set_fill(YELLOW)
        label.set_stroke(BLACK, 4, background=True)
        label.next_to(pixel, UL, buff=LARGE_BUFF)
        label.shift_onto_screen()
        arrow = Arrow(label, pixel, buff=0.1, stroke_width=3.0)
        arrow.set_color(YELLOW)

        self.play(
            FadeIn(label),
            ShowCreation(arrow),
            pixel.animate.set_stroke(YELLOW, 2.0),
        )
        pixels.add_updater(update_pixels)
        self.play(sw_tracker.animate.set_value(2.0), run_time=2)
        self.play(sw_tracker.animate.set_value(0.2), run_time=2)
        pixels.suspend_updating()
        self.play(ShowCreation(curve))

        # Show P(t) value
        ct = VGroup(OldTex("\\vec{\\textbf{c}}(")[0], DecimalNumber(0), OldTex(")")[0])
        ct.arrange(RIGHT, buff=0)
        ct.add_updater(lambda m: m.set_stroke(BLACK, 4, background=True))
        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value
        P_dot = Dot(color=GREEN)
        ct[1].add_updater(lambda m: m.set_value(get_t()))
        ct[1].next_to(ct[0], RIGHT, buff=0)
        P_dot.add_updater(lambda m: m.move_to(curve.pfp(get_t() / 2)))
        ct.add_updater(lambda m: m.move_to(P_dot).shift(
            (0.3 - 0.5 * get_t() * (1 - get_t())) * rotate_vector(np.array([-3, 1, 0]), -0.8 * get_t() * PI)
        ))
        curve_copy = curve.copy()
        curve_copy.pointwise_become_partial(curve, 0, 0.5)
        curve_copy.set_points(curve_copy.get_points_without_null_curves())
        curve_copy.set_stroke(YELLOW, 3.0)

        self.play(
            VFadeIn(ct),
            ApplyMethod(t_tracker.set_value, 1.0, run_time=3),
            ShowCreation(curve_copy, run_time=3),
            VFadeIn(P_dot),
        )
        new_ct = OldTex("\\vec{\\textbf{c}}(", "t", ")")
        new_ct.move_to(ct, LEFT)
        new_ct.set_stroke(BLACK, 4, background=True)
        self.play(FadeTransformPieces(ct, new_ct))
        ct = new_ct
        self.wait()

        # Show distance
        graph_group = self.get_corner_graph_group(pixel, curve)
        bg_rect, axes, y_label, graph = graph_group

        t_tracker = ValueTracker(0)
        dist_line = Line()
        dist_line.set_stroke(TEAL, 5)
        dist_line.add_updater(lambda l: l.put_start_and_end_on(
            pixel.get_center(),
            curve_copy.pfp(t_tracker.get_value())
        ))

        dist_lines = VGroup()
        graph_v_lines = VGroup()
        for t in np.linspace(0, 1, 20):
            t_tracker.set_value(t)
            dist_lines.add(dist_line.update().copy().clear_updaters())
            graph_v_lines.add(axes.get_v_line(
                axes.input_to_graph_point(t, graph)
            ))
        dist_lines.set_stroke(RED, 1, opacity=1.0)
        graph_v_lines.set_stroke(RED, 1, opacity=1.0)
        t_tracker.set_value(0)

        self.play(
            *map(FadeIn, graph_group[:-1]),
        )
        self.play(
            FadeIn(dist_lines, lag_ratio=1),
            FadeIn(graph_v_lines, lag_ratio=1),
            run_time=4
        )
        self.wait()
        t_tracker.set_value(0.0)
        self.play(
            VFadeIn(dist_line, rate_func=squish_rate_func(smooth, 0, 0.25)),
            ApplyMethod(t_tracker.set_value, 1.0),
            ShowCreation(graph),
            run_time=3,
        )
        self.play(dist_line.animate.set_stroke(RED, 1.0))
        self.wait()

        # Show width again
        pixels.resume_updating()
        self.play(sw_tracker.animate.set_value(1.5), run_time=2)
        self.play(sw_tracker.animate.set_value(0.5), run_time=1)
        pixels.suspend_updating()
        self.wait()

        # Show derivative
        deriv_graph_group = self.get_deriv_graph_group(graph_group)
        d_graph = deriv_graph_group[-1]
        d_graph.set_points_smoothly([d_graph.pfp(x) for x in np.linspace(0, 1, 20)])
        deriv_axes = deriv_graph_group[1]

        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value
        tan_line = always_redraw(
            lambda: axes.get_tangent_line(
                get_t(), graph, length=3,
            ).set_stroke(
                color=MAROON_B,
                width=1.0,
                opacity=clip(20 * get_t() * (1 - get_t()), 0, 1)
            )
        )

        self.play(*map(FadeIn, deriv_graph_group[:-1]))
        self.add(tan_line)
        self.play(
            t_tracker.animate.set_value(1),
            ShowCreation(d_graph),
            run_time=4
        )
        self.remove(tan_line)
        self.wait()

        points = graph.get_points()
        min_point = points[np.argmin([p[1] for p in points])]
        min_line = Line(min_point, [min_point[0], deriv_axes.c2p(0, 0)[1], 0])
        min_line.set_stroke(WHITE, 1)

        question = Text("What is\nthis value?", font_size=30)
        question.to_corner(DR)
        arrow = Arrow(
            question.get_left(), min_line.get_bottom(), stroke_width=3,
            buff=0.1
        )

        self.play(ShowCreation(min_line))
        self.play(
            Write(question),
            ShowCreation(arrow),
        )
        self.wait()

    def get_corner_graph_group(self, pixel, curve, t_range=(0, 0.5)):
        axes = Axes(
            x_range=(0, 1, 0.2),
            y_range=(0, 20, 5),
            height=3,
            width=5,
            axis_config={"include_tip": False}
        )
        axes.to_corner(UR, buff=SMALL_BUFF)
        y_label = OldTex(
            "&\\text{Distance}^2\\\\",
            "&||\\vec{\\textbf{p}} - \\vec{\\textbf{c}}(t)||^2",
            font_size=24,
        )
        # For future transition
        y_label = VGroup(VectorizedPoint(y_label.get_left()), *y_label)
        y_label.next_to(axes.y_axis.get_top(), RIGHT, aligned_edge=UP)
        y_label.shift_onto_screen(buff=MED_SMALL_BUFF)

        graph = axes.get_graph(lambda t: get_norm(
            pixel.get_center() - curve.pfp(interpolate(*t_range, t))
        )**2)
        graph.set_stroke(RED, 2)

        bg_rect = BackgroundRectangle(axes, buff=SMALL_BUFF)
        result = VGroup(bg_rect, axes, y_label, graph)

        return result

    def get_deriv_graph_group(self, graph_group):
        top_bg_rect, top_axes, top_y_label, top_graph = graph_group

        axes = Axes(
            x_range=top_axes.x_range,
            y_range=(-60, 60, 10),
            height=top_axes.get_height(),
            width=top_axes.get_width(),
            axis_config={"include_tip": False}
        )
        axes.to_corner(DR, buff=SMALL_BUFF)
        axes.shift((top_axes.c2p(0, 0) - axes.c2p(0, 0))[0] * RIGHT)
        dt = 1e-5
        f = top_graph.underlying_function
        graph = axes.get_graph(lambda t: (f(t + dt) - f(t)) / dt)
        graph.set_stroke(MAROON_B)
        # Dumb hack, not sure why it's needed
        graph.get_points()[:133] += 0.015 * UP

        y_label = VGroup(OldTex("\\frac{d}{dt}", font_size=24), top_y_label[2].copy())
        y_label.arrange(RIGHT, buff=0.05)
        y_label.next_to(axes.y_axis.get_top(), RIGHT, buff=2 * SMALL_BUFF)

        bg_rect = BackgroundRectangle(VGroup(axes, graph), buff=SMALL_BUFF)
        bg_rect.stretch(1.05, 1, about_edge=DOWN)

        result = VGroup(bg_rect, axes, y_label, graph)

        return result
