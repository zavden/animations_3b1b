# ==============================================================================
# Scene:      MapSphereOntoCylinder
# Source:     videos/_2018/sphere_area.py (lines 373-469)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl MapSphereOntoCylinder.py MapSphereOntoCylinder -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Cylinder(Sphere):
    """
    Inherits from sphere so as to be as aligned as possible
    for transformations
    """

    def func(self, u, v):
        return np.array([
            np.cos(v),
            np.sin(v),
            np.cos(u)
        ])


class UnwrappedCylinder(Cylinder):
    def func(self, u, v):
        return np.array([
            v - PI,
            -self.radius,
            np.cos(u)
        ])


class SphereCylinderScene(SpecialThreeDScene):
    CONFIG = {
        "cap_config": {
            "stroke_width": 1,
            "stroke_color": WHITE,
            "fill_color": BLUE_D,
            "fill_opacity": 1,
        }
    }

    def get_cylinder(self, **kwargs):
        config = merge_dicts_recursively(self.sphere_config, kwargs)
        return Cylinder(**config)

    def get_cylinder_caps(self):
        R = self.sphere_config["radius"]
        caps = VGroup(*[
            Circle(
                radius=R,
                **self.cap_config,
            ).shift(R * vect)
            for vect in [IN, OUT]
        ])
        caps.set_shade_in_3d(True)
        return caps

    def get_unwrapped_cylinder(self):
        return UnwrappedCylinder(**self.sphere_config)

    def get_xy_plane(self):
        pass

    def get_ghost_surface(self, surface):
        result = surface.copy()
        result.set_fill(BLUE_E, opacity=0.5)
        result.set_stroke(WHITE, width=0.5, opacity=0.5)
        return result

    def project_point(self, point):
        radius = self.sphere_config["radius"]
        result = np.array(point)
        result[:2] = normalize(result[:2]) * radius
        return result

    def project_mobject(self, mobject):
        return mobject.apply_function(self.project_point)


class MapSphereOntoCylinder(SphereCylinderScene):
    def construct(self):
        sphere = self.get_sphere()
        sphere_ghost = self.get_ghost_surface(sphere)
        sphere_ghost.set_stroke(width=0)
        axes = self.get_axes()
        cylinder = self.get_cylinder()
        cylinder.set_fill(opacity=0.75)
        radius = cylinder.get_width() / 2

        self.add(axes, sphere_ghost, sphere)
        self.wait()
        self.begin_ambient_camera_rotation()
        self.move_camera(
            **self.default_angled_camera_position,
            run_time=2,
        )
        self.wait(2)
        self.play(
            ReplacementTransform(sphere, cylinder),
            run_time=3
        )
        self.wait(3)

        # Get rid of caps
        caps = self.get_cylinder_caps()
        caps[1].set_shade_in_3d(False)
        label = OldTexText("Label")
        label.scale(1.5)
        label.stretch(0.8, 0)
        label.rotate(90 * DEGREES, RIGHT)
        label.rotate(90 * DEGREES, OUT)
        label.shift(np.log(radius + SMALL_BUFF) * RIGHT)
        label.apply_complex_function(np.exp)
        label.rotate(90 * DEGREES, IN, about_point=ORIGIN)
        label.shift(OUT)
        label.set_background_stroke(width=0)

        self.play(FadeIn(caps))
        self.wait()
        self.play(
            caps.space_out_submobjects, 2,
            caps.fade, 1,
            remover=True
        )
        self.play(Write(label))
        self.wait(2)
        self.play(FadeOut(label))

        # Unwrap
        unwrapped_cylinder = self.get_unwrapped_cylinder()
        unwrapped_cylinder.set_fill(opacity=0.75)
        self.play(
            ReplacementTransform(cylinder, unwrapped_cylinder),
            run_time=3
        )
        self.stop_ambient_camera_rotation()
        self.move_camera(
            phi=90 * DEGREES,
            theta=-90 * DEGREES,
        )

        # Show dimensions
        stroke_width = 5
        top_line = Line(
            PI * radius * LEFT + radius * OUT,
            PI * radius * RIGHT + radius * OUT,
            color=YELLOW,
            stroke_width=stroke_width,
        )
        side_line = Line(
            PI * radius * LEFT + radius * OUT,
            PI * radius * LEFT + radius * IN,
            color=RED,
            stroke_width=stroke_width,
        )
        lines = VGroup(top_line, side_line)
        lines.shift(radius * DOWN)
        two_pi_R = OldTex("2\\pi R")
        two_R = OldTex("2R")
        texs = VGroup(two_pi_R, two_R)
        for tex in texs:
            tex.scale(1.5)
            tex.rotate(90 * DEGREES, RIGHT)
        two_pi_R.next_to(top_line, OUT)
        two_R.next_to(side_line, RIGHT)

        self.play(
            ShowCreation(top_line),
            FadeIn(two_pi_R, IN)
        )
        self.wait()
        self.play(
            ShowCreation(side_line),
            FadeIn(two_R, RIGHT)
        )
        self.wait()
