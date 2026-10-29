# ==============================================================================
# Scene:      ProbabalisticDetection
# Source:     videos/_2018/uncertainty.py (lines 3994-4124)
# Category:   2 · Renders with modifications
# Includes code copied from: _2018/fourier.py
#
# Run from this folder:
#     manimgl ProbabalisticDetection.py ProbabalisticDetection -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the line endpoints can swap order while the path_arc animation interpolates the wrapper line, giving a negative sigma; a standard deviation is a magnitude, so use abs()
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


class GaussianDistributionWrapper(Line):
    """
    This is meant to encode a 2d normal distribution as
    a mobject (so as to be able to have it be interpolated
    during animations).  It is a line whose center is the mean
    mu of a distribution, and whose radial vector (center to end)
    is the distribution's standard deviation
    """
    CONFIG = {
        "stroke_width" : 0,
        "mu" : ORIGIN,
        "sigma" : RIGHT,
    }
    def __init__(self, **kwargs):
        Line.__init__(self, ORIGIN, RIGHT, **kwargs)
        self.change_parameters(self.mu, self.sigma)

    def change_parameters(self, mu = None, sigma = None):
        curr_mu, curr_sigma = self.get_parameters()
        mu = mu if mu is not None else curr_mu
        sigma = sigma if sigma is not None else curr_sigma
        self.put_start_and_end_on(mu - sigma, mu + sigma)
        return self

    def get_parameters(self):
        """ Return mu_x, mu_y, sigma_x, sigma_y"""
        center, end = self.get_center(), self.get_end()
        return center, end-center

    def get_random_points(self, size = 1):
        mu, sigma = self.get_parameters()
        return np.array([
            np.array([
                # CHANGE: the line endpoints can swap order while the path_arc animation interpolates the wrapper line, giving a negative sigma; a standard deviation is a magnitude, so use abs()
                np.random.normal(mu_coord, abs(sigma_coord))
                for mu_coord, sigma_coord in zip(mu, sigma)
            ])
            for x in range(size)
        ])


class ProbabalisticMobjectCloud(ContinualAnimation):
    CONFIG = {
        "fill_opacity" : 0.25,
        "n_copies" : 100,
        "gaussian_distribution_wrapper_config" : {},
        "time_per_change" : 1./60,
        "start_up_time" : 0,
    }
    def __init__(self, prototype, **kwargs):
        digest_config(self, kwargs)
        fill_opacity = self.fill_opacity or prototype.get_fill_opacity()
        if "mu" not in self.gaussian_distribution_wrapper_config:
            self.gaussian_distribution_wrapper_config["mu"] = prototype.get_center()
        self.gaussian_distribution_wrapper = GaussianDistributionWrapper(
            **self.gaussian_distribution_wrapper_config
        )
        self.time_since_last_change = np.inf
        group = VGroup(*[
            prototype.copy().set_fill(opacity = fill_opacity)
            for x in range(self.n_copies)
        ])
        ContinualAnimation.__init__(self, group, **kwargs)
        self.update_mobject(0)

    def update_mobject(self, dt):
        self.time_since_last_change += dt
        if self.time_since_last_change < self.time_per_change:
            return
        self.time_since_last_change = 0

        group = self.mobject
        points = self.gaussian_distribution_wrapper.get_random_points(len(group))
        for mob, point in zip(group, points):
            self.update_mobject_by_point(mob, point)
        return self

    def update_mobject_by_point(self, mobject, point):
        mobject.move_to(point)
        return self


