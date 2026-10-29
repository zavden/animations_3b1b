# ==============================================================================
# Scene:      FlipsToCertainDirection
# Source:     videos/_2025/grover/state_vectors.py (lines 486-524)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl FlipsToCertainDirection.py FlipsToCertainDirection -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class AmbientStateVector(InteractiveScene):
    moving = False

    def construct(self):
        plane, axes = self.get_plane_and_axes()

        frame.reorient(14, 76, 0)
        frame.add_ambient_rotation(3 * DEG)
        self.add(plane, axes)

        # Vector
        vector = Vector(2 * normalize([1, 1, 2]), thickness=5)
        vector.set_fill(border_width=2)
        vector.set_color(TEAL)
        vector.always.set_perpendicular_to_camera(frame)

        self.play(GrowArrow(vector))

        if not self.moving:
            self.wait(36)
        else:
            for n in range(16):
                axis = normalize(np.random.uniform(-1, 1, 3))
                angle = np.random.uniform(0, PI)
                self.play(Rotate(vector, angle, axis=axis, about_point=ORIGIN))
                self.wait()

        # Show the sphere
        frame.reorient(16, 77, 0)

        sphere = Sphere(radius=2)
        sphere.always_sort_to_camera(self.camera)
        sphere.set_color(BLUE, 0.25)
        sphere_mesh = SurfaceMesh(sphere, resolution=(41, 21))
        sphere_mesh.set_stroke(WHITE, 0.5, 0.5)

        self.play(
            ShowCreation(sphere),
            Write(sphere_mesh, lag_ratio=1e-3),
        )
        self.wait(10)

    def get_plane_and_axes(self, scale_factor=2.0):
        # Add axes
        frame = self.frame
        axes = ThreeDAxes((-1, 1), (-1, 1), (-1, 1))
        plane = NumberPlane(
            (-1, 1 - 1e-5),
            (-1, 1 - 1e-5),
            faded_line_ratio=5
        )
        plane.background_lines.set_stroke(opacity=0.5)
        plane.faded_lines.set_stroke(opacity=0.25)
        plane.axes.set_stroke(opacity=0.25)
        result = VGroup(plane, axes)
        result.scale(scale_factor)

        return result


class FlipsToCertainDirection(AmbientStateVector):
    def construct(self):
        # Test
        frame = self.frame
        plane, axes = axes_group = self.get_plane_and_axes(scale_factor=3)

        vector = Vector(axes.c2p(1, 0, 0), fill_color=TEAL, thickness=5)
        vector.always.set_perpendicular_to_camera(frame)

        frame.reorient(-31, 72, 0)
        frame.add_ambient_rotation(DEG)
        self.add(frame)
        self.add(plane, axes)
        self.add(vector)

        # Show some flips
        theta = 15 * DEG
        h_plane = Square3D()
        h_plane.replace(plane)
        h_plane.set_color(WHITE, 0.15)
        diag_plane = h_plane.copy().rotate(theta, axis=DOWN)
        ghosts = VGroup()

        for n in range(1, 14):
            axis = [UP, DOWN][n % 2]
            shown_plane = [h_plane, diag_plane][n % 2]
            if n == 1:
                shown_plane = VectorizedPoint()
            ghosts.add(vector.copy())
            ghosts.generate_target()
            for n, vect in enumerate(ghosts.target[::-1]):
                vect.set_opacity(0.5 / (n + 1))
            self.play(
                MoveToTarget(ghosts),
                Rotate(vector, n * theta, axis=axis, about_point=ORIGIN),
            )
            shown_plane.set_opacity(0.15)

        self.wait(6)
