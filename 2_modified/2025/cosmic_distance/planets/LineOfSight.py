# ==============================================================================
# Scene:      LineOfSight
# Source:     videos/_2025/cosmic_distance/planets.py (lines 963-1120)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl LineOfSight.py LineOfSight -w -m --fps 15
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


class LineOfSight(InteractiveScene):
    def construct(self):
        # Add earth
        light = self.camera.light_source
        light.move_to(20 * RIGHT)
        frame = self.frame
        frame.set_field_of_view(25 * DEG)

        conversion_factor = 1 / EARTH_RADIUS

        earth = get_earth(radius=EARTH_RADIUS * conversion_factor)
        earth.rotate(90 * DEG)
        earth.rotate(-EARTH_TILT_ANGLE, UP)
        earth_axis = rotate_vector(OUT, -EARTH_TILT_ANGLE, UP)

        frame.set_height(2.25)
        self.add(earth)

        # Add moon
        orbit = Circle(radius=MOON_ORBIT_RADIUS * conversion_factor)
        orbit.set_stroke(GREY_C, width=(0, 3))
        orbit.rotate(PI)

        moon = get_moon(radius=MOON_RADIUS * conversion_factor)
        moon.rotate(PI)
        moon.move_to(orbit.get_start())

        self.add(orbit, moon)

        # Show a line of sight
        line = Line(earth.get_center() + 0.75 * UP, moon.get_center())
        line.set_stroke(BLUE, 1)

        words = Text("Line of sight")
        words.set_width(line.get_width() * 0.5)
        words.set_color(BLUE)
        words.next_to(line, UP, buff=-0.5 * earth.get_height())

        angle = (MOON_RADIUS / (TAU * MOON_ORBIT_RADIUS)) * TAU
        line.rotate(angle, about_point=line.get_start())

        self.play(
            frame.animate.set_height(MOON_ORBIT_RADIUS * conversion_factor * 2.25),
            ShowCreation(line),
            FadeIn(words, lag_ratio=0.1, time_span=(2, 4)),
            run_time=5
        )

        # Zoom into the moon
        self.play(
            frame.animate.reorient(0, 0, 0, (-59.4, 0.01, 0.0), 2.83),
            line.animate.set_stroke(width=2),
            run_time=3
        )
        self.play(
            Rotate(line, -2 * angle, about_point=line.get_start()),
            run_time=2,
        )
        self.wait()
        self.play(
            frame.animate.set_height(MOON_ORBIT_RADIUS * conversion_factor * 2.25).center(),
            line.animate.set_stroke(width=1),
            run_time=3
        )

        # Rotate over 24 hours
        timer = DecimalNumber(0.0, num_decimal_places=1, edge_to_fix=RIGHT)
        units = Text("hours")
        timer[-1].shift(SMALL_BUFF * RIGHT)
        timer.fix_in_frame()
        timer.move_to(UR)
        timer.add_updater(lambda m: m.set_stroke(width=0).set_fill(border_width=0))
        units.next_to(timer, RIGHT, buff=0.2, aligned_edge=DOWN)
        units.fix_in_frame()
        units.set_stroke(width=0).set_fill(border_width=0)
        self.play(
            VFadeIn(timer, time_span=(0, 1)),
            VFadeIn(units, time_span=(0, 1)),
            ChangeDecimalToValue(timer, 24),
            Rotate(earth, -TAU, about_point=ORIGIN),
            Rotate(line, -TAU, about_point=ORIGIN),
            Rotate(words, -TAU, about_point=ORIGIN),
            Rotate(moon, TAU / 28, about_point=ORIGIN),
            Rotate(orbit, TAU / 28, about_point=ORIGIN),
            run_time=5
        )
        self.wait()

        self.play(*map(FadeOut, [timer, units, words, line]))

        # Ambient rotation
        self.play(
            Rotate(orbit, 90 * DEG, about_point=ORIGIN, rate_func=linear),
            Rotate(moon, 90 * DEG, about_point=ORIGIN, rate_func=linear),
            run_time=12
        )

        # Show elliptical orbit
        moon.f_always.move_to(orbit.get_end)

        orbit_ghost = orbit.copy().set_stroke(opacity=0.5)

        self.add(orbit_ghost)
        self.play(
            orbit.animate.stretch(0.9, 1).stretch(1.1, 0).shift(3 * earth.get_width() * LEFT),
            rate_func=there_and_back,
            run_time=5
        )

        # Zoom in then out
        self.play(
            frame.animate.reorient(80, 82, 0, moon.get_center(), 0.80),
            run_time=5
        )
        self.wait()
        self.play(
            frame.animate.reorient(0, 0, 0, ORIGIN, MOON_ORBIT_RADIUS * conversion_factor * 2.25),
            run_time=5
        )
        self.wait()

        # Show many moons
        ratio = int(2 * PI * MOON_ORBIT_RADIUS / MOON_RADIUS / 2)
        moons = Group()
        for a in np.arange(0, 1, 1 / ratio):
            lil_moon = get_moon(resolution=(21, 11))
            lil_moon.match_height(moon)
            lil_moon.move_to(orbit.pfp(a))
            moons.add(lil_moon)

        self.play(
            FadeOut(orbit, run_time=3),
            FadeIn(moons, lag_ratio=0.05, run_time=5),
        )
        self.wait()

        # Shrink down its orbit
        n_moons = 32
        small_orbit = orbit.copy()
        small_orbit.set_height(4.5 * n_moons * MOON_RADIUS * conversion_factor / TAU)
        small_orbit.set_stroke(WHITE, 1)

        inner_moons = Group()
        for a in np.arange(0, 1, 1.0 / n_moons):
            lil_moon = get_moon(resolution=(51, 25))
            lil_moon.match_height(moon)
            lil_moon.move_to(small_orbit.pfp(a))
            lil_moon.save_state()
            lil_moon.move_to(orbit.pfp(a))
            inner_moons.add(lil_moon)

        self.remove(moon)
        self.play(
            LaggedStartMap(Restore, inner_moons, lag_ratio=0),
            FadeOut(moons),
            frame.animate.set_height(1.5 * small_orbit.get_height()).center().set_anim_args(time_span=(1, 5)),
            run_time=5
        )
