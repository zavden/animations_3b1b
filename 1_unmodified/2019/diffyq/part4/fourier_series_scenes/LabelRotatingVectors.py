# ==============================================================================
# Scene:      LabelRotatingVectors
# Source:     videos/_2019/diffyq/part4/fourier_series_scenes.py (lines 461-1079)
# Category:   1 · Renders unmodified
# Includes code copied from: _2019/diffyq/part2/fourier_series.py
#
# Run from this folder:
#     manimgl LabelRotatingVectors.py LabelRotatingVectors -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *


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


class PiFourierSeries(ComplexFourierSeriesExample):
    CONFIG = {
        "tex": "\\pi",
        "n_vectors": 101,
        "path_height": 3.5,
        "max_circle_stroke_width": 1,
        "top_row_copy_scale_factor": 0.6,
    }

    def construct(self):
        self.setup_plane()
        self.add_vectors_circles_path()
        self.add_top_row(self.vectors, self.circles)

        for n in range(self.n_cycles):
            self.run_one_cycle()

    def get_path(self):
        pi = OldTex(self.tex)
        path = pi.family_members_with_points()[0]
        path.set_height(self.path_height)
        path.move_to(3 * DOWN, DOWN)
        path.set_stroke(YELLOW, 0)
        path.set_fill(opacity=0)
        return path


