# ==============================================================================
# Scene:      SineWaveScaledByExp
# Source:     videos/_2019/diffyq/part3/temperature_graphs.py (lines 1313-1492)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SineWaveScaledByExp.py SineWaveScaledByExp -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use Cairo surfaces/spheres/cubes as groups of VMobject faces compatible with DrawBorderThenFill and the original indexing.
# ==============================================================================

from manim_imports_ext import *

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


class SineWaveScaledByExp(TemperatureGraphScene):
    CONFIG = {
        "axes_config": {
            "z_min": -1.5,
            "z_max": 1.5,
            "z_axis_config": {
                "unit_size": 2,
                "tick_frequency": 0.5,
                "label_direction": LEFT,
            },
            "y_axis_config": {
                "label_direction": RIGHT,
            },
        },
        "k": 0.3,
    }

    def construct(self):
        self.setup_axes()
        self.setup_camera()
        self.show_sine_wave()
        self.show_decay_surface()
        self.linger_at_end()

    def setup_axes(self):
        axes = self.get_three_d_axes()

        # Add number labels
        self.add_axes_numbers(axes)
        for axis in [axes.x_axis, axes.y_axis]:
            axis.numbers.rotate(
                90 * DEGREES,
                axis=axis.get_vector(),
                about_point=axis.point_from_proportion(0.5)
            )
            axis.numbers.set_shade_in_3d(True)
        axes.z_axis.add_numbers(*range(-1, 2))
        for number in axes.z_axis.numbers:
            number.rotate(90 * DEGREES, RIGHT)

        axes.z_axis.label.next_to(
            axes.z_axis.get_end(), OUT,
        )

        # Input plane
        axes.input_plane.set_opacity(0.25)
        self.add(axes.input_plane)

        # Shift into place
        # axes.shift(5 * LEFT)
        self.axes = axes
        self.add(axes)

    def setup_camera(self):
        self.set_camera_orientation(
            phi=80 * DEGREES,
            theta=-80 * DEGREES,
            distance=50,
        )
        self.camera.frame.move_to(2 * RIGHT)

    def show_sine_wave(self):
        time_tracker = ValueTracker(0)
        graph = always_redraw(
            lambda: self.get_time_slice_graph(
                self.axes,
                self.sin_exp,
                t=time_tracker.get_value(),
            )
        )
        graph.suspend_updating()

        graph_label = OldTex("\\sin(x)")
        graph_label.set_color(BLUE)
        graph_label.rotate(90 * DEGREES, RIGHT)
        graph_label.next_to(
            graph.point_from_proportion(0.25),
            OUT,
            SMALL_BUFF,
        )

        self.play(
            ShowCreation(graph),
            FadeIn(graph_label, IN)
        )
        self.wait()
        graph.resume_updating()

        self.time_tracker = time_tracker
        self.graph = graph

    def show_decay_surface(self):
        time_tracker = self.time_tracker
        axes = self.axes

        plane = Rectangle()
        plane.rotate(90 * DEGREES, RIGHT)
        plane.set_stroke(width=0)
        plane.set_fill(WHITE, 0.2)
        plane.match_depth(axes.z_axis)
        plane.match_width(axes.x_axis, stretch=True)
        plane.add_updater(
            lambda p: p.move_to(axes.c2p(
                0,
                time_tracker.get_value(),
                0,
            ), LEFT)
        )

        time_slices = VGroup(*[
            self.get_time_slice_graph(
                self.axes,
                self.sin_exp,
                t=t,
            )
            for t in range(0, 10)
        ])
        surface_t_tracker = ValueTracker(0)
        surface = always_redraw(
            lambda: self.get_surface(
                self.axes,
                self.sin_exp,
                v_max=surface_t_tracker.get_value(),
            ).set_stroke(opacity=0)
        )

        exp_graph = ParametricCurve(
            lambda t: axes.c2p(
                PI / 2,
                t,
                self.sin_exp(PI / 2, t)
            ),
            t_min=axes.y_min,
            t_max=axes.y_max,
        )
        exp_graph.set_stroke(RED, 3)
        exp_graph.set_shade_in_3d(True)

        exp_label = OldTex("e^{-\\alpha t}")
        exp_label.scale(1.5)
        exp_label.set_color(RED)
        exp_label.rotate(90 * DEGREES, RIGHT)
        exp_label.rotate(90 * DEGREES, OUT)
        exp_label.next_to(
            exp_graph.point_from_proportion(0.3),
            OUT + UP,
        )

        self.move_camera(
            theta=-25 * DEGREES,
        )
        self.add(surface)
        self.add(plane)
        self.play(
            surface_t_tracker.set_value, axes.y_max,
            time_tracker.set_value, axes.y_max,
            ShowIncreasingSubsets(
                time_slices,
                int_func=np.ceil,
            ),
            run_time=5,
            rate_func=linear,
        )
        surface.clear_updaters()

        self.play(
            ShowCreation(exp_graph),
            FadeOut(plane),
            FadeIn(exp_label, IN),
            time_slices.set_stroke, {"width": 1},
        )

    def linger_at_end(self):
        self.wait()
        self.begin_ambient_camera_rotation(rate=-0.02)
        self.wait(20)

    #
    def sin_exp(self, x, t):
        return np.sin(x) * np.exp(-self.k * t)
