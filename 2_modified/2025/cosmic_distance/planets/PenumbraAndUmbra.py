# ==============================================================================
# Scene:      PenumbraAndUmbra
# Source:     videos/_2025/cosmic_distance/planets.py (lines 867-960)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl PenumbraAndUmbra.py PenumbraAndUmbra -w -m --fps 15
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


class PenumbraAndUmbra(InteractiveScene):
    def construct(self):
        # Add earth and sun
        frame = self.frame
        frame.set_field_of_view(10 * DEG)
        light_source = self.camera.light_source

        sun = get_sun(radius=2, big_glow_ratio=10, big_glow_factor=2)
        sun.move_to(7 * LEFT)

        earth = get_earth(radius=0.7)
        earth.rotate(90 * DEG, LEFT).rotate(EARTH_TILT_ANGLE, OUT)
        earth.move_to(2 * RIGHT)

        light_source.move_to(sun)
        self.add(sun, earth)

        # Add shadows
        umbra, penumbra, umbral_lines, penumbral_lines = shadow_group = self.get_umbral_lines(sun[0], earth)

        umbrum_word = Text("Umbra", font_size=24)
        umbrum_word.move_to(umbra)
        penumbrum_word = Text("Penumbra", font_size=24)
        penumbrum_word.move_to(umbrum_word)
        penumbrum_word.shift(0.55 * earth.get_height() * UP)

        self.add(penumbra, penumbral_lines, earth, penumbrum_word)
        self.play(
            FadeIn(penumbra),
            FadeIn(penumbral_lines),
            FadeIn(penumbrum_word),
        )
        self.add(*shadow_group, earth, umbrum_word, penumbrum_word)
        self.play(
            FadeIn(umbral_lines, lag_ratio=0),
            FadeIn(umbra, time_span=(0.5, 1)),
            FadeIn(umbrum_word, time_span=(0.5, 1)),
        )
        self.wait()

        # Pull away
        self.add(shadow_group, earth, umbrum_word, penumbrum_word)

        shift_vect = 100 * LEFT
        self.play(
            sun[:2].animate.shift(shift_vect),
            sun[2].animate.shift(5 * LEFT).scale(2),
            frame.animate.reorient(0, 0, 0, (4.21, 0.56, 0.0), 13.04),
            umbrum_word.animate.shift(2 * RIGHT),
            penumbrum_word.animate.scale(0.5, about_edge=DOWN).shift(2 * RIGHT),
            UpdateFromFunc(shadow_group, lambda m: m.become(self.get_umbral_lines(sun[0], earth))),
            run_time=8,
        )

    def get_umbral_lines(self, circle1, circle2):
        r1 = circle1.get_width() / 2
        r2 = circle2.get_width() / 2
        c1 = circle1.get_center()
        c2 = circle2.get_center()

        vect = c2 - c1
        dist = get_norm(vect)

        cs1 = c1 + vect / (1.0 - r2 / r1)
        cs2 = c1 + vect / (1.0 + r2 / r1)

        angle = math.asin(r1 / get_norm(cs1 - c1))

        v1 = rotate_vector(UP, -angle)
        v2 = rotate_vector(DOWN, angle)
        v3 = rotate_vector(UP, angle)
        v4 = rotate_vector(DOWN, -angle)

        umbral_lines = VGroup(
            Line(c1 + r1 * v1, cs1),
            Line(c1 + r1 * v2, cs1),
        )
        umbral_lines.set_stroke(WHITE, 0.5)
        umbra = Polygon(cs1, c2 + r2 * v1, c2, c2 + r2 * v2)
        umbra.set_fill(BLACK, 1).set_stroke(width=0)

        penumbral_lines = VGroup(
            Line(cs2, c2 + r2 * v3).scale(10),
            Line(cs2, c2 + r2 * v4).scale(10),
        )
        penumbral_lines.set_stroke(WHITE, 0.5)
        penumbra = Polygon(
            c2 + r2 * v3, penumbral_lines[0].get_end(),
            penumbral_lines[1].get_end(), c2 + r2 * v4,
        )
        penumbra.set_fill(BLACK, 0.5)
        penumbra.set_stroke(width=0)

        return VGroup(umbra, penumbra, umbral_lines, penumbral_lines)
