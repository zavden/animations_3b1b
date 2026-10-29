# ==============================================================================
# Scene:      CleanerFourierTradeoff
# Source:     videos/_2018/uncertainty.py (lines 1642-1647)
# Category:   1 · Renders unmodified
# Includes code copied from: _2018/fourier.py
#
# Run from this folder:
#     manimgl CleanerFourierTradeoff.py CleanerFourierTradeoff -w -m --fps 15
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


FREQUENCY_COLOR = RED


class FourierTradeoff(Scene):
    CONFIG = {
        "show_text" : True,
        "complex_to_real_func" : lambda z : z.real,
        "widths" : [6, 0.02, 1],
    }
    def construct(self):
        #Setup axes
        time_mean = 4
        time_axes = Axes(
            x_min = 0,
            x_max = 2*time_mean,
            x_axis_config = {"unit_size" : 1.5},
            y_min = -2, 
            y_max = 2,
            y_axis_config = {"unit_size" : 0.5}
        )
        time_label = OldTexText("Time")
        time_label.scale(1.5)
        time_label.next_to(
            time_axes.x_axis.get_right(), UP+LEFT,
            buff = MED_SMALL_BUFF,
        )
        time_axes.add(time_label)
        time_axes.center().to_edge(UP)
        time_axes.x_axis.add_numbers(*list(range(1, 2*time_mean)))

        frequency_axes = Axes(
            x_min = 0,
            x_max = 8,
            x_axis_config = {"unit_size" : 1.5},
            y_min = -0.025,
            y_max = 0.075,
            y_axis_config = {
                "unit_size" : 30,
                "tick_frequency" : 0.025,
            },
            color = TEAL,
        )
        frequency_label = OldTexText("Frequency")
        frequency_label.scale(1.5)
        frequency_label.next_to(
            frequency_axes.x_axis.get_right(), UP+LEFT,
            buff = MED_SMALL_BUFF, 
        )
        frequency_label.set_color(FREQUENCY_COLOR)
        frequency_axes.add(frequency_label)
        frequency_axes.move_to(time_axes, LEFT)
        frequency_axes.to_edge(DOWN, buff = LARGE_BUFF)
        frequency_axes.x_axis.add_numbers()

        # Graph information

        #x-coordinate of this point determines width of wave_packet graph
        width_tracker = ExponentialValueTracker(0.5)
        get_width = width_tracker.get_value

        def get_wave_packet_function():
            factor = 1./get_width()
            return lambda t : (factor**0.25)*np.cos(4*TAU*t)*np.exp(-factor*(t-time_mean)**2)

        def get_wave_packet():
            graph = time_axes.get_graph(
                get_wave_packet_function(),
                num_graph_points = 200,
            )
            graph.set_color(YELLOW)
            return graph

        time_radius = 10
        def get_wave_packet_fourier_transform():
            return get_fourier_graph(
                frequency_axes, 
                get_wave_packet_function(),
                t_min = time_mean - time_radius,
                t_max = time_mean + time_radius,
                n_samples = 2*time_radius*17,
                complex_to_real_func = self.complex_to_real_func,
                color = FREQUENCY_COLOR,
            )

        wave_packet = get_wave_packet()
        wave_packet_update = UpdateFromFunc(
            wave_packet, 
            lambda g : Transform(g, get_wave_packet()).update(1)
        )
        fourier_graph = get_wave_packet_fourier_transform()
        fourier_graph_update = UpdateFromFunc(
            fourier_graph, 
            lambda g : Transform(g, get_wave_packet_fourier_transform()).update(1)
        )

        arrow = Arrow(
            wave_packet, frequency_axes.coords_to_point(
                4, frequency_axes.y_max/2,
            ),
            color = FREQUENCY_COLOR,
        )
        fourier_words = OldTexText("Fourier Transform")
        fourier_words.next_to(arrow, LEFT, buff = MED_LARGE_BUFF)
        sub_words = OldTexText("(To be explained shortly)")
        sub_words.set_color(BLUE)
        sub_words.scale(0.75)
        sub_words.next_to(fourier_words, DOWN)

        #Draw items
        self.add(time_axes, frequency_axes)
        self.play(ShowCreation(wave_packet, rate_func = double_smooth))
        anims = [ReplacementTransform(
            wave_packet.copy(), fourier_graph
        )]
        if self.show_text:
            anims += [
                GrowArrow(arrow),
                Write(fourier_words, run_time = 1)
            ]
        self.play(*anims)
        # self.play(FadeOut(arrow))
        self.wait()
        for width in self.widths:
            self.play(
                width_tracker.set_value, width,
                wave_packet_update,
                fourier_graph_update,
                run_time = 3
            )
            if sub_words not in self.mobjects and self.show_text:
                self.play(FadeIn(sub_words))
            else:
                self.wait()
        self.wait()


class CleanerFourierTradeoff(FourierTradeoff):
    CONFIG = {
        "show_text" : False,
        "complex_to_real_func" : lambda z : z.real,
        "widths" : [0.02, 6, 1],
    }
