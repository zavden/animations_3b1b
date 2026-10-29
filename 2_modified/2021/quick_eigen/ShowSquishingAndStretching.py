# ==============================================================================
# Scene:      ShowSquishingAndStretching
# Source:     videos/_2021/quick_eigen.py (lines 1044-1111)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ShowSquishingAndStretching.py ShowSquishingAndStretching -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - NumberPlane requires stroke_color in background_line_style (before, it took the default color)
#   - np.linalg.eig returns a complex array (ComplexWarning); the real part is taken. With numpy 2.5 it gives v1=(0.82, 0.58), v2=(-0.82, 0.58)
# ==============================================================================

from manim_imports_ext import *

EIGEN_COLORS = [TEAL_A, TEAL_D]


class ShowSquishingAndStretching(Scene):
    def construct(self):
        self.camera.frame.set_height((3 / 4) * FRAME_HEIGHT)

        # Transform
        plane = NumberPlane(
            (-20, 20), (-20, 20),
            # CHANGE: NumberPlane requires stroke_color in background_line_style (before it took the default color)
            background_line_style={"stroke_color": BLUE_D, "stroke_width": 3},
            faded_line_ratio=0,
        )
        plane.axes.set_stroke(BLUE, 3)
        back_plane = NumberPlane(
            faded_line_ratio=0,
        )
        back_plane.set_stroke(GREY_B, 1, opacity=0.5)
        mat = [[2, 2], [1, 2]]
        eigenvalues, eigenvectors = np.linalg.eig(mat)
        # CHANGE: np.linalg.eig returns a complex array (ComplexWarning); the real part is taken. With numpy 2.5 it gives v1=(0.82, 0.58), v2=(-0.82, 0.58)
        eigenvectors = [normalize(v) for v in np.real(eigenvectors).T]
        eigenlines = VGroup(*(
            Line(10 * ev, -10 * ev, color=color)
            for ev, color in zip(eigenvectors, EIGEN_COLORS)
        ))
        eigenlines.set_stroke(GREY_B, 2)

        eigenvect_mobs = VGroup(*(
            Vector(ev, fill_color=color)
            for ev, color in zip(eigenvectors, EIGEN_COLORS)
        ))
        eigenvect_mobs[0].add_updater(lambda m: m.put_start_and_end_on(plane.c2p(0, 0), plane.c2p(*eigenvectors[0][:2])))
        eigenvect_mobs[1].add_updater(lambda m: m.put_start_and_end_on(plane.c2p(0, 0), plane.c2p(*eigenvectors[1][:2])))

        # Basis vectors
        bases = VGroup(
            Vector(RIGHT, fill_color=GREEN, thickness=0.05),
            Vector(UP, fill_color=RED, thickness=0.05),
        )
        bases[0].add_updater(lambda m: m.put_start_and_end_on(plane.c2p(0, 0), plane.c2p(1, 0)))
        bases[1].add_updater(lambda m: m.put_start_and_end_on(plane.c2p(0, 0), plane.c2p(0, 1)))

        disk = Circle(radius=1)
        disk.set_fill(YELLOW, 0.25)
        disk.set_stroke(YELLOW, 3)

        morpher = VGroup(plane, disk)

        self.add(back_plane, morpher, eigenlines, *eigenvect_mobs)

        self.play(
            morpher.animate.apply_matrix(mat), run_time=4
        )
        self.wait()

        # Labels
        labels = VGroup(*(
            OldTex("\\text{Stretch by }", f"\\lambda_{i}", color=color, font_size=30)
            for i, color in zip((1, 2), EIGEN_COLORS)
        ))
        for label, vect in zip(labels, eigenvect_mobs):
            label.next_to(
                vect.get_center(),
                rotate_vector(normalize(vect.get_vector()), 90 * DEGREES),
                buff=0.1,
                index_of_submobject_to_align=1,
            )
        labels.set_stroke(BLACK, 5, background=True)

        self.play(LaggedStartMap(FadeIn, labels, lag_ratio=0.7))
        self.wait()
