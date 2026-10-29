# ==============================================================================
# Scene:      CenterOfMassDescription
# Source:     videos/_2018/uncertainty.py (lines 1362-1452)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/fourier.py
#
# Run from this folder:
#     manimgl CenterOfMassDescription.py CenterOfMassDescription -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - removed typo line circle_plane.targets.set_stroke(...): NumberPlane has no attribute targets (the line before already does the same on .target)
#   - removed stray kwarg run_time_per_flash: Cairo's Animation absorbed unknown kwargs, GL raises TypeError
# ==============================================================================

import scipy
from manim_imports_ext import *
# -*- coding: utf-8 -*-
import scipy.integrate
import warnings


# ----- From _2018/fourier.py -----

USE_ALMOST_FOURIER_BY_DEFAULT = True


DEFAULT_COMPLEX_TO_REAL_FUNC = lambda z : z.real


def get_fourier_transform(
    func, t_min, t_max, 
    complex_to_real_func = DEFAULT_COMPLEX_TO_REAL_FUNC,
    use_almost_fourier = USE_ALMOST_FOURIER_BY_DEFAULT,
    **kwargs ##Just eats these
    ):
    scalar = 1./(t_max - t_min) if use_almost_fourier else 1.0
    def fourier_transform(f):
        z = scalar*scipy.integrate.quad(
            lambda t : func(t)*np.exp(complex(0, -TAU*f*t)),
            t_min, t_max
        )[0]
        return complex_to_real_func(z)
    return fourier_transform


