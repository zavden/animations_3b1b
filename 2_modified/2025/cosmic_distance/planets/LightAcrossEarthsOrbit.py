# ==============================================================================
# Scene:      LightAcrossEarthsOrbit
# Source:     videos/_2025/cosmic_distance/planets.py (lines 2949-2977)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LightAcrossEarthsOrbit.py LightAcrossEarthsOrbit -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder SunTexture texture (_lib/assets/raster_images/SunTexture.jpg); the original is private to Grant.
#   - Uses MoonTexture/DarkMoonTexture derived from MoonTextureMap.png (the originals are private to Grant).
#
# Placeholder assets (not Grant's originals):
#   - SunTexture.jpg (procedural solar surface with granulation and spots, 2:1 equirectangular map)
#   - MoonTexture.jpg and DarkMoonTexture.jpg (derived from the lib's real lunar map MoonTextureMap.png; the dark one is the same map dimmed)
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


# In km / s
SPEED_OF_LIGHT = 299792


def get_earth(radius=1.0, day_texture="EarthTextureMap", night_texture="NightEarthTextureMap"):
    sphere = Sphere(radius=radius)
    earth = TexturedSurface(sphere, day_texture, night_texture)
    return earth


def get_moon(radius=1.0, resolution=(101, 51)):
    moon = TexturedSurface(Sphere(radius=radius, resolution=resolution), "MoonTexture", "DarkMoonTexture")
    moon.set_shading(0.25, 0.25, 1)
    return moon


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


class LightFromEarthToMoon(InteractiveScene):
    def construct(self):
        # Earth and moon
        self.camera.light_source.move_to(20 * LEFT)
        self.frame.set_field_of_view(15 * DEG)

        conversion_factor = 12 / MOON_ORBIT_RADIUS
        earth = get_earth(radius=conversion_factor * EARTH_RADIUS)
        earth.rotate(EARTH_TILT_ANGLE, axis=DOWN)
        moon = get_moon(radius=conversion_factor * MOON_RADIUS)
        earth.to_edge(LEFT, buff=0.75)
        moon.move_to(earth.get_center() + conversion_factor * MOON_ORBIT_RADIUS * RIGHT)

        labels = VGroup(Text("Earth"), Text("Moon"))
        for label, body in zip(labels, [earth, moon]):
            label.scale(0.75).next_to(body, UP, buff=0.25)

        self.add(earth, moon)
        self.add(labels)

        # Light beam
        low_x = earth.get_x(RIGHT)
        high_x = moon.get_left()[0] - 0.1
        pulse = self.get_pulse(SPEED_OF_LIGHT * conversion_factor * LEFT, low_x, high_x)
        pulse.next_to(moon, LEFT, buff=0)

        self.add(pulse)
        self.wait(20)

    def get_pulse(
        self,
        velocity,
        low_x=-np.inf,
        high_x=np.inf,
        radius=0.2,
        max_stroke_width=6,
        tail_time=0.25,
        label_text=""
    ):
        pulse = GlowDot(radius=radius).set_color(WHITE)

        pulse.velocities = np.zeros_like(pulse.get_points())
        pulse.velocities[:] = velocity

        def update_pulse(pulse, dt):
            points = pulse.get_points()
            new_points = points.copy()
            too_low = points[:, 0] < low_x
            too_high = points[:, 0] > high_x

            new_points[too_low][:, 0] = low_x
            new_points[too_high][:, 0] = high_x

            pulse.velocities[too_low] *= -1
            pulse.velocities[too_high] *= -1
            new_points += pulse.velocities * dt
            pulse.set_points(new_points)

        pulse.add_updater(update_pulse)
        tail = TracingTail(pulse, stroke_width=(0, max_stroke_width), time_traced=tail_time)

        result = Group(pulse, tail)

        if label_text:
            label = Text(label_text, font_size=24)
            label.always.next_to(pulse, DOWN, buff=0)
            result.add(label)

        return result


class LightAcrossEarthsOrbit(LightFromEarthToMoon):
    def construct(self):
        # Add orbit
        orbit = Circle(radius=3)
        orbit.set_stroke(BLUE, width=(0, 3))
        orbit.rotate(190 * DEG)

        sun = get_sun(radius=0.05, big_glow_ratio=20)
        sun.center()

        self.add(sun, orbit)

        # Show light
        pulse = self.get_pulse(velocity=0.25 * LEFT, tail_time=5)
        pulse.next_to(orbit.get_right(), RIGHT, buff=LARGE_BUFF)
        pulse.match_y(orbit.get_start())
        label = Text("Light from Io", font_size=24)
        label.always.next_to(pulse, DOWN, buff=-0.05)

        self.add(pulse)
        self.wait(4)
        self.play(FadeIn(label))
        self.wait(20)

    def get_light_pulse(self, width=2, n_points=25, dropoff=2):
        pulse = GlowDots(np.linspace(ORIGIN, width * RIGHT, n_points), radius=0.1)
        pulse.set_opacity(np.linspace(1, 0, pulse.get_num_points())**dropoff)
        pulse.set_color(WHITE)
        return pulse
