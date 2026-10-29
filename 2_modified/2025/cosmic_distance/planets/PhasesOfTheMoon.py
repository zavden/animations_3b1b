# ==============================================================================
# Scene:      PhasesOfTheMoon
# Source:     videos/_2025/cosmic_distance/planets.py (lines 1704-1738)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PhasesOfTheMoon.py PhasesOfTheMoon -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Uses MoonTexture/DarkMoonTexture derived from MoonTextureMap.png (the originals are private to Grant).
#
# Placeholder assets (not Grant's originals):
#   - MoonTexture.jpg and DarkMoonTexture.jpg (derived from the lib's real lunar map MoonTextureMap.png; the dark one is the same map dimmed)
#
# Notes:
#   The textures by name are copied to _lib/assets/raster_images/ (they are generated with _lib/assets/generated/2025/cosmic_distance/make_cosmic_distance_assets.py).
# ==============================================================================

from manim_imports_ext import *

def get_moon(radius=1.0, resolution=(101, 51)):
    moon = TexturedSurface(Sphere(radius=radius, resolution=resolution), "MoonTexture", "DarkMoonTexture")
    moon.set_shading(0.25, 0.25, 1)
    return moon


class PhasesOfTheMoon(InteractiveScene):
    def construct(self):
        # Position ourselves
        moon = get_moon(radius=2)
        moon.set_shading(0, 0, 2)

        frame = self.frame
        frame.set_field_of_view(10 * DEG)
        light_source = self.camera.light_source
        light_source.move_to(10 * LEFT)

        self.add(moon)

        frame.reorient(-90, 90, 0)

        theta_tracker = ValueTracker(0)
        dist_to_earth = 20 * moon.get_width()
        earth_point = 10 * moon.get_width() * LEFT

        def get_sun_location():
            theta = theta_tracker.get_value()
            return earth_point + 2 * dist_to_earth * rotate_vector(RIGHT, -theta)

        light_source.f_always.move_to(get_sun_location)

        dot = GlowDot()
        dot.set_radius(5)
        dot.always.move_to(light_source)

        self.add(moon, light_source)
        self.play(
            theta_tracker.animate.set_value(TAU),
            run_time=10,
            rate_func=linear
        )
