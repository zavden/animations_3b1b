# ==============================================================================
# Scene:      SlowedAndAbsorbed
# Source:     videos/_2023/optics_puzzles/slowing_waves.py (lines 521-595)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl SlowedAndAbsorbed.py SlowedAndAbsorbed -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Old VectorField/TimeVaryingVectorField API (2023): they are imported from _lib/legacy_vector_field.py (a shim with the pre-Nov-2024 API) instead of from manimlib
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
# CHANGE: old VectorField API (2023); see _lib/legacy_vector_field.py
from legacy_vector_field import VectorField, TimeVaryingVectorField
from matplotlib import colormaps
from typing import TYPE_CHECKING


# ----- From _2023/optics_puzzles/objects.py -----

if TYPE_CHECKING:
    from typing import Callable
    from manimlib.typing import Vect3


spectral_cmap = colormaps.get_cmap("Spectral")


def get_spectral_color(alpha):
    return Color(rgb=spectral_cmap(alpha)[:3])


class OscillatingWave(VMobject):
    def __init__(
        self,
        axes,
        y_amplitude=0.0,
        z_amplitude=0.75,
        z_phase=0.0,
        y_phase=0.0,
        wave_len=0.5,
        twist_rate=0.0,  # In rotations per unit distance
        speed=1.0,
        sample_resolution=0.005,
        stroke_width=2,
        offset=ORIGIN,
        color=None,
        **kwargs,
    ):
        self.axes = axes
        self.y_amplitude = y_amplitude
        self.z_amplitude = z_amplitude
        self.z_phase = z_phase
        self.y_phase = y_phase
        self.wave_len = wave_len
        self.twist_rate = twist_rate
        self.speed = speed
        self.sample_resolution = sample_resolution
        self.offset = offset

        super().__init__(**kwargs)

        color = color or self.get_default_color(wave_len)
        self.set_stroke(color, stroke_width)
        self.set_flat_stroke(False)

        self.time = 0
        self.clock_is_stopped = False

        self.add_updater(lambda m, dt: m.update_points(dt))

    def update_points(self, dt):
        if not self.clock_is_stopped:
            self.time += dt
        xs = np.arange(
            self.axes.x_axis.x_min,
            self.axes.x_axis.x_max,
            self.sample_resolution
        )
        self.set_points_as_corners(
            self.offset + self.xt_to_point(xs, self.time)
        )

    def stop_clock(self):
        self.clock_is_stopped = True

    def start_clock(self):
        self.clock_is_stopped = False

    def xt_to_yz(self, x, t):
        phase = TAU * t * self.speed / self.wave_len
        y_outs = self.y_amplitude * np.sin(TAU * x / self.wave_len - phase - self.y_phase)
        z_outs = self.z_amplitude * np.sin(TAU * x / self.wave_len - phase - self.z_phase)
        twist_angles = x * self.twist_rate * TAU
        y = np.cos(twist_angles) * y_outs - np.sin(twist_angles) * z_outs
        z = np.sin(twist_angles) * y_outs + np.cos(twist_angles) * z_outs

        return y, z

    def xt_to_point(self, x, t):
        y, z = self.xt_to_yz(x, t)
        return self.axes.c2p(x, y, z)

    def get_default_color(self, wave_len):
        return get_spectral_color(inverse_interpolate(
            1.5, 0.5, wave_len
        ))


class GraphAsVectorField(VectorField):
    def __init__(
        self,
        axes: Axes | ThreeDAxes,
        # Maps x to y, or x to (y, z)
        graph_func: Callable[[VectN], VectN] | Callable[[VectN], Tuple[VectN, VectN]],
        x_density=10.0,
        max_vect_len=np.inf,
        **kwargs,
    ):
        self.sample_xs = np.arange(axes.x_axis.x_min, axes.x_axis.x_max, 1.0 / x_density)
        self.axes = axes

        def vector_func(points):
            output = graph_func(self.sample_xs)
            if isinstance(axes, ThreeDAxes):
                graph_points = axes.c2p(self.sample_xs, *output)
            else:
                graph_points = axes.c2p(self.sample_xs, output)
            base_points = axes.x_axis.n2p(self.sample_xs)
            return graph_points - base_points

        super().__init__(
            func=vector_func,
            max_vect_len=max_vect_len,
            **kwargs
        )
        always(self.update_vectors)

    def reset_sample_points(self):
        self.sample_points = self.get_sample_points()

    def get_sample_points(self, *args, **kwargs):
        # Override super class and ignore all length/density information
        return self.axes.x_axis.n2p(self.sample_xs)


