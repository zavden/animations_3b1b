# ==============================================================================
# Scene:      ProjectionTheorem
# Source:     videos/_2025/cosmic_distance/supplements.py (lines 472-537)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ProjectionTheorem.py ProjectionTheorem -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class ProjectionTheorem(InteractiveScene):
    def construct(self):
        # Add plane
        frame = self.frame

        width = 10
        plane = Square3D(side_length=2 * width)
        plane.set_color(GREY_E, 0.5)
        grid = NumberPlane(
            (-width, width), (-width, width),
        )
        grid.axes.set_stroke(WHITE, 0.5, 0.5)
        grid.background_lines.set_stroke(WHITE, 1, 0.25)
        grid.faded_lines.set_stroke(WHITE, 0.25, 0.1)

        frame.reorient(-30, 70, 0, 1.5 * OUT, 8.00)
        frame.add_ambient_rotation(2 * DEG)
        self.add(plane, grid)

        # Add sphere
        sphere = Sphere()
        sphere.set_color(BLUE_E, 0.5)
        sphere.always_sort_to_camera(self.camera)
        mesh = SurfaceMesh(sphere)
        mesh.set_stroke(WHITE, 1, 0.25)
        mesh.set_anti_alias_width(0)

        sphere_group = Group(sphere, mesh)
        sphere_group.move_to(2 * OUT)

        self.add(sphere_group)

        # Show many projections
        for _ in range(10):
            projection = self.show_projection(sphere_group)
            self.play(
                Rotate(sphere_group, random.uniform(0, TAU), axis=normalize(np.random.random(3))),
                FadeOut(projection)
            )

    def show_projection(self, sphere):
        # Test
        projection = sphere.copy()
        projection.stretch(5e-2, 2)
        projection.set_z(1e-2)

        circle = Circle(radius=1)
        circle.set_stroke(TEAL, 2)

        z = sphere.get_z()
        v_lines = VGroup(
            Line(circle.pfp(a) + z * OUT, circle.pfp(a))
            for a in np.arange(0, 1, 1.0 / 12.0)
        )
        v_lines.set_stroke(WHITE, 1, 0.25)
        v_lines.apply_depth_test()

        self.play(
            TransformFromCopy(sphere, projection),
            *map(ShowCreationThenFadeOut, v_lines),
            run_time=1
        )
        self.add(circle)
        self.wait()
        self.remove(circle)
        return projection
