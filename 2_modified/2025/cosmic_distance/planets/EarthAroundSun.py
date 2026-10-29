# ==============================================================================
# Scene:      EarthAroundSun
# Source:     videos/_2025/cosmic_distance/planets.py (lines 1791-1828)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl EarthAroundSun.py EarthAroundSun -w -m --fps 15
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


class EarthAroundSun(InteractiveScene):
    def construct(self):
        # Add earth and sun
        frame = self.frame
        frame.set_field_of_view(10 * DEG)
        frame.set_height(10)

        earth_radius = 0.1
        orbit_radius = 6.0

        earth = get_earth(radius=earth_radius)
        earth.move_to(3 * LEFT)

        sun = get_sun(radius=7 * earth_radius)
        sun.move_to(3 * RIGHT)

        # Orbits
        sun_orbit = TracingTail(sun, stroke_color=YELLOW, stroke_width=(0, 10), time_traced=5)
        earth_orbit = TracingTail(earth, stroke_color=BLUE, stroke_width=(0, 5), time_traced=5)

        self.add(sun_orbit, sun, earth_orbit, earth)
        self.wait(2)
        self.play(
            Rotate(sun, TAU, about_point=earth.get_center()),
            # ShowCreation(sun_orbit),
            frame.animate.move_to(earth).set_height(16).set_anim_args(time_span=(0, 4)),
            run_time=10
        )
        self.play(FadeOut(sun_orbit))
        self.wait()
        self.play(
            frame.animate.move_to(sun).set_anim_args(time_span=(0, 4)),
            Rotate(earth, TAU, about_point=sun.get_center()),
            run_time=10
        )
        self.wait(3)
        self.play(sun.animate.scale(109 / 7, about_edge=LEFT).move_to(10 * RIGHT), run_time=4)
        self.wait()
