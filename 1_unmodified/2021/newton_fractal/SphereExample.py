# ==============================================================================
# Scene:      SphereExample
# Source:     videos/_2021/newton_fractal.py (lines 387-455)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SphereExample.py SphereExample -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SphereExample(Scene):
    def construct(self):
        # Shape
        axes = ThreeDAxes(z_range=(-4, 4))
        axes.shift(IN)
        sphere = Sphere(radius=1.0)
        # sphere = TexturedSurface(sphere, "EarthTextureMap", "NightEarthTextureMap")
        sphere.move_to(axes.c2p(0, 0, 0))
        sphere.set_gloss(1.0)
        sphere.set_opacity(0.5)
        sphere.set_sort_to_camera()
        mesh = SurfaceMesh(sphere, resolution=(21, 11))
        mesh.set_stroke(BLUE, 0.5, 0.5)
        sphere = Group(sphere, mesh)

        frame = self.camera.frame
        frame.reorient(20, 80)
        frame.move_to(2 * RIGHT)
        light = self.camera.light_source

        self.add(axes)
        self.add(sphere)

        frame.add_updater(
            lambda m, dt: m.increment_theta(1 * dt * DEGREES)
        )

        # Expression
        equation = OldTex(
            "1.00", "\\,x^2", "+",
            "1.00", "\\,y^2", "+",
            "1.00", "\\,z^2", "=",
            "1.00",
        )
        decimals = VGroup()
        for i in range(0, len(equation), 3):
            decimal = DecimalNumber(1.0, edge_to_fix=RIGHT)
            decimal.replace(equation[i])
            equation.replace_submobject(i, decimal)
            decimals.add(decimal)
            decimal.add_updater(lambda m: m.fix_in_frame())
        equation.fix_in_frame()
        equation.to_corner(UR)
        self.add(equation)

        # Animations
        light.move_to([-10, -10, 20])
        self.wait()
        self.play(
            ChangeDecimalToValue(decimals[3], 9.0),
            VFadeInThenOut(SurroundingRectangle(decimals[3]).fix_in_frame()),
            sphere.animate.scale(3),
            run_time=3
        )
        self.wait()
        self.play(
            ChangeDecimalToValue(decimals[2], 4.0),
            VFadeInThenOut(SurroundingRectangle(decimals[2]).fix_in_frame()),
            sphere.animate.stretch(0.5, 2),
            run_time=3
        )
        self.wait()
        self.play(
            ChangeDecimalToValue(decimals[0], 9.0),
            VFadeInThenOut(SurroundingRectangle(decimals[0]).fix_in_frame()),
            sphere.animate.stretch(1 / 3, 0),
            run_time=3
        )
        self.wait(10)
