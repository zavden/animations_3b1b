# ==============================================================================
# Scene:      RadarToVenus
# Source:     videos/_2025/cosmic_distance/planets.py (lines 3039-3087)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl RadarToVenus.py RadarToVenus -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder SunTexture texture (_lib/assets/raster_images/SunTexture.jpg); the original is private to Grant.
#   - Uses MoonTexture/DarkMoonTexture derived from MoonTextureMap.png (the originals are private to Grant).
#   - Uses a procedural starry sky instead of NASA's Hipparcos-Tycho map (hiptyc_2020_8k) and placeholder constellation figures.
#
# Placeholder assets (not Grant's originals):
#   - SunTexture.jpg (procedural solar surface with granulation and spots, 2:1 equirectangular map)
#   - MoonTexture.jpg and DarkMoonTexture.jpg (derived from the lib's real lunar map MoonTextureMap.png; the dark one is the same map dimmed)
#   - hiptyc_2020_8k.jpg (procedural 8192x4096 starry sky with a Milky Way band) and constellation_figures.png (constellation figures between bright stars)
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


def get_celestial_sphere(radius=1000, constellation_opacity=0.1):
    sphere = Group(
        TexturedSurface(Sphere(radius=radius, clockwise=True), "hiptyc_2020_8k"),
        TexturedSurface(Sphere(radius=0.99 * radius, clockwise=True), "constellation_figures"),
    )
    sphere.set_shading(0, 0, 0)
    sphere[1].set_opacity(constellation_opacity)

    sphere.rotate(EARTH_TILT_ANGLE, RIGHT)

    return sphere


def get_planet_symbols(text, font_size=48):
    return Tex(
        Rf"\{text}",
        additional_preamble=R"\usepackage{wasysym}",
        font_size=font_size,
    )


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


class RadarToVenus(LightFromEarthToMoon):
    def construct(self):
        # Add sun, stars, and orbits
        frame = self.frame
        conversion_factor = 7 / EARTH_ORBIT_RADIUS
        celestial_sphere = get_celestial_sphere(radius=100, constellation_opacity=0.05)

        sun = get_sun(radius=SUN_RADIUS * conversion_factor, big_glow_ratio=20)
        sun.center()

        colors = [TEAL, BLUE]
        radii = np.array([VENUS_ORBIT_RADIUS, EARTH_ORBIT_RADIUS]) * conversion_factor
        angles = [160 * DEG, 180 * DEG]
        orbits = VGroup(
            Circle(radius=radius).rotate(angle).set_stroke(color, (0, 5))
            for radius, color, angle in zip(radii, colors, angles)
        )
        glows = Group(
            GlowDot(orbit.get_start(), color=orbit.get_color())
            for orbit in orbits
        )
        symbols = VGroup(*map(get_planet_symbols, ["venus", "earth"]))
        for symbol, glow in zip(symbols, glows):
            symbol.scale(0.5)
            symbol.rotate(110 * DEG, LEFT)
            symbol.rotate(-54 * DEG, OUT)
            symbol.next_to(glow, IN, buff=0)

        frame.reorient(-51, 60, 0, (-2.11, 1.24, -2.0), 7.66)
        frame.add_ambient_rotation(-1 * DEG)
        self.add(celestial_sphere, sun, orbits, glows, symbols)

        # Show pulses
        venus_point = orbits[0].get_start()
        earth_point = orbits[1].get_start()

        for _ in range(4):
            pulse = self.get_pulse(
                velocity=0.15 * (venus_point - earth_point),
                radius=0.05,
                max_stroke_width=2,
                low_x=earth_point[0],
                high_x=venus_point[0],
                tail_time=0.5,
            )
            pulse.move_to(earth_point)
            self.add(pulse)
            self.wait(0.2)
        self.wait(20)
