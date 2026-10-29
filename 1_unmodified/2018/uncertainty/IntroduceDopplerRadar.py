# ==============================================================================
# Scene:      IntroduceDopplerRadar
# Source:     videos/_2018/uncertainty.py (lines 1688-2044)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/fourier.py
#
# Run from this folder:
#     manimgl IntroduceDopplerRadar.py IntroduceDopplerRadar -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *
import warnings


# ----- From _2018/fourier.py -----

NUM_SAMPLES_FOR_FFT = 1000


def get_fourier_graph(
    axes, time_func, t_min, t_max,
    n_samples = NUM_SAMPLES_FOR_FFT,
    complex_to_real_func = lambda z : z.real,
    color = RED,
    ):
    # N = n_samples
    # T = time_range/n_samples
    time_range = float(t_max - t_min)
    time_step_size = time_range/n_samples
    time_samples = np.vectorize(time_func)(np.linspace(t_min, t_max, n_samples))
    fft_output = np.fft.fft(time_samples)
    frequencies = np.linspace(0.0, n_samples/(2.0*time_range), n_samples//2)
    #  #Cycles per second of fouier_samples[1]
    # (1/time_range)*n_samples
    # freq_step_size = 1./time_range
    graph = VMobject()
    graph.set_points_smoothly([
        axes.coords_to_point(
            x, complex_to_real_func(y)/n_samples,
        )
        for x, y in zip(frequencies, fft_output[:n_samples//2])
    ])
    graph.set_color(color)
    f_min, f_max = [
        axes.x_axis.point_to_number(graph.get_points()[i])
        for i in (0, -1)
    ]
    graph.underlying_function = lambda f : axes.y_axis.point_to_number(
        graph.point_from_proportion((f - f_min)/(f_max - f_min))
    )
    return graph



# ----- From _2018/uncertainty.py -----

warnings.warn("""
    Warning: This file makes use of
    ContinualAnimation, which has since
    been deprecated
""")


class RadarDish(SVGMobject):
    CONFIG = {
        "file_name" : "radar_dish",
        "fill_color" : GREY_B,
        "stroke_color" : WHITE,
        "stroke_width" : 1,
        "height" : 1,
    }


class Plane(SVGMobject):
    CONFIG = {
        "file_name" : "plane",
        "color" : GREY_B,
        "height" : 1,
    }
    def __init__(self, **kwargs):
        SVGMobject.__init__(self, **kwargs)
        self.rotate(-TAU/4)


class RadarPulseSingleton(ContinualAnimation):
    CONFIG = {
        "speed" : 3.0,
        "direction" : RIGHT,
        "start_up_time" : 0,
        "fade_in_time" : 0.5,
        "color" : WHITE,
        "stroke_width" : 3,
    }
    def __init__(self, radar_dish, target, **kwargs):
        digest_config(self, kwargs)
        self.direction = self.direction/get_norm(self.direction)
        self.radar_dish = radar_dish
        self.target = target
        self.reflection_distance = None
        self.arc = Arc(
            start_angle = -30*DEGREES,
            angle = 60*DEGREES,
        )
        self.arc.set_height(0.75*radar_dish.get_height())
        self.arc.move_to(radar_dish, UP+RIGHT)
        self.start_points = np.array(self.arc.get_points())
        self.start_center = self.arc.get_center()
        self.finished = False

        ContinualAnimation.__init__(self, self.arc, **kwargs)
        
    def update_mobject(self, dt):
        arc = self.arc
        total_distance = self.speed*self.internal_time
        arc.set_points(self.start_points)
        arc.shift(total_distance*self.direction)

        if self.internal_time < self.fade_in_time:
            alpha = np.clip(self.internal_time/self.fade_in_time, 0, 1)
            arc.set_stroke(self.color, alpha*self.stroke_width)

        if self.reflection_distance is None:
            #Check if reflection is happening
            arc_point = arc.get_edge_center(self.direction)
            target_point = self.target.get_edge_center(-self.direction)
            arc_distance = np.dot(arc_point, self.direction)
            target_distance = np.dot(target_point, self.direction)
            if arc_distance > target_distance:
                self.reflection_distance = target_distance
        #Don't use elif in case the above code creates reflection_distance
        if self.reflection_distance is not None:
            delta_distance = total_distance - self.reflection_distance
            point_distances = np.dot(self.direction, arc.get_points().T)
            diffs = point_distances - self.reflection_distance
            shift_vals = np.outer(-2*np.maximum(diffs, 0), self.direction)
            arc.set_points(arc.get_points() + shift_vals)

            #Check if done
            arc_point = arc.get_edge_center(-self.direction)
            if np.dot(arc_point, self.direction) < np.dot(self.start_center, self.direction):
                self.finished = True
                self.arc.fade(1)

    def is_finished(self):
        return self.finished


class RadarPulse(ContinualAnimation):
    CONFIG = {
        "n_pulse_singletons" : 8,
        "frequency" : 0.05,
        "colors" : [BLUE, YELLOW]
    }
    def __init__(self, *args, **kwargs):
        digest_config(self, kwargs)
        colors = color_gradient(self.colors, self.n_pulse_singletons)
        self.pulse_singletons = [
            RadarPulseSingleton(*args, color = color, **kwargs)
            for color in colors
        ]
        pluse_mobjects = VGroup(*[ps.mobject for ps in self.pulse_singletons])
        ContinualAnimation.__init__(self, pluse_mobjects, **kwargs)
        
    def update_mobject(self, dt):
        for i, ps in enumerate(self.pulse_singletons):
            ps.internal_time = self.internal_time - i*self.frequency
            ps.update_mobject(dt)

    def is_finished(self):
        return all([ps.is_finished() for ps in self.pulse_singletons])


class IntroduceDopplerRadar(Scene):
    CONFIG = {
        "frequency_spread_factor" : 100,
    }
    def construct(self):
        self.setup_axes()
        self.measure_distance_with_time()
        self.show_frequency_shift()
        self.show_frequency_shift_in_fourier()

    def setup_axes(self):
        self.dish = RadarDish()
        self.dish.to_corner(UP+LEFT)
        axes = Axes(
            x_min = 0,
            x_max = 10,
            y_min = -1.5,
            y_max = 1.5
        )
        axes.move_to(DOWN)
        time_label = OldTexText("Time")
        time_label.next_to(axes.x_axis.get_right(), UP)
        axes.time_label = time_label
        axes.add(time_label)
        self.axes = axes

        self.add(self.dish)
        self.add(axes)

    def measure_distance_with_time(self):
        dish = self.dish
        axes = self.axes
        distance = 5
        time_diff = 5
        speed = (2*distance)/time_diff
        randy = Randolph().flip()
        randy.match_height(dish)
        randy.move_to(dish.get_right(), LEFT)
        randy.shift(distance*RIGHT)

        pulse_graph, echo_graph, sum_graph = \
            self.get_pulse_and_echo_graphs(
                self.get_single_pulse_graph,
                (1,), (1+time_diff,)
            )
        words = ["Original signal", "Echo"]
        for graph, word in zip([pulse_graph, echo_graph], words):
            arrow = Vector(DOWN)
            arrow.next_to(graph.peak_point, UP, SMALL_BUFF)
            arrow.match_color(graph)
            graph.arrow = arrow
            label = OldTexText(word)
            label.next_to(arrow.get_start(), UP, SMALL_BUFF)
            label.match_color(graph)
            graph.label = label

        double_arrow = DoubleArrow(
            pulse_graph.peak_point,
            echo_graph.peak_point,
            color = WHITE
        )
        distance_text = OldTexText("$2 \\times$ distance/(signal speed)")
        distance_text.set_width(0.9*double_arrow.get_width())
        distance_text.next_to(double_arrow, UP, SMALL_BUFF)

        #v_line anim?

        pulse = RadarPulseSingleton(
            dish, randy, 
            speed = 0.97*speed, #Just needs slightly better alignment
        )
        graph_draw = turn_animation_into_updater(
            ShowCreation(
                sum_graph, 
                rate_func=linear, 
                run_time = 0.97*axes.x_max
            )
        )
        randy_look_at = Mobject.add_updater(
            randy, lambda pi : pi.look_at(pulse.mobject)
        )
        axes_anim = ContinualAnimation(axes)

        self.add(randy_look_at, axes_anim, graph_draw)
        self.wait(0.5)
        self.add(pulse)
        self.play(
            Write(pulse_graph.label),
            GrowArrow(pulse_graph.arrow),
            run_time = 1,
        )
        self.play(randy.change, "pondering")
        self.wait(time_diff - 2)
        self.play(
            Write(echo_graph.label),
            GrowArrow(echo_graph.arrow),
            run_time = 1
        )
        self.wait()
        self.play(
            GrowFromCenter(double_arrow),
            FadeIn(distance_text)
        )
        self.wait()

        self.remove(graph_draw, pulse, randy_look_at, axes_anim)
        self.add(axes)
        self.play(LaggedStartMap(FadeOut, VGroup(
            sum_graph, randy,
            pulse_graph.arrow, pulse_graph.label,
            echo_graph.arrow, echo_graph.label,
            double_arrow, distance_text
        )))

    def show_frequency_shift(self):
        axes = self.axes
        dish = self.dish
        plane = Plane()
        plane.flip()
        plane.move_to(dish)
        plane.to_edge(RIGHT)

        time_diff = 6

        pulse_graph, echo_graph, sum_graph = graphs = \
            self.get_pulse_and_echo_graphs(
                self.get_frequency_pulse_graph,
                (1,25), (1+time_diff,50)
            )
        for graph in graphs:
            graph.set_stroke(width = 3)
        signal_graph = self.get_frequency_pulse_graph(1)

        pulse_brace = Brace(Line(ORIGIN, RIGHT), UP)
        pulse_brace.move_to(axes.coords_to_point(1, 1.2))
        echo_brace = pulse_brace.copy()
        echo_brace.stretch(0.6, 0)
        echo_brace.move_to(axes.coords_to_point(7, 1.2))
        pulse_text = pulse_brace.get_text("Original signal")
        pulse_text.add_background_rectangle()
        echo_text = echo_brace.get_text("Echo")
        echo_subtext = OldTexText("(Higher frequency)")
        echo_subtext.next_to(echo_text, RIGHT)
        echo_subtext.match_color(echo_graph)

        graph_draw = turn_animation_into_updater(
            ShowCreation(sum_graph, run_time = 8, rate_func=linear)
        )
        pulse = RadarPulse(dish, plane, n_pulse_singletons = 12)
        always_shift(plane, LEFT, 1.5)

        self.add(graph_draw, pulse, plane)
        self.play(UpdateFromAlphaFunc(
            plane, lambda m, a : m.set_fill(opacity = a)
        ))
        self.play(
            GrowFromCenter(pulse_brace),
            FadeIn(pulse_text),
        )
        self.wait(3)
        self.play(
            GrowFromCenter(echo_brace),
            GrowFromCenter(echo_text),
        )
        self.play(UpdateFromAlphaFunc(
            plane, lambda m, a : m.set_fill(opacity = 1-a)
        ))
        #Only for when -s is run
        graph_draw.update(10) 
        self.wait(0.1)
        self.play(Write(echo_subtext, run_time = 1))
        self.wait()
        self.remove(graph_draw, pulse, plane)

        pulse_graph.set_stroke(width = 0)
        echo_graph.set_stroke(width = 0)
        self.time_graph_group = VGroup(
            axes, pulse_brace, pulse_text,
            echo_brace, echo_text, echo_subtext,
            pulse_graph, echo_graph, sum_graph,
        )
        self.set_variables_as_attrs(*self.time_graph_group)

    def show_frequency_shift_in_fourier(self):
        sum_graph = self.sum_graph
        pulse_graph = self.pulse_graph
        pulse_label = VGroup(self.pulse_brace, self.pulse_text)
        echo_graph = self.echo_graph
        echo_label = VGroup(
            self.echo_brace, self.echo_text, self.echo_subtext
        )

        #Setup all fourier graph stuff
        f_max = 0.02
        frequency_axes = Axes(
            x_min = 0, x_max = 20,
            x_axis_config = {"unit_size" : 0.5},
            y_min = -f_max, y_max = f_max,
            y_axis_config = {
                "unit_size" : 50,
                "tick_frequency" : 0.01,
            },
        )
        frequency_axes.move_to(self.axes, LEFT)
        frequency_axes.to_edge(DOWN)
        frequency_label = OldTexText("Frequency")
        frequency_label.next_to(
            frequency_axes.x_axis.get_right(), UP,
        )
        frequency_label.to_edge(RIGHT)
        frequency_axes.add(frequency_label)

        for graph in pulse_graph, echo_graph, sum_graph:
            graph.fourier_transform = get_fourier_graph(
                frequency_axes, graph.underlying_function,
                frequency_axes.x_min, 25,
                complex_to_real_func = abs,
            )

        #Braces labeling F.T.
        original_fourier_brace = Brace(
            Line(
                frequency_axes.coords_to_point(7, 0.9*f_max),
                frequency_axes.coords_to_point(9, 0.9*f_max),
            ),
            UP,
        ).set_color(BLUE)
        echo_fourier_brace = Brace(
            Line(
                frequency_axes.coords_to_point(14, 0.4*f_max),
                frequency_axes.coords_to_point(18, 0.4*f_max),
            ),
            UP,
        ).set_color(YELLOW)
        # braces = [original_fourier_brace, echo_fourier_brace]
        # words = ["original signal", "echo"]
        # for brace, word in zip(braces, words):
        #     brace.add(brace.get_text("F.T. of \\\\ %s"%word))
        fourier_label = OldTex("||\\text{Fourier transform}||")
        # fourier_label.next_to(sum_graph.fourier_transform, UP, MED_LARGE_BUFF)
        fourier_label.next_to(frequency_axes.y_axis, UP, buff = SMALL_BUFF)
        fourier_label.shift_onto_screen()
        fourier_label.set_color(RED)


        #v_lines
        v_line = DashedLine(
            frequency_axes.coords_to_point(8, 0),
            frequency_axes.coords_to_point(8, 1.2*f_max),
            color = YELLOW,
            dash_length = 0.025,
        )
        v_line_pair = VGroup(*[
            v_line.copy().shift(u*0.6*RIGHT)
            for u in (-1, 1)
        ])
        v_line = VGroup(v_line)

        double_arrow = DoubleArrow(
            frequency_axes.coords_to_point(8, 0.007),
            frequency_axes.coords_to_point(16, 0.007),
            buff = 0,
            color = WHITE
        )

        self.play(
            self.time_graph_group.to_edge, UP,
            ApplyMethod(
                self.dish.shift, 2*UP, 
                remover = True
            ),
            FadeIn(frequency_axes)
        )
        self.wait()
        self.play(
            FadeOut(sum_graph),
            FadeOut(echo_label),
            pulse_graph.set_stroke, {"width" : 3},
        )
        self.play(
            ReplacementTransform(
                pulse_label[0].copy(),
                original_fourier_brace
            ),
            ShowCreation(pulse_graph.fourier_transform)
        )
        self.play(Write(fourier_label))
        self.wait()
        self.play(ShowCreation(v_line))
        self.wait()
        self.play(ReplacementTransform(v_line, v_line_pair))
        self.wait()
        self.play(FadeOut(v_line_pair))
        self.wait()

        self.play(
            FadeOut(pulse_graph),
            FadeIn(sum_graph),
            ReplacementTransform(
                pulse_graph.fourier_transform,
                sum_graph.fourier_transform
            )
        )
        self.play(FadeIn(echo_label))
        self.play(ReplacementTransform(
            echo_label[0].copy(),
            echo_fourier_brace,
        ))
        self.wait(2)
        self.play(GrowFromCenter(double_arrow))
        self.wait()


    ###

    def get_graph(self, func, **kwargs):
        graph = self.axes.get_graph(func, **kwargs)
        graph.peak_point = self.get_peak_point(graph)
        return graph

    def get_single_pulse_graph(self, x, **kwargs):
        return self.get_graph(self.get_single_pulse_function(x), **kwargs)

    def get_single_pulse_function(self, x):
        return lambda t : -2*np.sin(10*(t-x))*np.exp(-100*(t-x)**2)

    def get_frequency_pulse_graph(self, x, freq = 50, **kwargs):
        return self.get_graph(
            self.get_frequency_pulse_function(x, freq), 
            num_graph_points = 700,
            **kwargs
        )

    def get_frequency_pulse_function(self, x, freq):
        factor = self.frequency_spread_factor
        return lambda t : op.mul(
            2*np.cos(2*freq*(t-x)),
            min(np.exp(-(freq**2/factor)*(t-x)**2), 0.5)
        )

    def get_peak_point(self, graph):
        anchors = graph.get_anchors()
        return anchors[np.argmax([p[1] for p in anchors])]

    def get_pulse_and_echo_graphs(self, func, args1, args2):
        pulse_graph = func(*args1, color = BLUE)
        echo_graph = func(*args2, color = YELLOW)
        sum_graph = self.axes.get_graph(
            lambda x : sum([
                pulse_graph.underlying_function(x),
                echo_graph.underlying_function(x),
            ]),
            num_graph_points = echo_graph.get_num_curves(),
            color = WHITE
        )
        sum_graph.background_image_file = "blue_yellow_gradient"
        return pulse_graph, echo_graph, sum_graph
