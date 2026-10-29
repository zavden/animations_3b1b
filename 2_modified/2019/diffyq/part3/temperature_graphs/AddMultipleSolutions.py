# ==============================================================================
# Scene:      AddMultipleSolutions
# Source:     videos/_2019/diffyq/part3/temperature_graphs.py (lines 275-369)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AddMultipleSolutions.py AddMultipleSolutions -w -m --fps 15
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


class SimpleCosExpGraph(TemperatureGraphScene):
    def construct(self):
        axes = self.get_three_d_axes()
        cos_graph = self.get_cos_graph(axes)
        cos_exp_surface = self.get_cos_exp_surface(axes)

        self.set_camera_orientation(
            phi=80 * DEGREES,
            theta=-80 * DEGREES,
        )
        self.camera.frame_center.shift(3 * RIGHT)
        self.begin_ambient_camera_rotation(rate=0.01)

        self.add(axes)
        self.play(ShowCreation(cos_graph))
        self.play(UpdateFromAlphaFunc(
            cos_exp_surface,
            lambda m, a: m.become(
                self.get_cos_exp_surface(axes, v_max=a * 10)
            ),
            run_time=3
        ))

        self.add(cos_graph.copy())

        t_tracker = ValueTracker(0)
        get_t = t_tracker.get_value
        cos_graph.add_updater(
            lambda m: m.become(self.get_time_slice_graph(
                axes,
                lambda x: self.cos_exp(x, get_t()),
                t=get_t()
            ))
        )

        plane = Rectangle(
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=0.1,
        )
        plane.rotate(90 * DEGREES, RIGHT)
        plane.match_width(axes.x_axis)
        plane.match_depth(axes.z_axis, stretch=True)
        plane.move_to(axes.c2p(0, 0, 0), LEFT)

        self.add(plane, cos_graph)
        self.play(
            ApplyMethod(
                t_tracker.set_value, 10,
                run_time=10,
                rate_func=linear,
            ),
            ApplyMethod(
                plane.shift, 10 * UP,
                run_time=10,
                rate_func=linear,
            ),
            VFadeIn(plane),
        )
        self.wait(10)

    #
    def cos_exp(self, x, t, A=2, omega=1.5, k=0.1):
        return A * np.cos(omega * x) * np.exp(-k * (omega**2) * t)

    def get_cos_graph(self, axes, **config):
        return self.get_initial_state_graph(
            axes,
            lambda x: self.cos_exp(x, 0),
            **config
        )

    def get_cos_exp_surface(self, axes, **config):
        return self.get_surface(
            axes,
            lambda x, t: self.cos_exp(x, t),
            **config
        )


class AddMultipleSolutions(SimpleCosExpGraph):
    CONFIG = {
        "axes_config": {
            "x_axis_config": {
                "unit_size": 0.7,
            },
        }
    }

    def construct(self):
        axes1, axes2, axes3 = all_axes = VGroup(*[
            self.get_three_d_axes(
                include_labels=False,
            )
            for x in range(3)
        ])
        all_axes.scale(0.5)
        self.orient_three_d_mobject(all_axes)

        As = [1.5, 1.5]
        omegas = [1.5, 2.5]
        ks = [0.1, 0.1]
        quads = [
            (axes1, [As[0]], [omegas[0]], [ks[0]]),
            (axes2, [As[1]], [omegas[1]], [ks[1]]),
            (axes3, As, omegas, ks),
        ]

        for axes, As, omegas, ks in quads:
            graph = self.get_initial_state_graph(
                axes,
                lambda x: np.sum([
                    self.cos_exp(x, 0, A, omega, k)
                    for A, omega, k in zip(As, omegas, ks)
                ])
            )
            surface = self.get_surface(
                axes,
                lambda x, t: np.sum([
                    self.cos_exp(x, t, A, omega, k)
                    for A, omega, k in zip(As, omegas, ks)
                ])
            )
            surface.sort(lambda p: -p[2])

            axes.add(surface, graph)
            axes.graph = graph
            axes.surface = surface

        self.set_camera_orientation(distance=100)
        plus = OldTex("+").scale(2)
        equals = OldTex("=").scale(2)
        group = VGroup(
            axes1, plus, axes2, equals, axes3,
        )
        group.arrange(RIGHT, buff=SMALL_BUFF)

        for axes in all_axes:
            checkmark = OldTex("\\checkmark")
            checkmark.set_color(GREEN)
            checkmark.scale(2)
            checkmark.next_to(axes, UP)
            checkmark.shift(0.7 * DOWN)
            axes.checkmark = checkmark

        self.add(axes1, axes2)
        self.play(
            LaggedStart(
                Write(axes1.surface),
                Write(axes2.surface),
            ),
            LaggedStart(
                FadeIn(axes1.checkmark, DOWN),
                FadeIn(axes2.checkmark, DOWN),
            ),
            lag_ratio=0.2,
            run_time=1,
        )
        self.wait()
        self.play(Write(plus))
        self.play(
            Transform(
                axes1.copy().set_fill(opacity=0),
                axes3
            ),
            Transform(
                axes2.copy().set_fill(opacity=0),
                axes3
            ),
            FadeIn(equals, LEFT)
        )
        self.play(
            FadeIn(axes3.checkmark, DOWN),
        )
        self.wait()