class FourierMachineScene(Scene):
    CONFIG = {
        "time_axes_config" : {
            "x_min" : 0,
            "x_max" : 4.4,
            "x_axis_config" : {
                "unit_size" : 3,
                "tick_frequency" : 0.25,
                "big_tick_numbers" : [1, 2, 3],
            },
            "y_min" : 0,
            "y_max" : 2,
            "y_axis_config" : {"unit_size" : 0.8},
        },
        "time_label_t" : 3.4,
        "circle_plane_config" : {
            "x_radius" : 2.1,
            "y_radius" : 2.1,
            "x_unit_size" : 1,
            "y_unit_size" : 1,
        },
        "frequency_axes_config" : {
            "axis_config" : {
                "color" : TEAL,
            },
            "x_min" : 0,
            "x_max" : 5.0,
            "x_axis_config" : {
                "unit_size" : 1.4,
                "numbers_to_show" : list(range(1, 6)),
            },
            "y_min" : -1.0,
            "y_max" : 1.0,
            "y_axis_config" : {
                "unit_size" : 1.8,
                "tick_frequency" : 0.5,
                "label_direction" : LEFT,
            },
            "color" : TEAL,
        },
        "frequency_axes_box_color" : TEAL_E,
        "text_scale_val" : 0.75,
        "default_graph_config" : {
            "num_graph_points" : 100,
            "color" : YELLOW,
        },
        "equilibrium_height" : 1,
        "default_y_vector_animation_config" : {
            "run_time" : 5,
            "rate_func" : None,
            "remover" : True,
        },
        "default_time_sweep_config" : {
            "rate_func" : None,
            "run_time" : 5,
        },
        "default_num_v_lines_indicating_periods" : 20,
    }

    def get_time_axes(self):
        time_axes = Axes(**self.time_axes_config)
        time_axes.x_axis.add_numbers()
        time_label = OldTexText("Time")
        intensity_label = OldTexText("Intensity")
        labels = VGroup(time_label, intensity_label)
        for label in labels:
            label.scale(self.text_scale_val)
        time_label.next_to(
            time_axes.coords_to_point(self.time_label_t,0), 
            DOWN
        )
        intensity_label.next_to(time_axes.y_axis.get_top(), RIGHT)
        time_axes.labels = labels
        time_axes.add(labels)
        time_axes.to_corner(UP+LEFT)
        self.time_axes = time_axes
        return time_axes

    def get_circle_plane(self):
        circle_plane = NumberPlane(**self.circle_plane_config)
        circle_plane.to_corner(DOWN+LEFT)
        circle = DashedLine(ORIGIN, TAU*UP).apply_complex_function(np.exp)
        circle.scale(circle_plane.x_unit_size)
        circle.move_to(circle_plane.coords_to_point(0, 0))
        circle_plane.circle = circle
        circle_plane.add(circle)
        circle_plane.fade()
        self.circle_plane = circle_plane
        return circle_plane

    def get_frequency_axes(self):
        frequency_axes = Axes(**self.frequency_axes_config)
        frequency_axes.x_axis.add_numbers()
        frequency_axes.y_axis.add_numbers(
            *frequency_axes.y_axis.get_tick_numbers()
        )
        box = SurroundingRectangle(
            frequency_axes,
            buff = MED_SMALL_BUFF,
            color = self.frequency_axes_box_color,
        )
        frequency_axes.box = box
        frequency_axes.add(box)
        frequency_axes.to_corner(DOWN+RIGHT, buff = MED_SMALL_BUFF)

        frequency_label = OldTexText("Frequency")
        frequency_label.scale(self.text_scale_val)
        frequency_label.next_to(
            frequency_axes.x_axis.get_right(), DOWN, 
            buff = MED_LARGE_BUFF,
            aligned_edge = RIGHT,
        )
        frequency_axes.label = frequency_label
        frequency_axes.add(frequency_label)

        self.frequency_axes = frequency_axes
        return frequency_axes

    def get_time_graph(self, func, **kwargs):
        if not hasattr(self, "time_axes"):
            self.get_time_axes()
        config = dict(self.default_graph_config)
        config.update(kwargs)
        graph = self.time_axes.get_graph(func, **config)
        return graph

    def get_cosine_wave(self, freq = 1, shift_val = 1, scale_val = 0.9):
        return self.get_time_graph(
            lambda t : shift_val + scale_val*np.cos(TAU*freq*t)
        )

    def get_fourier_transform_graph(self, time_graph, **kwargs):
        if not hasattr(self, "frequency_axes"):
            self.get_frequency_axes()
        func = time_graph.underlying_function
        t_axis = self.time_axes.x_axis
        t_min = t_axis.point_to_number(time_graph.get_points()[0])
        t_max = t_axis.point_to_number(time_graph.get_points()[-1])
        f_max = self.frequency_axes.x_max
        # result = get_fourier_graph(
        #     self.frequency_axes, func, t_min, t_max,
        #     **kwargs
        # )
        # too_far_right_point_indices = [
        #     i
        #     for i, point in enumerate(result.get_points())
        #     if self.frequency_axes.x_axis.point_to_number(point) > f_max
        # ]
        # if too_far_right_point_indices:
        #     i = min(too_far_right_point_indices)
        #     prop = float(i)/len(result.get_points())
        #     result.pointwise_become_partial(result, 0, prop)
        # return result
        return self.frequency_axes.get_graph(
            get_fourier_transform(func, t_min, t_max, **kwargs),
            color = self.center_of_mass_color,
            **kwargs
        )

    def get_polarized_mobject(self, mobject, freq = 1.0):
        if not hasattr(self, "circle_plane"):
            self.get_circle_plane()
        polarized_mobject = mobject.copy()
        polarized_mobject.apply_function(lambda p : self.polarize_point(p, freq))
        # polarized_mobject.make_smooth()
        mobject.polarized_mobject = polarized_mobject
        polarized_mobject.frequency = freq
        return polarized_mobject

    def polarize_point(self, point, freq = 1.0):
        t, y = self.time_axes.point_to_coords(point)
        z = y*np.exp(complex(0, -2*np.pi*freq*t))
        return self.circle_plane.coords_to_point(z.real, z.imag)

    def get_polarized_animation(self, mobject, freq = 1.0):
        p_mob = self.get_polarized_mobject(mobject, freq = freq)
        def update_p_mob(p_mob):
            Transform(
                p_mob, 
                self.get_polarized_mobject(mobject, freq = freq)
            ).update(1)
            mobject.polarized_mobject = p_mob
            return p_mob
        return UpdateFromFunc(p_mob, update_p_mob)

    def animate_frequency_change(self, mobjects, new_freq, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 3.0)
        added_anims = kwargs.get("added_anims", [])
        self.play(*[
            self.get_frequency_change_animation(mob, new_freq, **kwargs)
            for mob in mobjects
        ] + added_anims)

    def get_frequency_change_animation(self, mobject, new_freq, **kwargs):
        if not hasattr(mobject, "polarized_mobject"):
            mobject.polarized_mobject = self.get_polarized_mobject(mobject)
        start_freq = mobject.polarized_mobject.frequency
        def update(pm, alpha):
            freq = interpolate(start_freq, new_freq, alpha)
            new_pm = self.get_polarized_mobject(mobject, freq)
            Transform(pm, new_pm).update(1)
            mobject.polarized_mobject = pm
            mobject.polarized_mobject.frequency = freq
            return pm
        return UpdateFromAlphaFunc(mobject.polarized_mobject, update, **kwargs)

    def get_time_graph_y_vector_animation(self, graph, **kwargs):
        config = dict(self.default_y_vector_animation_config)
        config.update(kwargs)
        vector = Vector(UP, color = WHITE)
        graph_copy = graph.copy()
        x_axis = self.time_axes.x_axis
        x_min = x_axis.point_to_number(graph.get_points()[0])
        x_max = x_axis.point_to_number(graph.get_points()[-1])
        def update_vector(vector, alpha):
            x = interpolate(x_min, x_max, alpha)
            vector.put_start_and_end_on(
                self.time_axes.coords_to_point(x, 0),
                self.time_axes.input_to_graph_point(x, graph_copy)
            )
            return vector
        return UpdateFromAlphaFunc(vector, update_vector, **config)

    def get_polarized_vector_animation(self, polarized_graph, **kwargs):
        config = dict(self.default_y_vector_animation_config)
        config.update(kwargs)
        vector = Vector(RIGHT, color = WHITE)
        origin = self.circle_plane.coords_to_point(0, 0)
        graph_copy = polarized_graph.copy()
        def update_vector(vector, alpha):
            # Not sure why this is needed, but without smoothing 
            # out the alpha like this, the vector would occasionally
            # jump around
            point = center_of_mass([
                graph_copy.point_from_proportion(alpha+d)
                for d in np.linspace(-0.001, 0.001, 5)
            ])
            vector.put_start_and_end_on_with_projection(origin, point)
            return vector
        return UpdateFromAlphaFunc(vector, update_vector, **config)

    def get_vector_animations(self, graph, draw_polarized_graph = True, **kwargs):
        config = dict(self.default_y_vector_animation_config)
        config.update(kwargs)
        anims = [
            self.get_time_graph_y_vector_animation(graph, **config),
            self.get_polarized_vector_animation(graph.polarized_mobject, **config),
        ]
        if draw_polarized_graph:
            new_config = dict(config)
            new_config["remover"] = False
            anims.append(ShowCreation(graph.polarized_mobject, **new_config))
        return anims

    def animate_time_sweep(self, freq, n_repeats = 1, t_max = None, **kwargs):
        added_anims = kwargs.pop("added_anims", [])
        config = dict(self.default_time_sweep_config)
        config.update(kwargs)
        circle_plane = self.circle_plane
        time_axes = self.time_axes
        ctp = time_axes.coords_to_point
        t_max = t_max or time_axes.x_max
        v_line = DashedLine(
            ctp(0, 0), ctp(0, time_axes.y_max),
            stroke_width = 6,
        )
        v_line.set_color(RED)

        for x in range(n_repeats):
            v_line.move_to(ctp(0, 0), DOWN)
            self.play(
                ApplyMethod(
                    v_line.move_to, 
                    ctp(t_max, 0), DOWN
                ),
                self.get_polarized_animation(v_line, freq = freq),
                *added_anims,
                **config
            )
            self.remove(v_line.polarized_mobject)
        self.play(FadeOut(VGroup(v_line, v_line.polarized_mobject)))

    def get_v_lines_indicating_periods(self, freq, n_lines = None):
        if n_lines is None:
            n_lines = self.default_num_v_lines_indicating_periods
        period = np.divide(1., max(freq, 0.01))
        v_lines = VGroup(*[
            DashedLine(ORIGIN, 1.5*UP).move_to(
                self.time_axes.coords_to_point(n*period, 0),
                DOWN
            )
            for n in range(1, n_lines + 1)
        ])
        v_lines.set_stroke(GREY_B)
        return v_lines

    def get_period_v_lines_update_anim(self):
        def update_v_lines(v_lines):
            freq = self.graph.polarized_mobject.frequency
            Transform(
                v_lines,
                self.get_v_lines_indicating_periods(freq)
            ).update(1)
        return UpdateFromFunc(
            self.v_lines_indicating_periods, update_v_lines
        )


