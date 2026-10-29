# ==============================================================================
# Scene:      ExplainCircleAnimations
# Source:     videos/_2019/diffyq/part2/fourier_series.py (lines 654-957)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ExplainCircleAnimations.py ExplainCircleAnimations -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - the earlier FourierCirclesScene API is rebuilt (self-rotating circles, get_circles(coefficients=...), get_rotating_vectors(circles)) which the repo no longer had and this scene uses
# ==============================================================================

from manim_imports_ext import *

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


class ExplainCircleAnimations(FourierCirclesScene):
    CONFIG = {
        "n_vectors": 100,
        "center_point": 2 * DOWN,
        "n_top_circles": 9,
        "path_height": 3,
    }

    def construct(self):
        self.add_path()
        self.add_circles()
        self.wait(8)
        self.organize_circles_in_a_row()
        self.show_frequencies()
        self.show_examples_for_frequencies()
        self.show_as_vectors()
        self.show_vector_sum()
        self.tweak_starting_vectors()

    # CHANGE: the earlier FourierCirclesScene API is rebuilt (self-rotating circles, get_circles(coefficients=...), get_rotating_vectors(circles)) which the repo no longer had and this scene uses
    # CHANGE (block): this scene uses an earlier FourierCirclesScene API that no longer exists either in the repo or in
    # Cairo sep19: self-rotating circles (with .freq, .coefficient, .center_func and get_start() = tip of the vector),
    # get_circles(coefficients=...), get_rotating_vectors(circles) and get_rotating_vector(circle). It is rebuilt here.
    def get_circles(self, vectors=None, coefficients=None, freqs=None):
        if vectors is not None:
            return super().get_circles(vectors)
        if freqs is None:
            freqs = self.get_freqs()
        if coefficients is None:
            coefficients = self.get_coefficients()
        circles = VGroup()
        last_circle = None
        for freq, coefficient, color in zip(freqs, coefficients, self.get_color_iterator()):
            circle = Circle(radius=abs(coefficient), color=color, **self.circle_config)
            circle.freq = freq
            circle.coefficient = coefficient
            phase = np.log(coefficient).imag if abs(coefficient) > 0 else 0
            circle.rotate(phase)
            if last_circle is None:
                circle.center_func = lambda: self.center_point
            else:
                circle.center_func = last_circle.get_start
            circle.move_to(circle.center_func())
            circle.add_updater(self.update_old_circle)
            circles.add(circle)
            last_circle = circle
        return circles

    def update_old_circle(self, circle, dt):
        circle.rotate(TAU * circle.freq * self.get_slow_factor() * dt)
        circle.move_to(circle.center_func())
        return circle

    def get_rotating_vectors(self, freqs=None, coefficients=None):
        if freqs is not None and len(freqs) > 0 and hasattr(freqs[0], "coefficient"):
            circles = freqs
            freqs = [c.freq for c in circles]
            coefficients = [c.coefficient for c in circles]
        return super().get_rotating_vectors(freqs, coefficients)

    def get_rotating_vector(self, coefficient=None, freq=None, center_func=None):
        if hasattr(coefficient, "coefficient"):
            circle = coefficient
            coefficient, freq, center_func = circle.coefficient, circle.freq, circle.center_func
        return super().get_rotating_vector(coefficient, freq, center_func)

    def get_vector_sum_path(self, vectors, color=YELLOW):
        coefs = [v.coefficient for v in vectors]
        freqs = [v.freq for v in vectors]
        center = vectors[0].center_func()
        return ParametricCurve(
            lambda t: center + reduce(op.add, [
                complex_to_R3(coef * np.exp(TAU * 1j * freq * t))
                for coef, freq in zip(coefs, freqs)
            ]),
            t_min=0,
            t_max=1,
            color=color,
            step_size=self.parametric_function_step_size,
        )

    def add_path(self):
        self.path = self.get_path()
        self.add(self.path)

    def add_circles(self):
        coefs = self.get_coefficients_of_path(self.path)
        self.circles = self.get_circles(coefficients=coefs)

        self.add(self.circles)
        self.drawn_path = self.get_drawn_path(self.circles)
        self.add(self.drawn_path)

    def organize_circles_in_a_row(self):
        circles = self.circles
        top_circles = circles[:self.n_top_circles].copy()

        center_trackers = VGroup()
        for circle in top_circles:
            tracker = VectorizedPoint(circle.center_func())
            circle.center_func = tracker.get_location
            center_trackers.add(tracker)
            tracker.freq = circle.freq
            tracker.circle = circle

        center_trackers.submobjects.sort(
            key=lambda m: m.freq
        )
        center_trackers.generate_target()
        right_buff = 1.45
        center_trackers.target.arrange(RIGHT, buff=right_buff)
        center_trackers.target.to_edge(UP, buff=1.25)

        self.add(top_circles)
        self.play(
            MoveToTarget(center_trackers),
            run_time=2
        )
        self.wait(4)

        self.top_circles = top_circles
        self.center_trackers = center_trackers

    def show_frequencies(self):
        center_trackers = self.center_trackers

        freq_numbers = VGroup()
        for ct in center_trackers:
            number = Integer(ct.freq)
            number.next_to(ct, DOWN, buff=1)
            freq_numbers.add(number)
            ct.circle.number = number

        ld, rd = [
            OldTex("\\dots")
            for x in range(2)
        ]
        ld.next_to(freq_numbers, LEFT, MED_LARGE_BUFF)
        rd.next_to(freq_numbers, RIGHT, MED_LARGE_BUFF)
        freq_numbers.add_to_back(ld)
        freq_numbers.add(rd)

        freq_word = OldTexText("Frequencies")
        freq_word.scale(1.5)
        freq_word.set_color(YELLOW)
        freq_word.next_to(freq_numbers, DOWN, MED_LARGE_BUFF)

        self.play(
            LaggedStartMap(
                FadeInFromDown, freq_numbers
            )
        )
        self.play(
            Write(freq_word),
            LaggedStartMap(
                ShowCreationThenFadeAround, freq_numbers,
            )
        )
        self.wait(2)

        self.freq_numbers = freq_numbers
        self.freq_word = freq_word

    def show_examples_for_frequencies(self):
        top_circles = self.top_circles
        c1, c2, c3 = [
            list(filter(
                lambda c: c.freq == k,
                top_circles
            ))[0]
            for k in (1, 2, 3)
        ]

        neg_circles = VGroup(*filter(
            lambda c: c.freq < 0,
            top_circles
        ))

        for c in [c1, c2, c3, *neg_circles]:
            c.rect = SurroundingRectangle(c)

        self.play(
            ShowCreation(c2.rect),
            WiggleOutThenIn(c2.number),
        )
        self.wait(2)
        self.play(
            ReplacementTransform(c2.rect, c1.rect),
        )
        self.play(FadeOut(c1.rect))
        self.wait()
        self.play(
            ShowCreation(c3.rect),
            WiggleOutThenIn(c3.number),
        )
        self.play(
            FadeOut(c3.rect),
        )
        self.wait(2)
        self.play(
            LaggedStart(*[
                ShowCreationThenFadeOut(c.rect)
                for c in neg_circles
            ])
        )
        self.wait(3)
        self.play(FadeOut(self.freq_word))

    def show_as_vectors(self):
        top_circles = self.top_circles
        top_vectors = self.get_rotating_vectors(top_circles)
        top_vectors.set_color(WHITE)

        original_circles = top_circles.copy()
        self.play(
            FadeIn(top_vectors),
            top_circles.set_opacity, 0,
        )
        self.wait(3)
        self.play(
            top_circles.match_style, original_circles
        )
        self.remove(top_vectors)

        self.top_vectors = top_vectors

    def show_vector_sum(self):
        trackers = self.center_trackers.copy()
        trackers.sort(
            submob_func=lambda t: abs(t.circle.freq - 0.1)
        )
        plane = self.plane = NumberPlane(
            x_min=-3,
            x_max=3,
            y_min=-2,
            y_max=2,
            axis_config={
                "stroke_color": GREY_B,
            }
        )
        plane.set_stroke(width=1)
        plane.fade(0.5)
        plane.move_to(self.center_point)

        self.play(
            FadeOut(self.drawn_path),
            FadeOut(self.circles),
            self.slow_factor_tracker.set_value, 0.05,
        )
        self.add(plane, self.path)
        self.play(FadeIn(plane))

        new_circles = VGroup()
        last_tracker = None
        for tracker in trackers:
            if last_tracker:
                tracker.new_location_func = last_tracker.circle.get_start
            else:
                tracker.new_location_func = lambda: self.center_point

            original_circle = tracker.circle
            tracker.circle = original_circle.copy()
            tracker.circle.center_func = tracker.get_location
            new_circles.add(tracker.circle)

            self.add(tracker, tracker.circle)
            start_point = tracker.get_location()
            self.play(
                UpdateFromAlphaFunc(
                    tracker, lambda t, a: t.move_to(
                        interpolate(
                            start_point,
                            tracker.new_location_func(),
                            a,
                        )
                    ),
                    run_time=2
                )
            )
            tracker.add_updater(lambda t: t.move_to(
                t.new_location_func()
            ))
            self.wait(2)
            last_tracker = tracker

        self.wait(3)

        self.clear()
        self.slow_factor_tracker.set_value(0.1)
        self.add(
            self.top_circles,
            self.freq_numbers,
            self.path,
        )
        self.add_circles()
        for tc in self.top_circles:
            for c in self.circles:
                if c.freq == tc.freq:
                    tc.rotate(
                        angle_of_vector(c.get_start() - c.get_center()) -
                        angle_of_vector(tc.get_start() - tc.get_center())
                    )
        self.wait(10)

    def tweak_starting_vectors(self):
        top_circles = self.top_circles
        circles = self.circles
        path = self.path
        drawn_path = self.drawn_path

        new_path = self.get_new_path()
        new_coefs = self.get_coefficients_of_path(new_path)
        new_circles = self.get_circles(coefficients=new_coefs)

        new_top_circles = VGroup()
        new_top_vectors = VGroup()
        for top_circle in top_circles:
            for circle in new_circles:
                if circle.freq == top_circle.freq:
                    new_top_circle = circle.copy()
                    new_top_circle.center_func = top_circle.get_center
                    new_top_vector = self.get_rotating_vector(
                        new_top_circle
                    )
                    new_top_circles.add(new_top_circle)
                    new_top_vectors.add(new_top_vector)

        self.play(
            self.slow_factor_tracker.set_value, 0,
            FadeOut(drawn_path)
        )
        self.wait()
        self.play(
            ReplacementTransform(top_circles, new_top_circles),
            ReplacementTransform(circles, new_circles),
            FadeOut(path),
            run_time=3,
        )
        new_drawn_path = self.get_drawn_path(
            new_circles, stroke_width=4,
        )
        self.add(new_drawn_path)
        self.slow_factor_tracker.set_value(0.1)
        self.wait(20)

    #
    def configure_path(self, path):
        path.set_stroke(WHITE, 1)
        path.set_fill(BLACK, opacity=1)
        path.set_height(self.path_height)
        path.move_to(self.center_point)
        return path

    def get_path(self):
        tex = OldTex("f")
        path = tex.family_members_with_points()[0]
        self.configure_path(path)
        return path
        # return Square().set_height(3)

    def get_new_path(self):
        shape = SVGMobject("TrebleClef")
        path = shape.family_members_with_points()[0]
        self.configure_path(path)
        path.scale(1.5, about_edge=DOWN)
        return path
