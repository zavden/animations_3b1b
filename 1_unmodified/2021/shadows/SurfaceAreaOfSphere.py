# ==============================================================================
# Scene:      SurfaceAreaOfSphere
# Source:     videos/_2021/shadows.py (lines 3962-3989)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SurfaceAreaOfSphere.py SurfaceAreaOfSphere -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class SurfaceAreaOfSphere(Scene):
    def construct(self):
        sphere = Sphere(radius=3)
        sphere.set_color(BLUE_E, 1)
        sphere.always_sort_to_camera(self.camera)
        sphere.rotate(5 * DEGREES, OUT)
        sphere.rotate(80 * DEGREES, LEFT)
        sphere.move_to(0.5 * DOWN)

        sphere_mesh = SurfaceMesh(sphere)
        sphere_mesh.set_stroke(WHITE, 0.5, 0.5)

        equation = OldTex(
            "\\text{Surface area} = 4\\pi R^2",
            tex_to_color_map={
                "R": YELLOW,
                "\\text{Surface area}": BLUE,
            },
        )
        equation.to_edge(UP)

        self.add(equation, sphere, sphere_mesh)
        self.play(
            Write(sphere_mesh, lag_ratio=0.02, stroke_width=1),
            ShowCreation(sphere, rate_func=squish_rate_func(smooth, 0.25, 1)),
            run_time=5,
        )
        self.wait()