class WrapCosineGraphAroundCircle(FourierMachineScene):
    CONFIG = {
        "initial_winding_frequency" : 0.5,
        "signal_frequency" : 3.0,
    }
    def construct(self):
        self.show_initial_signal()
        self.show_finite_interval()
        self.wrap_around_circle()
        self.show_time_sweeps()
        self.compare_two_frequencies()
        self.change_wrapping_frequency()

    def show_initial_signal(self):
        axes = self.get_time_axes()
        graph = self.get_cosine_wave(freq = self.signal_frequency)
        self.graph = graph
        braces = VGroup(*self.get_peak_braces()[3:6])
        v_lines = VGroup(*[
            DashedLine(
                ORIGIN, 2*UP, color = RED
            ).move_to(axes.coords_to_point(x, 0), DOWN)
            for x in (1, 2)
        ])
        words = self.get_bps_label()
        words.save_state()
        words.next_to(axes.coords_to_point(1.5, 0), DOWN, MED_LARGE_BUFF)

        self.add(axes)
        self.play(ShowCreation(graph, run_time = 2, rate_func=linear))
        self.play(
            FadeIn(words),
            LaggedStartMap(FadeIn, braces),
            *list(map(ShowCreation, v_lines))
        )
        self.wait()
        self.play(
            FadeOut(VGroup(braces, v_lines)),
            words.restore,
        )
        self.wait()

        self.beats_per_second_label = words
        self.graph = graph

    def show_finite_interval(self):
        axes = self.time_axes
        v_line = DashedLine(
            axes.coords_to_point(0, 0),
            axes.coords_to_point(0, axes.y_max),
            color = RED,
            stroke_width = 6,
        )
        h_line = Line(
            axes.coords_to_point(0, 0),
            axes.coords_to_point(axes.x_max, 0),
        )
        rect = Rectangle(
            stroke_width = 0,
            fill_color = TEAL,
            fill_opacity = 0.5,
        )
        rect.match_height(v_line)
        rect.match_width(h_line, stretch = True)
        rect.move_to(v_line, DOWN+LEFT)
        right_v_line = v_line.copy()
        right_v_line.move_to(rect, RIGHT)

        rect.save_state()
        rect.stretch(0, 0, about_edge = ORIGIN)
        self.play(rect.restore, run_time = 2)
        self.play(FadeOut(rect))
        for line in v_line, right_v_line:
            self.play(ShowCreation(line))
            self.play(FadeOut(line))
        self.wait()

    def wrap_around_circle(self):
        graph = self.graph
        freq = self.initial_winding_frequency
        low_freq = freq/3
        polarized_graph = self.get_polarized_mobject(graph, low_freq)
        circle_plane = self.get_circle_plane()
        moving_graph = graph.copy()

        self.play(ShowCreation(circle_plane, lag_ratio = 0))
        self.play(ReplacementTransform(
            moving_graph,
            polarized_graph,
            run_time = 3,
            path_arc = -TAU/2
        ))
        self.animate_frequency_change([graph], freq)
        self.wait()
        pg_copy = polarized_graph.copy()
        self.remove(polarized_graph)
        self.play(pg_copy.fade, 0.75)
        self.play(*self.get_vector_animations(graph), run_time = 15)
        self.remove(pg_copy)
        self.wait()

    def show_time_sweeps(self):
        freq = self.initial_winding_frequency
        graph = self.graph

        v_lines = self.get_v_lines_indicating_periods(freq)
        winding_freq_label = self.get_winding_frequency_label()

        self.animate_time_sweep(
            freq = freq,
            t_max = 4,
            run_time = 6,
            added_anims = [FadeIn(v_lines)]
        )
        self.play(
            FadeIn(winding_freq_label),
            *self.get_vector_animations(graph)
        )
        self.wait()

        self.v_lines_indicating_periods = v_lines

    def compare_two_frequencies(self):
        bps_label = self.beats_per_second_label
        wps_label = self.winding_freq_label
        for label in bps_label, wps_label:
            label.rect = SurroundingRectangle(
                label, color = RED
            )
        graph = self.graph
        freq = self.initial_winding_frequency
        braces = self.get_peak_braces(buff = 0)

        self.play(ShowCreation(bps_label.rect))
        self.play(FadeOut(bps_label.rect))
        self.play(LaggedStartMap(FadeIn, braces, run_time = 3))
        self.play(FadeOut(braces))
        self.play(ShowCreation(wps_label.rect))
        self.play(FadeOut(wps_label.rect))
        self.animate_time_sweep(freq = freq, t_max = 4)
        self.wait()

    def change_wrapping_frequency(self):
        graph = self.graph
        v_lines = self.v_lines_indicating_periods
        freq_label = self.winding_freq_label[0]

        count = 0
        for target_freq in [1.23, 0.2, 0.79, 1.55, self.signal_frequency]:
            self.play(
                Transform(
                    v_lines, 
                    self.get_v_lines_indicating_periods(target_freq)
                ),
                ChangeDecimalToValue(freq_label, target_freq),
                self.get_frequency_change_animation(graph, target_freq),
                run_time = 4,
            )
            self.wait()
            if count == 2:
                self.play(LaggedStartMap(
                    ApplyFunction, v_lines,
                    lambda mob : (
                        lambda m : m.shift(0.25*UP).set_color(YELLOW), 
                        mob
                    ),
                    rate_func = there_and_back
                ))
                self.animate_time_sweep(target_freq, t_max = 2)
            count += 1
        self.wait()
        self.play(
            *self.get_vector_animations(graph, False),
            run_time = 15
        )

    ##

    def get_winding_frequency_label(self):
        freq = self.initial_winding_frequency
        winding_freq_label = VGroup(
            DecimalNumber(freq, num_decimal_places=2),
            OldTexText("cycles/second")
        )
        winding_freq_label.arrange(RIGHT)
        winding_freq_label.next_to(
            self.circle_plane, RIGHT, aligned_edge = UP
        )
        self.winding_freq_label = winding_freq_label
        return winding_freq_label

    def get_peak_braces(self, **kwargs):
        peak_points = [
            self.time_axes.input_to_graph_point(x, self.graph)
            for x in np.arange(0, 3.5, 1./self.signal_frequency)
        ]
        return VGroup(*[
            Brace(Line(p1, p2), UP, **kwargs)
            for p1, p2 in zip(peak_points, peak_points[1:])
        ])

    def get_bps_label(self, freq = 3):
        braces = VGroup(*self.get_peak_braces()[freq:2*freq])
        words = OldTexText("%d beats/second"%freq)
        words.set_width(0.9*braces.get_width())
        words.move_to(braces, DOWN)
        return words


