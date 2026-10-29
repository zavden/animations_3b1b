# ==============================================================================
# Scene:      UniSphereAndSquare
# Source:     videos/_2026/spheres_talk/volumes.py (lines 1403-1421)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl UniSphereAndSquare.py UniSphereAndSquare -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class UniSphereAndSquare(InteractiveScene):
    def construct(self):
        radius = 2
        sphere = Sphere(radius=radius)
        sphere.set_color(BLUE, 0.2)
        sphere.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(sphere, resolution=(51, 26))
        mesh.set_stroke(WHITE, 1, 0.25)
        cube = VCube(side_length=radius)
        cube.move_to(ORIGIN, DL + IN)
        cube.set_color(RED, 0.25)
        cube.set_stroke(RED, 3)
        cube.deactivate_depth_test()
        one_label = Integer(1)
        one_label.rotate(90 * DEG, RIGHT)
        one_label.next_to(RIGHT, OUT, SMALL_BUFF)

        self.frame.reorient(25, 65, 0, (0.22, 0.13, 0.09), 4.66)
        self.add(sphere, mesh, cube, one_label)
