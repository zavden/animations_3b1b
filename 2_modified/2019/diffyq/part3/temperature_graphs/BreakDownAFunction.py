# ==============================================================================
# Scene:      BreakDownAFunction
# Source:     videos/_2019/diffyq/part3/temperature_graphs.py (lines 372-643)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BreakDownAFunction.py BreakDownAFunction -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use Cairo surfaces/spheres/cubes as groups of VMobject faces compatible with DrawBorderThenFill and the original indexing.
# ==============================================================================

from scipy import integrate
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


class BreakDownAFunction(SimpleCosExpGraph):
    CONFIG = {
        "axes_config": {
            "z_axis_config": {
                "unit_size": 0.75,
                "include_tip": False,
            },
            "z_min": -2,
            "y_max": 20,
        },
        "low_axes_config": {
            "z_min": -3,
            "z_axis_config": {"unit_size": 1}
        },
        "n_low_axes": 4,
        "k": 0.2,
    }

    def construct(self):
        self.set_camera_orientation(distance=100)
        self.set_axes()
        self.setup_graphs()
        self.show_break_down()
        self.show_solutions_for_waves()

    def set_axes(self):
        top_axes = self.get_three_d_axes()
        top_axes.z_axis.label.next_to(
            top_axes.z_axis.get_end(), OUT, SMALL_BUFF
        )
        top_axes.y_axis.set_opacity(0)
        self.orient_three_d_mobject(top_axes)
        top_axes.y_axis.label.rotate(-10 * DEGREES, UP)
        top_axes.scale(0.75)
        top_axes.center()
        top_axes.to_edge(UP)

        low_axes = self.get_three_d_axes(**self.low_axes_config)
        low_axes.y_axis.set_opacity(0)
        for axis in low_axes:
            axis.label.fade(1)
        # low_axes.add(low_axes.input_plane)
        # low_axes.input_plane.set_opacity(0)

        self.orient_three_d_mobject(low_axes)
        low_axes_group = VGroup(*[
            low_axes.deepcopy()
            for x in range(self.n_low_axes)
        ])
        low_axes_group.arrange(
            RIGHT, buff=low_axes.get_width() / 3
        )
        low_axes_group.set_width(FRAME_WIDTH - 2.5)
        low_axes_group.next_to(top_axes, DOWN, LARGE_BUFF)
        low_axes_group.to_edge(LEFT)

        self.top_axes = top_axes
        self.low_axes_group = low_axes_group

    def setup_graphs(self):
        top_axes = self.top_axes
        low_axes_group = self.low_axes_group

        top_graph = self.get_initial_state_graph(
            top_axes,
            self.initial_func,
            discontinuities=self.get_initial_func_discontinuities(),
            color=YELLOW,
        )
        top_graph.set_stroke(width=4)

        fourier_terms = self.get_fourier_cosine_terms(
            self.initial_func
        )

        low_graphs = VGroup(*[
            self.get_initial_state_graph(
                axes,
                lambda x: A * np.cos(n * x / 2)
            )
            for n, axes, A in zip(
                it.count(),
                low_axes_group,
                fourier_terms
            )
        ])
        k = self.k
        low_surfaces = VGroup(*[
            self.get_surface(
                axes,
                lambda x, t: np.prod([
                    A,
                    np.cos(n * x / 2),
                    np.exp(-k * (n / 2)**2 * t)
                ])
            )
            for n, axes, A in zip(
                it.count(),
                low_axes_group,
                fourier_terms
            )
        ])
        top_surface = self.get_surface(
            top_axes,
            lambda x, t: np.sum([
                np.prod([
                    A,
                    np.cos(n * x / 2),
                    np.exp(-k * (n / 2)**2 * t)
                ])
                for n, A in zip(
                    it.count(),
                    fourier_terms
                )
            ])
        )

        self.top_graph = top_graph
        self.low_graphs = low_graphs
        self.low_surfaces = low_surfaces
        self.top_surface = top_surface

    def show_break_down(self):
        top_axes = self.top_axes
        low_axes_group = self.low_axes_group
        top_graph = self.top_graph
        low_graphs = self.low_graphs

        plusses = VGroup(*[
            OldTex("+").next_to(
                axes.x_axis.get_end(),
                RIGHT, MED_SMALL_BUFF
            )
            for axes in low_axes_group
        ])
        dots = OldTex("\\cdots")
        dots.next_to(plusses, RIGHT, MED_SMALL_BUFF)

        arrow = Arrow(
            dots.get_right(),
            top_graph.get_end() + 1.4 * DOWN + 1.7 * RIGHT,
            path_arc=90 * DEGREES,
        )

        top_words = OldTexText("Arbitrary\\\\function")
        top_words.next_to(top_axes, LEFT, MED_LARGE_BUFF)
        top_words.set_color(YELLOW)
        top_arrow = Arrow(
            top_words.get_right(),
            top_graph.point_from_proportion(0.3)
        )

        low_words = OldTexText("Sine curves")
        low_words.set_color(BLUE)
        low_words.next_to(low_axes_group, DOWN, MED_LARGE_BUFF)

        self.add(top_axes)
        self.play(ShowCreation(top_graph))
        self.play(
            FadeIn(top_words, RIGHT),
            ShowCreation(top_arrow)
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, low_axes_group),
            FadeIn(low_words, UP),
            LaggedStartMap(FadeInFromDown, [*plusses, dots]),
            *[
                TransformFromCopy(top_graph, low_graph)
                for low_graph in low_graphs
            ],
        )
        self.play(ShowCreation(arrow))
        self.wait()

    def show_solutions_for_waves(self):
        low_axes_group = self.low_axes_group
        top_axes = self.top_axes
        low_graphs = self.low_graphs
        low_surfaces = self.low_surfaces
        top_surface = self.top_surface
        top_graph = self.top_graph

        for surface in [top_surface, *low_surfaces]:
            surface.sort(lambda p: -p[2])

        anims1 = []
        anims2 = [
            ApplyMethod(
                top_axes.y_axis.set_opacity, 1,
            ),
        ]
        for axes, surface, graph in zip(low_axes_group, low_surfaces, low_graphs):
            axes.y_axis.set_opacity(1)
            axes.y_axis.label.fade(1)
            anims1 += [
                ShowCreation(axes.y_axis),
                Write(surface, run_time=2),
            ]
            anims2.append(AnimationGroup(
                TransformFromCopy(graph, top_graph.copy()),
                Transform(
                    surface.copy().set_fill(opacity=0),
                    top_surface,
                )
            ))

        self.play(*anims1)
        self.wait()
        self.play(LaggedStart(*anims2, run_time=2))
        self.wait()

        checkmark = OldTex("\\checkmark")
        checkmark.set_color(GREEN)
        low_checkmarks = VGroup(*[
            checkmark.copy().next_to(
                surface.get_top(), UP, SMALL_BUFF
            )
            for surface in low_surfaces
        ])
        top_checkmark = checkmark.copy()
        top_checkmark.scale(1.5)
        top_checkmark.move_to(top_axes.get_corner(UR))

        self.play(LaggedStartMap(FadeInFromDown, low_checkmarks))
        self.wait()
        self.play(*[
            TransformFromCopy(low_checkmark, top_checkmark.copy())
            for low_checkmark in low_checkmarks
        ])
        self.wait()

    #
    def initial_func(self, x):
        # return 3 * np.exp(-(x - PI)**2)

        x1 = TAU / 4 - 1
        x2 = TAU / 4 + 1
        x3 = 3 * TAU / 4 - 1.6
        x4 = 3 * TAU / 4 + 0.3

        T0 = -2
        T1 = 2
        T2 = 1

        if x < x1:
            return T0
        elif x < x2:
            alpha = inverse_interpolate(x1, x2, x)
            return bezier([T0, T0, T1, T1])(alpha)
        elif x < x3:
            return T1
        elif x < x4:
            alpha = inverse_interpolate(x3, x4, x)
            return bezier([T1, T1, T2, T2])(alpha)
        else:
            return T2

    def get_initial_func_discontinuities(self):
        # return [TAU / 4, 3 * TAU / 4]
        return []

    def get_fourier_cosine_terms(self, func, n_terms=40):
        result = [
            integrate.quad(
                lambda x: (1 / PI) * func(x) * np.cos(n * x / 2),
                0, TAU
            )[0]
            for n in range(n_terms)
        ]
        result[0] = result[0] / 2
        return result
