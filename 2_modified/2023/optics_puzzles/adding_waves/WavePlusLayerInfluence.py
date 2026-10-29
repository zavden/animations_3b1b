# ==============================================================================
# Scene:      WavePlusLayerInfluence
# Source:     videos/_2023/optics_puzzles/adding_waves.py (lines 735-1024)
# Category:   2 · Renders with modifications
# Includes code copied from: _2023/optics_puzzles/objects.py
#
# Run from this folder:
#     manimgl WavePlusLayerInfluence.py WavePlusLayerInfluence -w -m --fps 15
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



# ----- From _2023/optics_puzzles/adding_waves.py -----

class WavePlusLayerInfluence(InteractiveScene):
    default_frame_orientation = (-90, 0, 90)

    def construct(self):
        # Initialize axes
        frame = self.frame
        boxes = FullScreenRectangle().replicate(3)
        boxes.set_height(FRAME_HEIGHT / 3, stretch=True)
        boxes.arrange(DOWN, buff=0)

        x_range = (-12, 12)
        y_range = (-1, 1)
        z_range = (-1, 1)
        top_axes, mid_axes, low_axes = (
            ThreeDAxes(x_range, y_range, z_range),
            Axes(x_range, y_range),
            Axes(x_range, y_range),
        )
        all_axes = VGroup(top_axes, mid_axes, low_axes)
        all_axes.move_to(boxes[1])
        low_axes.move_to(boxes[2])
        for axes in all_axes:
            axes.set_stroke(opacity=0)
            axes.x_axis.set_stroke(opacity=0.5)

        # Initialize labels
        text_kw = dict(font_size=36)
        labels = VGroup(
            Text("Incoming light", **text_kw),
            Text("Wave from layer oscillations", **text_kw),
            Text("Net effect", **text_kw),
        )
        for label, box in zip(labels, boxes):
            label.next_to(box.get_corner(UL), DR, buff=MED_SMALL_BUFF)
        labels[2].shift(0.25 * UP)

        # Initialize waves
        wave1 = OscillatingWave(
            top_axes,
            y_amplitude=0.75,
            z_amplitude=0.0,
            wave_len=4.0,
            speed=1.5,
        )
        wave2_scale_tracker = ValueTracker(0.2)

        def wave2_func(x):
            offset_x = np.abs(x) + wave1.wave_len / 4
            y, z = wave1.xt_to_yz(offset_x, wave1.time)
            return wave2_scale_tracker.get_value() * y

        def sum_func(x):
            return wave1.xt_to_yz(x, wave1.time)[0] + wave2_func(x)


        wave2 = mid_axes.get_graph(wave2_func, bind=True)
        wave2.set_stroke(BLUE, 2)
        wave3 = low_axes.get_graph(sum_func, bind=True)
        wave3.set_stroke(TEAL, 2)

        # Vect waves
        field_kw = dict(stroke_width=2, stroke_opacity=0.5, tip_width_ratio=3)
        vect_wave1 = OscillatingFieldWave(top_axes, wave1, **field_kw)
        vect_wave2 = GraphAsVectorField(
            mid_axes, wave2_func,
            stroke_color=wave2.get_color(),
            **field_kw
        )
        vect_wave3 = GraphAsVectorField(
            low_axes, sum_func,
            stroke_color=wave3.get_color(),
            **field_kw
        )
        for vect_wave in [vect_wave1, vect_wave2, vect_wave3]:
            vect_wave.insert_updater(lambda m: m.reset_sample_points(), index=0)

        wave1_group = VGroup(wave1, vect_wave1)
        wave2_group = VGroup(wave2, vect_wave2)
        wave3_group = VGroup(wave3, vect_wave3)

        # Layers of charges
        layer_xs = np.arange(0, 6, 0.25)
        layers = Group()
        for x in layer_xs:
            charges = DotCloud(color=BLUE)
            charges.to_grid(31, 15)
            charges.make_3d()
            charges.set_shape(3, 3)
            charges.set_radius(0.035)
            charges.set_opacity(0.5)
            charges.rotate(90 * DEGREES, UP)
            charges.sort_points(lambda p: np.dot(p, OUT + UP))
            charges.x = x
            charges.amplitude_tracker = ValueTracker(0)
            charges.add_updater(lambda m: m.move_to(mid_axes.c2p(
                m.x, m.amplitude_tracker.get_value() * wave1.xt_to_yz(m.x, wave1.time)[0], 0,
            )))
            layers.add(charges)

        # Glass
        glass = VCube()
        glass.set_fill(opacity=0.25)
        glass.deactivate_depth_test()                                                              
        glass.set_shading(0.5, 0.5, 0)
        buff = 0.1
        glass.set_shape(*(
            dim + buff
            for dim in layers.get_shape()
        ))
        glass.move_to(layers, LEFT)
        glass.sort(lambda p: -p[0])
        glass.set_stroke(WHITE, 0.5, 0.5)

        # Show initial wave, then add layers
        frame = self.frame
        frame.reorient(-135, 20, 135)

        self.add(top_axes)
        self.add(wave1, vect_wave1)
        self.wait(2)
        self.play(
            Write(glass, time_span=(0, 2)),
            frame.animate.reorient(-110, 10, 110).set_anim_args(run_time=4),
        )
        self.play(
            LaggedStart(*(
                layer.amplitude_tracker.animate.set_value(0.1)
                for layer in layers
            ), lag_ratio=0, time_span=(0, 2)),
            LaggedStart(*(
                FadeIn(layer, suspend_mobject_updating=False)
                for layer in layers
            ), lag_ratio=0, time_span=(0, 2)),
        )
        self.play(
            self.frame.animate.reorient(-90, -40, 90),
            FadeOut(glass),
            run_time=9
        )
        self.wait(3)

        # Go back to just one layer
        self.play(
            LaggedStart(*(
                FadeOut(charges, suspend_mobject_updating=False)
                for charges in layers[1:]
            ), run_time=5, lag_ratio=0.25),
            layers[0].amplitude_tracker.animate.set_value(0.2),
            self.frame.animate.reorient(-90, -20, 90),
            run_time=5
        )
        self.wait(3)

        # Add the second order wave, then separate
        self.play(
            VFadeIn(wave2_group),
            FadeIn(mid_axes),
            run_time=1
        )
        self.wait(5)
        self.play(
            top_axes.animate.move_to(boxes[0], DOWN),
            frame.animate.reorient(-90, 0, 90).set_focal_distance(100),
            LaggedStartMap(FadeIn, labels[:2], shift=UP),
            run_time=2
        )
        self.wait(6)

        # Show sum (todo, add + and =)
        plus, eq = plus_eq = Tex("+=", font_size=72) 
        eq.rotate(90 * DEGREES)
        plus.move_to(all_axes[0:2])
        eq.move_to(all_axes[1:3])
        plus_eq.set_x(FRAME_WIDTH / 4)

        self.play(
            LaggedStartMap(FadeIn, plus_eq),
            ShowCreation(low_axes),
        )
        self.play(
            VFadeIn(wave3_group),
            Write(labels[2]),
        )
        self.wait(12)

        # Comment on reflected light
        reflection_label = VGroup(
            Vector(2 * LEFT),
            Text("Reflected light", font_size=36),
        )
        reflection_label.arrange(RIGHT)
        reflection_label.next_to(mid_axes.get_origin(), LEFT, buff=0.75)
        reflection_label.shift(0.5 * DOWN)
        reflection_label.set_color(YELLOW)

        self.play(
            GrowArrow(reflection_label[0]),
            Write(reflection_label[1]),
        )
        self.wait(8)

        # Cover left half
        cover = FullScreenFadeRectangle()
        cover.set_fill(BLACK, 0.9)
        cover.stretch(0.5, 0, about_edge=LEFT)

        self.add(cover, charges, labels)
        self.play(
            FadeOut(reflection_label),
            FadeIn(cover),
            plus_eq.animate.set_x(1.5),
            frame.animate.set_x(0.5 * FRAME_WIDTH - 2),
            *(
                label.animate.set_x(FRAME_WIDTH - 2.5, RIGHT)
                for label in labels
            ),
            run_time=2
        )
        self.wait(9)

        # Compare
        wave1.stop_clock()
        wave1_copy = wave1.copy()
        wave1_copy.clear_updaters()
        wave1_copy.set_stroke(width=3)

        self.wait()
        self.add(wave1_copy, cover, charges)
        self.play(
            wave1_copy.animate.match_y(wave3),
            run_time=2
        )
        self.wait()

        # Indicate tiny change
        def find_peak(wave, threshold=1e-2):
            points = wave.get_points()
            sub_points = points[int(0.6 * len(points)):int(0.8 * len(points))]
            top_y = wave.get_top()[1]
            index = np.argmax(sub_points[:, 1])
            return sub_points[index]

        line = Line(find_peak(wave3), find_peak(wave1_copy))
        shift_arrow = Vector(
            line.get_length() * LEFT * 2,
            stroke_width=3,
            max_tip_length_to_length_ratio=10,
        )
        shift_arrow.next_to(line, UP, buff=0.2)
        shift_label = Text("shift", font_size=24)
        always(shift_label.next_to, shift_arrow, UP)

        self.play(
            ShowCreation(shift_arrow),
            Write(shift_label),
        )
        self.wait()

        # Play with different strengths
        net_stretch = 1.0
        for stretch_factor in [3.0, 0.5, 2.0, 0.5, 1.0]:
            stretch = stretch_factor / net_stretch
            net_stretch = stretch_factor

            scale_arrows = VGroup(Vector(0.5 * UP), Vector(0.5 * DOWN))
            scale_arrows.arrange(DOWN if stretch > 1 else UP, buff=1.0)
            scale_arrows.move_to(mid_axes.c2p(2, 0))
            scale_arrows.set_stroke(opacity=1)
            scale_arrows.save_state()
            scale_arrows.stretch(0.5 if stretch > 1 else 1.5, 1)
            scale_arrows.set_stroke(opacity=0)

            self.play(
                Restore(scale_arrows),
                wave2_scale_tracker.animate.set_value(stretch * wave2_scale_tracker.get_value()),
                shift_arrow.animate.stretch(stretch, 0, about_edge=RIGHT),
            )
            self.play(FadeOut(scale_arrows))
            self.wait()

        self.play(
            wave2_scale_tracker.animate.set_value(0.2),
            FadeOut(wave1_copy),
            FadeOut(shift_arrow),
            FadeOut(shift_label),
        )

        # Restart
        wave1.start_clock()
        self.wait(8)
