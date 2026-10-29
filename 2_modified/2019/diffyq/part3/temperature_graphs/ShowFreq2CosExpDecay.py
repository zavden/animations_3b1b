# ==============================================================================
# Scene:      ShowFreq2CosExpDecay
# Source:     videos/_2019/diffyq/part3/temperature_graphs.py (lines 2533-2536)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowFreq2CosExpDecay.py ShowFreq2CosExpDecay -w -m --fps 15
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


class ManipulateSinExpSurface(TemperatureGraphScene):
    CONFIG = {
        "axes_config": {
            "z_max": 1.25,
            "z_min": -1.25,
            "z_axis_config": {
                "unit_size": 2.5,
                "tick_frequency": 0.5,
            },
            "x_axis_config": {
                # "unit_size": 1.5,
                "unit_size": 1.0,
                "tick_frequency": 1,
            },
            "x_max": 10,
            "y_max": 15,
        },
        "alpha": 0.2,
        "tex_mobject_config": {
            "tex_to_color_map": {
                "{x}": GREEN,
                "{t}": YELLOW,
                "\\omega": MAROON_B,
                "^2": WHITE,
            },
        },
        "graph_config": {},
        "initial_phi": -90 * DEGREES,
        "initial_omega": 1,
    }

    def construct(self):
        self.setup_axes()
        self.add_sine_wave()
        self.shift_sine_to_cosine()
        self.show_derivatives_of_cos()
        self.show_cos_exp_surface()
        self.change_frequency()
        self.talk_through_omega()
        self.show_cos_omega_derivatives()
        self.show_rebalanced_exp()

    def setup_axes(self):
        axes = self.get_three_d_axes(include_numbers=True)
        axes.x_axis.remove(axes.x_axis.numbers)
        L = OldTex("L")
        L.rotate(90 * DEGREES, RIGHT)
        L.next_to(axes.x_axis.get_end(), IN)
        axes.x_axis.label = L
        axes.x_axis.add(L)

        axes.shift(5 * LEFT + 0.5 * IN)
        axes.z_axis.label[0].remove(
            *axes.z_axis.label[0][1:]
        )
        axes.z_axis.label.next_to(
            axes.z_axis.get_end(), OUT
        )
        axes.z_axis.add_numbers(
            *np.arange(-1, 1.5, 0.5),
            direction=LEFT,
            num_decimal_places=1
        )
        for number in axes.z_axis.numbers:
            number.rotate(90 * DEGREES, RIGHT)

        self.set_camera_orientation(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
            distance=100,
        )

        self.add(axes)
        self.remove(axes.y_axis)
        self.axes = axes

    def add_sine_wave(self):
        self.initialize_parameter_trackers()
        graph = self.get_graph()
        sin_label = OldTex(
            "\\sin\\left({x}\\right)",
            **self.tex_mobject_config,
        )
        sin_label.shift(2 * LEFT + 2.75 * UP)

        self.add_fixed_in_frame_mobjects(sin_label)
        graph.suspend_updating()
        self.play(
            ShowCreation(graph),
            Write(sin_label),
        )
        graph.resume_updating()
        self.wait()

        self.sin_label = sin_label
        self.graph = graph

    def shift_sine_to_cosine(self):
        graph = self.graph
        sin_label = self.sin_label

        sin_cross = Cross(sin_label)
        sin_cross.add_updater(
            lambda m: m.move_to(sin_label)
        )
        cos_label = OldTex(
            "\\cos\\left({x}\\right)",
            **self.tex_mobject_config,
        )
        cos_label.move_to(sin_label, LEFT)
        cos_label.shift(LEFT)
        # cos_label.shift(
        #     axes.c2p(0, 0) - axes.c2p(PI / 2, 0),
        # )

        left_tangent = Line(ORIGIN, RIGHT)
        left_tangent.set_stroke(WHITE, 5)

        self.add_fixed_in_frame_mobjects(cos_label)
        self.play(
            ApplyMethod(
                self.phi_tracker.set_value, 0,
            ),
            FadeOut(sin_label, LEFT),
            FadeIn(cos_label, RIGHT),
            run_time=2,
        )
        left_tangent.move_to(graph.get_start(), LEFT)
        self.play(ShowCreation(left_tangent))
        self.play(FadeOut(left_tangent))

        self.cos_label = cos_label

    def show_derivatives_of_cos(self):
        cos_label = self.cos_label
        cos_exp_label = OldTex(
            "\\cos\\left({x}\\right)",
            "e^{-\\alpha {t}}",
            **self.tex_mobject_config
        )
        cos_exp_label.move_to(cos_label, LEFT)

        ddx_group, ddx_exp_group = [
            self.get_ddx_computation_group(
                label,
                *[
                    OldTex(
                        s + "\\left({x}\\right)" + exp,
                        **self.tex_mobject_config,
                    )
                    for s in ["-\\sin", "-\\cos"]
                ]
            )
            for label, exp in [
                (cos_label, ""),
                (cos_exp_label, "e^{-\\alpha {t}}"),
            ]
        ]

        self.add_fixed_in_frame_mobjects(ddx_group)
        self.play(FadeIn(ddx_group))
        self.wait()

        # Cos exp
        transforms = [
            ReplacementTransform(
                cos_label, cos_exp_label,
            ),
            ReplacementTransform(
                ddx_group, ddx_exp_group,
            ),
        ]
        for trans in transforms:
            trans.begin()
            self.add_fixed_in_frame_mobjects(trans.mobject)
        self.play(*transforms)
        self.add_fixed_in_frame_mobjects(
            cos_exp_label, ddx_exp_group
        )
        self.remove_fixed_in_frame_mobjects(
            cos_label,
            *[
                trans.mobject
                for trans in transforms
            ]
        )

        self.cos_exp_label = cos_exp_label
        self.ddx_exp_group = ddx_exp_group

    def show_cos_exp_surface(self):
        axes = self.axes

        surface = self.get_cos_exp_surface()
        self.add(surface)
        surface.max_t_tracker.set_value(0)
        self.move_camera(
            phi=85 * DEGREES,
            theta=-80 * DEGREES,
            added_anims=[
                ApplyMethod(
                    surface.max_t_tracker.set_value,
                    axes.y_max,
                    run_time=4,
                ),
                Write(axes.y_axis),
            ]
        )
        self.wait()

        self.surface = surface

    def change_frequency(self):
        cos_exp_label = self.cos_exp_label
        ddx_exp_group = self.ddx_exp_group
        omega_tracker = self.omega_tracker

        cos_omega = OldTex(
            "\\cos\\left(",
            "\\omega", "\\cdot", "{x}",
            "\\right)",
            **self.tex_mobject_config
        )
        cos_omega.move_to(cos_exp_label, LEFT)

        omega = cos_omega.get_part_by_tex("\\omega")
        brace = Brace(omega, UP, buff=SMALL_BUFF)
        omega_decimal = always_redraw(
            lambda: DecimalNumber(
                omega_tracker.get_value(),
                color=omega.get_color(),
            ).next_to(brace, UP, SMALL_BUFF)
        )

        self.add_fixed_in_frame_mobjects(
            cos_omega,
            brace,
            omega_decimal,
        )
        self.play(
            self.camera.phi_tracker.set_value, 90 * DEGREES,
            self.camera.theta_tracker.set_value, -90 * DEGREES,
            FadeOut(self.surface),
            FadeOut(self.axes.y_axis),
            FadeOut(cos_exp_label),
            FadeOut(ddx_exp_group),
            FadeIn(cos_omega),
            GrowFromCenter(brace),
            FadeInFromDown(omega_decimal)
        )
        for n in [2, 6, 1, 4]:
            freq = n * PI / self.axes.x_max
            self.play(
                omega_tracker.set_value, freq,
                run_time=2
            )
            self.wait()
        self.wait()

        self.cos_omega = cos_omega
        self.omega_brace = brace

    def talk_through_omega(self):
        axes = self.axes

        x_tracker = ValueTracker(0)
        get_x = x_tracker.get_value
        v_line = always_redraw(lambda: DashedLine(
            axes.c2p(get_x(), 0, 0),
            axes.c2p(get_x(), 0, self.func(get_x(), 0)),
        ))

        x = self.cos_omega.get_part_by_tex("{x}")
        brace = Brace(x, DOWN)
        x_decimal = always_redraw(
            lambda: DecimalNumber(
                get_x(),
                color=x.get_color()
            ).next_to(brace, DOWN, SMALL_BUFF)
        )

        self.add(v_line)
        self.add_fixed_in_frame_mobjects(brace, x_decimal)
        self.play(
            x_tracker.set_value, 5,
            run_time=5,
            rate_func=linear,
        )
        self.play(
            FadeOut(v_line),
            FadeOut(brace),
            FadeOut(x_decimal),
        )
        self.remove_fixed_in_frame_mobjects(
            brace, x_decimal
        )

    def show_cos_omega_derivatives(self):
        cos_omega = self.cos_omega
        ddx_omega_group = self.get_ddx_computation_group(
            cos_omega,
            *[
                OldTex(
                    s + "\\left(\\omega \\cdot {x}\\right)",
                    **self.tex_mobject_config,
                )
                for s in ["-\\omega \\sin", "-\\omega^2 \\cos"]
            ]
        )

        omega_squared = ddx_omega_group[-1][1:3]
        rect = SurroundingRectangle(omega_squared)

        self.add_fixed_in_frame_mobjects(ddx_omega_group)
        self.play(FadeIn(ddx_omega_group))
        self.wait()
        self.add_fixed_in_frame_mobjects(rect)
        self.play(ShowCreationThenFadeOut(rect))
        self.wait()

        self.ddx_omega_group = ddx_omega_group

    def show_rebalanced_exp(self):
        cos_omega = self.cos_omega
        ddx_omega_group = self.ddx_omega_group

        cos_exp = OldTex(
            "\\cos\\left(",
            "\\omega", "\\cdot", "{x}",
            "\\right)",
            "e^{-\\alpha \\omega^2 {t}}",
            **self.tex_mobject_config
        )
        cos_exp.move_to(cos_omega, DL)

        self.add_fixed_in_frame_mobjects(cos_exp)
        self.play(
            FadeOut(cos_omega),
            FadeOut(ddx_omega_group),
            FadeIn(cos_exp),
        )
        self.remove_fixed_in_frame_mobjects(
            cos_omega,
            ddx_omega_group,
        )

        self.play(
            FadeIn(self.surface),
            FadeIn(self.axes.y_axis),
            VGroup(
                cos_exp,
                self.omega_brace,
            ).shift, 4 * RIGHT,
            self.camera.phi_tracker.set_value, 80 * DEGREES,
            self.camera.theta_tracker.set_value, -80 * DEGREES,
        )
        self.wait()
        self.play(
            self.omega_tracker.set_value, TAU / 10,
            run_time=6,
        )

    #
    def initialize_parameter_trackers(self):
        self.phi_tracker = ValueTracker(
            self.initial_phi
        )
        self.omega_tracker = ValueTracker(
            self.initial_omega
        )
        self.t_tracker = ValueTracker(0)

    def get_graph(self):
        return always_redraw(
            lambda: self.get_time_slice_graph(
                self.axes, self.func,
                t=self.t_tracker.get_value(),
                **self.graph_config
            )
        )

    def get_cos_exp_surface(self):
        max_t_tracker = ValueTracker(self.axes.y_max)
        surface = always_redraw(
            lambda: self.get_surface(
                self.axes,
                self.func,
                v_max=max_t_tracker.get_value(),
            )
        )
        surface.max_t_tracker = max_t_tracker
        return surface

    def func(self, x, t):
        phi = self.phi_tracker.get_value()
        omega = self.omega_tracker.get_value()
        alpha = self.alpha
        return op.mul(
            np.cos(omega * (x + phi)),
            np.exp(-alpha * (omega**2) * t)
        )

    def get_ddx_computation_group(self, f, df, ddf):
        arrows = VGroup(*[
            Vector(0.5 * RIGHT) for x in range(2)
        ])
        group = VGroup(
            arrows[0], df, arrows[1], ddf
        )
        group.arrange(RIGHT)
        group.next_to(f, RIGHT)

        for arrow in arrows:
            label = OldTex(
                "\\partial \\over \\partial {x}",
                **self.tex_mobject_config,
            )
            label.scale(0.5)
            label.next_to(arrow, UP, SMALL_BUFF)
            arrow.add(label)

        group.arrows = arrows
        group.funcs = VGroup(df, ddf)

        return group


