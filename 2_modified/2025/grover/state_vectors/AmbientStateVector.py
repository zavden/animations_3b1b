# ==============================================================================
# Scene:      AmbientStateVector
# Source:     videos/_2025/grover/state_vectors.py (lines 422-479)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl AmbientStateVector.py AmbientStateVector -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - `frame` was not defined (NameError): frame = self.frame is added at the start of construct.
# ==============================================================================

from manim_imports_ext import *

class AmbientStateVector(InteractiveScene):
    moving = False

    def construct(self):
        # CHANGE: `frame` was not defined (NameError); it is taken from self.frame
        frame = self.frame
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
