# ==============================================================================
# Scene:      AnalyzeSineCurve
# Source:     videos/_2019/diffyq/part3/temperature_graphs.py (lines 878-1310)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AnalyzeSineCurve.py AnalyzeSineCurve -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use Cairo surfaces/spheres/cubes as groups of VMobject faces compatible with DrawBorderThenFill and the original indexing.
#   - Use the Cairo signature of smooth(t, inflection), keeping the one-argument call.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: adapt the Cairo APIs that require arguments removed from GL.
from cairo_compat import cairo_smooth as smooth

# CHANGE: keep Cairo's VMobject faces, needed for fill, stroke and indexing.
from cairo_compat import CairoParametricSurface as ParametricSurface

class TemperatureGraphScene(SpecialThreeDScene):
    CONFIG = {
        "axes_config": {
            "x_min": 0,
            "x_max": TAU,
            "y_min": 0,
            "y_max": 10,
            "z_min": -3,
            "z_max": 3,
            "x_axis_config": {
                "tick_frequency": TAU / 8,
                "include_tip": False,
            },
            "num_axis_pieces": 1,
        },
        "default_graph_style": {
            "stroke_width": 2,
            "stroke_color": WHITE,
            "background_image_file": "VerticalTempGradient",
        },
        "default_surface_config": {
            "fill_opacity": 0.1,
            "checkerboard_colors": [GREY_B],
            "stroke_width": 0.5,
            "stroke_color": WHITE,
            "stroke_opacity": 0.5,
        },
        "temp_text": "Temperature",
    }

    def get_three_d_axes(self, include_labels=True, include_numbers=False, **kwargs):
        config = dict(self.axes_config)
        config.update(kwargs)
        axes = ThreeDAxes(**config)
        axes.set_stroke(width=2)

        if include_numbers:
            self.add_axes_numbers(axes)

        if include_labels:
            self.add_axes_labels(axes)

        # Adjust axis orientation
        axes.x_axis.rotate(
            90 * DEGREES, RIGHT,
            about_point=axes.c2p(0, 0, 0),
        )
        axes.y_axis.rotate(
            90 * DEGREES, UP,
            about_point=axes.c2p(0, 0, 0),
        )

        # Add xy-plane
        input_plane = self.get_surface(
            axes, lambda x, t: 0
        )
        input_plane.set_style(
            fill_opacity=0.5,
            fill_color=BLUE_B,
            stroke_width=0.5,
            stroke_color=WHITE,
        )

        axes.input_plane = input_plane

        return axes

    def add_axes_numbers(self, axes):
        x_axis = axes.x_axis
        y_axis = axes.y_axis
        tex_vals = [
            ("\\pi \\over 2", TAU / 4),
            ("\\pi", TAU / 2),
            ("3\\pi \\over 2", 3 * TAU / 4),
            ("2\\pi", TAU)
        ]
        x_labels = VGroup()
        for tex, val in tex_vals:
            label = OldTex(tex)
            label.scale(0.5)
            label.next_to(x_axis.n2p(val), DOWN)
            x_labels.add(label)
        x_axis.add(x_labels)
        x_axis.numbers = x_labels

        y_axis.add_numbers()
        for number in y_axis.numbers:
            number.rotate(90 * DEGREES)
        return axes

    def add_axes_labels(self, axes):
        x_label = OldTex("x")
        x_label.next_to(axes.x_axis.get_end(), RIGHT)
        axes.x_axis.label = x_label

        t_label = OldTexText("Time")
        t_label.rotate(90 * DEGREES, OUT)
        t_label.next_to(axes.y_axis.get_end(), UP)
        axes.y_axis.label = t_label

        temp_label = OldTexText(self.temp_text)
        temp_label.rotate(90 * DEGREES, RIGHT)
        temp_label.next_to(axes.z_axis.get_zenith(), RIGHT)
        axes.z_axis.label = temp_label
        for axis in axes:
            axis.add(axis.label)
        return axes

    def get_time_slice_graph(self, axes, func, t, **kwargs):
        config = dict()
        config.update(self.default_graph_style)
        config.update({
            "t_min": axes.x_min,
            "t_max": axes.x_max,
        })
        config.update(kwargs)
        return ParametricCurve(
            lambda x: axes.c2p(
                x, t, func(x, t)
            ),
            **config,
        )

    def get_initial_state_graph(self, axes, func, **kwargs):
        return self.get_time_slice_graph(
            axes,
            lambda x, t: func(x),
            t=0,
            **kwargs
        )

    def get_surface(self, axes, func, **kwargs):
        config = {
            "u_min": axes.y_min,
            "u_max": axes.y_max,
            "v_min": axes.x_min,
            "v_max": axes.x_max,
            "resolution": (
                (axes.y_max - axes.y_min) // axes.y_axis.tick_frequency,
                (axes.x_max - axes.x_min) // axes.x_axis.tick_frequency,
            ),
        }
        config.update(self.default_surface_config)
        config.update(kwargs)
        return ParametricSurface(
            lambda t, x: axes.c2p(
                x, t, func(x, t)
            ),
            **config
        )

    def orient_three_d_mobject(self, mobject,
                               phi=85 * DEGREES,
                               theta=-80 * DEGREES):
        mobject.rotate(-90 * DEGREES - theta, OUT)
        mobject.rotate(phi, LEFT)
        return mobject

    def get_rod_length(self):
        return self.axes_config["x_max"]

    def get_const_time_plane(self, axes):
        t_tracker = ValueTracker(0)
        plane = Polygon(
            *[
                axes.c2p(x, 0, z)
                for x, z in [
                    (axes.x_min, axes.z_min),
                    (axes.x_max, axes.z_min),
                    (axes.x_max, axes.z_max),
                    (axes.x_min, axes.z_max),
                ]
            ],
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.2
        )
        plane.add_updater(lambda m: m.shift(
            axes.c2p(
                axes.x_min,
                t_tracker.get_value(),
                axes.z_min,
            ) - plane.get_points()[0]
        ))
        plane.t_tracker = t_tracker
        return plane