class DrawFrequencyPlot(WrapCosineGraphAroundCircle, PiCreatureScene):
    CONFIG = {
        "initial_winding_frequency" : 3.0,
        "center_of_mass_color" : RED,
        "center_of_mass_multiple" : 1,
    }
    def construct(self):
        self.remove(self.pi_creature)
        self.setup_graph()
        self.indicate_weight_of_wire()
        self.show_center_of_mass_dot()
        self.change_to_various_frequencies()
        self.introduce_frequency_plot()
        self.draw_full_frequency_plot()
        self.recap_objects_on_screen()
        self.lower_graph()
        self.label_as_almost_fourier()

    def setup_graph(self):
        self.add(self.get_time_axes())
        self.add(self.get_circle_plane())
        self.graph = self.get_cosine_wave(self.signal_frequency)
        self.add(self.graph)
        self.add(self.get_polarized_mobject(
            self.graph, self.initial_winding_frequency
        ))
        self.add(self.get_winding_frequency_label())
        self.beats_per_second_label = self.get_bps_label()
        self.add(self.beats_per_second_label)        
        self.v_lines_indicating_periods = self.get_v_lines_indicating_periods(
            self.initial_winding_frequency
        )
        self.add(self.v_lines_indicating_periods)
        self.change_frequency(1.03)
        self.wait()

    def indicate_weight_of_wire(self):
        graph = self.graph
        pol_graph = graph.polarized_mobject.copy()
        pol_graph.save_state()
        morty = self.pi_creature
        morty.change("raise_right_hand")
        morty.save_state()
        morty.change("plain")
        morty.fade(1)

        self.play(
            morty.restore,
            pol_graph.scale, 0.5,
            pol_graph.next_to, morty.get_corner(UP+LEFT), UP, -SMALL_BUFF,
        )
        self.play(
            morty.change, "lower_right_hand", pol_graph.get_bottom(),
            pol_graph.shift, 0.45*DOWN,
            rate_func = there_and_back,
            run_time = 2,
        )
        self.wait()

        metal_wire = pol_graph.copy().set_stroke(GREY_B)
        self.play(
            ShowCreationThenDestruction(metal_wire),
            run_time = 2,
        )
        self.play(
            pol_graph.restore,
            morty.change, "pondering"
        )
        self.remove(pol_graph)

    def show_center_of_mass_dot(self):
        color = self.center_of_mass_color
        dot = self.get_center_of_mass_dot()
        dot.save_state()
        arrow = Vector(DOWN+2*LEFT, color = color)
        arrow.next_to(dot.get_center(), UP+RIGHT, buff = SMALL_BUFF)
        dot.move_to(arrow.get_start())
        words = OldTexText("Center of mass")
        words.next_to(arrow.get_start(), RIGHT)
        words.set_color(color)

        self.play(
            GrowArrow(arrow),
            dot.restore,
        )
        self.play(Write(words))
        self.play(FadeOut(arrow), FadeOut(self.pi_creature))
        self.wait()

        self.generate_center_of_mass_dot_update_anim()
        self.center_of_mass_label = words

    def change_to_various_frequencies(self):
        self.change_frequency(
            3.0, run_time = 30,
            rate_func = bezier([0, 0, 1, 1])
        )
        self.wait()
        self.play(
            *self.get_vector_animations(self.graph),
            run_time = 15
        )

    def introduce_frequency_plot(self):
        wps_label = self.winding_freq_label
        wps_label.add_to_back(BackgroundRectangle(wps_label))
        com_label = self.center_of_mass_label
        com_label.add_background_rectangle()
        frequency_axes = self.get_frequency_axes()
        x_coord_label = OldTexText("$x$-coordinate for center of mass")
        x_coord_label.set_color(self.center_of_mass_color)
        x_coord_label.scale(self.text_scale_val)
        x_coord_label.next_to(
            frequency_axes.y_axis.get_top(),
            RIGHT, aligned_edge = UP, buff = LARGE_BUFF
        )
        x_coord_label.add_background_rectangle()
        flower_path = ParametricCurve(
            lambda t : self.circle_plane.coords_to_point(
                np.sin(2*t)*np.cos(t),
                np.sin(2*t)*np.sin(t),
            ),
            t_min = 0, t_max = TAU,
        )
        flower_path.move_to(self.center_of_mass_dot)

        self.play(
            wps_label.move_to, self.circle_plane.get_top(),
            com_label.move_to, self.circle_plane, DOWN,
        )
        self.play(LaggedStartMap(FadeIn, frequency_axes))
        self.wait()
        self.play(MoveAlongPath(
            self.center_of_mass_dot, flower_path,
            run_time = 4,
        ))
        self.play(ReplacementTransform(
            com_label.copy(), x_coord_label
        ))
        self.wait()

        self.x_coord_label = x_coord_label

    def draw_full_frequency_plot(self):
        graph = self.graph
        fourier_graph = self.get_fourier_transform_graph(graph)
        fourier_graph.save_state()
        fourier_graph_update = self.get_fourier_graph_drawing_update_anim(
            fourier_graph
        )
        v_line = DashedLine(
            self.frequency_axes.coords_to_point(0, 0),
            self.frequency_axes.coords_to_point(0, 1),
            stroke_width = 6,
            color = fourier_graph.get_color()
        )

        self.change_frequency(0.0)
        self.generate_fourier_dot_transform(fourier_graph)
        self.wait()
        self.play(ShowCreation(v_line))
        self.play(
            GrowFromCenter(self.fourier_graph_dot),
            FadeOut(v_line)
        )
        f_max = int(self.frequency_axes.x_max)
        for freq in [0.2, 1.5, 3.0, 4.0, 5.0]:
            fourier_graph.restore()
            self.change_frequency(
                freq,
                added_anims = [fourier_graph_update],
                run_time = 8,
            )
            self.wait()
        self.fourier_graph = fourier_graph

    def recap_objects_on_screen(self):
        rect = FullScreenFadeRectangle()
        time_group = VGroup(
            self.graph,
            self.time_axes,
            self.beats_per_second_label,
        ).copy()
        circle_group = VGroup(
            self.graph.polarized_mobject,
            self.circle_plane,
            self.winding_freq_label,
            self.center_of_mass_label,
            self.center_of_mass_dot,
        ).copy()
        frequency_group = VGroup(
            self.fourier_graph,
            self.frequency_axes,
            self.x_coord_label,
        ).copy()
        groups = [time_group, circle_group, frequency_group]

        self.play(FadeIn(rect))
        self.wait()
        for group in groups:
            graph_copy = group[0].copy().set_color(PINK)
            self.play(FadeIn(group))
            self.play(ShowCreation(graph_copy))
            self.play(FadeOut(graph_copy))
            self.wait()
            self.play(FadeOut(group))
        self.wait()
        self.play(FadeOut(rect))

    def lower_graph(self):
        graph = self.graph
        time_axes = self.time_axes
        shift_vect = time_axes.coords_to_point(0, 1)
        shift_vect -= time_axes.coords_to_point(0, 0)
        fourier_graph = self.fourier_graph
        new_graph = self.get_cosine_wave(
            self.signal_frequency, shift_val = 0
        )
        new_fourier_graph = self.get_fourier_transform_graph(new_graph)
        for mob in graph, time_axes, fourier_graph:
            mob.save_state()

        new_freq = 0.03
        self.change_frequency(new_freq)
        self.wait()
        self.play(
            time_axes.shift, shift_vect/2,
            graph.shift, -shift_vect/2,
            self.get_frequency_change_animation(
                self.graph, new_freq
            ),
            self.center_of_mass_dot_anim,
            self.get_period_v_lines_update_anim(),
            Transform(fourier_graph, new_fourier_graph),
            self.fourier_graph_dot.move_to,
                self.frequency_axes.coords_to_point(new_freq, 0),
            run_time = 2
        )
        self.wait()
        self.remove(self.fourier_graph_dot)
        self.generate_fourier_dot_transform(new_fourier_graph)
        self.change_frequency(3.0, run_time = 15, rate_func=linear)
        self.wait()
        self.play(
            graph.restore, 
            time_axes.restore,
            self.get_frequency_change_animation(
                self.graph, 3.0
            ),
            self.center_of_mass_dot_anim,
            self.get_period_v_lines_update_anim(),
            fourier_graph.restore,
            Animation(self.fourier_graph_dot),
            run_time = 2
        )
        self.generate_fourier_dot_transform(self.fourier_graph)
        self.wait()
        self.play(FocusOn(self.fourier_graph_dot))
        self.wait()

    def label_as_almost_fourier(self):
        x_coord_label = self.x_coord_label
        almost_fourier_label = OldTexText(
            "``Almost Fourier Transform''",
        )
        almost_fourier_label.move_to(x_coord_label, UP+LEFT)
        x_coord_label.generate_target()
        x_coord_label.target.next_to(almost_fourier_label, DOWN)

        self.play(
            MoveToTarget(x_coord_label),
            Write(almost_fourier_label)
        )
        self.wait(2)

    ##

    def get_center_of_mass_dot(self):
        dot = Dot(
            self.get_pol_graph_center_of_mass(),
            color = self.center_of_mass_color
        )
        self.center_of_mass_dot = dot
        return dot

    def get_pol_graph_center_of_mass(self):
        pg = self.graph.polarized_mobject
        result = center_of_mass(pg.get_anchors())
        if self.center_of_mass_multiple != 1:
            mult = self.center_of_mass_multiple
            origin = self.circle_plane.coords_to_point(0, 0)
            result = mult*(result - origin) + origin
        return result

    def generate_fourier_dot_transform(self, fourier_graph):
        self.fourier_graph_dot = Dot(color = WHITE, radius = 0.05)
        def update_dot(dot):
            f = self.graph.polarized_mobject.frequency
            dot.move_to(self.frequency_axes.input_to_graph_point(
                f, fourier_graph
            ))
        self.fourier_graph_dot_anim = UpdateFromFunc(
            self.fourier_graph_dot, update_dot
        )
        self.fourier_graph_dot_anim.update(0)

    def get_fourier_graph_drawing_update_anim(self, fourier_graph):
        fourier_graph_copy = fourier_graph.copy()
        max_freq = self.frequency_axes.x_max
        def update_fourier_graph(fg):
            freq = self.graph.polarized_mobject.frequency
            fg.pointwise_become_partial(
                fourier_graph_copy,
                0, freq/max_freq
            )
            return fg
        self.fourier_graph_drawing_update_anim = UpdateFromFunc(
            fourier_graph, update_fourier_graph
        )
        return self.fourier_graph_drawing_update_anim

    def generate_center_of_mass_dot_update_anim(self, multiplier = 1):
        origin = self.circle_plane.coords_to_point(0, 0)
        com = self.get_pol_graph_center_of_mass
        self.center_of_mass_dot_anim = UpdateFromFunc(
            self.center_of_mass_dot, 
            lambda d : d.move_to(
                multiplier*(com()-origin)+origin
            )
        )

    def change_frequency(self, new_freq, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 3)
        rate_func = kwargs.pop("rate_func", None)
        if rate_func is None:
            rate_func = bezier([0, 0, 1, 1])
        added_anims = kwargs.get("added_anims", [])
        anims = [self.get_frequency_change_animation(self.graph, new_freq)]
        if hasattr(self, "winding_freq_label"):
            freq_label = [
                sm for sm in self.winding_freq_label
                if isinstance(sm, DecimalNumber)
            ][0]
            self.add(freq_label)
            anims.append(
                ChangeDecimalToValue(freq_label, new_freq)
            )
        if hasattr(self, "v_lines_indicating_periods"):
            anims.append(self.get_period_v_lines_update_anim())
        if hasattr(self, "center_of_mass_dot"):
            anims.append(self.center_of_mass_dot_anim)
        if hasattr(self, "fourier_graph_dot"):
            anims.append(self.fourier_graph_dot_anim)
        if hasattr(self, "fourier_graph_drawing_update_anim"):
            anims.append(self.fourier_graph_drawing_update_anim)
        for anim in anims:
            anim.rate_func = rate_func
        anims += added_anims
        self.play(*anims, **kwargs)

    def create_pi_creature(self):
        return Mortimer().to_corner(DOWN+RIGHT)



# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


USE_ALMOST_FOURIER_BY_DEFAULT = False


class FourierRecapScene(DrawFrequencyPlot):
    CONFIG = {
        "frequency_axes_config" : {
            "x_max" : 10.0,
            "x_axis_config" : {
                "unit_size" : 0.7,
                "numbers_to_show" : list(range(1, 10, 1)),
            }
        },
        "initial_winding_frequency" : 0.1,
    }
    def construct(self):
        self.setup_axes()
        self.preview_fourier_plot()
        self.wrap_signal_around_circle()
        self.match_winding_to_beat_frequency()
        self.follow_center_of_mass()
        self.draw_fourier_plot()
        self.set_color_spike()

    def setup_axes(self):
        self.remove(self.pi_creature)
        time_axes = self.get_time_axes()
        time_axes.to_edge(UP, buff = MED_SMALL_BUFF)
        time_axes.scale(0.9, about_edge = UP)
        frequency_axes = self.get_frequency_axes()
        circle_plane = self.get_circle_plane()

        self.add(time_axes)

        self.set_variables_as_attrs(
            time_axes, frequency_axes,
            circle_plane
        )

    def preview_fourier_plot(self):
        time_graph = self.graph = self.get_time_graph(
            width = 2,
            num_graph_points = 200,
        )
        fourier_graph = self.get_fourier_transform_graph(
            time_graph
        )
        fourier_graph.pointwise_become_partial(fourier_graph, 0.1, 1)

        #labels
        signal_label = OldTexText("Signal")
        fourier_label = OldTexText("Fourier transform")
        signal_label.next_to(time_graph, UP, buff = SMALL_BUFF)
        fourier_label.next_to(fourier_graph, UP)
        fourier_label.match_color(fourier_graph)

        self.play(
            ShowCreation(time_graph, run_time = 2),
            Write(signal_label),
        )
        self.wait()
        self.play(
            LaggedStartMap(FadeIn, self.frequency_axes),
            ReplacementTransform(
                time_graph.copy(),
                fourier_graph,
                run_time = 2
            ),
            ReplacementTransform(
                signal_label.copy(),
                fourier_label,
                run_time = 2,
                rate_func = squish_rate_func(smooth, 0.5, 1)
            ),
        )
        self.wait()
        self.play(LaggedStartMap(
            Indicate, self.frequency_axes.x_axis.numbers,
            run_time = 4,
            rate_func = wiggle,
        ))
        self.wait()
        self.play(*list(map(FadeOut, [
            self.frequency_axes, fourier_graph,
            signal_label,  fourier_label,
        ])))

        self.time_graph = time_graph
        self.set_variables_as_attrs(time_graph, fourier_label)

    def wrap_signal_around_circle(self):
        time_graph = self.time_graph
        circle_plane = self.circle_plane
        freq = self.initial_winding_frequency
        pol_graph = self.get_polarized_mobject(time_graph, freq)
        winding_freq_label = self.get_winding_frequency_label()
        winding_freq_label.add_to_back(BackgroundRectangle(winding_freq_label))
        winding_freq_label.move_to(circle_plane.get_top(), DOWN)

        self.add_foreground_mobjects(winding_freq_label)
        self.play(
            Write(circle_plane, run_time = 1),
            ReplacementTransform(
                time_graph.copy(), pol_graph,
                path_arc = -TAU/4,
                # CHANGE: removed stray kwarg run_time_per_flash: Cairo's Animation absorbed unknown kwargs, GL raises TypeError

                run_time = 2,
            ),
            FadeIn(winding_freq_label),
        )
        freq = 0.3
        self.change_frequency(freq, run_time = 2)
        ghost_pol_graph = pol_graph.copy()
        self.remove(pol_graph)
        self.play(ghost_pol_graph.set_stroke, {"width" : 0.5})
        self.play(
            *self.get_vector_animations(time_graph),
            run_time = 15
        )
        self.remove(ghost_pol_graph)
        self.wait()

    def match_winding_to_beat_frequency(self):
        self.v_lines_indicating_periods = self.get_v_lines_indicating_periods(0.3)
        self.add(self.v_lines_indicating_periods)
        for freq in range(1, 6):
            self.change_frequency(freq, run_time = 5)
        self.play(
            *self.get_vector_animations(
                self.time_graph,
                draw_polarized_graph = False
            ),
            run_time = 10
        )
        self.wait()

    def follow_center_of_mass(self):
        com_dot = self.get_center_of_mass_dot()
        self.generate_center_of_mass_dot_update_anim()
        com_arrow = Arrow(UP+3*RIGHT, ORIGIN)
        com_arrow.shift(com_dot.get_center())
        com_arrow.match_color(com_dot)
        com_words = OldTexText("Center of mass")
        com_words.next_to(com_arrow.get_start(), UP)
        com_words.match_color(com_arrow)
        com_words.add_background_rectangle()

        com_dot.save_state()
        com_dot.move_to(com_arrow.get_start())
        com_dot.fade(1)

        self.play(
            com_dot.restore,
            GrowArrow(com_arrow, rate_func = squish_rate_func(smooth, 0.2, 1)),
            Write(com_words),
        )
        self.wait()
        squished_func = squish_rate_func(smooth, 0, 0.2)
        self.change_frequency(
            4,
            added_anims = [
                FadeOut(com_arrow, rate_func = squished_func),
                FadeOut(com_words, rate_func = squished_func),
            ],
            run_time = 5
        )

    def draw_fourier_plot(self):
        frequency_axes = self.frequency_axes
        fourier_label = self.fourier_label

        self.change_frequency(0, run_time = 2)
        self.play(
            FadeIn(frequency_axes),
            FadeIn(fourier_label),
        )

        fourier_graph = self.get_fourier_transform_graph(self.time_graph)
        self.get_fourier_graph_drawing_update_anim(fourier_graph)
        self.generate_fourier_dot_transform(fourier_graph)

        self.change_frequency(5, run_time = 20)
        self.wait()
        self.change_frequency(7.5, run_time = 10)
        self.fourier_graph_drawing_update_anim = Animation(Mobject())
        self.fourier_graph = fourier_graph

    def set_color_spike(self):
        spike_point = self.frequency_axes.input_to_graph_point(
            5, self.fourier_graph
        )
        circle = Circle(color = YELLOW, radius = 0.25)
        circle.move_to(spike_point)
        circle.save_state()
        circle.scale(5)
        circle.fade(1)

        self.change_frequency(5)
        self.play(circle.restore)
        self.play(FadeOut(circle))
        self.wait()
        for x in range(2):
            self.change_frequency(5.2, run_time = 3)
            self.change_frequency(4.8, run_time = 3)
        self.change_frequency(5, run_time = 1.5)
        self.wait()


    #########

    def get_time_graph(self, frequency = 5, width = 2, **kwargs):
        # low_x = center-width/2
        # high_x = center+width/2
        # new_smooth = lambda x : np.clip(smooth((x+0.5)), 0, 1)
        # def func(x):
        #     pure_signal = 0.9*np.cos(TAU*frequency*x)
        #     factor = new_smooth(x - low_x) - new_smooth(x-high_x)
        #     return 1 + factor*pure_signal
        graph = self.time_axes.get_graph(
            lambda x : 1+0.9*np.cos(TAU*frequency*x),
            x_min = 0, x_max = width,
            **kwargs
        )
        graph.set_color(YELLOW)
        return graph


