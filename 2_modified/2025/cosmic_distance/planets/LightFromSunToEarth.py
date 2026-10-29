# ==============================================================================
# Scene:      LightFromSunToEarth
# Source:     videos/_2025/cosmic_distance/planets.py (lines 2858-2914)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LightFromSunToEarth.py LightFromSunToEarth -w -m --fps 15
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


SUN_RADIUS = 695_700


MERCURY_ORBIT_RADIUS = 6.805e7


VENUS_ORBIT_RADIUS = 1.082e8


EARTH_ORBIT_RADIUS = 1.473e8


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


class LightFromSunToEarth(LightFromEarthToMoon):
    def construct(self):
        # Sun and earth
        self.frame.set_field_of_view(15 * DEG)

        conversion_factor = 12 / EARTH_ORBIT_RADIUS
        earth = get_earth(radius=conversion_factor * EARTH_RADIUS)
        earth.rotate(EARTH_TILT_ANGLE, axis=DOWN)

        sun = get_sun(radius=SUN_RADIUS * conversion_factor, big_glow_ratio=20)
        sun.move_to(6.5 * LEFT)
        earth.move_to(sun.get_center() + conversion_factor * EARTH_ORBIT_RADIUS * RIGHT)
        earth_glow = GlowDot(earth.get_center(), color=BLUE)

        colors = [GREY_C, TEAL, BLUE]
        radii = [MERCURY_ORBIT_RADIUS, VENUS_ORBIT_RADIUS, EARTH_ORBIT_RADIUS]
        orbits = VGroup(
            Circle(radius=radius * conversion_factor)
            for radius, color in zip(radii, colors)
        )
        glows = Group()
        np.random.seed(1)
        angles = [-7 * DEG, 8 * DEG, 0]
        for orbit, angle, color in zip(orbits, angles, colors):
            orbit.rotate(angle)
            orbit.move_to(sun)
            orbit.set_stroke(color, (0, 3))
            glow = GlowDot(color=orbit.get_color())
            glow.move_to(orbit.get_start())
            glows.add(glow)

        symbol_texs = [R"\sun", R"\mercury", R"\venus", R"\earth"]
        labels = Tex(
            "".join(symbol_texs),
            additional_preamble=R"\usepackage{wasysym}",
            font_size=40
        )
        labels[0].set_opacity(0)
        for label, body in zip(labels, [sun[0], *glows]):
            label.next_to(body.get_center(), UR, buff=0.15)

        self.camera.light_source.move_to(sun)

        self.add(sun, earth, glows, orbits, labels)

        # Add pulse
        pulse = self.get_pulse(
            SPEED_OF_LIGHT * conversion_factor * RIGHT,
            low_x=sun.get_x(RIGHT),
            high_x=earth.get_x(LEFT),
            tail_time=20,
            label_text="Light"
        )
        pulse.next_to(sun, RIGHT)

        self.add(pulse)
        self.wait(40)
