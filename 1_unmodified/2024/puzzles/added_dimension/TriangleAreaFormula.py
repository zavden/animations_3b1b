# ==============================================================================
# Scene:      TriangleAreaFormula
# Source:     videos/_2024/puzzles/added_dimension.py (lines 2620-2731)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl TriangleAreaFormula.py TriangleAreaFormula -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class TriangleAreaFormula(InteractiveScene):
    def construct(self):
        # Set up triangle
        plane = NumberPlane(faded_line_ratio=1)
        plane.add_coordinate_labels(font_size=16)
        plane.background_lines.set_stroke(opacity=0.75)
        plane.faded_lines.set_stroke(opacity=0.25)
        verts = [
            (1, 1, 0),
            (2, -1, 0),
            (3, 2, 0),
        ]
        triangle = Polygon(*verts)
        triangle.set_stroke(YELLOW, 3)
        dots = Group(TrueDot(vert, radius=0.1) for vert in verts)
        dots.set_color(WHITE)

        self.add(plane)
        self.add(triangle)
        self.add(dots)

        # Add labels
        labels = VGroup(
            Tex(Rf"(x_{n}, y_{n})", font_size=36)
            for n in [1, 2, 3]
        )
        labels.set_backstroke(BLACK, 3)
        for label, dot, vect in zip(labels, dots, [UP, DOWN, UP]):
            label.next_to(dot, vect, SMALL_BUFF)
        labels[0].shift(0.3 * LEFT)

        self.frame.reorient(0, 0, 0, (2.02, 0.72, 0.0), 4.49),
        self.play(
            LaggedStartMap(FadeIn, labels, shift=0.25 * UP, lag_ratio=0.5, run_time=2),
            self.frame.animate.to_default_state().set_anim_args(run_time=6),
        )
        self.wait()
        self.play(triangle.animate.set_fill(YELLOW, 0.5))
        self.wait()

        # Set up 3D labels
        labels_3d = VGroup(
            Tex(Rf"(x_{n}, y_{n}, 1)", font_size=36)
            for n in [1, 2, 3]
        )
        for label, dot, vect in zip(labels_3d, dots, [LEFT, UR, RIGHT]):
            label.rotate(89 * DEGREES, RIGHT)
            label.next_to(dot, vect + OUT, SMALL_BUFF)
            label.shift(OUT)

        # Move up to 3d
        frame = self.frame
        z_axis = NumberLine((-4, 4))
        z_axis.rotate(PI / 2, DOWN)
        z_axis.set_flat_stroke(False)
        ghost_plane = plane.copy()
        ghost_plane.fade(0.5)
        ghost_plane.shift(OUT)

        self.play(
            frame.animate.reorient(-13, 75, 0, (-0.14, 0.7, 1.48), 9.34).set_anim_args(run_time=2),
            FadeIn(z_axis),
        )
        self.play(
            frame.animate.reorient(15, 81, 0, (-0.56, 0.95, 1.43), 9.34).set_anim_args(run_time=8),
            TransformFromCopy(plane, ghost_plane),
            triangle.animate.shift(OUT),
            Transform(labels, labels_3d),
            *(
                dot.animate.shift(OUT).make_3d()
                for dot in dots
            ),
        )
        self.wait()

        # Show parallelpiped
        cube = VCube(side_length=1)
        cube.set_stroke(WHITE, 2)
        cube.set_fill(WHITE, 0.1)
        cube.deactivate_depth_test()
        cube.move_to(ORIGIN, [-1, -1, -1])
        cube.apply_matrix(np.transpose([
            dot.get_center()
            for dot in dots
        ]))

        self.play(
            frame.animate.reorient(-5, 63, 0, (-0.04, 0.69, 0.39), 7.73).set_anim_args(run_time=5),
            Write(cube),
        )
        self.wait()

        # Show tetrehedron
        tetrahedron = VGroup(
            triangle.copy(),
            Polygon(ORIGIN, dots[0].get_center(), dots[1].get_center()),
            Polygon(ORIGIN, dots[0].get_center(), dots[2].get_center()),
            Polygon(ORIGIN, dots[1].get_center(), dots[2].get_center()),
        )
        tetrahedron.set_stroke(width=0)
        tetrahedron.set_fill(YELLOW, 0.5)

        self.play(
            frame.animate.reorient(-4, 77, 0, (0.28, 0.78, 0.41), 7.73).set_anim_args(run_time=4),
            Write(tetrahedron)
        )
        self.wait()
        self.play(
            frame.animate.reorient(-5, 64, 0, (0.22, 0.72, -0.04), 7.14),
            run_time=8
        )
        self.wait()
