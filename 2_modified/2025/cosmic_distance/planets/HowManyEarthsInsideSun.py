# ==============================================================================
# Scene:      HowManyEarthsInsideSun
# Source:     videos/_2025/cosmic_distance/planets.py (lines 1741-1788)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl HowManyEarthsInsideSun.py HowManyEarthsInsideSun -w -m --fps 15
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


class HowManyEarthsInsideSun(InteractiveScene):
    def construct(self):
        # Add earth and sun
        frame = self.frame
        frame.set_field_of_view(10 * DEG)

        earth_radius = 0.25
        earth = get_earth(radius=earth_radius)
        earth.move_to(0.25 * FRAME_WIDTH * LEFT)

        sun = get_sun(radius=7 * earth_radius)
        sun.move_to(0.25 * FRAME_WIDTH * RIGHT)

        self.add(earth)
        self.add(sun)

        # Show seven circles
        circle = Circle(radius=earth_radius)
        circle.move_to(earth)
        circle.set_stroke(BLUE, 5)

        stack = circle.get_grid(7, 1, buff=0)
        stack.move_to(sun)

        self.play(ShowCreation(circle))
        self.play(LaggedStart(
            (TransformFromCopy(circle, circle2)
            for circle2 in stack),
            lag_ratio=0.05,
        ))
        self.wait()

        # Show large sun
        big_sun = get_sun(radius=109 * earth_radius)
        big_sun.move_to(200 * earth_radius * RIGHT)

        big_stack = circle.get_grid(109, 1, buff=0)
        big_stack.move_to(big_sun[0])
        big_stack.set_stroke(width=1)

        self.play(
            Transform(sun, big_sun),
            frame.animate.reorient(0, 0, 0, (8.71, 0.01, 0.0), 89.70),
            circle.animate.set_stroke(width=1),
            # FadeOut(stack),
            Transform(stack, big_stack, lag_ratio=0.001),
            run_time=3
        )
