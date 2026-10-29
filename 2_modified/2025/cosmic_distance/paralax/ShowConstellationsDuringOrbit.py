# ==============================================================================
# Scene:      ShowConstellationsDuringOrbit
# Source:     videos/_2025/cosmic_distance/paralax.py (lines 160-161)
# Category:   2 · Renders with modifications
# Includes code copied from: _2025/cosmic_distance/planets.py
#
# Run from this folder:
#     manimgl ShowConstellationsDuringOrbit.py ShowConstellationsDuringOrbit -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses the placeholder SunTexture texture (_lib/assets/raster_images/SunTexture.jpg); the original is private to Grant.
#   - Uses a procedural starry sky instead of NASA's Hipparcos-Tycho map (hiptyc_2020_8k) and placeholder constellation figures.
#   - With the starry sky (show_celestial_sphere) n_stars goes from 0 to 1: an empty GlowDots makes this manimgl fail when animating its radii (zero-size array).
#
# Placeholder assets (not Grant's originals):
#   - SunTexture.jpg (procedural solar surface with granulation and spots, 2:1 equirectangular map)
#   - hiptyc_2020_8k.jpg (procedural 8192x4096 starry sky with a Milky Way band) and constellation_figures.png (constellation figures between bright stars)
#
# Notes:
#   The textures by name are copied to _lib/assets/raster_images/ (they are generated with _lib/assets/generated/2025/cosmic_distance/make_cosmic_distance_assets.py).
# ==============================================================================

from manim_imports_ext import *


# ----- From _2025/cosmic_distance/planets.py -----

EARTH_TILT_ANGLE = 23.3 * DEG


def get_earth(radius=1.0, day_texture="EarthTextureMap", night_texture="NightEarthTextureMap"):
    sphere = Sphere(radius=radius)
    earth = TexturedSurface(sphere, day_texture, night_texture)
    return earth


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



# ----- From _2025/cosmic_distance/paralax.py -----

class ParalxInSolarSystem(InteractiveScene):
    show_celestial_sphere = False

    def construct(self):
        # Add sun and earth
        frame = self.frame
        light_source = self.camera.light_source

        earth = get_earth(radius=0.01)
        earth.rotate(EARTH_TILT_ANGLE, UP)
        earth_axis = rotate_vector(OUT, EARTH_TILT_ANGLE, UP)
        sun = get_sun(radius=0.07, big_glow_ratio=10)

        orbit_radius = 5
        sun.move_to(ORIGIN)
        light_source.move_to(sun)

        orbit = Circle(radius=orbit_radius, n_components=100)
        orbit.set_stroke(BLUE, width=(0, 3))
        orbit.rotate(-30 * DEG)
        orbit.add_updater(lambda m, dt: m.rotate(10 * dt * DEG))
        orbit.set_stroke(flat=False)
        orbit.set_anti_alias_width(5)
        orbit.apply_depth_test()

        earth.add_updater(lambda m: m.move_to(orbit.get_end()))
        # earth.add_updater(lambda m, dt: m.rotate(2 * TAU * dt, axis=earth_axis))

        self.add(orbit, earth, sun)
        self.wait(3)

        # Add stars
        if self.show_celestial_sphere:
            # CHANGE: with 0 stars the GlowDots is empty and this manimgl fails when animating its radii
            # (get_radii().max() of an empty array); a single star (of almost no brightness) is left as a minimum.
            n_stars = 1
            celestial_sphere = get_celestial_sphere()
            self.add(celestial_sphere)
        else:
            n_stars = 3000
        points = np.random.uniform(-1, 1, (n_stars, 3))
        points = normalize_along_axis(points, 1)
        distances = np.random.uniform(10, 50, n_stars)
        radii = np.random.uniform(0, 0.2, n_stars)
        points = points * distances[:, np.newaxis]
        stars = GlowDots(points)
        stars.set_color(WHITE)
        stars.set_radii(radii)

        self.add(stars, orbit, earth)
        self.play(
            ShowCreation(stars),
            frame.animate.reorient(0, 71, 0, (2.29, -0.66, 0.52), 43.56),
            run_time=4,
        )
        self.wait(3)

        self.play(
            frame.animate.set_euler_angles(-10 * DEG, 86 * DEG, 0).set_height(0.25),
            # frame.animate.set_height(0.1),
            UpdateFromAlphaFunc(sun, lambda m, a: frame.move_to(interpolate(frame.get_center(), earth.get_center(), min(2 * a, 1)))),
            run_time=5
        )
        frame.clear_updaters()
        frame.add_updater(lambda m: m.move_to(earth))

        self.wait(30)

        # Zoom back out
        self.play(
            frame.animate.reorient(7, 74, 0, ORIGIN, 120),
            stars.animate.set_radii(2 * radii),
            run_time=3,
        )
        new_points = 1000 * normalize_along_axis(stars.get_points(), 1)
        self.play(
            stars.animate.set_points(new_points).set_radii(20 * radii),
            run_time=4,
        )
        self.play(
            frame.animate.reorient(-89, 74, 0),
            run_time=12
        )


class ShowConstellationsDuringOrbit(ParalxInSolarSystem):
    show_celestial_sphere = True