class CenterOfMassDescription(FourierRecapScene):
    def construct(self):
        self.remove(self.pi_creature)
        circle_plane = self.get_circle_plane()
        circle_plane.save_state()
        circle_plane.generate_target()
        circle_plane.target.set_height(FRAME_HEIGHT)
        circle_plane.target.center()
        circle_plane.target.axes.set_stroke(width = 2)
        # CHANGE: removed typo line circle_plane.targets.set_stroke(...): NumberPlane has no attribute targets (the line before already does the same on .target)
        pass  # circle_plane.targets.set_stroke(width = 2)
        circle_plane.target.secondary_lines.set_stroke(width = 1)

        start_coords = (0.5, 0.5)
        alt_coords = (0.8, 0.8)

        com_dot = Dot(color = self.center_of_mass_color)
        com_dot.move_to(circle_plane.coords_to_point(*start_coords))

        self.add(circle_plane, com_dot)
        self.wait()
        self.play(
            MoveToTarget(circle_plane),
            com_dot.move_to, 
            circle_plane.target.coords_to_point(*start_coords)
        )
        self.wait()

        alt_com_dot = com_dot.copy().move_to(
            circle_plane.coords_to_point(*alt_coords)
        )

        for dot in com_dot, alt_com_dot:
            line = Line(ORIGIN, dot.get_center())
            line.match_color(com_dot)
            angle = line.get_angle()
            line.rotate(-angle, about_point = ORIGIN)
            brace = Brace(line, UP)
            words = brace.get_text("Strength of frequency")
            words.add_background_rectangle()
            dot.length_label_group = VGroup(line, brace, words)
            dot.length_label_group.rotate(angle, about_point = ORIGIN)

        line, brace, words = com_dot.length_label_group
        self.play(
            GrowFromCenter(line),
            GrowFromCenter(brace),
            FadeIn(words),
        )
        self.wait()
        self.play(
            Transform(
                com_dot.length_label_group,
                alt_com_dot.length_label_group,
            ),
            Transform(com_dot, alt_com_dot),
            rate_func = there_and_back,
            run_time = 4,
        )

        #Do rotation
        line = com_dot.length_label_group[0]
        com_dot.length_label_group.remove(line)
        angle = line.get_angle()
        arc, alt_arc = [
            Arc(
                start_angle = 0, 
                angle = factor*angle,
                radius = 0.5,
            )
            for factor in (1, 2)
        ]
        theta = OldTex("\\theta")
        theta.shift(1.5*arc.point_from_proportion(0.5))

        self.play(
            FadeOut(com_dot.length_label_group),
            Animation(line),
            ShowCreation(arc),
            Write(theta)
        )
        self.play(
            Rotate(
                VGroup(line, com_dot),
                angle, about_point = ORIGIN
            ),
            Transform(arc, alt_arc),
            theta.move_to, 1.5*alt_arc.point_from_proportion(0.5),
            rate_func = there_and_back,
            run_time = 4
        )
        self.wait()
