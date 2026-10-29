# ==============================================================================
# Scene:      SumOfWaves
# Source:     videos/_2022/piano/fourier_animations.py (lines 26-189)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SumOfWaves.py SumOfWaves -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def get_wave_sum(axes, freqs, amplitudes=None, phases=None):
    if amplitudes is None:
        amplitudes = np.ones(len(freqs))
    if phases is None:
        phases = np.zeros(len(freqs))
    return axes.get_graph(lambda t: sum(
        amp * math.sin(TAU * freq * (t - phase))
        for freq, amp, phase in zip(freqs, amplitudes, phases)
    ))


class SumOfWaves(Scene):
    def construct(self):
        # Show single pure wave
        axes = Axes(
            (0, 12), (-1, 1),
            height=2,
        )
        base_freq = 0.5
        wave = get_wave_sum(axes, [base_freq])
        wave.set_stroke(BLUE, 2)

        x = 4.5
        brace = Brace(
            Line(axes.i2gp(x, wave), axes.i2gp(x + 1 / base_freq, wave)),
            UP, buff=SMALL_BUFF
        )
        brace_label = brace.get_text(
            "220 cycles / sec.",
            buff=SMALL_BUFF,
            font_size=36,
        )

        axes_labels = VGroup(*(
            Text(word, font_size=30)
            for word in ["Air pressure", "Time"]
        ))
        axes_labels[0].next_to(axes.y_axis, UP).to_edge(LEFT)
        axes_labels[1].next_to(axes.x_axis, UP).to_edge(RIGHT)

        self.add(axes)
        brace_rf = squish_rate_func(smooth, 0.25, 0.5)
        label_rf = squish_rate_func(smooth, 0.25, 1)
        self.play(
            ShowCreation(wave, rate_func=linear),
            GrowFromCenter(brace, rate_func=brace_rf),
            Write(brace_label, rate_func=label_rf),
            run_time=3,
        )
        self.play(LaggedStartMap(
            Write, axes_labels,
            lag_ratio=0.8
        ))
        self.wait()

        # Show multiple waves
        freq_multiples = [1, 6 / 5, 3 / 2, 21 / 12]
        freqs = [base_freq * r for r in freq_multiples]

        low_axes_group = VGroup(*(
            Axes((0, 12), (-1, 1), height=0.65)
            for freq in freqs
        ))
        low_axes_group.arrange(UP, buff=0.4)
        low_axes_group.to_edge(DOWN)
        low_axes_group.to_edge(RIGHT)

        waves = VGroup(*(
            get_wave_sum(la, [freq])
            for la, freq in zip(low_axes_group, freqs)
        ))
        waves.set_submobject_colors_by_gradient(BLUE, YELLOW)
        waves.set_stroke(width=2)

        axes_labels = VGroup(*(
            Text(f"{int(mult * 220)} Hz", font_size=24)
            for mult in freq_multiples
        ))
        for low_axes, label in zip(low_axes_group, axes_labels):
            label.next_to(low_axes, LEFT)

        self.play(
            FadeOut(VGroup(axes_labels[1], brace), DOWN),
            ReplacementTransform(brace_label, axes_labels[0]),
            ReplacementTransform(axes, low_axes_group[0]),
            ReplacementTransform(wave, waves[0]),
            *(
                TransformFromCopy(axes, low_axes)
                for low_axes in low_axes_group[1:]
            )
        )
        self.play(
            LaggedStartMap(
                ShowCreation, waves[1:],
                lag_ratio=0.5,
                rate_func=linear,
            ),
            LaggedStartMap(
                FadeIn, axes_labels[1:],
                lag_ratio=0.5,
            ),
            run_time=2,
        )
        self.wait()

        # Show sum
        top_axes = Axes((0, 12), (-4, 4), height=2.25)
        top_axes.to_edge(UP, buff=MED_SMALL_BUFF)
        top_axes.align_to(low_axes_group, RIGHT)
        top_rect = Rectangle(FRAME_WIDTH, top_axes.get_height() + 0.5)
        top_rect.move_to(top_axes)
        top_rect.set_x(0)
        top_rect.set_stroke(WHITE, 0)
        top_rect.set_fill(GREY_E, 1.0)
        sum_label = Text("Sum")
        sum_label.to_edge(UP, buff=0.25)

        amp_tracker = ValueTracker(np.ones(len(freqs)))
        comp_wave = always_redraw(lambda: get_wave_sum(
            top_axes, freqs, amplitudes=amp_tracker.get_value(),
        ).set_stroke(TEAL, 2))

        self.play(
            FadeIn(top_rect),
            FadeIn(top_axes),
            FadeIn(sum_label),
            *(
                Transform(wave.deepcopy(), comp_wave, remover=True)
                for wave in waves
            )
        )
        self.add(comp_wave)
        self.wait()

        # Tweak magnitudes
        for index in range(len(waves)):
            wave = waves[index]
            wave.index = index
            wave.max_height = wave.get_height()
            wave.add_updater(lambda w: w.set_height(
                amp_tracker.get_value()[w.index] * w.max_height,
                stretch=True
            ))

        self.add(*waves)

        changes = [
            # (index, d_value)
            (3, -0.8),
            (2, -0.9),
            (1, 0.6),
            (0, 0.5),
            (3, 0.8),
            (0, -1.1),
            (1, 0.5),
        ]
        for index, d_value in changes:
            values = amp_tracker.get_value().copy()
            values[index] += d_value
            arrows = VGroup(
                Vector(0.5 * UP),
                Vector(0.5 * DOWN),
            )
            arrows.arrange(DOWN if d_value > 0 else UP)
            axes = low_axes_group[index]
            arrows.match_height(axes)
            arrows.next_to(axes, LEFT)

            self.play(
                amp_tracker.animate.set_value(values),
                FadeIn(arrows[0], 0.25 * UP),
                FadeIn(arrows[1], 0.25 * DOWN),
            )
            self.play(FadeOut(arrows, run_time=0.75))
        self.wait()
