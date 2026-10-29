# ==============================================================================
# Scene:      AmbientEncodingMachine3
# Source:     videos/_2026/cross_entropy/supplements.py (lines 38-166)
# Category:   1 · Renders unmodified
# Includes code copied from: _2024/transformers/helpers.py, _2026/cross_entropy/entropy.py
#
# Run from this folder:
#     manimgl AmbientEncodingMachine3.py AmbientEncodingMachine3 -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *
import numpy as np


# ----- From _2026/cross_entropy/entropy.py -----

def bit_string_mobject(
    bit_string: str,
    font: str = "Consolas",
    font_size: int = 48,
    colors: List[Colors] = [GREY_C, GREY_B]
):
    result = Text(bit_string, font=font, font_size=font_size)
    result["0"].set_color(colors[0])
    result["1"].set_color(colors[1])
    return result



# ----- From _2024/transformers/helpers.py -----

def value_to_color(
    value,
    low_positive_color=BLUE_E,
    high_positive_color=BLUE_B,
    low_negative_color=RED_E,
    high_negative_color=RED_B,
    min_value=0.0,
    max_value=10.0
):
    alpha = clip(float(inverse_interpolate(min_value, max_value, abs(value))), 0, 1)
    if value >= 0:
        colors = (low_positive_color, high_positive_color)
    else:
        colors = (low_negative_color, high_negative_color)
    return interpolate_color_by_hsl(*colors, alpha)


