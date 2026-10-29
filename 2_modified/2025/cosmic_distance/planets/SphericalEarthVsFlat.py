# ==============================================================================
# Scene:      SphericalEarthVsFlat
# Source:     videos/_2025/cosmic_distance/planets.py (lines 205-257)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl SphericalEarthVsFlat.py SphericalEarthVsFlat -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Removed the line flat_earth.data['d_normal_point'] = ...: that field no longer exists in this manimgl.
# ==============================================================================

from manim_imports_ext import *

EARTH_TILT_ANGLE = 23.3 * DEG


def get_earth(radius=1.0, day_texture="EarthTextureMap", night_texture="NightEarthTextureMap"):
    sphere = Sphere(radius=radius)
    earth = TexturedSurface(sphere, day_texture, night_texture)
    return earth


class SphericalEarthVsFlat(InteractiveScene):
    def construct(self):
        # Add earth
        light = self.camera.light_source
        light.move_to(50 * LEFT)
        frame = self.frame
        frame.set_field_of_view(25 * DEG)
        earth = get_earth(radius=3)
        earth.rotate(-EARTH_TILT_ANGLE, UP)
        earth_axis = rotate_vector(OUT, -EARTH_TILT_ANGLE, UP)
        self.add(earth)

        frame.reorient(160, 75, 0, (-0.53, -0.33, 1.91), 1.84)
        self.play(
            frame.animate.reorient(166, 63, 0, ORIGIN, FRAME_HEIGHT),
            run_time=2
        )
        self.wait()
        self.play(frame.animate.to_default_state(), run_time=2)
        self.wait()

        # Look around
        self.look_from_various_angles()

        # Squish
        day_earth = get_earth(radius=earth.get_height() / 2, night_texture="EarthTextureMap")
        flat_earth = day_earth.copy().set_depth(1e-2, stretch=True)
        # CHANGE: this manimgl no longer has the d_normal_point field (normals are computed in the shader from the mesh), so
        # forcing the flattened Earth's normal is no longer needed; the line is removed.
        self.play(FadeOut(earth, scale=0.99), FadeIn(day_earth, scale=0.99))
        self.play(
            Transform(day_earth, flat_earth),
            light.animate.set_z(10),
            run_time=2
        )

        # Ellipse
        circle = Circle(radius=3)
        circle.set_stroke(TEAL, 3)
        self.play(frame.animate.reorient(10, 80, 0), run_time=2)
        self.play(ShowCreation(circle))
        self.wait()

    def look_from_various_angles(self, run_time=1.5):
        frame = self.frame
        orientations = [
            (10, 80, 0),
            (-150, 129, 0),
            (97, 55, 0),
            (0, 0, 0)
        ]
        for orientation in orientations:
            self.play(frame.animate.reorient(*orientation), run_time=run_time)
            self.wait()
