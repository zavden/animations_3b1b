# ==============================================================================
# Scene:      LuarEclipse
# Source:     videos/_2025/cosmic_distance/planets.py (lines 673-864)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LuarEclipse.py LuarEclipse -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses MoonTexture/DarkMoonTexture derived from MoonTextureMap.png (the originals are private to Grant).
#   - Uses RedMoonTexture derived from MoonTextureMap.png (the original is private to Grant).
#
# Placeholder assets (not Grant's originals):
#   - MoonTexture.jpg and DarkMoonTexture.jpg (derived from the lib's real lunar map MoonTextureMap.png; the dark one is the same map dimmed)
#   - RedMoonTexture.jpg (MoonTextureMap.png tinted coppery red, eclipsed moon)
#
# Notes:
#   The textures by name are copied to _lib/assets/raster_images/ (they are generated with _lib/assets/generated/2025/cosmic_distance/make_cosmic_distance_assets.py).
# ==============================================================================

from manim_imports_ext import *

EARTH_TILT_ANGLE = 23.3 * DEG


# All in Kilometers
EARTH_RADIUS = 6_371


MOON_RADIUS = 1_737.4


MOON_ORBIT_RADIUS = 384_400


def get_earth(radius=1.0, day_texture="EarthTextureMap", night_texture="NightEarthTextureMap"):
    sphere = Sphere(radius=radius)
    earth = TexturedSurface(sphere, day_texture, night_texture)
    return earth


def get_moon(radius=1.0, resolution=(101, 51)):
    moon = TexturedSurface(Sphere(radius=radius, resolution=resolution), "MoonTexture", "DarkMoonTexture")
    moon.set_shading(0.25, 0.25, 1)
    return moon


