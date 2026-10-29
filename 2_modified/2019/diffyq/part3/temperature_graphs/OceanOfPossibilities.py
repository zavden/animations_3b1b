# ==============================================================================
# Scene:      OceanOfPossibilities
# Source:     videos/_2019/diffyq/part3/temperature_graphs.py (lines 646-875)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl OceanOfPossibilities.py OceanOfPossibilities -w -m --fps 15
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


class OceanOfPossibilities(TemperatureGraphScene):
    CONFIG = {
        "axes_config": {
            "z_min": 0,
            "z_max": 4,
        },
        "k": 0.2,
        "default_surface_config": {
            # "resolution": (32, 20),
            # "resolution": (8, 5),
        }
    }

    def construct(self):
        self.setup_camera()
        self.setup_axes()
        self.setup_surface()
        self.show_solution()
        self.reference_boundary_conditions()
        self.reference_initial_condition()
        self.ambiently_change_solution()

    def setup_camera(self):
        self.set_camera_orientation(
            phi=80 * DEGREES,
            theta=-80 * DEGREES,
        )
        self.begin_ambient_camera_rotation(rate=0.01)

    def setup_axes(self):
        axes = self.get_three_d_axes(include_numbers=True)
        axes.add(axes.input_plane)
        axes.scale(0.8)
        axes.center()
        axes.shift(OUT + RIGHT)

        self.add(axes)
        self.axes = axes

    def setup_surface(self):
        axes = self.axes
        k = self.k

        # Parameters for surface function
        initial_As = [2] + [
            0.8 * random.choice([-1, 1]) / n
            for n in range(1, 20)
        ]
        A_trackers = Group(*[
            ValueTracker(A)
            for A in initial_As
        ])

        def get_As():
            return [At.get_value() for At in A_trackers]

        omegas = [n / 2 for n in range(0, 10)]

        def func(x, t):
            return np.sum([
                np.prod([
                    A * np.cos(omega * x),
                    np.exp(-k * omega**2 * t)
                ])
                for A, omega in zip(get_As(), omegas)
            ])

        # Surface and graph
        surface = always_redraw(
            lambda: self.get_surface(axes, func)
        )
        t_tracker = ValueTracker(0)
        graph = always_redraw(
            lambda: self.get_time_slice_graph(
                axes, func, t_tracker.get_value(),
            )
        )

        surface.suspend_updating()
        graph.suspend_updating()

        self.surface_func = func
        self.surface = surface
        self.graph = graph
        self.t_tracker = t_tracker
        self.A_trackers = A_trackers
        self.omegas = omegas

    def show_solution(self):
        axes = self.axes
        surface = self.surface
        graph = self.graph
        t_tracker = self.t_tracker
        get_t = t_tracker.get_value

        opacity_tracker = ValueTracker(0)
        plane = always_redraw(lambda: Polygon(
            *[
                axes.c2p(x, get_t(), T)
                for x, T in [
                    (0, 0), (TAU, 0), (TAU, 4), (0, 4)
                ]
            ],
            stroke_width=0,
            fill_color=WHITE,
            fill_opacity=opacity_tracker.get_value(),
        ))

        self.add(surface, plane, graph)
        graph.resume_updating()
        self.play(
            opacity_tracker.set_value, 0.2,
            ApplyMethod(
                t_tracker.set_value, 1,
                rate_func=linear
            ),
            run_time=1
        )
        self.play(
            ApplyMethod(
                t_tracker.set_value, 10,
                rate_func=linear,
                run_time=9
            )
        )
        self.wait()

        self.plane = plane

    def reference_boundary_conditions(self):
        axes = self.axes
        t_numbers = axes.y_axis.numbers

        lines = VGroup(*[
            Line(
                axes.c2p(x, 0, 0),
                axes.c2p(x, axes.y_max, 0),
                stroke_width=3,
                stroke_color=MAROON_B,
            )
            for x in [0, axes.x_max]
        ])
        surface_boundary_lines = always_redraw(lambda: VGroup(*[
            ParametricCurve(
                lambda t: axes.c2p(
                    x, t,
                    self.surface_func(x, t)
                ),
                t_max=axes.y_max
            ).match_style(self.graph)
            for x in [0, axes.x_max]
        ]))
        # surface_boundary_lines.suspend_updating()
        words = VGroup()
        for line in lines:
            word = OldTexText("Boundary")
            word.set_stroke(BLACK, 3, background=True)
            word.scale(1.5)
            word.match_color(line)
            word.rotate(90 * DEGREES, RIGHT)
            word.rotate(90 * DEGREES, OUT)
            word.next_to(line, OUT, SMALL_BUFF)
            words.add(word)

        self.stop_ambient_camera_rotation()
        self.move_camera(
            theta=-45 * DEGREES,
            added_anims=[
                LaggedStartMap(ShowCreation, lines),
                LaggedStartMap(
                    FadeInFrom, words,
                    lambda m: (m, IN)
                ),
                FadeOut(t_numbers),
            ]
        )
        self.play(
            LaggedStart(*[
                TransformFromCopy(l1, l2)
                for l1, l2 in zip(lines, surface_boundary_lines)
            ])
        )
        self.add(surface_boundary_lines)
        self.wait()
        self.move_camera(
            theta=-70 * DEGREES,
        )

        self.surface_boundary_lines = surface_boundary_lines

    def reference_initial_condition(self):
        plane = self.plane
        t_tracker = self.t_tracker

        self.play(
            t_tracker.set_value, 0,
            run_time=2
        )
        plane.clear_updaters()
        self.play(FadeOut(plane))

    def ambiently_change_solution(self):
        A_trackers = self.A_trackers

        def generate_A_updater(A, rate):
            def update(m, dt):
                m.total_time += dt
                m.set_value(
                    2 * A * np.sin(rate * m.total_time + PI / 6)
                )
            return update

        rates = [0, 0.2] + [
            0.5 + 0.5 * np.random.random()
            for x in range(len(A_trackers) - 2)
        ]

        for tracker, rate in zip(A_trackers, rates):
            tracker.total_time = 0
            tracker.add_updater(generate_A_updater(
                tracker.get_value(),
                rate
            ))

        self.add(*A_trackers)
        self.surface_boundary_lines.resume_updating()
        self.surface.resume_updating()
        self.graph.resume_updating()
        self.begin_ambient_camera_rotation(rate=0.01)
        self.wait(30)
