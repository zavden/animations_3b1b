# ==============================================================================
# Scene:      SurfaceAreaToVolume
# Source:     videos/_2026/spheres_talk/volumes.py (lines 77-110)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SurfaceAreaToVolume.py SurfaceAreaToVolume -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SurfaceAreaToVolume(InteractiveScene):
    def construct(self):
        # Test
        frame = self.frame
        radius = 3
        sphere = Sphere(radius=radius)
        sphere.set_color(BLUE, 0.5)
        sphere.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(sphere, resolution=(51, 26))
        mesh.set_stroke(WHITE, 2, 0.2)

        frame.reorient(44, 56, 0)
        self.play(
            ShowCreation(sphere),
            Write(mesh),
            run_time=2
        )
        self.wait()

        # Inner spheres
        inner_spheres = Group(
            sphere.copy().set_width(a * sphere.get_width())
            for a in np.linspace(0, 1, 30)
        )
        inner_spheres.set_color(BLUE, 0.05)
        # inner_spheres.set_clip_plane(IN, 0)

        self.remove(sphere)
        self.add(inner_spheres, mesh)
        self.play(
            ShowCreation(inner_spheres, lag_ratio=0.1, run_time=20),
        )
        self.play(inner_spheres.animate.set_clip_plane(IN, radius), run_time=2)
        self.wait()
