# ==============================================================================
# Scene:      Transformation
# Source:     videos/_2024/linalg/eigenlecture.py (lines 321-370)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl Transformation.py Transformation -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class Transformation(InteractiveScene):
    def construct(self):
        # Apply matrix
        mat = np.array([[1, 2], [3, 1]])

        ghost_plane = NumberPlane(faded_line_ratio=0)
        ghost_plane.set_stroke(GREY, 1)
        plane = self.get_plane()
        basis = VGroup(
            self.get_updated_vector((1, 0), plane, GREEN),
            self.get_updated_vector((0, 1), plane, RED),
        )

        self.add(ghost_plane, plane, basis)
        self.play(
            plane.animate.apply_matrix(mat),
            run_time=4
        )
        self.wait()

        # Fade out
        self.play(FadeOut(VGroup(ghost_plane, plane, basis)))

        # Show matrix in new coordinate system
        eigenvalues, eigenvectors = np.linalg.eig(mat)
        eigenplane = self.get_plane()
        eigenplane.apply_matrix(eigenvectors, about_point=ORIGIN)

        eigenbasis = VGroup(
            self.get_updated_vector((1, 0), eigenplane, TEAL),
            self.get_updated_vector((0, 1), eigenplane, YELLOW),
        )

        self.add(eigenplane, eigenbasis)
        self.play(
            eigenplane.animate.apply_matrix(mat),
            run_time=4
        )
        self.wait()

    def get_plane(self, x_range=(-16, 16), y_range=(-8, 8)):
        return NumberPlane(x_range, y_range, faded_line_ratio=1)

    def get_updated_vector(self, coords, coord_system, color=YELLOW, thickness=4, **kwargs):
        vect = Vector(RIGHT, fill_color=color, thickness=thickness, **kwargs)
        vect.add_updater(lambda m: m.put_start_and_end_on(
            coord_system.get_origin(),
            coord_system.c2p(*coords),
        ))
        return vect
