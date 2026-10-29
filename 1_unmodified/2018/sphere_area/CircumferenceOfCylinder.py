# ==============================================================================
# Scene:      CircumferenceOfCylinder
# Source:     videos/_2018/sphere_area.py (lines 472-499)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl CircumferenceOfCylinder.py CircumferenceOfCylinder -w -m --fps 15
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


class CircumferenceOfCylinder(SphereCylinderScene):
    def construct(self):
        sphere = self.get_sphere()
        sphere_ghost = self.get_ghost_surface(sphere)
        cylinder = self.get_cylinder()
        cylinder_ghost = self.get_ghost_surface(cylinder)
        cylinder_ghost.set_stroke(width=0)

        radius = self.sphere_config["radius"]
        circle = Circle(radius=radius)
        circle.set_stroke(YELLOW, 5)
        circle.shift(radius * OUT)

        height = Line(radius * IN, radius * OUT)
        height.shift(radius * LEFT)
        height.set_stroke(RED, 5)

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-95 * DEGREES,
        )
        self.begin_ambient_camera_rotation(0.01)
        self.add(sphere_ghost, cylinder_ghost)
        self.wait()
        self.play(ShowCreation(circle))
        self.wait(2)
        self.play(ShowCreation(height))
        self.wait(5)