class Dial(VGroup):
    def __init__(
        self,
        radius=0.5,
        relative_tick_size=0.2,
        value_range=(0, 1, 0.1),
        initial_value=0,
        arc_angle=270 * DEGREES,
        stroke_width=2,
        stroke_color=WHITE,
        needle_color=BLUE,
        needle_stroke_width=5.0,
        value_to_color_config=dict(),
        set_anim_streak_color=TEAL,
        set_anim_streak_width=4,
        set_value_anim_streak_density=6,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.value_range = value_range
        self.value_to_color_config = value_to_color_config
        self.set_anim_streak_color = set_anim_streak_color
        self.set_anim_streak_width = set_anim_streak_width
        self.set_value_anim_streak_density = set_value_anim_streak_density

        # Main dial
        self.arc = Arc(arc_angle / 2, -arc_angle, radius=radius)
        self.arc.rotate(90 * DEGREES, about_point=ORIGIN)

        low, high, step = value_range
        n_values = int(1 + (high - low) / step)
        tick_points = map(self.arc.pfp, np.linspace(0, 1, n_values))
        self.ticks = VGroup(*(
            Line((1.0 - relative_tick_size) * point, point)
            for point in tick_points
        ))
        self.bottom_point = VectorizedPoint(radius * DOWN)
        for mob in self.arc, self.ticks:
            mob.set_stroke(stroke_color, stroke_width)

        self.add(self.arc, self.ticks, self.bottom_point)

        # Needle
        self.needle = Line()
        self.needle.set_stroke(
            color=needle_color,
            width=[needle_stroke_width, 0]
        )
        self.add(self.needle)

        # Initialize
        self.set_value(initial_value)

    def value_to_point(self, value):
        low, high, step = self.value_range
        alpha = inverse_interpolate(low, high, value)
        return self.arc.pfp(alpha)

    def set_value(self, value):
        self.needle.put_start_and_end_on(
            self.get_center(),
            self.value_to_point(value)
        )
        self.needle.set_color(value_to_color(
            value,
            min_value=self.value_range[0],
            max_value=self.value_range[1],
            **self.value_to_color_config
        ))

    def animate_set_value(self, value, **kwargs):
        kwargs.pop("path_arc", None)
        center = self.get_center()
        points = [self.needle.get_end(), self.value_to_point(value)]
        vects = [point - center for point in points]
        angle1, angle2 = [
            (angle_of_vector(vect) + TAU / 4) % TAU - TAU / 4
            for vect in vects
        ]
        path_arc = angle2 - angle1

        density = self.set_value_anim_streak_density
        radii = np.linspace(0, 0.5 * self.get_width(), density + 1)[1:]
        diff_arcs = VGroup(*(
            Arc(
                angle1, angle2 - angle1,
                radius=radius,
                arc_center=center,
            )
            for radius in radii
        ))
        diff_arcs.set_stroke(self.set_anim_streak_color, self.set_anim_streak_width)

        return AnimationGroup(
            self.animate.set_value(value).set_anim_args(path_arc=path_arc, **kwargs),
            *(
                VShowPassingFlash(diff_arc, time_width=1.5, **kwargs)
                for diff_arc in diff_arcs
            )
        )

    def get_random_value(self):
        low, high, step = self.value_range
        return interpolate(low, high, random.random())



# ----- From _2026/cross_entropy/supplements.py -----

class AmbientEncodingMachine3(InteractiveScene):
    def construct(self):
        # Set up machine, bit stream and text stream
        machine = self.get_machine()
        text_stream = self.get_text_stream()
        bit_stream = self.get_bit_stream()

        vel_tracker = bit_stream.vel_tracker

        dial = Dial(
            value_range=(0, 10, 1),
            arc_angle=180 * DEG,
            radius=1,
            set_anim_streak_width=0,
        )
        dial.set_value(8)
        dial.next_to(machine, UP, buff=-0.5)

        label = Tex(R"8.0 \text{bits} / \text{sym}", font_size=36)
        dec = label.make_number_changeable("8.0")
        dec.shift(0.1 * LEFT)
        dec.set_color(BLUE)
        label.next_to(dial, UP)

        self.add(text_stream, bit_stream)
        self.add(machine, dial, label)

        self.wait(2)

        # Decrease
        # values = [4, 2.5, 1.5]
        values = [8]
        for value in values:
            self.play(
                vel_tracker.animate.set_value(value),
                dial.animate_set_value(value),
                ChangeDecimalToValue(dec, value),
                run_time=3
            )
            self.wait()

        # Ask about a fundamental limit
        limit_line = Line(dial.needle.get_start(), dial.value_to_point(1))
        limit_line.scale(1.5, about_point=limit_line.get_start())
        limit_line.set_stroke(RED, 5)
        # limit_word = Text("Limit?", font_size=30)
        limit_word = Tex("H(P)", font_size=30)
        limit_word.set_color(RED)
        limit_word.next_to(limit_line.get_end(), LEFT, SMALL_BUFF)

        self.play(
            ShowCreation(limit_line),
            FadeIn(limit_word, 0.25 * LEFT, lag_ratio=0.1, time_span=(0.5, 1.5))
        )
        self.play(
            vel_tracker.animate.set_value(1.0),
            dial.animate_set_value(1.0),
            ChangeDecimalToValue(dec, 1.0),
            run_time=10,
        )
        self.wait(20)

    def get_machine(self, width=1.5, height=1, color=GREY_D):
        square = Rectangle(width, height)
        in_tri = ArrowTip().set_height(0.5 * height)
        in_tri.stretch(2, 1)
        out_tri = in_tri.copy().rotate(PI)
        in_tri.move_to(square.get_left())
        out_tri.move_to(square.get_right())
        machine = Union(square, in_tri, out_tri)
        machine.set_fill(color, 1)
        machine.set_stroke(WHITE, 2)
        machine.set_z_index(1)
        machine.set_fill(opacity=0.8)
        return machine

    def get_text_stream(self, velocity=1, symbols=True):
        # Test
        text_parts = [
            "It was the best of times, it was the worst of times,",
            "it was the age of wisdom, it was the age of foolishness,",
            "it was the epoch of belief, it was the epoch of incredulity,",
            "it was the season of Light, it was the season of Darkness,",
            "it was the spring of hope, it was the winter of despair,",
            "we had everything before us, we had nothing before us,",
            "we were all going direct to Heaven, we were all going",
            "direct the other way – in short, the period was so far",
            "like the present period, that some of its noisiest authorities",
            "insisted on its being received, for good or for evil, in the",
            "superlative degree of comparison only.",
        ]
        text_mobs = VGroup(Text(part, font="Consolas") for part in text_parts)
        text_mobs.arrange(RIGHT, MED_SMALL_BUFF)
        text_stream = VGroup(*it.chain(*text_mobs))
        if symbols:
            values = np.random.choice([1, 2, 3, 4, 5], size=100, p=[0.1, 0.4, 0.2, 0.1, 0.2])
            colors = color_gradient([BLUE, YELLOW], 5, interp_by_hsl=True)
            text_stream = VGroup(
                Tex(Rf"s_{{{n}}}").set_color(colors[n - 1])
                for n in values
            )
            text_stream.arrange(RIGHT, buff=SMALL_BUFF, aligned_edge=UP)
        text_stream.next_to(ORIGIN, RIGHT)

        def update_stream(stream, dt):
            stream.shift(velocity * dt * LEFT)
            for ch in stream:
                ch.set_opacity(clip(ch.get_x(), 0, 1))

        text_stream.add_updater(update_stream)

        return text_stream

    def get_bit_stream(self, n_bits=100, velocity=8):
        bits = bit_string_mobject("".join(random.choice("01") for n in range(n_bits)))
        bits.vel_tracker = ValueTracker(velocity)
        buff = get_norm(bits[0].get_right() - bits[1].get_left())

        def update_bit_stream(bits, dt):
            bits.shift(bits.vel_tracker.get_value() * dt * LEFT)
            for bit in bits:
                bit.set_opacity(clip(-bit.get_x(), 0, 1))
                if bit.get_x() < -10:
                    bit.next_to(bits, RIGHT, buff=buff)

        bits.move_to(ORIGIN, RIGHT)
        bits.add_updater(update_bit_stream)

        return bits
