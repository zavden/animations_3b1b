# ==============================================================================
# Scene:      SmoothSphere
# Source:     videos/_2018/sphere_area.py (lines 2208-2215)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SmoothSphere.py SmoothSphere -w -m --fps 15
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


class RectangulatedSphere(SphereCylinderScene):
    CONFIG = {
        "sphere_config": {
            "resolution": (10, 20)
        },
        "uniform_color": False,
        "wait_time": 10,
    }

    def construct(self):
        sphere = self.get_sphere()
        if self.uniform_color:
            sphere.set_stroke(BLUE_E, width=0.5)
            sphere.set_fill(BLUE_E)
        self.set_camera_to_default_position()
        self.begin_ambient_camera_rotation(0.05)
        self.add(sphere)
        self.wait(self.wait_time)


class SmoothSphere(RectangulatedSphere):
    CONFIG = {
        "sphere_config": {
            "resolution": (200, 400),
        },
        "uniform_color": True,
        "wait_time": 0,
    }