class LuarEclipse(InteractiveScene):
    def construct(self):
        # Setup earth and moon
        light = self.camera.light_source
        light.move_to(50 * LEFT)
        frame = self.frame
        frame.set_field_of_view(25 * DEG)

        conversion_factor = 1.0 / EARTH_RADIUS

        earth = get_earth(radius=EARTH_RADIUS * conversion_factor)
        earth.rotate(-EARTH_TILT_ANGLE, UP)
        earth_axis = rotate_vector(OUT, -EARTH_TILT_ANGLE, UP)

        earth.add_updater(lambda m, dt: m.rotate(dt * 10 * DEG, axis=earth_axis))

        self.add(earth)

        # Clearly show the size of the earth
        brace = Brace(earth, LEFT)
        label = brace.get_tex(Rf"2 R_E")
        re_label = Integer(2 * EARTH_RADIUS, unit=" km", font_size=36)
        re_label.next_to(label, DOWN, aligned_edge=RIGHT)
        dashed_lines = VGroup(
            DashedLine(brace.get_corner(UR), earth.get_top() + RIGHT, dash_length=0.03),
            DashedLine(brace.get_corner(DR), earth.get_bottom() + RIGHT, dash_length=0.03),
        )
        dashed_lines.set_stroke(GREY, 2)

        frame.reorient(-2, 59, 0, (-0.08, 0.07, -0.08), 2.76)
        self.play(
            frame.animate.to_default_state(),
            LaggedStart(
                Animation(Mobject(), remover=True),
                Animation(Mobject(), remover=True),
                Animation(Mobject(), remover=True),
                FadeIn(brace, scale=100),
                FadeIn(label),
                FadeIn(dashed_lines),
                lag_ratio=0.5,
            ),
            run_time=3
        )
        self.wait()
        self.play(FadeIn(re_label))
        self.wait()

        # Zoom out from earth to moon
        orbit = Circle(radius=MOON_ORBIT_RADIUS * conversion_factor)
        orbit.set_stroke(GREY_C, width=(0, 3))
        # orbit.rotate(-45 * DEG)
        orbit.rotate(-135 * DEG)
        orbit.add_updater(lambda m, dt: m.rotate(3 * dt * DEG))

        moon = get_moon(radius=MOON_RADIUS * conversion_factor)
        moon.to_edge(RIGHT)
        moon.add_updater(lambda m: m.move_to(orbit.get_start()))

        radial_line = Line()
        radial_line.set_stroke(WHITE, 0.5)
        radial_line.add_updater(lambda m: m.put_start_and_end_on(earth.get_center(), moon.get_center()))

        # dist_question = Text("Distance to the moon?", font_size=400)
        # dist_question.add_updater(lambda m: m.next_to(radial_line.get_center(), UR, buff=1))
        dist_question = TexText(R"Distance to the moon \\ $\approx$ 385,000km $\pm$ 21,000km", font_size=600)
        dist_question.add_updater(lambda m: m.next_to(radial_line.get_center(), DR, buff=1))

        trg_height = 1.2 * orbit.get_height()
        self.add(orbit, moon)
        self.play(
            frame.animate.set_height(trg_height),
            FadeIn(radial_line, time_span=(2, 3)),
            FadeIn(dist_question, time_span=(2, 3)),
            run_time=4,
        )
        self.wait(20)

        # Show earth's shadow
        sunlight = GlowDot(radius=3 * FRAME_WIDTH, glow_factor=1, opacity=0.5)
        sunlight.move_to(1.5 * FRAME_WIDTH * LEFT)
        sunlight.fix_in_frame()

        shadow = Rectangle(
            width=3 * MOON_ORBIT_RADIUS * conversion_factor,
            height=2 * EARTH_RADIUS * conversion_factor,
        )
        shadow.set_stroke(width=0)
        shadow.set_fill(BLACK, 1)
        shadow.move_to(ORIGIN, LEFT)

        sunlight.set_z_index(-1)
        shadow.set_z_index(-1)

        self.add(sunlight, shadow)
        self.play(GrowFromCenter(sunlight, run_time=3))
        self.wait()

        # Zoom in to the moon
        orbit.clear_updaters()

        self.play(
            Rotate(orbit, -angle_of_vector(orbit.get_start()) - 1.25 * DEG),
            frame.animate.set_height(6 * EARTH_RADIUS * conversion_factor).move_to(MOON_ORBIT_RADIUS * conversion_factor * RIGHT),
            FadeOut(radial_line, time_span=(0, 2)),
            FadeOut(dist_question, time_span=(0, 2)),
            sunlight.animate.set_opacity(0.35),
            run_time=5
        )

        # Show the moon passing through
        self.play(
            Rotate(orbit, 2.5 * DEG, about_point=ORIGIN),
            Rotate(moon, 2.5 * DEG, about_point=ORIGIN),
            run_time=12,
            rate_func=linear,
        )
        self.wait()

        # Show the width
        brace_copy = brace.copy().flip()
        brace_copy.next_to(orbit, RIGHT, LARGE_BUFF)
        label_copy = VGroup(label, re_label).copy()
        label_copy.arrange(DOWN, aligned_edge=LEFT)
        label_copy.next_to(brace_copy, RIGHT, SMALL_BUFF)

        self.play(
            GrowFromCenter(brace_copy),
            FadeIn(label_copy, lag_ratio=0.1)
        )
        self.wait()

        # Show the time
        time_label = Tex(R"~4 \text{ hours}", font_size=60)
        time_label.next_to(brace_copy, RIGHT)

        self.play(
            FadeOut(label_copy, lag_ratio=0.1),
            FadeIn(time_label, lag_ratio=0.1),
        )
        self.wait()

        # Show the full lunar month
        orbit_rate = ValueTracker(0)
        orbit.clear_updaters()
        orbit.add_updater(lambda m, dt: m.rotate(orbit_rate.get_value() * dt * DEG))

        large_text_height = 2 * earth.get_height()

        month_arrow = Arc(
            5 * DEG,
            350 * DEG,
            arc_center=2.0 * earth.get_right(),
            radius=0.9 * MOON_ORBIT_RADIUS * conversion_factor
        )
        month_arrow.set_stroke(TEAL, 3)
        month_arrow.add_tip()
        month_arrow.tip.set_height(4 * EARTH_RADIUS * conversion_factor, about_point=month_arrow.get_end())

        month_label = Text("28 days")
        month_label.set_height(2 * large_text_height)
        month_label.match_color(month_arrow)
        month_label.next_to(month_arrow.pfp(3 / 8), DR, buff=earth.get_height())

        self.play(
            frame.animate.move_to(MOON_ORBIT_RADIUS * conversion_factor * LEFT).set_height(1.35 * orbit.get_height()).set_anim_args(run_time=4),
            orbit_rate.animate.set_value(15).set_anim_args(run_time=4),
            time_label.animate.set_height(large_text_height, about_point=brace_copy.get_right()).set_anim_args(run_time=4),
            ShowCreation(month_arrow, time_span=(1, 5)),
            Write(month_label, time_span=(2, 3)),
        )
        self.wait(32)

    def show_circles(self):
        radii = [1e4, 1e5]
        circles = VGroup()
        for n, radius in enumerate(radii):
            circle = Circle(radius=radius * conversion_factor)
            circle.set_stroke(WHITE, 2)
            radial_line = Line(ORIGIN, circle.get_right())
            radial_line.set_stroke(GREY, 1)
            label = Integer(radius, unit=" km")
            label.set_width(0.25 * radial_line.get_width())
            label.move_to(radial_line.pfp(0.6), DOWN).shift(0.001 * radius * UP)
            group = VGroup(radial_line, label, circle)
            circles.add(group)

    def get_red_moon(self):
        red_moon = TexturedSurface(
            Sphere(radius=MOON_RADIUS * conversion_factor),
            "RedMoonTexture", "DarkMoonTexture",
        ).set_opacity(0.8)
        return red_moon
