# ==============================================================================
# Scene:      DemonstrateAnArcSecond
# Source:     videos/_2025/cosmic_distance/part2.py (lines 401-580)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/cosmic_distance/planets.py
#
# Run from this folder:
#     manimgl DemonstrateAnArcSecond.py DemonstrateAnArcSecond -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder SunTexture texture (_lib/assets/raster_images/SunTexture.jpg); the original is private to Grant.
#
# Placeholder assets (not Grant's originals):
#   - SunTexture.jpg (procedural solar surface with granulation and spots, 2:1 equirectangular map)
#
# Notes:
#   The textures by name are copied to _lib/assets/raster_images/ (they are generated with _lib/assets/generated/2025/cosmic_distance/make_cosmic_distance_assets.py).
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/cosmic_distance/planets.py -----

def get_sun(
    radius=1.0,
    near_glow_ratio=2.0,
    near_glow_factor=2,
    big_glow_ratio=4,
    big_glow_factor=1,
    big_glow_opacity=0.35,
):
    sun = TexturedSurface(Sphere(radius=radius), "SunTexture")
    sun.set_shading(0, 0, 0)
    sun.to_edge(LEFT)

    # Glows
    near_glow = GlowDot(radius=near_glow_ratio * radius, glow_factor=near_glow_factor)
    near_glow.move_to(sun)

    big_glow = GlowDot(radius=big_glow_ratio * radius, glow_factor=big_glow_factor, opacity=big_glow_opacity)
    big_glow.move_to(sun)

    return Group(sun, near_glow, big_glow)



# ----- From _2025/cosmic_distance/part2.py -----

class DemonstrateAnArcSecond(InteractiveScene):
    def construct(self):
        # Add circle
        frame = self.frame
        frame.set_height(90)
        frame.set_field_of_view(10 * DEG)
        radius = 35

        circle = Circle(radius=radius)
        circle.set_stroke(WHITE, 2)

        frame = self.frame
        deg_height = radius * DEG
        zero_point = circle.get_right()

        # Add degree tick marks
        deg_ticks = VGroup(
            self.get_tick_mark(circle, n * DEG, 1, max_aparent_length=1)
            for n in range(360)
        )
        deg10_ticks = VGroup(
            self.get_tick_mark(circle, n * DEG, 2.5, max_aparent_length=1)
            for n in range(0, 360, 10)
        )
        deg30_labels = VGroup(
            self.get_tick_label(tick, number)
            for tick, number in zip(deg10_ticks[0::3], range(0, 360, 30))
        )
        deg10_labels = VGroup(
            self.get_tick_label(tick, number, visibility_range=(60, 30))
            for tick, number in zip(
                [*deg10_ticks[-2:], *deg10_ticks[1:3]],
                [340, 350, 10, 20]
            )
        )
        deg_labels = VGroup(
            self.get_tick_label(tick, number, visibility_range=(12, 6))
            for tick, number in zip(deg_ticks[1:10], range(1, 10))
        )

        self.add(circle, deg_ticks, deg10_ticks)
        self.add(deg30_labels, deg10_labels, deg_labels)

        # Add arc minute labels
        arc_minute_ticks = VGroup(
            self.get_tick_mark(circle, n * DEG / 60, 2.5e-2, max_aparent_length=0.75)
            for n in range(0, 60)
        )
        arc_minute_labels = VGroup(
            self.get_tick_label(
                tick,
                number,
                unit="arc-minutes",
                frame_prop=0.025,
                visibility_range=(0.35 * deg_height, 0.15 * deg_height),
            )
            for tick, number in zip(arc_minute_ticks[1:20], range(1, 20))
        )

        self.add(arc_minute_ticks)
        self.add(arc_minute_labels)

        # Add arc second labels
        arc_second_ticks = VGroup(
            self.get_tick_mark(circle, n * DEG / 60 / 60, 3.5e-4, max_aparent_length=0.5)
            for n in range(0, 60)
        )
        arc_second_ticks.rotate(0.25 * DEG, about_point=zero_point)

        am_height = deg_height / 60
        arc_second_labels = VGroup(
            self.get_tick_label(
                tick,
                number,
                unit="arc-seconds",
                frame_prop=0.025,
                visibility_range=(0.35 * am_height, 0.15 * am_height),
                font_size=0.1
            )
            for tick, number in zip(arc_second_ticks[1:20], range(1, 20))
        )

        self.add(arc_second_ticks)
        self.add(arc_second_labels)

        # Zoom in to one degree
        sun = get_sun(radius=(16 / 60) * deg_height, big_glow_ratio=2)
        sun.shift(zero_point - sun[0].get_bottom())
        sun.shift(0.5 * deg_height * LEFT)

        self.play(
            frame.animate.set_height(1.5 * deg_height).move_to(circle.pfp(0.5 * DEG / TAU)),
            run_time=8
        )
        self.wait(2)
        if False:
            # For insertion
            sun[0].always_sort_to_camera(self.camera)
            self.play(FadeIn(sun, 0.1 * LEFT))
            self.wait()
            self.play(FadeOut(sun))


        # Zoom in to arc seconds
        self.play(
            frame.animate.set_height(1.5 * deg_height / 60).move_to(circle.pfp(0.5 * DEG / TAU / 60)),
            run_time=4
        )
        self.wait()

        op_tracker = ValueTracker(0)
        arc_second_labels.add_updater(lambda m: m.set_opacity(op_tracker.get_value()))
        self.play(
            VGroup(circle, arc_minute_ticks, arc_second_ticks).animate.scale(20, about_point=zero_point),
            op_tracker.animate.set_value(1).set_anim_args(time_span=(1, 3)),
            run_time=4
        )
        self.wait()

    def get_tick_mark(
        self,
        circle,
        angle,
        tick_length,
        max_aparent_length=0.5,
        stroke_color=WHITE,
        stroke_width=2
    ):
        tick = Line(ORIGIN, tick_length * RIGHT)
        tick.move_to(circle.get_right())
        tick.rotate(angle, about_point=circle.get_center())
        tick.set_stroke(WHITE, stroke_width)

        frame_prop = max_aparent_length / FRAME_WIDTH
        tick.add_updater(lambda m: m.set_length(
            min(frame_prop * self.frame.get_width(), tick_length)
        ))

        return tick

    def get_tick_label(
        self,
        tick,
        number,
        unit=R"^\circ",
        buff_ratio=0.5,
        font_size=360,
        visibility_range=(1000, 900),
        frame_prop=0.05,
    ):
        label = Integer(number, unit=unit, font_size=font_size)
        if not unit.startswith("^"):
            label[-1].shift(0.5 * label[0].get_width() * RIGHT)
            if number == 1:
                label[-1][-1].scale(0, about_edge=LEFT)

        direction = normalize(tick.get_vector())
        direction[abs(direction) < 0.2] = 0

        label_height = label.get_height()

        def update_label(label):
            frame_height = self.frame.get_height()

            # Opacity
            opacity = clip(inverse_interpolate(*visibility_range, frame_height), 0, 1)
            label.set_opacity(opacity)

            # Max height
            height = min(frame_prop * frame_height, label_height)
            label.set_height(height)

            # Location
            buff = buff_ratio * label[0].get_width()
            label.next_to(tick.get_end(), direction, buff=buff)
            return label

        label.add_updater(update_label)

        return label