class OscillatingFieldWave(GraphAsVectorField):
    def __init__(self, axes, wave, **kwargs):
        self.wave = wave
        if "stroke_color" not in kwargs:
            kwargs["stroke_color"] = wave.get_color()
        super().__init__(
            axes=axes,
            graph_func=lambda x: wave.xt_to_yz(x, wave.time),
            **kwargs
        )

    def get_sample_points(self, *args, **kwargs):
        # Override super class and ignore all length/density information
        return self.wave.offset + self.axes.x_axis.n2p(self.sample_xs)



# ----- From _2023/optics_puzzles/slowing_waves.py -----

class SlicedWave(Group):
    default_wave_config = dict(
        z_amplitude=0,
        y_amplitude=1,
        wave_len=2.0,
        color=BLUE,
    )
    default_layer_style = dict(
        stroke_width=2.0,
        stroke_color=WHITE,
    )
    default_vect_wave_style = dict(
        stroke_opacity=0.5
    )

    def __init__(
        self,
        axes,
        layer_xs,
        phase_kick_back=0,
        layer_height=4.0,
        damping_per_layer=1.0,
        wave_config = dict(),
        vect_wave_style=dict(),
        layer_style=dict(),
    ):
        self.layer_xs = layer_xs
        self.axes = axes
        wave_kw = merge_dicts_recursively(self.default_wave_config, wave_config)
        vwave_kw = merge_dicts_recursively(self.default_vect_wave_style, vect_wave_style)
        line_kw = merge_dicts_recursively(self.default_layer_style, layer_style)

        self.wave = OscillatingWave(axes, **wave_kw)
        self.vect_wave = OscillatingFieldWave(axes, self.wave, **vwave_kw)
        self.phase_kick_trackers = [
            ValueTracker(phase_kick_back)
            for x in layer_xs
        ]
        self.absorbtion_trackers = [
            ValueTracker(damping_per_layer)
            for x in layer_xs
        ]
        self.layers = VGroup()
        for x in layer_xs:
            line = Line(DOWN, UP, **line_kw)
            line.set_height(layer_height)
            line.move_to(axes.c2p(x, 0))
            self.layers.add(line)

        self.wave.xt_to_yz = self.xt_to_yz

        super().__init__(
            self.wave,
            self.vect_wave,
            self.layers,
            *self.phase_kick_trackers
        )

    def set_layer_xs(self, xs):
        self.layer_xs = xs

    def xt_to_yz(self, x, t):
        phase = np.ones_like(x)
        phase *= TAU * t * self.wave.speed / self.wave.wave_len
        amplitudes = self.wave.y_amplitude * np.ones_like(x)
        for layer_x, pkt, at in zip(self.layer_xs, self.phase_kick_trackers, self.absorbtion_trackers):
            phase[x > layer_x] += pkt.get_value()
            amplitudes[x > layer_x] *= at.get_value()

        y = amplitudes * np.sin(TAU * x / self.wave.wave_len - phase)
        return y, np.zeros_like(x)


class SpeedInMediumFastPart(InteractiveScene):
    z_amplitude = 0
    y_amplitude = 1.0
    color = YELLOW
    wave_len = 3.0
    speed = 1.5
    medium_color = BLUE
    medium_opacity = 0.35
    add_label = True
    run_time = 30
    material_label = "Glass"

    def construct(self):
        # Basic wave
        axes = ThreeDAxes((-12, 12), (-4, 4))
        axes.z_axis.set_stroke(opacity=0)
        axes.y_axis.set_stroke(opacity=0)
        wave = OscillatingWave(
            axes,
            z_amplitude=self.z_amplitude,
            y_amplitude=self.y_amplitude,
            color=self.color,
            wave_len=self.wave_len,
            speed=self.speed,
        )
        vect_wave = OscillatingFieldWave(axes, wave)
        vect_wave.set_stroke(opacity=0.5)

        self.add(axes, wave, vect_wave)

        # Water label
        rect = FullScreenRectangle()
        rect.stretch(0.5, 0, about_edge=RIGHT)
        rect.set_stroke(width=0)
        rect.set_fill(self.medium_color, self.medium_opacity)
        self.add(rect)

        if self.add_label:
            label = Text(self.material_label, font_size=60)
            label.next_to(rect.get_top(), DOWN)
            self.add(label)

        # Propagate
        self.wait(self.run_time)