class ProbabalisticDotCloud(ProbabalisticMobjectCloud):
    CONFIG = {
        "color" : BLUE,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        dot = Dot(color = self.color)
        ProbabalisticMobjectCloud.__init__(self, dot)


class FourierTransformOfWaveFunction(Scene):
    CONFIG = {
        "wave_stroke_width" : 3,
        "wave_color" : BLUE,
    }
    def construct(self):
        self.show_wave_packet()
        self.take_fourier_transform()
        self.show_correlations_with_pure_frequencies()
        self.this_is_momentum()
        self.show_tradeoff()

    def setup(self):
        self.x0_tracker = ValueTracker(-3)
        self.k_tracker = ValueTracker(1)
        self.a_tracker = ExponentialValueTracker(0.5)

    def show_wave_packet(self):
        axes = Axes(
            x_min = 0, x_max = 12,
            y_min = -1, y_max = 1,
            y_axis_config = {
                "tick_frequency" : 0.5
            }
        )
        position_label = OldTexText("Position")
        position_label.next_to(axes.x_axis.get_right(), UP)
        axes.add(position_label)
        axes.center().to_edge(UP, buff = LARGE_BUFF)

        wave = self.get_wave(axes)
        wave_update_animation = UpdateFromFunc(
            wave, lambda w : Transform(w, self.get_wave(axes)).update(1)
        )

        self.add(axes, wave)
        self.play(
            self.x0_tracker.set_value, 5,
            wave_update_animation,
            run_time = 3,
        )
        self.wait()

        self.wave_function = wave.underlying_function
        self.wave_update_animation = wave_update_animation
        self.wave = wave
        self.axes = axes

    def take_fourier_transform(self):
        wave = self.wave
        wave_update_animation = self.wave_update_animation
        frequency_axes = Axes(
            x_min = 0, x_max = 3,
            x_axis_config = {
                "unit_size" : 4,
                "tick_frequency" : 0.25,
                "big_tick_numbers" : [1, 2]
            },
            y_min = -0.15,
            y_max = 0.15,
            y_axis_config = {
                "unit_size" : 7.5,
                "tick_frequency" : 0.05,
            }
        )
        label = self.frequency_x_axis_label = OldTexText("Spatial frequency")
        label.next_to(frequency_axes.x_axis.get_right(), UP)
        frequency_axes.add(label)
        frequency_axes.move_to(self.axes, LEFT)
        frequency_axes.to_edge(DOWN, buff = LARGE_BUFF)
        label.shift_onto_screen()

        def get_wave_function_fourier_graph():
            return get_fourier_graph(
                frequency_axes, self.get_wave_func(),
                t_min = 0, t_max = 15,
            )
        fourier_graph = get_wave_function_fourier_graph()
        self.fourier_graph_update_animation = UpdateFromFunc(
            fourier_graph, lambda m : Transform(
                m, get_wave_function_fourier_graph()
            ).update(1)
        )

        wave_copy = wave.copy()
        wave_copy.generate_target()
        wave_copy.target.move_to(fourier_graph, LEFT)
        wave_copy.target.fade(1)
        fourier_graph.save_state()
        fourier_graph.move_to(wave, LEFT)
        fourier_graph.fade(1)

        arrow = Arrow(
            self.axes.coords_to_point(5, -1),
            frequency_axes.coords_to_point(1, 0.1),
            color = YELLOW,
        )
        fourier_label = OldTexText("Fourier Transform")
        fourier_label.next_to(arrow.get_center(), RIGHT)

        self.play(ReplacementTransform(
            self.axes.copy(), frequency_axes
        ))
        self.play(
            MoveToTarget(wave_copy, remover = True),
            fourier_graph.restore,
            GrowArrow(arrow),
            Write(fourier_label, run_time = 1),
        )
        self.wait()

        self.frequency_axes = frequency_axes
        self.fourier_graph = fourier_graph
        self.fourier_label = VGroup(arrow, fourier_label)

    def show_correlations_with_pure_frequencies(self):
        frequency_axes = self.frequency_axes
        axes = self.axes

        sinusoid = axes.get_graph(
            lambda x : 0.5*np.cos(TAU*x),
            x_min = -FRAME_X_RADIUS, x_max = 3*FRAME_X_RADIUS,
        )
        sinusoid.to_edge(UP, buff = SMALL_BUFF)

        v_line = DashedLine(1.5*UP, ORIGIN, color = YELLOW)
        v_line.move_to(frequency_axes.coords_to_point(1, 0), DOWN)

        f_equals = OldTex("f = ")
        freq_decimal = DecimalNumber(1)
        freq_decimal.next_to(f_equals, RIGHT, buff = SMALL_BUFF)
        freq_label = VGroup(f_equals, freq_decimal)
        freq_label.next_to(
            v_line, UP, SMALL_BUFF, 
            submobject_to_align = f_equals[0]
        )

        self.play(
            ShowCreation(sinusoid),
            ShowCreation(v_line),
            Write(freq_label, run_time = 1),
            FadeOut(self.fourier_label)
        )
        last_f = 1
        for f in 1.4, 0.7, 1:
            self.play(
                sinusoid.stretch,f/last_f, 0, 
                    {"about_point" : axes.coords_to_point(0, 0)},
                v_line.move_to, frequency_axes.coords_to_point(f, 0), DOWN,
                MaintainPositionRelativeTo(freq_label, v_line),
                ChangeDecimalToValue(freq_decimal, f),
                run_time = 3,
            )
            last_f = f
        self.play(*list(map(FadeOut, [
            sinusoid, v_line,  freq_label
        ])))

    def this_is_momentum(self):
        formula = OldTex("p", "=", "h", "\\xi")
        formula.set_color_by_tex_to_color_map({
            "p" : BLUE,
            "xi" : YELLOW,
        })
        formula.next_to(
            self.frequency_x_axis_label, UP
        )

        f_max = 0.12
        brace = Brace(Line(2*LEFT, 2*RIGHT), UP)
        brace.move_to(self.frequency_axes.coords_to_point(1, f_max), DOWN)
        words = OldTexText("This wave \\\\ describes momentum")
        words.next_to(brace, UP)

        self.play(Write(formula))
        self.wait()
        self.play(
            GrowFromCenter(brace),
            Write(words)
        )
        brace.add(words)
        for k in 2, 0.5, 1:
            self.play(
                self.k_tracker.set_value, k,
                self.wave_update_animation,
                self.fourier_graph_update_animation,
                UpdateFromFunc(
                    brace, lambda b : b.move_to(
                        self.frequency_axes.coords_to_point(
                            self.k_tracker.get_value(),
                            f_max,
                        ),
                        DOWN
                    )
                ),
                run_time = 2
            )
        self.wait()
        self.play(*list(map(FadeOut, [brace, words, formula])))

    def show_tradeoff(self):
        for a in 5, 0.1, 0.01, 10, 0.5:
            self.play(
                ApplyMethod(
                    self.a_tracker.set_value, a,
                    run_time = 2
                ),
                self.wave_update_animation,
                self.fourier_graph_update_animation
            )
            self.wait()

    ##

    def get_wave_func(self):
        x0 = self.x0_tracker.get_value()
        k = self.k_tracker.get_value()
        a = self.a_tracker.get_value()
        A = a**(0.25)
        return lambda x : A*np.cos(TAU*k*x)*np.exp(-a*(x - x0)**2)

    def get_wave(self, axes):
        return axes.get_graph(
            self.get_wave_func(), 
            color = self.wave_color,
            stroke_width = self.wave_stroke_width
        )


class ProbabalisticDetection(FourierTransformOfWaveFunction):
    CONFIG = {
        "wave_stroke_width" : 2,
    }
    def construct(self):
        self.setup_wave()
        self.detect_only_single_points()
        self.show_probability_distribution()
        self.show_concentration_of_the_wave()

    def setup_wave(self):
        axes = Axes(
            x_min = 0, x_max = 10,
            y_min = -0.5, y_max = 1.5,
            y_axis_config = {
                "unit_size" : 1.5,
                "tick_frequency" : 0.25,
            }
        )
        axes.set_stroke(width = 2)
        axes.center()
        self.x0_tracker.set_value(5)
        self.k_tracker.set_value(1)
        self.a_tracker.set_value(0.2)
        wave = self.get_wave(axes)
        self.wave_update_animation = UpdateFromFunc(
            wave, lambda w : Transform(w, self.get_wave(axes)).update(1)
        )

        self.k_tracker.save_state()
        self.k_tracker.set_value(0)
        bell_curve = self.get_wave(axes)
        self.k_tracker.restore()
        bell_curve.set_stroke(width = 0)
        bell_curve.set_fill(BLUE, opacity = 0.5)
        squared_bell_curve = axes.get_graph(
            lambda x : bell_curve.underlying_function(x)**2
        ).match_style(bell_curve)

        self.set_variables_as_attrs(
            axes, wave, bell_curve, squared_bell_curve
        )

    def detect_only_single_points(self):
        particle = ProbabalisticDotCloud(
            n_copies = 100, 
            fill_opacity = 0.05, 
            time_per_change = 0.05,
        )
        particle.mobject[0].set_fill(BLUE, opacity = 1)
        gdw = particle.gaussian_distribution_wrapper

        rect = Rectangle(
            stroke_width = 0,
            height = 0.5,
            width = 2,
        )
        rect.set_fill(YELLOW, 0.3)
        rect.move_to(self.axes.coords_to_point(self.x0_tracker.get_value(), 0))
        brace = Brace(rect, UP, buff = 0)
        question = OldTexText("Do we detect the particle \\\\ in this region?")
        question.next_to(brace, UP)
        question.add_background_rectangle()
        rect.save_state()
        rect.stretch(0, 0)

        gdw_anim = Mobject.add_updater(
            gdw, lambda m : m.set_width(
                2.0/(self.a_tracker.get_value()**(0.5))
            ).move_to(rect)
        )

        self.add(rect, brace, question)

        yes = OldTexText("Yes").set_color(GREEN)
        no = OldTexText("No").set_color(RED)
        for word in yes, no:
            word.next_to(rect, DOWN)
            # word.add_background_rectangle()
        answer = VGroup()
        def update_answer(answer):
            px = particle.mobject[0].get_center()[0]
            lx = rect.get_left()[0]
            rx = rect.get_right()[0]
            if lx < px < rx:
                answer.submobjects = [yes]
            else:
                answer.submobjects = [no]
        answer_anim = Mobject.add_updater(answer, update_answer)

        self.add(gdw_anim, particle)
        self.play(
            GrowFromCenter(brace),
            rect.restore,
            Write(question)
        )
        self.wait()
        self.add(answer_anim)
        self.wait(4)
        self.add_foreground_mobjects(answer, particle.mobject)

        self.question_group = VGroup(question, brace)
        self.particle = particle
        self.rect = rect

    def show_probability_distribution(self):
        axes = self.axes
        wave = self.wave
        bell_curve = self.bell_curve
        question_group = self.question_group
        gdw = self.particle.gaussian_distribution_wrapper
        rect = self.rect

        v_lines = VGroup(*[
            DashedLine(ORIGIN, 3*UP).move_to(point, DOWN)
            for point in (rect.get_left(), rect.get_right())
        ])
        
        self.play(
            FadeIn(VGroup(axes, wave)),
            question_group.next_to, v_lines, UP, {"buff" : 0},
            *list(map(ShowCreation, v_lines))
        )
        self.wait(10)

    def show_concentration_of_the_wave(self):
        self.play(
            self.a_tracker.set_value, 5,
            self.wave_update_animation,
        )
        self.wait(10)
