# ==============================================================================
# Scene:      Spheres
# Source:     videos/outside_videos/aeoud.py (lines 91-114)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Spheres.py Spheres -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Spheres(InteractiveScene):
    def construct(self):
        # Add spheres
        radius = 2.5
        s1, s2 = spheres = Sphere(radius=radius).replicate(2)
        s1.shift(radius * LEFT / 2)
        s2.shift(radius * RIGHT / 2)
        spheres.set_opacity(0.35)
        spheres.set_color(BLUE)
        meshes = VGroup()
        for sphere in spheres:
            sphere.always_sort_to_camera(self.camera)
            meshes.add(SurfaceMesh(sphere))
        meshes.set_stroke(width=1, opacity=0.25)

        cap = Sphere(v_range=(0, PI / 3), radius=radius)
        cap.rotate(90 * DEGREES, axis=UP, about_point=ORIGIN)
        cap.shift(s2.get_center())
        cap.set_color(YELLOW)
        cap.set_opacity(0.8)
        cap.always_sort_to_camera(self.camera)

        self.camera.frame.reorient(-20, 60)
        self.add(cap, spheres, meshes)