class PhaseKickBacks(SpeedInMediumFastPart):
    layer_xs = np.arange(0, 8, 1)
    kick_back_value = 0
    axes_config = dict(
        x_range=(-8, 8),
        y_range=(-4, 4),
    )
    line_style = dict()
    wave_config = dict()
    vect_wave_style = dict()
    layer_add_on_run_time = 5
    damping_per_layer = 1.0

    def get_axes(self):
        axes = ThreeDAxes(**self.axes_config)
        axes.z_axis.set_stroke(opacity=0)
        return axes

    def get_layer_xs(self):
        return self.layer_xs

    def get_sliced_wave(self):
        return SlicedWave(
            self.get_axes(),
            self.get_layer_xs(),
            wave_config=self.wave_config,
            vect_wave_style=self.vect_wave_style,
            layer_style=self.line_style,
            phase_kick_back=self.kick_back_value,
            damping_per_layer=self.damping_per_layer,
        )

    def setup(self):
        super().setup()
        self.sliced_wave = self.get_sliced_wave()
        self.add(self.sliced_wave)


class RevertToOneLayerAtATime(PhaseKickBacks):
    layer_xs = np.arange(0, FRAME_WIDTH / 2, FRAME_WIDTH / 2**(11))
    kick_back_value = -0.025
    n_layers_skipped = 64

    exagerated_phase_kick = -0.8

    line_style = dict(
        stroke_width=1,
        stroke_opacity=0.25,
        stroke_color=BLUE_B
    )
    axes_config = dict(
        x_range=(-12, 12),
        y_range=(-4, 4),
    )
    wave_config = dict(
        color=YELLOW,
        sample_resolution=0.001
    )
    vect_wave_style = dict(tip_width_ratio=3, stroke_opacity=0.5)

    def construct(self):
        # Objects
        sliced_wave = self.sliced_wave
        wave = sliced_wave.wave
        layers = sliced_wave.layers
        pkts = sliced_wave.phase_kick_trackers

        # Add label
        block_label = Text("Material (e.g. glass)")
        block_label.next_to(layers, UP, aligned_edge=LEFT)

        for pkt in pkts:
            pkt.set_value(-0.015)

        self.wait(5)
        self.play(Write(block_label["Material"], run_time=1))
        self.play(FadeIn(block_label["(e.g. glass)"], 0.25 * UP))
        self.add(block_label)
        self.wait(2)

        # Show layers
        layers.save_state()

        rect = BackgroundRectangle(sliced_wave)
        rect.set_fill(BLACK, 0.9)
        self.add(sliced_wave, rect, layers)
        self.play(
            layers.animate.arrange(RIGHT, buff=0.3).move_to(ORIGIN, LEFT).set_stroke(width=2, opacity=1),
            FadeIn(rect),
            *(pkt.animate.set_value(0) for pkt in pkts),
            run_time=2,
        )
        self.wait(3)

        # Revert to one single layer
        left_layers = VGroup()
        for layer in layers:
            if layer.get_x() < FRAME_WIDTH / 2:
                left_layers.add(layer)
        self.remove(layers)
        self.add(left_layers)

        layer_label = Text("Thin layer of material")
        layer_label.next_to(layers[0], UP, buff=0.75)

        kw = dict(run_time=5, lag_ratio=0.1)
        self.play(
            LaggedStart(*(
                layer.animate().set_stroke(opacity=0).shift(DOWN)
                for layer in left_layers[:0:-1]
            ), **kw),
            layers[0].animate.set_stroke(width=2, opacity=1).set_height(5).set_anim_args(time_span=(4, 5)),
            FadeTransform(
                block_label, layer_label,
                time_span=(4, 5)
            ),
            FadeOut(rect, time_span=(3, 5)),
        )
        self.wait(4)

        # Pause, shift the phase a bit
        arrow = Vector(1.0 * LEFT, stroke_width=6)
        arrow.next_to(wave, UP, buff=0.75)
        arrow.set_x(0, LEFT).shift(0.1 * RIGHT)
        phase_kick = self.exagerated_phase_kick
        kick_words = Text("Kick back\nthe phase", font_size=36)
        kick_words.next_to(arrow, RIGHT)
        kick_label = VGroup(arrow, kick_words)
        kick_label.set_color(RED)

        self.wait(1 - (wave.time % 1))
        wave.stop_clock()
        self.wait()
        self.play(
            pkts[0].animate.set_value(phase_kick),
            FadeIn(kick_label, LEFT),
        )
        self.wait()

        # Show the phase kick
        form1 = Tex(R"A\sin(kx)")
        form2 = Tex(R"A\sin(kx + 1.00)")
        pk_decimal: DecimalNumber = form2.make_number_changeable("1.00")
        pk_decimal.set_value(-phase_kick)
        pk_decimal.set_color(RED)

        VGroup(form1, form2).next_to(wave, DOWN)
        form1.set_x(-FRAME_WIDTH / 4)
        form2.set_x(+FRAME_WIDTH / 4)


        self.play(FadeIn(form1, 0.5 * DOWN))
        self.wait()
        self.play(TransformMatchingStrings(form1.copy(), form2, path_arc=20 * DEGREES))
        self.wait()
        for value in [-0.01, phase_kick]:
            self.play(
                pkts[0].animate.set_value(value),
                ChangeDecimalToValue(pk_decimal, -value),
                run_time=2,
            )
            self.wait()

        # Add phase kick label
        pk_label = Text("Phase kick = ", font_size=36, fill_color=GREY_B)
        pk_label.next_to(wave, UP, LARGE_BUFF)
        pk_label.to_edge(LEFT)

        form2.remove(pk_decimal)
        form2.add(pk_decimal.copy())
        self.add(form2)
        self.play(
            pk_decimal.animate.match_height(pk_label).next_to(pk_label, RIGHT, 0.2, DOWN),
            ReplacementTransform(kick_words["Kick"].copy(), pk_label["kick"]),
            ReplacementTransform(kick_words["phase"].copy(), pk_label["Phase"]),
            FadeIn(pk_label["="]),
            run_time=2
        )
        pk_label.add(pk_decimal)
        self.add(pk_label)
        self.play(
            FadeOut(form1),
            FadeOut(form2),
        )

        # Show following layers
        for layer in layers[1:]:
            layer.match_height(layers[0])
            layer.match_style(layers[0])
            layer.set_stroke(opacity=0)

        nls = self.n_layers_skipped
        shown_layers = VGroup(layers[0])
        layer_arrows = VGroup(VectorizedPoint(layer_label.get_center()))
        for layer, pkt in zip(layers[nls::nls], pkts[nls::nls]):
            layer.set_stroke(opacity=1)
            shown_layers.add(layer)

            layer_label.target = layer_label.generate_target()
            layer_label.target.set_height(0.35)
            layer_label.target.match_x(shown_layers)
            layer_label.target.to_edge(UP, buff=0.25)

            layer_arrows.target = VGroup(*(
                Arrow(
                    layer_label.target.get_bottom(),
                    sl.get_top(),
                    buff=0.1,
                    stroke_width=2,
                    stroke_opacity=0.5,
                )
                for sl in shown_layers
            ))

            self.play(
                FadeOut(kick_label),
                GrowFromCenter(layer),
                MoveToTarget(layer_label),
                MoveToTarget(layer_arrows),
            )
            kick_label.align_to(layer, LEFT).shift(0.1 * RIGHT)
            self.play(
                FadeIn(kick_label, 0.5 * LEFT),
                pkt.animate.set_value(phase_kick)
            )
        self.play(FadeOut(kick_label))

        # Restart clock
        wave.start_clock()
        self.play(FadeOut(layer_label), FadeOut(layer_arrows))
        self.wait(6)

        # Change phase kick
        self.play(FlashAround(pk_label))
        for value in [-0.01, self.exagerated_phase_kick]:
            phase_kick = value
            self.play(
                ChangeDecimalToValue(pk_decimal, -phase_kick),
                *(
                    pkt.animate.set_value(phase_kick)
                    for pkt in pkts[::nls]
                ),
                run_time=4
            )
            self.wait(2)
        self.wait(2)

        # Number of layers label
        n_shown_layers = len(layers[::nls])
        n_layers_label = TexText(f"Num. layers = {n_shown_layers}", font_size=36)
        n_layers_label.set_color(GREY_B)
        n_layers_label.next_to(pk_label, UP, MED_LARGE_BUFF, LEFT)
        nl_decimal = n_layers_label.make_number_changeable(n_shown_layers)
        nl_decimal.set_color(BLUE)

        self.play(FadeIn(n_layers_label, UP))
        self.wait(8)

        # Fill in
        opacity = 1.0
        stroke_width = 2.0
        kw = dict(lag_ratio=0.1, run_time=3)
        while nls > 1:
            # Update parameters
            nls //= 2
            opacity = 0.25 + 0.5 * (opacity - 0.25)
            stroke_width = 1.0 + 0.5 * (stroke_width - 1.0)
            phase_kick /= 2

            new_layers = layers[nls::2 * nls]
            old_layers = layers[0::2 * nls]

            new_nl_decimal = Integer(len(layers[::nls]))
            new_nl_decimal.match_height(nl_decimal)
            new_nl_decimal.match_style(nl_decimal)
            new_nl_decimal.move_to(nl_decimal, LEFT)

            new_pk_decimal = DecimalNumber(
                -phase_kick,
                num_decimal_places=(2 if -phase_kick > 0.05 else 3)
            )
            new_pk_decimal.match_height(pk_decimal)
            new_pk_decimal.match_style(pk_decimal)
            new_pk_decimal.move_to(pk_decimal, LEFT)

            new_layers.set_stroke(width=stroke_width, opacity=opacity)

            self.play(
                LaggedStart(*(
                    GrowFromCenter(layer)
                    for layer in new_layers
                ), **kw),
                old_layers.animate.set_stroke(width=stroke_width, opacity=opacity),
                LaggedStart(*(
                    pkt.animate.set_value(phase_kick)
                    for pkt in pkts[::nls]
                ), **kw),
                LaggedStart(
                    FadeOut(nl_decimal, 0.2 * UP),
                    FadeIn(new_nl_decimal, 0.2 * UP),
                    FadeOut(pk_decimal, 0.2 * UP),
                    FadeIn(new_pk_decimal, 0.2 * UP),
                    lag_ratio=0.1,
                    run_time=1
                )
            )

            nl_decimal = new_nl_decimal
            pk_decimal = new_pk_decimal

            self.play(*(
                pkt.animate.set_value(phase_kick)
                for pkt in pkts[::nls]
            ))
            self.wait(3 if nls >= 32 else 1)

        # Wait
        self.wait(10)