class AnalyzeSineCurve(TemperatureGraphScene):
    CONFIG = {
        "origin_point": 3 * LEFT,
        "axes_config": {
            "z_min": -1.5,
            "z_max": 1.5,
            "z_axis_config": {
                "unit_size": 2,
                "tick_frequency": 0.5,
            }
        },
        "tex_to_color_map": {
            "{x}": GREEN,
            "T": YELLOW,
            "=": WHITE,
            "0": WHITE,
            "\\Delta t": WHITE,
            "\\sin": WHITE,
            "{t}": PINK,
        }
    }

    def construct(self):
        self.setup_axes()
        self.ask_about_sine_curve()
        self.show_sine_wave_on_axes()
        self.reference_curvature()
        self.show_derivatives()
        self.show_curvature_matching_height()
        self.show_time_step_scalings()
        self.smooth_evolution()

    def setup_axes(self):
        axes = self.get_three_d_axes()
        axes.rotate(90 * DEGREES, LEFT)
        axes.shift(self.origin_point - axes.c2p(0, 0, 0))
        y_axis = axes.y_axis
        y_axis.fade(1)
        z_axis = axes.z_axis
        z_axis.label.next_to(z_axis.get_end(), UP, SMALL_BUFF)

        self.add_axes_numbers(axes)
        y_axis.remove(y_axis.numbers)
        axes.z_axis.add_numbers(
            *range(-1, 2),
            direction=LEFT,
        )

        self.axes = axes

    def ask_about_sine_curve(self):
        curve = FunctionGraph(
            lambda t: np.sin(t),
            x_min=0,
            x_max=TAU,
        )
        curve.move_to(DR)
        curve.set_width(5)
        curve.set_color(YELLOW)
        question = OldTexText("What's so special?")
        question.scale(1.5)
        question.to_edge(UP)
        question.shift(2 * LEFT)
        arrow = Arrow(
            question.get_bottom(),
            curve.point_from_proportion(0.25)
        )

        self.play(
            ShowCreation(curve),
            Write(question, run_time=1),
            GrowArrow(arrow),
        )
        self.wait()

        self.quick_sine_curve = curve
        self.question_group = VGroup(question, arrow)

    def show_sine_wave_on_axes(self):
        axes = self.axes
        graph = self.get_initial_state_graph(
            axes, lambda x: np.sin(x)
        )
        graph.set_stroke(width=4)
        graph_label = OldTex(
            "T({x}, 0) = \\sin\\left({x}\\right)",
            tex_to_color_map=self.tex_to_color_map,
        )
        graph_label.next_to(
            graph.point_from_proportion(0.25), UR,
            buff=SMALL_BUFF,
        )

        v_line, x_tracker = self.get_v_line_with_x_tracker(graph)

        xs = VGroup(
            *graph_label.get_parts_by_tex("x"),
            axes.x_axis.label,
        )

        self.play(
            Write(axes),
            self.quick_sine_curve.become, graph,
            FadeOut(self.question_group, UP),
        )
        self.play(
            FadeInFromDown(graph_label),
            FadeIn(graph),
        )
        self.remove(self.quick_sine_curve)
        self.add(v_line)
        self.play(
            ApplyMethod(
                x_tracker.set_value, TAU,
                rate_func=lambda t: smooth(t, 3),
                run_time=5,
            ),
            LaggedStartMap(
                ShowCreationThenFadeAround, xs,
                run_time=3,
                lag_ratio=0.2,
            )
        )
        self.remove(v_line, x_tracker)
        self.wait()

        self.graph = graph
        self.graph_label = graph_label
        self.v_line = v_line
        self.x_tracker = x_tracker

    def reference_curvature(self):
        curve_segment, curve_x_tracker = \
            self.get_curve_segment_with_x_tracker(self.graph)

        self.add(curve_segment)
        self.play(
            curve_x_tracker.set_value, TAU,
            run_time=5,
            rate_func=lambda t: smooth(t, 3),
        )
        self.play(FadeOut(curve_segment))

        self.curve_segment = curve_segment
        self.curve_x_tracker = curve_x_tracker

    def show_derivatives(self):
        deriv1 = OldTex(
            "{\\partial T \\over \\partial {x}}({x}, 0)",
            "= \\cos\\left({x}\\right)",
            tex_to_color_map=self.tex_to_color_map,
        )
        deriv2 = OldTex(
            "{\\partial^2 T \\over \\partial {x}^2}({x}, 0)",
            "= -\\sin\\left({x}\\right)",
            tex_to_color_map=self.tex_to_color_map,
        )

        deriv1.to_corner(UR)
        deriv2.next_to(
            deriv1, DOWN,
            buff=0.75,
            aligned_edge=LEFT,
        )
        VGroup(deriv1, deriv2).shift(1.4 * RIGHT)

        self.play(
            Animation(Group(*self.get_mobjects())),
            FadeIn(deriv1, LEFT),
            self.camera.frame_center.shift, 2 * RIGHT,
        )
        self.wait()
        self.play(
            FadeIn(deriv2, UP)
        )
        self.wait()

        self.deriv1 = deriv1
        self.deriv2 = deriv2

    def show_curvature_matching_height(self):
        axes = self.axes
        graph = self.graph
        curve_segment = self.curve_segment
        curve_x_tracker = self.curve_x_tracker

        d2_graph = self.get_initial_state_graph(
            axes, lambda x: -np.sin(x),
        )
        dashed_d2_graph = DashedVMobject(d2_graph, num_dashes=50)
        dashed_d2_graph.color_using_background_image(None)
        dashed_d2_graph.set_stroke(RED, 2)

        vector, x_tracker = self.get_v_line_with_x_tracker(
            d2_graph,
            line_creator=lambda p1, p2: Arrow(
                p1, p2, color=RED, buff=0
            )
        )

        lil_vectors = self.get_many_lil_vectors(graph)
        lil_vector = always_redraw(
            lambda: self.get_lil_vector(
                graph, x_tracker.get_value()
            )
        )

        d2_rect = SurroundingRectangle(
            self.deriv2[-5:],
            color=RED,
        )
        self.play(ShowCreation(d2_rect))
        self.add(vector)
        self.add(lil_vector)
        self.add(curve_segment)
        curve_x_tracker.set_value(0)
        self.play(
            ShowCreation(dashed_d2_graph),
            x_tracker.set_value, TAU,
            curve_x_tracker.set_value, TAU,
            ShowIncreasingSubsets(lil_vectors[1:]),
            run_time=8,
            rate_func=linear,
        )
        self.remove(vector)
        self.remove(lil_vector)
        self.add(lil_vectors)
        self.play(
            FadeOut(curve_segment),
            FadeOut(d2_rect),
        )

        self.lil_vectors = lil_vectors
        self.dashed_d2_graph = dashed_d2_graph

    def show_time_step_scalings(self):
        axes = self.axes
        graph_label = self.graph_label
        dashed_d2_graph = self.dashed_d2_graph
        lil_vectors = self.lil_vectors
        graph = self.graph

        factor = 0.9

        new_label = OldTex(
            "T({x}, \\Delta t) = c \\cdot \\sin\\left({x}\\right)",
            tex_to_color_map=self.tex_to_color_map,
        )
        final_label = OldTex(
            "T({x}, {t}) = (\\text{something}) \\cdot \\sin\\left({x}\\right)",
            tex_to_color_map=self.tex_to_color_map,
        )
        for label in (new_label, final_label):
            label.shift(
                graph_label.get_part_by_tex("=").get_center() -
                label.get_part_by_tex("=").get_center()
            )
        final_label.shift(1.5 * LEFT)

        h_lines = VGroup(
            DashedLine(axes.c2p(0, 0, 1), axes.c2p(TAU, 0, 1)),
            DashedLine(axes.c2p(0, 0, -1), axes.c2p(TAU, 0, -1)),
        )

        lil_vectors.add_updater(lambda m: m.become(
            self.get_many_lil_vectors(graph)
        ))

        i = 4
        self.play(
            ReplacementTransform(
                graph_label[:i], new_label[:i],
            ),
            ReplacementTransform(
                graph_label[i + 1:i + 3],
                new_label[i + 1:i + 3],
            ),
            FadeOut(graph_label[i], UP),
            FadeIn(new_label[i], DOWN),
        )
        self.play(
            ReplacementTransform(
                graph_label[i + 3:],
                new_label[i + 4:]
            ),
            FadeInFromDown(new_label[i + 3])
        )
        self.play(
            FadeOut(dashed_d2_graph),
            FadeIn(h_lines),
        )
        self.play(
            graph.stretch, factor, 1,
            h_lines.stretch, factor, 1,
        )
        self.wait()

        # Repeat
        last_coef = None
        last_exp = None
        delta_T = new_label.get_part_by_tex("\\Delta t")
        c = new_label.get_part_by_tex("c")[0]
        prefix = new_label[:4]
        prefix.generate_target()
        for x in range(5):
            coef = Integer(x + 2)
            exp = coef.copy().scale(0.7)
            coef.next_to(
                delta_T, LEFT, SMALL_BUFF,
                aligned_edge=DOWN,
            )
            exp.move_to(c.get_corner(UR), DL)
            anims1 = [FadeIn(coef, 0.25 * DOWN)]
            anims2 = [FadeIn(exp, 0.25 * DOWN)]
            if last_coef:
                anims1.append(
                    FadeOut(last_coef, 0.25 * UP)
                )
                anims2.append(
                    FadeOut(last_exp, 0.25 * UP)
                )
            last_coef = coef
            last_exp = exp
            prefix.target.next_to(coef, LEFT, SMALL_BUFF)
            prefix.target.match_y(prefix)
            anims1.append(MoveToTarget(prefix))

            self.play(*anims1)
            self.play(
                graph.stretch, factor, 1,
                h_lines.stretch, factor, 1,
                *anims2,
            )
        self.play(
            ReplacementTransform(
                new_label[:4],
                final_label[:4],
            ),
            ReplacementTransform(
                VGroup(last_coef, delta_T),
                final_label.get_part_by_tex("{t}"),
            ),
            ReplacementTransform(
                last_exp,
                final_label.get_part_by_tex("something"),
            ),
            FadeOut(new_label.get_part_by_tex("\\cdot"), UP),
            ReplacementTransform(
                new_label[-4:],
                final_label[-4:],
            ),
            ReplacementTransform(
                new_label.get_part_by_tex("="),
                final_label.get_part_by_tex("="),
            ),
            ReplacementTransform(
                new_label.get_part_by_tex(")"),
                final_label.get_part_by_tex(")"),
            ),
        )
        final_label.add_background_rectangle(opacity=1)
        self.add(final_label)
        self.wait()

        group = VGroup(graph, h_lines)
        group.add_updater(lambda m, dt: m.stretch(
            (1 - 0.1 * dt), 1
        ))
        self.add(group)
        self.wait(10)

    def smooth_evolution(self):
        pass

    #
    def get_rod(self, temp_func):
        pass

    def get_v_line_with_x_tracker(self, graph, line_creator=DashedLine):
        axes = self.axes
        x_min = axes.x_axis.p2n(graph.get_start())
        x_max = axes.x_axis.p2n(graph.get_end())
        x_tracker = ValueTracker(x_min)
        get_x = x_tracker.get_value
        v_line = always_redraw(lambda: line_creator(
            axes.c2p(get_x(), 0, 0),
            graph.point_from_proportion(
                inverse_interpolate(
                    x_min, x_max, get_x()
                )
            ),
        ))
        return v_line, x_tracker

    def get_curve_segment_with_x_tracker(self, graph, delta_x=0.5):
        axes = self.axes
        x_min = axes.x_axis.p2n(graph.get_start())
        x_max = axes.x_axis.p2n(graph.get_end())
        x_tracker = ValueTracker(x_min)
        get_x = x_tracker.get_value

        def x2a(x):
            return inverse_interpolate(x_min, x_max, x)

        curve = VMobject(
            stroke_color=WHITE,
            stroke_width=5
        )
        curve.add_updater(lambda m: m.pointwise_become_partial(
            graph,
            max(x2a(get_x() - delta_x), 0),
            min(x2a(get_x() + delta_x), 1),
        ))
        return curve, x_tracker

    def get_lil_vector(self, graph, x):
        x_axis = self.axes.x_axis
        point = graph.point_from_proportion(x / TAU)
        x_axis_point = x_axis.n2p(x_axis.p2n(point))
        return Arrow(
            point,
            interpolate(
                point, x_axis_point, 0.5,
            ),
            buff=0,
            color=RED
        )

    def get_many_lil_vectors(self, graph, n=13):
        return VGroup(*[
            self.get_lil_vector(graph, x)
            for x in np.linspace(0, TAU, n)
        ])