class ShowFreq1CosExpDecay(ManipulateSinExpSurface):
    CONFIG = {
        "freq": 1,
        "alpha": 0.2,
    }

    def construct(self):
        self.setup_axes()
        self.add_back_y_axis()
        self.initialize_parameter_trackers()
        self.phi_tracker.set_value(0)
        self.omega_tracker.set_value(
            self.freq * TAU / 10,
        )
        #
        self.show_decay()

    def add_back_y_axis(self):
        axes = self.axes
        self.add(axes.y_axis)
        self.remove(axes.y_axis.numbers)
        self.remove(axes.y_axis.label)

    def show_decay(self):
        axes = self.axes
        t_tracker = self.t_tracker
        t_max = self.axes.y_max

        graph = always_redraw(
            lambda: self.get_time_slice_graph(
                axes,
                self.func,
                t=t_tracker.get_value(),
                stroke_width=5,
            )
        )

        surface = self.get_surface(
            self.axes, self.func,
        )
        plane = self.get_const_time_plane(axes)

        self.add(surface, plane, graph)

        self.set_camera_orientation(
            phi=80 * DEGREES,
            theta=-85 * DEGREES,
        )
        self.begin_ambient_camera_rotation(rate=0.01)
        self.play(
            t_tracker.set_value, t_max,
            plane.t_tracker.set_value, t_max,
            run_time=t_max,
            rate_func=linear,
        )


class ShowFreq2CosExpDecay(ShowFreq1CosExpDecay):
    CONFIG = {
        "freq": 2,
    }
