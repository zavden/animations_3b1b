# ==============================================================================
# Scene:      ShowStepFunctionIn2dView
# Source:     videos/_2019/diffyq/part4/fourier_series_scenes.py (lines 1513-1755)
# Category:   2 · Renders with modifications
# Includes code copied from: _2019/diffyq/part2/fourier_series.py, _2019/diffyq/part4/complex_functions.py
#
# Run from this folder:
#     manimgl ShowStepFunctionIn2dView.py ShowStepFunctionIn2dView -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Use the Cairo signature of smooth(t, inflection), keeping the one-argument call.
# ==============================================================================

from manim_imports_ext import *

# CHANGE: adapt the Cairo APIs that require arguments removed from GL.
from cairo_compat import cairo_smooth as smooth


# ----- From _2019/diffyq/part2/fourier_series.py -----

class FourierCirclesScene(Scene):
    CONFIG = {
        "n_vectors": 10,
        "big_radius": 2,
        "colors": [
            BLUE_D,
            BLUE_C,
            BLUE_E,
            GREY_BROWN,
        ],
        "circle_style": {
            "stroke_width": 2,
        },
        "vector_config": {
            "buff": 0,
            "max_tip_length_to_length_ratio": 0.35,
            "fill_opacity": 0.75,
        },
        "circle_config": {
            "stroke_width": 1,
            "stroke_opacity": 0.75,
        },
        "base_frequency": 1,
        "slow_factor": 0.25,
        "center_point": ORIGIN,
        "parametric_function_step_size": 0.01,
        "drawn_path_color": YELLOW,
        "drawn_path_stroke_width": 2,
    }

    def setup(self):
        self.slow_factor_tracker = ValueTracker(
            self.slow_factor
        )
        self.vector_clock = ValueTracker(0)
        self.vector_clock.add_updater(
            lambda m, dt: m.increment_value(
                self.get_slow_factor() * dt
            )
        )
        self.add(self.vector_clock)

    def get_slow_factor(self):
        return self.slow_factor_tracker.get_value()

    def get_vector_time(self):
        return self.vector_clock.get_value()

    #
    def get_freqs(self):
        n = self.n_vectors
        all_freqs = list(range(n // 2, -n // 2, -1))
        all_freqs.sort(key=abs)
        return all_freqs

    def get_coefficients(self):
        return [complex(0) for x in range(self.n_vectors)]

    def get_color_iterator(self):
        return it.cycle(self.colors)

    def get_rotating_vectors(self, freqs=None, coefficients=None):
        vectors = VGroup()
        self.center_tracker = VectorizedPoint(self.center_point)

        if freqs is None:
            freqs = self.get_freqs()
        if coefficients is None:
            coefficients = self.get_coefficients()

        last_vector = None
        for freq, coefficient in zip(freqs, coefficients):
            if last_vector is not None:
                center_func = last_vector.get_end
            else:
                center_func = self.center_tracker.get_location
            vector = self.get_rotating_vector(
                coefficient=coefficient,
                freq=freq,
                center_func=center_func
            )
            vectors.add(vector)
            last_vector = vector
        return vectors

    def get_rotating_vector(self, coefficient, freq, center_func):
        vector = Vector(RIGHT, **self.vector_config)
        vector.scale(abs(coefficient))
        if abs(coefficient) == 0:
            phase = 0
        else:
            phase = np.log(coefficient).imag
        vector.rotate(phase, about_point=ORIGIN)
        vector.freq = freq
        vector.coefficient = coefficient
        vector.center_func = center_func
        vector.add_updater(self.update_vector)
        return vector

    def update_vector(self, vector, dt):
        time = self.get_vector_time()
        coef = vector.coefficient
        freq = vector.freq
        phase = np.log(coef).imag

        vector.set_length(abs(coef))
        vector.set_angle(phase + time * freq * TAU)
        vector.shift(vector.center_func() - vector.get_start())
        return vector

    def get_circles(self, vectors):
        return VGroup(*[
            self.get_circle(
                vector,
                color=color
            )
            for vector, color in zip(
                vectors,
                self.get_color_iterator()
            )
        ])

    def get_circle(self, vector, color=BLUE):
        circle = Circle(color=color, **self.circle_config)
        circle.center_func = vector.get_start
        circle.radius_func = vector.get_length
        circle.add_updater(self.update_circle)
        return circle

    def update_circle(self, circle):
        circle.set_width(2 * circle.radius_func())
        circle.move_to(circle.center_func())
        return circle

    def get_vector_sum_path(self, vectors, color=YELLOW):
        coefs = [v.coefficient for v in vectors]
        freqs = [v.freq for v in vectors]
        center = vectors[0].get_start()

        path = ParametricCurve(
            lambda t: center + reduce(op.add, [
                complex_to_R3(coef * np.exp(TAU * 1j * freq * t))
                for coef, freq in zip(coefs, freqs)
            ]),
            t_min=0,
            t_max=1,
            color=color,
            step_size=self.parametric_function_step_size,
        )
        return path

    # TODO, this should be a general animated mobect
    def get_drawn_path_alpha(self):
        return self.get_vector_time()

    def get_drawn_path(self, vectors, stroke_width=None, fade_rate=0.2, **kwargs):
        if stroke_width is None:
            stroke_width = self.drawn_path_stroke_width
        path = self.get_vector_sum_path(vectors, **kwargs)
        path.set_stroke(self.drawn_path_color, stroke_width)
        self.add_path_fader(path, fade_rate)
        return path

    def add_path_fader(self, path, fade_rate=0.2):
        stroke_width = np.max(path.get_stroke_width())
        stroke_opacity = np.max(path.get_stroke_opacity())

        def update_path(path_, dt):
            alpha = self.get_vector_time()
            n = path_.get_num_points()
            fade_factors = (np.linspace(0, 1, n) - alpha) % 1
            fade_factors = fade_factors**fade_rate
            path_.set_stroke(
                width=stroke_width * fade_factors,
                opacity=stroke_opacity * fade_factors,
            )
            return path_

        path.add_updater(update_path)
        return path

    def get_y_component_wave(self,
                             vectors,
                             left_x=1,
                             color=PINK,
                             n_copies=2,
                             right_shift_rate=5):
        path = self.get_vector_sum_path(vectors)
        wave = ParametricCurve(
            lambda t: op.add(
                right_shift_rate * t * LEFT,
                path.function(t)[1] * UP
            ),
            t_min=path.t_min,
            t_max=path.t_max,
            color=color,
        )
        wave_copies = VGroup(*[
            wave.copy()
            for x in range(n_copies)
        ])
        wave_copies.arrange(RIGHT, buff=0)
        top_point = wave_copies.get_top()
        wave.creation = ShowCreation(
            wave,
            run_time=(1 / self.get_slow_factor()),
            rate_func=linear,
        )
        cycle_animation(wave.creation)
        wave.add_updater(lambda m: m.shift(
            (m.get_left()[0] - left_x) * LEFT
        ))

        def update_wave_copies(wcs):
            index = int(
                wave.creation.total_time * self.get_slow_factor()
            )
            wcs[:index].match_style(wave)
            wcs[index:].set_stroke(width=0)
            wcs.next_to(wave, RIGHT, buff=0)
            wcs.align_to(top_point, UP)
        wave_copies.add_updater(update_wave_copies)

        return VGroup(wave, wave_copies)

    def get_wave_y_line(self, vectors, wave):
        return DashedLine(
            vectors[-1].get_end(),
            wave[0].get_end(),
            stroke_width=1,
            dash_length=DEFAULT_DASH_LENGTH * 0.5,
        )

    # Computing Fourier series
    # i.e. where all the math happens
    def get_coefficients_of_path(self, path, n_samples=10000, freqs=None):
        if freqs is None:
            freqs = self.get_freqs()
        dt = 1 / n_samples
        ts = np.arange(0, 1, dt)
        samples = np.array([
            path.point_from_proportion(t)
            for t in ts
        ])
        samples -= self.center_point
        complex_samples = samples[:, 0] + 1j * samples[:, 1]

        result = []
        for freq in freqs:
            riemann_sum = np.array([
                np.exp(-TAU * 1j * freq * t) * cs
                for t, cs in zip(ts, complex_samples)
            ]).sum() * dt
            result.append(riemann_sum)

        return result


class FourierOfPiSymbol(FourierCirclesScene):
    CONFIG = {
        "n_vectors": 101,
        "center_point": ORIGIN,
        "slow_factor": 0.1,
        "n_cycles": 1,
        "tex": "\\pi",
        "start_drawn": False,
        "max_circle_stroke_width": 1,
    }

    def construct(self):
        self.add_vectors_circles_path()
        for n in range(self.n_cycles):
            self.run_one_cycle()

    def add_vectors_circles_path(self):
        path = self.get_path()
        coefs = self.get_coefficients_of_path(path)

        for freq, coef in zip(self.get_freqs(), coefs):
            print(freq, "\t", coef)

        vectors = self.get_rotating_vectors(coefficients=coefs)
        circles = self.get_circles(vectors)
        self.set_decreasing_stroke_widths(circles)
        # approx_path = self.get_vector_sum_path(circles)
        drawn_path = self.get_drawn_path(vectors)
        if self.start_drawn:
            self.vector_clock.increment_value(1)

        self.add(path)
        self.add(vectors)
        self.add(circles)
        self.add(drawn_path)

        self.vectors = vectors
        self.circles = circles
        self.path = path
        self.drawn_path = drawn_path

    def run_one_cycle(self):
        time = 1 / self.slow_factor
        self.wait(time)

    def set_decreasing_stroke_widths(self, circles):
        mcsw = self.max_circle_stroke_width
        for k, circle in zip(it.count(1), circles):
            circle.set_stroke(width=max(
                # mcsw / np.sqrt(k),
                mcsw / k,
                mcsw,
            ))
        return circles

    def get_path(self):
        tex_mob = OldTex(self.tex)
        tex_mob.set_height(6)
        path = tex_mob.family_members_with_points()[0]
        path.set_fill(opacity=0)
        path.set_stroke(WHITE, 1)
        return path


class FourierOfTrebleClef(FourierOfPiSymbol):
    CONFIG = {
        "n_vectors": 101,
        "run_time": 10,
        "start_drawn": True,
        "file_name": "TrebleClef",
        "height": 7.5,
    }

    def get_shape(self):
        shape = SVGMobject(self.file_name)
        return shape

    def get_path(self):
        shape = self.get_shape()
        path = shape.family_members_with_points()[0]
        path.set_height(self.height)
        path.set_fill(opacity=0)
        path.set_stroke(WHITE, 0)
        return path



# ----- From _2019/diffyq/part4/complex_functions.py -----

class GeneralizeToComplexFunctions(Scene):
    CONFIG = {
        "axes_config": {
            "x_min": 0,
            "x_max": 10,
            "x_axis_config": {
                "stroke_width": 2,
            },
            "y_min": -2.5,
            "y_max": 2.5,
            "y_axis_config": {
                "tick_frequency": 0.25,
                "unit_size": 1.5,
                "include_tip": False,
                "stroke_width": 2,
            },
        },
        "complex_plane_config": {
            "axis_config": {
                "unit_size": 2
            }
        },
    }

    def construct(self):
        self.show_cosine_wave()
        self.transition_to_complex_plane()
        self.add_rotating_vectors_making_cos()

    def show_cosine_wave(self):
        axes = Axes(**self.axes_config)
        axes.shift(2 * LEFT - axes.c2p(0, 0))
        y_axis = axes.y_axis
        y_labels = y_axis.get_number_mobjects(
            *range(-2, 3),
            num_decimal_places=1
        )

        t_tracker = ValueTracker(0)
        t_tracker.add_updater(lambda t, dt: t.increment_value(dt))
        get_t = t_tracker.get_value

        def func(x):
            return 2 * np.cos(x)

        cos_x_max = 20
        cos_wave = axes.get_graph(func, x_max=cos_x_max)
        cos_wave.set_color(YELLOW)
        shown_cos_wave = cos_wave.copy()
        shown_cos_wave.add_updater(
            lambda m: m.pointwise_become_partial(
                cos_wave, 0,
                np.clip(get_t() / cos_x_max, 0, 1),
            ),
        )

        dot = Dot()
        dot.set_color(PINK)
        dot.add_updater(lambda d: d.move_to(
            y_axis.n2p(func(get_t())),
        ))

        h_line = always_redraw(lambda: Line(
            dot.get_right(),
            shown_cos_wave.get_end(),
            stroke_width=1,
        ))

        real_words = OldTexText(
            "Real number\\\\output"
        )
        real_words.to_edge(LEFT)
        real_words.shift(2 * UP)
        real_arrow = Arrow()
        real_arrow.add_updater(
            lambda m: m.put_start_and_end_on(
                real_words.get_corner(DR),
                dot.get_center(),
            ).scale(0.9),
        )

        self.add(t_tracker)
        self.add(axes)
        self.add(y_labels)
        self.add(shown_cos_wave)
        self.add(dot)
        self.add(h_line)

        self.wait(2)
        self.play(
            FadeIn(real_words, RIGHT),
            FadeIn(real_arrow),
        )
        self.wait(5)

        y_axis.generate_target()
        y_axis.target.rotate(-90 * DEGREES)
        y_axis.target.center()
        y_axis.target.scale(2 / 1.5)
        y_labels.generate_target()
        for label in y_labels.target:
            label.next_to(
                y_axis.target.n2p(label.get_value()),
                DOWN, MED_SMALL_BUFF,
            )
        self.play(
            FadeOut(shown_cos_wave),
            FadeOut(axes.x_axis),
            FadeOut(h_line),
        )
        self.play(
            MoveToTarget(y_axis),
            MoveToTarget(y_labels),
            real_words.shift, 2 * RIGHT + UP,
        )
        self.wait()

        self.y_axis = y_axis
        self.y_labels = y_labels
        self.real_words = real_words
        self.real_arrow = real_arrow
        self.dot = dot
        self.t_tracker = t_tracker

    def transition_to_complex_plane(self):
        y_axis = self.y_axis
        y_labels = self.y_labels

        plane = self.get_complex_plane()
        plane_words = plane.label

        self.add(plane, *self.get_mobjects())
        self.play(
            FadeOut(y_labels),
            FadeOut(y_axis),
            ShowCreation(plane),
        )
        self.play(Write(plane_words))
        self.wait()

        self.plane = plane
        self.plane_words = plane_words

    def add_rotating_vectors_making_cos(self):
        plane = self.plane
        real_words = self.real_words
        real_arrow = self.real_arrow
        t_tracker = self.t_tracker
        get_t = t_tracker.get_value

        v1 = Vector(2 * RIGHT)
        v2 = Vector(2 * RIGHT)
        v1.set_color(BLUE)
        v2.set_color(interpolate_color(GREY_BROWN, WHITE, 0.5))
        v1.add_updater(
            lambda v: v.set_angle(get_t())
        )
        v2.add_updater(
            lambda v: v.set_angle(-get_t())
        )
        v1.add_updater(
            lambda v: v.shift(plane.n2p(0) - v.get_start())
        )
        # Change?
        v2.add_updater(
            lambda v: v.shift(plane.n2p(0) - v.get_start())
        )

        ghost_v1 = v1.copy()
        ghost_v1.set_opacity(0.5)
        ghost_v1.add_updater(
            lambda v: v.shift(
                v2.get_end() - v.get_start()
            )
        )

        ghost_v2 = v2.copy()
        ghost_v2.set_opacity(0.5)
        ghost_v2.add_updater(
            lambda v: v.shift(
                v1.get_end() - v.get_start()
            )
        )

        circle = Circle(color=GREY_BROWN)
        circle.set_stroke(width=1)
        circle.set_width(2 * v1.get_length())
        circle.move_to(plane.n2p(0))

        formula = OldTex(
            # "\\cos(x) ="
            # "{1 \\over 2}e^{ix} +"
            # "{1 \\over 2}e^{-ix}",
            "2\\cos(x) =",
            "e^{ix}", "+", "e^{-ix}",
            tex_to_color_map={
                "e^{ix}": v1.get_color(),
                "e^{-ix}": v2.get_color(),
            }
        )
        formula.next_to(ORIGIN, UP, buff=0.75)
        # formula.add_background_rectangle()
        formula.set_stroke(BLACK, 3, background=True)
        formula.to_edge(LEFT, buff=MED_SMALL_BUFF)
        formula_brace = Brace(formula[1:], UP)
        formula_words = formula_brace.get_text(
            "Sum of\\\\rotations"
        )
        formula_words.set_stroke(BLACK, 3, background=True)

        randy = Randolph()
        randy.to_corner(DL)
        randy.look_at(formula)

        self.play(
            FadeOut(real_words),
            FadeOut(real_arrow),
        )
        self.play(
            FadeIn(v1),
            FadeIn(v2),
            FadeIn(circle),
            FadeIn(ghost_v1),
            FadeIn(ghost_v2),
        )
        self.wait(3)
        self.play(FadeInFromDown(formula))
        self.play(
            GrowFromCenter(formula_brace),
            FadeIn(formula_words),
        )
        self.wait(2)
        self.play(FadeIn(randy))
        self.play(randy.change, "pleading")
        self.play(Blink(randy))
        self.wait()
        self.play(randy.change, "confused")
        self.play(Blink(randy))
        self.wait()
        self.play(FadeOut(randy))
        self.wait(20)

    #
    def get_complex_plane(self):
        plane = ComplexPlane(**self.complex_plane_config)
        plane.add_coordinates()

        plane.label = OldTexText("Complex plane")
        plane.label.scale(1.5)
        plane.label.to_corner(UR, buff=MED_SMALL_BUFF)
        return plane


class ClarifyInputAndOutput(GeneralizeToComplexFunctions):
    CONFIG = {
        "input_space_rect_config": {
            "stroke_color": WHITE,
            "stroke_width": 1,
            "fill_color": GREY_E,
            "fill_opacity": 1,
            "width": 6,
            "height": 2,
        },
    }

    def construct(self):
        self.setup_plane()
        self.setup_input_space()
        self.setup_input_trackers()

        self.describe_input()
        self.describe_output()

    def setup_plane(self):
        plane = self.get_complex_plane()
        plane.sublabel = OldTexText("(Output space)")
        plane.sublabel.add_background_rectangle()
        plane.sublabel.next_to(plane.label, DOWN)
        self.add(plane, plane.label)
        self.plane = plane

    def setup_input_space(self):
        rect = Rectangle(**self.input_space_rect_config)
        rect.to_corner(UL, buff=SMALL_BUFF)

        input_line = self.get_input_line(rect)
        input_words = OldTexText("Input space")
        input_words.next_to(
            rect.get_bottom(), UP,
            SMALL_BUFF,
        )

        self.add(rect)
        self.add(input_line)

        self.input_rect = rect
        self.input_line = input_line
        self.input_words = input_words

    def setup_input_trackers(self):
        plane = self.plane
        input_line = self.input_line
        input_tracker = ValueTracker(0)
        get_input = input_tracker.get_value

        input_dot = Dot()
        input_dot.set_color(PINK)
        f_always(
            input_dot.move_to,
            lambda: input_line.n2p(get_input())
        )

        input_decimal = DecimalNumber()
        input_decimal.scale(0.7)
        always(input_decimal.next_to, input_dot, UP)
        f_always(input_decimal.set_value, get_input)

        path = self.get_path()

        def get_output_point():
            return path.point_from_proportion(
                get_input()
            )

        output_dot = Dot()
        output_dot.match_style(input_dot)
        f_always(output_dot.move_to, get_output_point)

        output_vector = Vector()
        output_vector.set_color(WHITE)
        output_vector.add_updater(
            lambda v: v.put_start_and_end_on(
                plane.n2p(0),
                get_output_point()
            )
        )

        output_decimal = DecimalNumber()
        output_decimal.scale(0.7)
        always(output_decimal.next_to, output_dot, UR, SMALL_BUFF)
        f_always(
            output_decimal.set_value,
            lambda: plane.p2n(get_output_point()),
        )

        self.input_tracker = input_tracker
        self.input_dot = input_dot
        self.input_decimal = input_decimal
        self.path = path
        self.output_dot = output_dot
        self.output_vector = output_vector
        self.output_decimal = output_decimal

    def describe_input(self):
        input_tracker = self.input_tracker

        self.play(FadeIn(self.input_words, UP))
        self.play(
            FadeInFromLarge(self.input_dot),
            FadeIn(self.input_decimal),
        )
        for value in 1, 0:
            self.play(
                input_tracker.set_value, value,
                run_time=2
            )
        self.wait()

    def describe_output(self):
        path = self.path
        output_dot = self.output_dot
        output_decimal = self.output_decimal
        input_dot = self.input_dot
        input_tracker = self.input_tracker
        plane = self.plane
        real_line = plane.x_axis.copy()
        real_line.set_stroke(RED, 4)
        real_words = OldTexText("Real number line")
        real_words.next_to(ORIGIN, UP)
        real_words.to_edge(RIGHT)

        traced_path = TracedPath(output_dot.get_center)
        traced_path.match_style(path)

        self.play(
            ShowCreation(real_line),
            FadeIn(real_words, DOWN)
        )
        self.play(
            FadeOut(real_line),
            FadeOut(real_words),
        )
        self.play(
            FadeIn(plane.sublabel, UP)
        )
        self.play(
            FadeIn(output_decimal),
            TransformFromCopy(input_dot, output_dot),
        )

        kw = {
            "run_time": 10,
            "rate_func": lambda t: smooth(t, 1),
        }
        self.play(
            ApplyMethod(input_tracker.set_value, 1, **kw),
            ShowCreation(path.copy(), remover=True, **kw),
        )
        self.add(path)
        self.add(output_dot)
        self.wait()

        # Flatten to 1d
        real_function_word = OldTexText(
            "Real-valued function"
        )
        real_function_word.next_to(ORIGIN, DOWN, MED_LARGE_BUFF)
        path.generate_target()
        path.target.stretch(0, 1)
        path.target.move_to(plane.n2p(0))

        self.play(
            FadeIn(real_function_word),
            MoveToTarget(path),
        )
        input_tracker.set_value(0)
        self.play(
            input_tracker.set_value, 1,
            **kw
        )

    #
    def get_input_line(self, input_rect):
        input_line = UnitInterval()
        input_line.move_to(input_rect)
        input_line.shift(0.25 * UP)
        input_line.set_width(
            input_rect.get_width() - 1
        )
        input_line.add_numbers(0, 0.5, 1)
        return input_line

    def get_path(self):
        # mob = SVGMobject("BatmanLogo")
        mob = OldTex("\\pi")
        path = mob.family_members_with_points()[0]
        path.set_height(3.5)
        path.move_to(2 * DOWN, DOWN)
        path.set_stroke(YELLOW, 2)
        path.set_fill(opacity=0)
        return path


class SimpleComplexExponentExample(ClarifyInputAndOutput):
    CONFIG = {
        "input_space_rect_config": {
            "width": 14,
            "height": 1.5,
        },
        "input_line_config": {
            "unit_size": 0.5,
            "x_min": 0,
            "x_max": 25,
            "stroke_width": 2,
        },
        "input_numbers": range(0, 30, 5),
        "input_tex_args": ["t", "="],
    }

    def construct(self):
        self.setup_plane()
        self.setup_input_space()
        self.setup_input_trackers()
        self.setup_output_trackers()

        # Testing
        time = self.input_line.x_max
        self.play(
            self.input_tracker.set_value, time,
            run_time=time,
            rate_func=linear,
        )

    def setup_plane(self):
        plane = ComplexPlane()
        plane.scale(2)
        plane.add_coordinates()
        plane.shift(DOWN)
        self.plane = plane
        self.add(plane)

    def setup_input_trackers(self):
        input_line = self.input_line
        input_tracker = ValueTracker(0)
        get_input = input_tracker.get_value

        input_tip = ArrowTip(start_angle=-TAU / 4)
        input_tip.scale(0.5)
        input_tip.set_color(PINK)
        f_always(
            input_tip.move_to,
            lambda: input_line.n2p(get_input()),
            lambda: DOWN,
        )

        input_label = VGroup(
            OldTex(*self.input_tex_args),
            DecimalNumber(),
        )
        input_label[0].set_color_by_tex("t", PINK)
        input_label.scale(0.7)
        input_label.add_updater(
            lambda m: m.arrange(RIGHT, buff=SMALL_BUFF)
        )
        input_label.add_updater(
            lambda m: m[1].set_value(get_input())
        )
        input_label.add_updater(
            lambda m: m.next_to(input_tip, UP, SMALL_BUFF)
        )

        self.input_tracker = input_tracker
        self.input_tip = input_tip
        self.input_label = input_label

        self.add(input_tip, input_label)

    def setup_output_trackers(self):
        plane = self.plane
        get_input = self.input_tracker.get_value

        def get_output():
            return np.exp(complex(0, get_input()))

        def get_output_point():
            return plane.n2p(get_output())

        output_label, static_output_label = [
            OldTex(
                "e^{i t}" + s,
                tex_to_color_map={"t": PINK},
                background_stroke_width=3,
            )
            for s in ["", "\\approx"]
        ]
        output_label.scale(1.2)
        output_label.add_updater(
            lambda m: m.shift(
                -m.get_bottom() +
                get_output_point() +
                rotate_vector(
                    0.35 * RIGHT,
                    get_input(),
                )
            )
        )

        output_vector = Vector()
        output_vector.set_opacity(0.75)
        output_vector.add_updater(
            lambda m: m.put_start_and_end_on(
                plane.n2p(0), get_output_point(),
            )
        )

        t_max = 40
        full_output_path = ParametricCurve(
            lambda t: plane.n2p(np.exp(complex(0, t))),
            t_min=0,
            t_max=t_max
        )
        output_path = VMobject()
        output_path.set_stroke(YELLOW, 2)
        output_path.add_updater(
            lambda m: m.pointwise_become_partial(
                full_output_path,
                0, get_input() / t_max,
            )
        )

        static_output_label.next_to(plane.c2p(1, 1), UR)
        output_decimal = DecimalNumber(
            include_sign=True,
        )
        output_decimal.scale(0.8)
        output_decimal.set_stroke(BLACK, 3, background=True)
        output_decimal.add_updater(
            lambda m: m.set_value(get_output())
        )
        output_decimal.add_updater(
            lambda m: m.next_to(
                static_output_label,
                RIGHT, 2 * SMALL_BUFF,
                aligned_edge=DOWN,
            )
        )

        self.add(output_path)
        self.add(output_vector)
        self.add(output_label)
        self.add(static_output_label)
        self.add(BackgroundRectangle(output_decimal))
        self.add(output_decimal)

    #
    def get_input_line(self, input_rect):
        input_line = NumberLine(**self.input_line_config)
        input_line.move_to(input_rect)
        input_line.set_width(
            input_rect.get_width() - 1.5,
            stretch=True,
        )
        input_line.add_numbers(*self.input_numbers)
        return input_line



# ----- From _2019/diffyq/part4/fourier_series_scenes.py -----

class ComplexFourierSeriesExample(FourierOfTrebleClef):
    CONFIG = {
        "file_name": "EighthNote",
        "run_time": 10,
        "n_vectors": 200,
        "n_cycles": 2,
        "max_circle_stroke_width": 0.75,
        "drawing_height": 5,
        "center_point": DOWN,
        "top_row_center": 3 * UP,
        "top_row_label_y": 2,
        "top_row_x_spacing": 1.75,
        "top_row_copy_scale_factor": 0.9,
        "start_drawn": False,
        "plane_config": {
            "axis_config": {"unit_size": 2},
            "y_min": -1.25,
            "y_max": 1.25,
            "x_min": -2.5,
            "x_max": 2.5,
            "background_line_style": {
                "stroke_width": 1,
                "stroke_color": GREY_B,
            },
        },
        "top_rect_height": 2.5,
    }

    def construct(self):
        self.add_vectors_circles_path()
        self.add_top_row(self.vectors, self.circles)
        self.write_title()
        self.highlight_vectors_one_by_one()
        self.change_shape()

    def write_title(self):
        title = OldTexText("Complex\\\\Fourier series")
        title.scale(1.5)
        title.to_edge(LEFT)
        title.match_y(self.path)

        self.wait(11)
        self.play(FadeInFromDown(title))
        self.wait(2)
        self.title = title

    def highlight_vectors_one_by_one(self):
        # Don't know why these vectors can't get copied.
        # That seems like a problem that will come up again.
        labels = self.top_row[-1]
        next_anims = []
        for vector, circle, label in zip(self.vectors, self.circles, labels):
            # v_color = vector.get_color()
            c_color = circle.get_color()
            c_stroke_width = circle.get_stroke_width()

            rect = SurroundingRectangle(label, color=PINK)
            self.play(
                # vector.set_color, PINK,
                circle.set_stroke, RED, 3,
                FadeIn(rect),
                *next_anims
            )
            self.wait()
            next_anims = [
                # vector.set_color, v_color,
                circle.set_stroke, c_color, c_stroke_width,
                FadeOut(rect),
            ]
        self.play(*next_anims)

    def change_shape(self):
        # path_mob = OldTex("\\pi")
        path_mob = SVGMobject("Nail_And_Gear")
        new_path = path_mob.family_members_with_points()[0]
        new_path.set_height(4)
        new_path.move_to(self.path, DOWN)
        new_path.shift(0.5 * UP)

        self.transition_to_alt_path(new_path)
        for n in range(self.n_cycles):
            self.run_one_cycle()

    def transition_to_alt_path(self, new_path, morph_path=False):
        new_coefs = self.get_coefficients_of_path(new_path)
        new_vectors = self.get_rotating_vectors(
            coefficients=new_coefs
        )
        new_drawn_path = self.get_drawn_path(new_vectors)

        self.vector_clock.suspend_updating()

        vectors = self.vectors
        anims = []

        for vect, new_vect in zip(vectors, new_vectors):
            new_vect.update()
            new_vect.clear_updaters()

            line = Line(stroke_width=0)
            line.put_start_and_end_on(*vect.get_start_and_end())
            anims.append(ApplyMethod(
                line.put_start_and_end_on,
                *new_vect.get_start_and_end()
            ))
            vect.freq = new_vect.freq
            vect.coefficient = new_vect.coefficient

            vect.line = line
            vect.add_updater(
                lambda v: v.put_start_and_end_on(
                    *v.line.get_start_and_end()
                )
            )
        if morph_path:
            anims.append(
                ReplacementTransform(
                    self.drawn_path,
                    new_drawn_path
                )
            )
        else:
            anims.append(
                FadeOut(self.drawn_path)
            )

        self.play(*anims, run_time=3)
        for vect in self.vectors:
            vect.remove_updater(vect.updaters[-1])

        if not morph_path:
            self.add(new_drawn_path)
            self.vector_clock.set_value(0)

        self.vector_clock.resume_updating()
        self.drawn_path = new_drawn_path

    #
    def get_path(self):
        path = super().get_path()
        path.set_height(self.drawing_height)
        path.to_edge(DOWN)
        return path

    def add_top_row(self, vectors, circles, max_freq=3):
        self.top_row = self.get_top_row(
            vectors, circles, max_freq
        )
        self.add(self.top_row)

    def get_top_row(self, vectors, circles, max_freq=3):
        vector_copies = VGroup()
        circle_copies = VGroup()
        for vector, circle in zip(vectors, circles):
            if vector.freq > max_freq:
                break
            vcopy = vector.copy()
            vcopy.clear_updaters()
            ccopy = circle.copy()
            ccopy.clear_updaters()
            ccopy.original = circle
            vcopy.original = vector

            vcopy.center_point = op.add(
                self.top_row_center,
                vector.freq * self.top_row_x_spacing * RIGHT,
            )
            ccopy.center_point = vcopy.center_point
            vcopy.add_updater(self.update_top_row_vector_copy)
            ccopy.add_updater(self.update_top_row_circle_copy)
            vector_copies.add(vcopy)
            circle_copies.add(ccopy)

        dots = VGroup(*[
            OldTex("\\dots").next_to(
                circle_copies, direction,
                MED_LARGE_BUFF,
            )
            for direction in [LEFT, RIGHT]
        ])
        labels = self.get_top_row_labels(vector_copies)
        return VGroup(
            vector_copies,
            circle_copies,
            dots,
            labels,
        )

    def update_top_row_vector_copy(self, vcopy):
        vcopy.become(vcopy.original)
        vcopy.scale(self.top_row_copy_scale_factor)
        vcopy.shift(vcopy.center_point - vcopy.get_start())
        return vcopy

    def update_top_row_circle_copy(self, ccopy):
        ccopy.become(ccopy.original)
        ccopy.scale(self.top_row_copy_scale_factor)
        ccopy.move_to(ccopy.center_point)
        return ccopy

    def get_top_row_labels(self, vector_copies):
        labels = VGroup()
        for vector_copy in vector_copies:
            freq = vector_copy.freq
            label = Integer(freq)
            label.move_to(np.array([
                freq * self.top_row_x_spacing,
                self.top_row_label_y,
                0
            ]))
            labels.add(label)
        return labels

    def setup_plane(self):
        plane = ComplexPlane(**self.plane_config)
        plane.shift(self.center_point)
        plane.add_coordinates()

        top_rect = Rectangle(
            width=FRAME_WIDTH,
            fill_color=BLACK,
            fill_opacity=1,
            stroke_width=0,
            height=self.top_rect_height,
        )
        top_rect.to_edge(UP, buff=0)

        self.plane = plane
        self.add(plane)
        self.add(top_rect)

    def get_path_end(self, vectors, stroke_width=None, **kwargs):
        if stroke_width is None:
            stroke_width = self.drawn_path_st
        full_path = self.get_vector_sum_path(vectors, **kwargs)
        path = VMobject()
        path.set_stroke(
            self.drawn_path_color,
            stroke_width
        )

        def update_path(p):
            alpha = self.get_vector_time() % 1
            p.pointwise_become_partial(
                full_path,
                np.clip(alpha - 0.01, 0, 1),
                np.clip(alpha, 0, 1),
            )
            p.get_points()[-1] = vectors[-1].get_end()

        path.add_updater(update_path)
        return path

    def get_drawn_path_alpha(self):
        return super().get_drawn_path_alpha() - 0.002

    def get_drawn_path(self, vectors, stroke_width=2, **kwargs):
        odp = super().get_drawn_path(vectors, stroke_width, **kwargs)
        return VGroup(
            odp,
            self.get_path_end(vectors, stroke_width, **kwargs),
        )

    def get_vertically_falling_tracing(self, vector, color, stroke_width=3, rate=0.25):
        path = VMobject()
        path.set_stroke(color, stroke_width)
        path.start_new_path(vector.get_end())
        path.vector = vector

        def update_path(p, dt):
            p.shift(rate * dt * DOWN)
            p.add_smooth_curve_to(p.vector.get_end())
        path.add_updater(update_path)
        return path


class ShowStepFunctionIn2dView(SimpleComplexExponentExample, ComplexFourierSeriesExample):
    CONFIG = {
        "input_space_rect_config": {
            "width": 5,
            "height": 2,
        },
        "input_line_config": {
            "unit_size": 3,
            "x_min": 0,
            "x_max": 1,
            "tick_frequency": 0.1,
            "stroke_width": 2,
            "decimal_number_config": {
                "num_decimal_places": 1,
            }
        },
        "input_numbers": [0, 0.5, 1],
        "input_tex_args": [],
        # "n_vectors": 300,
        "n_vectors": 2,
    }

    def construct(self):
        self.setup_plane()
        self.setup_input_space()
        self.setup_input_trackers()
        self.clear()

        self.transition_from_step_function()
        self.show_output()
        self.show_fourier_series()

    def setup_input_space(self):
        super().setup_input_space()
        rect = self.input_rect
        line = self.input_line
        # rect.stretch(1.2, 1, about_edge=UP)
        line.shift(MED_SMALL_BUFF * UP)
        sf = 1.2
        line.stretch(sf, 0)
        for n in line.numbers:
            n.stretch(1 / sf, 0)

        label = OldTexText("Input space")
        label.next_to(rect.get_bottom(), UP, SMALL_BUFF)
        self.add(label)
        self.input_space_label = label

    def transition_from_step_function(self):
        x_axis = self.input_line
        input_tip = self.input_tip
        input_label = self.input_label
        input_rect = self.input_rect
        input_space_label = self.input_space_label
        plane = self.plane
        plane.set_opacity(0)

        x_axis.save_state()
        # x_axis.center()
        x_axis.move_to(ORIGIN, LEFT)
        sf = 1.5
        x_axis.stretch(sf, 0)
        for number in x_axis.numbers:
            number.stretch(1 / sf, 0)
        x_axis.numbers[0].set_opacity(0)

        y_axis = NumberLine(
            unit_size=2,
            x_min=-1.5,
            x_max=1.5,
            tick_frequency=0.5,
            stroke_color=GREY_B,
            stroke_width=2,
        )
        # y_axis.match_style(x_axis)
        y_axis.rotate(90 * DEGREES)
        y_axis.shift(x_axis.n2p(0) - y_axis.n2p(0))
        y_axis.add_numbers(
            -1, 0, 1,
            direction=LEFT,
        )
        axes = Axes()
        axes.x_axis = x_axis
        axes.y_axis = y_axis
        axes.axes = VGroup(x_axis, y_axis)

        graph = VGroup(
            Line(
                axes.c2p(0, 1),
                axes.c2p(0.5, 1),
                color=RED,
            ),
            Line(
                axes.c2p(0.5, -1),
                axes.c2p(1, -1),
                color=BLUE,
            ),
        )

        dot1 = Dot(color=RED)
        dot2 = Dot(color=BLUE)
        dot1.add_updater(lambda d: d.move_to(y_axis.n2p(1)))
        dot2.add_updater(lambda d: d.move_to(y_axis.n2p(-1)))
        squish_graph = VGroup(dot1, dot2)

        self.add(x_axis)
        self.add(y_axis)
        self.add(input_tip)
        self.add(input_label)

        self.play(
            self.input_tracker.set_value, 1,
            ShowCreation(graph),
            run_time=3,
            rate_func=lambda t: smooth(t, 1)
        )
        self.wait()
        self.add(
            plane, input_rect, input_space_label,
            x_axis, input_tip, input_label,
        )
        self.play(
            FadeIn(input_rect),
            FadeIn(input_space_label),
            Restore(x_axis),
        )
        self.play(ReplacementTransform(graph, squish_graph))

        # Rotate y-axis, fade in plane
        y_axis.generate_target(use_deepcopy=True)
        y_axis.target.rotate(-TAU / 4)
        y_axis.target.shift(
            plane.n2p(0) - y_axis.target.n2p(0)
        )
        y_axis.target.numbers.set_opacity(0)

        plane.set_opacity(1)
        self.play(
            MoveToTarget(y_axis),
            ShowCreation(plane),
        )
        self.play(FadeOut(y_axis))
        self.wait()
        self.play(self.input_tracker.set_value, 0)

        self.output_dots = squish_graph

    def show_output(self):
        input_tracker = self.input_tracker

        def get_output_point():
            return self.get_output_point(input_tracker.get_value())

        tip = ArrowTip(start_angle=-TAU / 4)
        tip.set_fill(YELLOW)
        tip.match_height(self.input_tip)
        tip.add_updater(lambda m: m.move_to(
            get_output_point(), DOWN,
        ))
        output_label = OldTexText("Output")
        output_label.add_background_rectangle()
        output_label.add_updater(lambda m: m.next_to(
            tip, UP, SMALL_BUFF,
        ))

        self.play(
            FadeIn(tip),
            FadeIn(output_label),
        )

        self.play(
            input_tracker.set_value, 1,
            run_time=8,
            rate_func=linear
        )
        self.wait()
        self.play(input_tracker.set_value, 0)

        self.output_tip = tip

    def show_fourier_series(self):
        plane = self.plane
        input_tracker = self.input_tracker
        output_tip = self.output_tip

        self.play(
            plane.axes.set_stroke, WHITE, 1,
            plane.background_lines.set_stroke, GREY_B, 0.5,
            plane.faded_lines.set_stroke, GREY_B, 0.25, 0.5,
        )

        self.vector_clock.set_value(0)
        self.add(self.vector_clock)
        input_tracker.add_updater(lambda m: m.set_value(
            self.vector_clock.get_value() % 1
        ))
        self.add_vectors_circles_path()
        self.remove(self.drawn_path)
        self.add(self.vectors)
        output_tip.clear_updaters()
        output_tip.add_updater(lambda m: m.move_to(
            self.vectors[-1].get_end(), DOWN
        ))

        self.run_one_cycle()
        path = self.get_vertically_falling_tracing(
            self.vectors[1], GREEN, rate=0.5,
        )
        self.add(path)
        for x in range(3):
            self.run_one_cycle()

    #
    def get_freqs(self):
        n = self.n_vectors
        all_freqs = [
            *range(1, n + 1 // 2, 2),
            *range(-1, -n + 1 // 2, -2),
        ]
        all_freqs.sort(key=abs)
        return all_freqs

    def get_path(self):
        path = VMobject()
        p0, p1 = [
            self.get_output_point(x)
            for x in [0, 1]
        ]
        for p in p0, p1:
            path.start_new_path(p)
            path.add_line_to(p)
        return path

    def get_output_point(self, x):
        return self.plane.n2p(self.step(x))

    def step(self, x):
        if x < 0.5:
            return 1
        elif x == 0.5:
            return 0
        else:
            return -1