class SlowedAndAbsorbed(RevertToOneLayerAtATime):
    layer_xs = np.arange(-FRAME_WIDTH / 3, FRAME_WIDTH / 3, FRAME_WIDTH / 2**(8))
    kick_back_value = -0.2
    damping_per_layer = 1 - 2e-2
    wave_config = dict(
        color=YELLOW,
        sample_resolution=0.001,
    )
    line_style = dict(
        stroke_color=BLUE_B,
        stroke_width=1.5,
        stroke_opacity=0.5,
    )

    def construct(self):
        # Objects
        sliced_wave = self.sliced_wave
        wave = sliced_wave.wave
        layers = sliced_wave.layers
        pkts = sliced_wave.phase_kick_trackers
        ats = sliced_wave.absorbtion_trackers

        # Show labels
        label = Text("Wave gets slowed and absorbed")
        label.next_to(layers, UP)
        abs_words = label["and absorbed"]

        mu_label = Tex(R"\mu").set_color(PINK)
        mu_line = NumberLine((0, 1, 0.2), width=1.0, tick_size=0.05)
        mu_line.rotate(PI / 2)
        mu_line.to_corner(UR)
        mu_indicator = Triangle(start_angle=0)
        mu_indicator.set_width(0.15)
        mu_indicator.set_fill(PINK, 1)
        mu_indicator.set_stroke(width=0)
        mu_tracker = ValueTracker(1)
        mu_indicator.add_updater(lambda m: m.move_to(mu_line.n2p(mu_tracker.get_value()), RIGHT))
        mu_label.add_updater(lambda m: m.next_to(mu_indicator, LEFT, buff=0.1))

        for pkt in pkts:
            pkt.set_value(0)
        for at in ats:
            at.set_value(1)

        self.play(
            FadeIn(label, time_span=(0, 2)),
            FlashAround(abs_words, color=PINK, time_span=(2, 4)),
            abs_words.animate.set_color(PINK).set_anim_args(time_span=(2, 4)),
            FadeIn(mu_line),
            FadeIn(mu_indicator),
            FadeIn(mu_label),
            LaggedStart(*(
                pkt.animate.set_value(self.kick_back_value)
                for pkt in pkts
            )),
            LaggedStart(*(
                at.animate.set_value(self.damping_per_layer)
                for at in ats
            )),
            LaggedStart(*(
                FadeIn(layer, scale=0.8)
                for layer in layers
            )),
            run_time=5,
        )

        # Play with mu
        for mu in [0.1, 1.0]:
            self.play(
                mu_tracker.animate.set_value(mu),
                *(at.animate.set_value(1 - mu * 2e-2) for at in ats),
                run_time=3,
            )

        self.wait(17)