class LabelRotatingVectors(PiFourierSeries):
    CONFIG = {
        "n_vectors": 6,
        "center_point": 1.5 * DOWN,
        "top_rect_height": 3,
        "plane_config": {
            "axis_config": {
                "unit_size": 1.75,
                "stroke_color": GREY_B,
            },
        },
        "top_row_x_spacing": 1.9,
        "top_row_center": 3 * UP + 0.2 * LEFT,
    }

    def construct(self):
        self.setup_plane()
        self.setup_top_row()

        self.ask_about_labels()
        self.initialize_at_one()
        self.show_complex_exponents()
        # self.show_complex_exponents_temp()

        self.tweak_initial_states()
        self.constant_examples()

    def setup_top_row(self):
        vectors = self.get_rotating_vectors(
            coefficients=0.5 * np.ones(self.n_vectors)
        )
        circles = self.get_circles(vectors)

        top_row = self.get_top_row(vectors, circles)
        top_row.shift(0.5 * DOWN + 0.25 * RIGHT)
        v_copies, c_copies, dots, labels = top_row
        labels.to_edge(UP, MED_SMALL_BUFF)
        freq_label = OldTexText("Frequencies:")
        freq_label.to_edge(LEFT, MED_SMALL_BUFF)
        freq_label.match_y(labels)
        VGroup(freq_label, labels).set_color(YELLOW)

        def get_constant_func(const):
            return lambda: const

        for vector, v_copy in zip(vectors, v_copies):
            vector.center_func = get_constant_func(
                v_copy.get_start()
            )
        vectors.update(0)
        circles.update(0)

        self.add(vectors)
        self.add(circles)
        self.add(dots)
        self.add(freq_label)
        self.add(labels)

        self.vectors = vectors
        self.circles = circles
        self.labels = labels
        self.freq_label = freq_label

    def ask_about_labels(self):
        circles = self.circles

        formulas = OldTexText("Formulas:")
        formulas.next_to(circles, DOWN)
        formulas.to_edge(LEFT, MED_SMALL_BUFF)

        q_marks = VGroup(*[
            OldTex("??").scale(1.0).next_to(circle, DOWN)
            for circle in circles
        ])

        self.play(FadeIn(formulas, DOWN))
        self.play(LaggedStartMap(
            FadeInFrom, q_marks,
            lambda m: (m, UP),
            lag_ratio=0.2,
            run_time=3,
        ))
        self.wait(3)

        self.q_marks = q_marks
        self.formulas_word = formulas

    def initialize_at_one(self):
        vectors = self.vectors
        circles = self.circles
        vector_clock = self.vector_clock
        plane = self.plane
        q_marks = self.q_marks

        # Why so nuclear?
        vc_updater = vector_clock.updaters.pop()
        self.play(
            vector_clock.set_value, 0,
            run_time=2,
        )

        zero_vect = Vector()
        zero_vect.replace(vectors[0])
        zero_circle = self.get_circle(zero_vect)
        zero_circle.match_style(circles[0])
        self.add(zero_circle)

        one_label = OldTex("1")
        one_label.move_to(q_marks[0])

        self.play(
            zero_vect.put_start_and_end_on,
            plane.n2p(0), plane.n2p(1),
        )
        vector_clock.add_updater(vc_updater)
        self.wait()
        self.play(
            FadeOut(q_marks[0], UP),
            FadeIn(one_label, DOWN),
        )
        self.wait(4)

        self.one_label = one_label
        self.zero_vect = zero_vect
        self.zero_circle = zero_circle

    def show_complex_exponents(self):
        vectors = self.vectors
        circles = self.circles
        q_marks = self.q_marks
        labels = self.labels
        one_label = self.one_label
        v_lines = self.get_v_lines(circles)

        # Vector 1
        v1_rect = SurroundingRectangle(
            VGroup(circles[1], q_marks[1], labels[1]),
            stroke_color=GREY,
            stroke_width=2,
        )
        f1_exp = self.get_exp_tex()
        f1_exp.move_to(q_marks[1], DOWN)

        self.play(
            FadeOut(self.zero_vect),
            FadeOut(self.zero_circle),
            FadeIn(v1_rect)
        )

        vg1 = self.get_vector_in_plane_group(
            vectors[1], circles[1],
        )
        vg1_copy = vg1.copy()
        vg1_copy.clear_updaters()
        vg1_copy.replace(circles[1])

        cps_1 = self.get_cps_label(1)

        circle_copy = vg1[1].copy().clear_updaters()
        circle_copy.set_stroke(YELLOW, 3)
        arclen_decimal = DecimalNumber(
            num_decimal_places=3,
            show_ellipsis=True,
        )
        arclen_tracker = ValueTracker(0)
        arclen_decimal.add_updater(lambda m: m.next_to(
            circle_copy.get_end(), UR, SMALL_BUFF,
        ))
        arclen_decimal.add_updater(lambda m: m.set_value(
            arclen_tracker.get_value()
        ))

        self.play(
            ReplacementTransform(vg1_copy, vg1),
        )
        self.play(FadeIn(cps_1, DOWN))
        self.wait(2)
        self.play(
            FadeOut(q_marks[1], UP),
            FadeIn(f1_exp, DOWN),
        )
        self.wait(2)
        self.play(ShowCreationThenFadeAround(
            f1_exp.get_part_by_tex("2\\pi")
        ))
        self.add(arclen_decimal),
        self.play(
            ShowCreation(circle_copy),
            arclen_tracker.set_value, TAU,
            run_time=3,
        )
        self.wait()
        self.play(
            FadeOut(circle_copy),
            FadeOut(arclen_decimal),
        )
        self.wait(8)
        self.play(
            v1_rect.move_to, circles[2],
            v1_rect.match_y, v1_rect,
            FadeOut(vg1),
            FadeOut(cps_1),
        )

        # Vector -1
        vgm1 = self.get_vector_in_plane_group(
            vectors[2], circles[2],
        )
        vgm1_copy = vgm1.copy()
        vgm1_copy.clear_updaters()
        vgm1_copy.replace(circles[2])
        cps_m1 = self.get_cps_label(-1)
        fm1_exp = self.get_exp_tex(-1)
        fm1_exp.move_to(q_marks[2], DOWN)

        self.play(
            ReplacementTransform(vgm1_copy, vgm1),
            FadeInFromDown(cps_m1)
        )
        self.wait(2)
        self.play(
            FadeOut(q_marks[2], UP),
            FadeInFromDown(fm1_exp),
            v1_rect.stretch, 1.4, 0,
        )
        self.wait(5)
        self.play(
            v1_rect.move_to, circles[3],
            v1_rect.match_y, v1_rect,
            FadeOut(vgm1),
            FadeOut(cps_m1),
        )

        # Vector 2
        # (Lots of copy-pasting here)
        vg2 = self.get_vector_in_plane_group(
            vectors[3], circles[3],
        )
        vg2_copy = vg2.copy()
        vg2_copy.clear_updaters()
        vg2_copy.replace(circles[3])
        cps_2 = self.get_cps_label(2)
        f2_exp = self.get_exp_tex(2)
        f2_exp.move_to(q_marks[3], DOWN)
        circle_copy.append_vectorized_mobject(circle_copy)

        self.play(
            ReplacementTransform(vg2_copy, vg2),
            FadeInFromDown(cps_2)
        )
        self.wait()
        self.play(
            FadeOut(q_marks[3], UP),
            FadeInFromDown(f2_exp),
        )
        self.wait(3)

        self.play(ShowCreationThenFadeAround(
            f2_exp.get_parts_by_tex("2"),
        ))
        self.add(arclen_decimal)
        arclen_tracker.set_value(0)
        self.play(
            ShowCreation(circle_copy),
            arclen_tracker.set_value, 2 * TAU,
            run_time=5
        )
        self.wait(3)
        self.play(
            FadeOut(circle_copy),
            FadeOut(arclen_decimal),
        )
        self.play(
            FadeOut(vg2),
            FadeOut(cps_2),
            FadeOut(v1_rect),
        )

        # Show all formulas
        fm2_exp = self.get_exp_tex(-2)
        fm2_exp.move_to(q_marks[4], DOWN)
        f3_exp = self.get_exp_tex(3)
        f3_exp.move_to(q_marks[5], DOWN)
        f1_exp_new = self.get_exp_tex(1)
        f1_exp_new.move_to(q_marks[1], DOWN)
        f0_exp = self.get_exp_tex(0)
        f0_exp.move_to(q_marks[0], DOWN)
        f_exp_general = self.get_exp_tex("n")
        f_exp_general.next_to(self.formulas_word, DOWN)

        self.play(
            FadeOut(q_marks[4:]),
            FadeOut(f1_exp),
            FadeIn(f1_exp_new),
            FadeInFromDown(fm2_exp),
            FadeInFromDown(f3_exp),
            FadeIn(v_lines, lag_ratio=0.2)
        )
        self.play(
            FadeIn(f_exp_general, UP)
        )
        self.play(ShowCreationThenFadeAround(f_exp_general))
        self.wait(3)
        self.play(
            FadeOut(one_label, UP),
            TransformFromCopy(f_exp_general, f0_exp),
        )
        self.wait(5)

        self.f_exp_labels = VGroup(
            f0_exp, f1_exp_new, fm1_exp,
            f2_exp, fm2_exp, f3_exp,
        )
        self.f_exp_general = f_exp_general

    def show_complex_exponents_temp(self):
        self.f_exp_labels = VGroup(*[
            self.get_exp_tex(n).move_to(qm, DOWN)
            for n, qm in zip(
                [0, 1, -1, 2, -2, 3],
                self.q_marks,
            )
        ])
        self.f_exp_general = self.get_exp_tex("n")
        self.f_exp_general.next_to(self.formulas_word, DOWN)

        self.remove(*self.q_marks, self.one_label)
        self.remove(self.zero_vect, self.zero_circle)
        self.add(self.f_exp_labels, self.f_exp_general)

    def tweak_initial_states(self):
        vector_clock = self.vector_clock
        f_exp_labels = self.f_exp_labels
        f_exp_general = self.f_exp_general
        vectors = self.vectors

        cn_terms = VGroup()
        for i, f_exp in enumerate(f_exp_labels):
            n = (i + 1) // 2
            if i % 2 == 0 and i > 0:
                n *= -1
            cn_terms.add(self.get_cn_label(n, f_exp))
        cn_general = self.get_cn_label("n", f_exp_general)

        new_coefs = [
            0.5,
            np.exp(complex(0, TAU / 8)),
            0.7 * np.exp(-complex(0, TAU / 8)),
            0.6 * np.exp(complex(0, TAU / 3)),
            1.1 * np.exp(-complex(0, TAU / 12)),
            0.3 * np.exp(complex(0, TAU / 12)),
        ]

        def update_vectors(alpha):
            for vect, new_coef in zip(vectors, new_coefs):
                vect.coefficient = 0.5 * interpolate(
                    1, new_coef, alpha
                )

        vector_clock.incrementer = vector_clock.updaters.pop()
        self.play(
            vector_clock.set_value,
            int(vector_clock.get_value())
        )
        self.play(
            LaggedStartMap(
                MoveToTarget,
                VGroup(f_exp_general, *f_exp_labels),
            ),
            LaggedStartMap(
                FadeInFromDown,
                VGroup(cn_general, *cn_terms),
            ),
            UpdateFromAlphaFunc(
                VectorizedPoint(),
                lambda m, a: update_vectors(a)
            ),
            run_time=2
        )
        self.wait()
        self.play(
            LaggedStart(*[
                ShowCreationThenFadeAround(
                    cn_term,
                    surrounding_rectangle_config={
                        "buff": 0.05,
                        "stroke_width": 2,
                    },
                )
                for cn_term in cn_terms
            ])
        )

        self.cn_terms = cn_terms
        self.cn_general = cn_general

    def constant_examples(self):
        cn_terms = self.cn_terms
        vectors = self.vectors
        circles = self.circles

        # c0 term
        c0_brace = Brace(cn_terms[0], DOWN, buff=SMALL_BUFF)
        c0_label = OldTex("0.5")
        c0_label.next_to(c0_brace, DOWN, SMALL_BUFF)
        c0_label.add_background_rectangle()
        vip_group0 = self.get_vector_in_plane_group(
            vectors[0], circles[0]
        )
        vip_group0_copy = vip_group0.copy()
        vip_group0_copy.clear_updaters()
        vip_group0_copy.replace(circles[0])

        self.play(
            Transform(vip_group0_copy, vip_group0)
        )
        self.wait()
        self.play(vip_group0_copy.scale, 2)
        self.play(
            vip_group0_copy.scale, 0.5,
            GrowFromCenter(c0_brace),
            GrowFromCenter(c0_label),
        )
        self.wait(2)
        self.play(
            FadeOut(c0_brace),
            FadeOut(c0_label),
            FadeOut(vip_group0_copy),
        )

        # c1 term
        c1_brace = Brace(cn_terms[1], DOWN, buff=SMALL_BUFF)
        c1_label = OldTex("e^{(\\pi / 4)i}")
        c1_label.next_to(c1_brace, DOWN, SMALL_BUFF)
        c1_decimal = DecimalNumber(
            np.exp(np.complex(0, PI / 4)),
            num_decimal_places=3,
        )
        approx = OldTex("\\approx")
        approx.next_to(c1_label, RIGHT, MED_SMALL_BUFF)
        c1_decimal.next_to(approx, RIGHT, MED_SMALL_BUFF)
        scalar = DecimalNumber(0.3)
        scalar.next_to(
            c1_label, LEFT, SMALL_BUFF,
            aligned_edge=DOWN,
        )

        vip_group1 = self.get_vector_in_plane_group(
            vectors[1], circles[1]
        )
        vip_group1_copy = vip_group1.copy()
        vip_group1_copy[0].stroke_width = 3
        vip_group1_copy.clear_updaters()
        vip_group1_copy.save_state()
        vip_group1_copy.replace(circles[1])

        self.play(
            Restore(vip_group1_copy)
        )
        self.play(Rotate(vip_group1_copy, -PI / 4))
        self.play(Rotate(vip_group1_copy, PI / 4))
        self.play(
            GrowFromCenter(c1_brace),
            FadeIn(c1_label),
        )
        self.play(
            Write(approx),
            Write(c1_decimal),
            run_time=1,
        )
        self.wait(2)

        def update_v1(alpha):
            vectors[1].coefficient = 0.5 * interpolate(
                np.exp(complex(0, PI / 4)),
                0.3 * np.exp(complex(0, PI / 4)),
                alpha
            )

        self.play(
            FadeIn(scalar),
            c1_decimal.set_value,
            scalar.get_value() * c1_decimal.get_value(),
            vip_group1_copy.scale, scalar.get_value(),
            UpdateFromAlphaFunc(
                VMobject(),
                lambda m, a: update_v1(a)
            )
        )
        self.wait()
        self.play(
            FadeOut(c1_brace),
            FadeOut(c1_label),
            FadeOut(approx),
            FadeOut(c1_decimal),
            FadeOut(scalar),
            FadeOut(vip_group1_copy),
        )

        fade_anims = []
        for cn_term, vect in zip(cn_terms[2:], vectors[2:]):
            rect = SurroundingRectangle(cn_term, buff=0.025)
            rect.set_stroke(width=2)
            decimal = DecimalNumber(vect.coefficient)
            decimal.next_to(rect, DOWN)
            decimal.add_background_rectangle()
            if cn_term is cn_terms[4]:
                decimal.shift(0.7 * RIGHT)

            self.play(
                ShowCreation(rect),
                FadeIn(decimal),
                *fade_anims
            )
            self.wait()
            fade_anims = [FadeOut(rect), FadeOut(decimal)]
        self.play(*fade_anims)

    #
    def get_vector_in_plane_group(self, top_vector, top_circle):
        plane = self.plane
        origin = plane.n2p(0)

        vector = Vector()
        vector.add_updater(
            lambda v: v.put_start_and_end_on(
                origin,
                plane.n2p(2 * top_vector.coefficient)
            ).set_angle(top_vector.get_angle())
        )
        circle = Circle()
        circle.match_style(top_circle)
        circle.set_width(2 * vector.get_length())
        circle.move_to(origin)

        return VGroup(vector, circle)

    def get_exp_tex(self, freq=None):
        if freq is None:
            freq_str = "{}"
        else:
            freq_str = "{" + str(freq) + "}" + "\\cdot"

        result = OldTex(
            "e^{", freq_str, "2\\pi i {t}}",
            tex_to_color_map={
                "2\\pi": WHITE,
                "{t}": PINK,
                freq_str: YELLOW,
            }
        )
        result.scale(0.9)
        return result

    def get_cn_label(self, n, exp_label):
        exp_label.generate_target()
        exp_label.target.scale(0.9)

        n_str = "{" + str(n) + "}"
        term = OldTex("c_", n_str)
        term.set_color(GREEN)
        term[1].set_color(YELLOW)
        term[1].set_width(0.12)
        term[1].move_to(term[0].get_corner(DR), LEFT)
        if isinstance(n, str):
            term[1].scale(1.4, about_edge=LEFT)
            term[1].shift(0.03 * RIGHT)
        elif n < 0:
            term[1].scale(1.4, about_edge=LEFT)
            term[1].set_stroke(width=0.5)
        else:
            term[1].shift(0.05 * RIGHT)
        term.scale(0.9)
        term.shift(
            exp_label.target[0].get_corner(LEFT) -
            term[0].get_corner(RIGHT) +
            0.2 * LEFT
        )
        VGroup(exp_label.target, term).move_to(
            exp_label, DOWN
        )

        if isinstance(n, str):
            VGroup(term, exp_label.target).scale(
                1.3, about_edge=UP
            )

        return term

    def get_cps_label(self, n):
        n_str = str(n)
        if n == 1:
            frac_tex = "\\frac{\\text{cycle}}{\\text{second}}"
        else:
            frac_tex = "\\frac{\\text{cycles}}{\\text{second}}"

        result = OldTex(
            n_str, frac_tex,
            tex_to_color_map={
                n_str: YELLOW
            },
        )
        result[1].scale(0.7, about_edge=LEFT)
        result[0].scale(1.2, about_edge=RIGHT)
        result.next_to(self.plane.n2p(2), UR)
        return result

    def get_v_lines(self, circles):
        lines = VGroup()
        o_circles = VGroup(*circles)
        o_circles.sort(lambda p: p[0])
        for c1, c2 in zip(o_circles, o_circles[1:]):
            line = DashedLine(3 * UP, ORIGIN)
            line.set_stroke(WHITE, 1)
            line.move_to(midpoint(
                c1.get_center(), c2.get_center(),
            ))
            lines.add(line)
        return lines
