# ==============================================================================
# Scene:      EarthAndVenus
# Source:     videos/_2025/cosmic_distance/planets.py (lines 2980-3036)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl EarthAndVenus.py EarthAndVenus -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder SunTexture texture (_lib/assets/raster_images/SunTexture.jpg); the original is private to Grant.
#   - Uses a procedural starry sky instead of NASA's Hipparcos-Tycho map (hiptyc_2020_8k) and placeholder constellation figures.
#
# Placeholder assets (not Grant's originals):
#   - SunTexture.jpg (procedural solar surface with granulation and spots, 2:1 equirectangular map)
#   - hiptyc_2020_8k.jpg (procedural 8192x4096 starry sky with a Milky Way band) and constellation_figures.png (constellation figures between bright stars)
#
# Notes:
#   The textures by name are copied to _lib/assets/raster_images/ (they are generated with _lib/assets/generated/2025/cosmic_distance/make_cosmic_distance_assets.py).
# ==============================================================================

from manim_imports_ext import *

EARTH_TILT_ANGLE = 23.3 * DEG


SUN_RADIUS = 695_700


VENUS_ORBIT_RADIUS = 1.082e8


EARTH_ORBIT_RADIUS = 1.473e8


VENUS_ORBIT_PERIOD = 224.7


EARTH_ORBIT_PERIOD = 365.25


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


class EarthAndVenus(InteractiveScene):
    def construct(self):
        # Add sun, stars, and orbits (copied from below)
        frame = self.frame
        conversion_factor = 3.5 / EARTH_ORBIT_RADIUS
        celestial_sphere = get_celestial_sphere(radius=100, constellation_opacity=0.05)

        sun = get_sun(radius=SUN_RADIUS * conversion_factor, big_glow_ratio=20)
        sun.center()

        colors = [TEAL, BLUE]
        radii = np.array([VENUS_ORBIT_RADIUS, EARTH_ORBIT_RADIUS]) * conversion_factor
        orbits = VGroup(
            Circle(radius=radius).set_stroke(color, (0, 5))
            for radius, color in zip(radii, colors)
        )
        glows = Group(GlowDot(color=orbit.get_color()) for orbit in orbits)
        symbols = VGroup(*map(get_planet_symbols, ["venus", "earth"]))

        for symbol, glow, orbit in zip(symbols, glows, orbits):
            orbit.rotate(PI)
            glow.f_always.move_to(orbit.get_start)
            symbol.scale(0.5)
            symbol.glow = glow
            # symbol.add_updater(lambda m: m.move_to(1.075 * m.glow.get_center()))
            symbol.always.next_to(glow, UL, buff=-SMALL_BUFF)

        self.add(celestial_sphere, sun, orbits, glows, symbols)

        # Add line
        venus, earth = glows
        angles = [(180 / period) * TAU for period in [VENUS_ORBIT_PERIOD, EARTH_ORBIT_PERIOD]]
        for orbit, angle in zip(orbits, angles):
            orbit.rotate(-angle)

        line_of_sight = Line()
        line_of_sight.set_stroke(WHITE, 1)
        line_of_sight.f_always.put_start_and_end_on(earth.get_center, venus.get_center)
        line_of_sight.add_updater(lambda m: m.scale(5, about_point=m.get_start())),

        self.play(
            *(Rotate(orbit, angle) for orbit, angle in zip(orbits, angles)),
            VFadeIn(line_of_sight, time_span=(8, 10)),
            run_time=20,
            # rate_func=lambda t: 0.999 * bezier([0, 1, 1])(t),
            rate_func=lambda t: 0.999 * t,
        )
        line_of_sight.clear_updaters()
        self.play(
            frame.animate.reorient(-89, 82, 0, (-0.0, 0.01, -0.01), 0.49),
            run_time=5,
        )
        self.play(
            line_of_sight.animate.rotate(-0.6 * DEG, about_point=earth.get_center()),
            run_time=6,
        )
        self.wait()
