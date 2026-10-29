# ==============================================================================
# Scene:      SphereEquator
# Source:     videos/_2026/spheres_talk/volumes.py (lines 1353-1364)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SphereEquator.py SphereEquator -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SphereEquator(InteractiveScene):
    def construct(self):
        frame = self.frame
        radius = 3
        sphere = Sphere(radius=radius)
        equator = Circle(radius=radius)
        sphere.set_color(BLUE_E, 0.7)
        sphere.always_sort_to_camera(self.camera)
        equator.set_stroke(YELLOW, 3)
        equator.apply_depth_test()

        self.add(equator, sphere)
