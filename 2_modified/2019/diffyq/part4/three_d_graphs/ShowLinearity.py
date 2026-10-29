# ==============================================================================
# Scene:      ShowLinearity
# Source:     videos/_2019/diffyq/part4/three_d_graphs.py (lines 6-245)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part2/wordy_scenes.py, _2019/diffyq/part3/temperature_graphs.py
#
# Run from this folder:
#     manimgl ShowLinearity.py ShowLinearity -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use Cairo surfaces/spheres/cubes as groups of VMobject faces compatible with DrawBorderThenFill and the original indexing.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: keep Cairo's VMobject faces, needed for fill, stroke and indexing.
from cairo_compat import CairoParametricSurface as ParametricSurface


# ----- From _2019/diffyq/part3/temperature_graphs.py -----

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



# ----- From _2019/diffyq/part2/wordy_scenes.py -----

class WriteHeatEquationTemplate(Scene):
    CONFIG = {
        "tex_mobject_config": {
            "tex_to_color_map": {
                "{T}": WHITE,
                "{t}": YELLOW,
                "{x}": GREEN,
                "{y}": RED,
                "{z}": BLUE,
                "\\partial": WHITE,
                "2": WHITE,
            },
        },
    }

    def get_d1_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}({x}, {t})", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2} ({x}, {t})",
            **self.tex_mobject_config
        )

    def get_d1_equation_without_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\cdot",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            **self.tex_mobject_config
        )

    def get_d3_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2} + ",
            "{\\partial^2 {T} \\over \\partial {y}^2} + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_general_equation(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}", "=",
            "\\alpha", "\\nabla^2 {T}",
            **self.tex_mobject_config,
        )

    def get_d3_equation_with_inputs(self):
        return OldTex(
            "{\\partial {T} \\over \\partial {t}}",
            "({x}, {y}, {z}, {t})", "=",
            "\\alpha \\left(",
            "{\\partial^2 {T} \\over \\partial {x}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {y}^2}",
            "({x}, {y}, {z}, {t}) + ",
            "{\\partial^2 {T} \\over \\partial {z}^2}",
            "({x}, {y}, {z}, {t})",
            "\\right)",
            **self.tex_mobject_config
        )

    def get_d1_words(self):
        return OldTexText("Heat equation\\\\", "(1 dimension)")

    def get_d3_words(self):
        return OldTexText("Heat equation\\\\", "(3 dimensions)")

    def get_d1_group(self):
        group = VGroup(
            self.get_d1_words(),
            self.get_d1_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group

    def get_d3_group(self):
        group = VGroup(
            self.get_d3_words(),
            self.get_d3_equation(),
        )
        group.arrange(DOWN, buff=MED_LARGE_BUFF)
        return group



# ----- From _2019/diffyq/part4/three_d_graphs.py -----

class ShowLinearity(WriteHeatEquationTemplate, TemperatureGraphScene):
    CONFIG = {
        "temp_text": "Temp",
        "alpha": 0.1,
        "axes_config": {
            "z_max": 2,
            "z_min": -2,
            "z_axis_config": {
                "tick_frequency": 0.5,
                "unit_size": 1.5,
            },
        },
        "default_surface_config": {
            "resolution": (16, 16)
            # "resolution": (4, 4)
        },
        "freqs": [2, 5],
    }

    def setup(self):
        TemperatureGraphScene.setup(self)
        WriteHeatEquationTemplate.setup(self)

    def construct(self):
        self.init_camera()
        self.add_three_graphs()
        self.show_words()
        self.add_function_labels()
        self.change_scalars()

    def init_camera(self):
        self.camera.set_distance(1000)

    def add_three_graphs(self):
        axes_group = self.get_axes_group()
        axes0, axes1, axes2 = axes_group
        freqs = self.freqs
        scalar_trackers = Group(
            ValueTracker(1),
            ValueTracker(1),
        )
        graphs = VGroup(
            self.get_graph(axes0, [freqs[0]], [scalar_trackers[0]]),
            self.get_graph(axes1, [freqs[1]], [scalar_trackers[1]]),
            self.get_graph(axes2, freqs, scalar_trackers),
        )

        plus = OldTex("+").scale(2)
        equals = OldTex("=").scale(2)
        plus.move_to(midpoint(
            axes0.get_right(),
            axes1.get_left(),
        ))
        equals.move_to(midpoint(
            axes1.get_right(),
            axes2.get_left(),
        ))

        self.add(axes_group)
        self.add(graphs)
        self.add(plus)
        self.add(equals)

        self.axes_group = axes_group
        self.graphs = graphs
        self.scalar_trackers = scalar_trackers
        self.plus = plus
        self.equals = equals

    def show_words(self):
        equation = self.get_d1_equation()
        name = OldTexText("Heat equation")
        name.next_to(equation, DOWN)
        name.set_color_by_gradient(RED, YELLOW)
        group = VGroup(equation, name)
        group.to_edge(UP)

        shift_val = 0.5 * RIGHT

        arrow = Vector(1.5 * RIGHT)
        arrow.move_to(group)
        arrow.shift(shift_val)
        linear_word = OldTexText("``Linear''")
        linear_word.scale(2)
        linear_word.next_to(arrow, RIGHT)

        self.add(group)
        self.wait()
        self.play(
            ShowCreation(arrow),
            group.next_to, arrow, LEFT
        )
        self.play(FadeIn(linear_word, LEFT))
        self.wait()

    def add_function_labels(self):
        axes_group = self.axes_group
        graphs = self.graphs

        solution_labels = VGroup()
        for axes in axes_group:
            label = OldTexText("Solution", "$\\checkmark$")
            label.set_color_by_tex("checkmark", GREEN)
            label.next_to(axes, DOWN)
            solution_labels.add(label)

        kw = {
            "tex_to_color_map": {
                "T_1": BLUE,
                "T_2": GREEN,
            }
        }
        T1 = OldTex("a", "T_1", **kw)
        T2 = OldTex("b", "T_2", **kw)
        T_sum = OldTex("T_1", "+", "T_2", **kw)
        T_sum_with_scalars = OldTex(
            "a", "T_1", "+", "b", "T_2", **kw
        )

        T1.next_to(graphs[0], UP)
        T2.next_to(graphs[1], UP)
        T_sum.next_to(graphs[2], UP)
        T_sum.shift(SMALL_BUFF * DOWN)
        T_sum_with_scalars.move_to(T_sum)

        a_brace = Brace(T1[0], UP, buff=SMALL_BUFF)
        b_brace = Brace(T2[0], UP, buff=SMALL_BUFF)
        s1_decimal = DecimalNumber()
        s1_decimal.match_color(T1[1])
        s1_decimal.next_to(a_brace, UP, SMALL_BUFF)
        s1_decimal.add_updater(lambda m: m.set_value(
            self.scalar_trackers[0].get_value()
        ))
        s2_decimal = DecimalNumber()
        s2_decimal.match_color(T2[1])
        s2_decimal.next_to(b_brace, UP, SMALL_BUFF)
        s2_decimal.add_updater(lambda m: m.set_value(
            self.scalar_trackers[1].get_value()
        ))

        self.play(
            FadeIn(T1[1], DOWN),
            FadeIn(solution_labels[0], UP),
        )
        self.play(
            FadeIn(T2[1], DOWN),
            FadeIn(solution_labels[1], UP),
        )
        self.wait()
        self.play(
            TransformFromCopy(T1[1], T_sum[0]),
            TransformFromCopy(T2[1], T_sum[2]),
            TransformFromCopy(self.plus, T_sum[1]),
            *[
                Transform(
                    graph.copy().set_fill(opacity=0),
                    graphs[2].copy().set_fill(opacity=0),
                    remover=True
                )
                for graph in graphs[:2]
            ]
        )
        self.wait()
        self.play(FadeIn(solution_labels[2], UP))
        self.wait()

        # Show constants
        self.play(
            FadeIn(T1[0]),
            FadeIn(T2[0]),
            FadeIn(a_brace),
            FadeIn(b_brace),
            FadeIn(s1_decimal),
            FadeIn(s2_decimal),
            FadeOut(T_sum),
            FadeIn(T_sum_with_scalars),
        )

    def change_scalars(self):
        s1, s2 = self.scalar_trackers

        kw = {
            "run_time": 2,
        }
        for graph in self.graphs:
            graph.resume_updating()
        self.play(s2.set_value, -0.5, **kw)
        self.play(s1.set_value, -0.2, **kw)
        self.play(s2.set_value, 1.5, **kw)
        self.play(s1.set_value, 1.2, **kw)
        self.play(s2.set_value, 0.3, **kw)
        self.wait()

    #
    def get_axes_group(self):
        axes_group = VGroup(*[
            self.get_axes()
            for x in range(3)
        ])
        axes_group.arrange(RIGHT, buff=2)
        axes_group.set_width(FRAME_WIDTH - 1)
        axes_group.to_edge(DOWN, buff=1)
        return axes_group

    def get_axes(self, **kwargs):
        axes = self.get_three_d_axes(**kwargs)
        # axes.input_plane.set_fill(opacity=0)
        # axes.input_plane.set_stroke(width=0.5)
        # axes.add(axes.input_plane)
        self.orient_three_d_mobject(axes)
        axes.rotate(-5 * DEGREES, UP)
        axes.set_width(4)
        axes.x_axis.label.next_to(
            axes.x_axis.get_end(), DOWN,
            buff=2 * SMALL_BUFF
        )
        return axes

    def get_graph(self, axes, freqs, scalar_trackers):
        L = axes.x_max
        a = self.alpha

        def func(x, t):
            scalars = [st.get_value() for st in scalar_trackers]
            return np.sum([
                s * np.cos(k * x) * np.exp(-a * (k**2) * t)
                for freq, s in zip(freqs, scalars)
                for k in [freq * PI / L]
            ])

        def get_surface_graph_group():
            return VGroup(
                self.get_surface(axes, func),
                self.get_time_slice_graph(axes, func, t=0),
            )

        result = always_redraw(get_surface_graph_group)
        result.func = func
        result.suspend_updating()
        return result
