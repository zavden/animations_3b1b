# ==============================================================================
# Scene:      AskAboutVolumeOfParallelpiped
# Source:     videos/_2024/puzzles/added_dimension.py (lines 2572-2617)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl AskAboutVolumeOfParallelpiped.py AskAboutVolumeOfParallelpiped -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class AskAboutVolumeOfParallelpiped(InteractiveScene):
    def construct(self):
        # Axes and plane
        frame = self.frame
        axes = ThreeDAxes((-8, 8), (-4, 4), (-4, 4))
        axes.set_stroke(WHITE, 2)
        plane = NumberPlane()
        frame.reorient(-43, 73, 0, (1.18, 0.21, 1.19), 5.96)
        self.add(plane, axes)

        # Tetrahedron
        verts = [
            (-2, 1, 1),
            (1, 0, 3),
            (3, 0, 0),
            (2, -2, 0),
        ]
        tetrahedron = VGroup(
            Polygon(*subset)
            for subset in it.combinations(verts, 3)
        )
        tetrahedron.set_stroke(WHITE, 1)
        tetrahedron.set_fill(TEAL_E, 0.5)
        tetrahedron.set_shading(0.5, 0.5, 0)
        dots = DotCloud(verts, radius=0.05)
        dots.make_3d()
        dots.set_color(WHITE)

        self.add(tetrahedron)
        self.add(dots)

        # Add vertex labels
        labels = VGroup(
            Tex(f"(x_{n}, y_{n}, z_{n})", font_size=36)
            for n in range(1, 5)
        )
        vects = [OUT + LEFT, OUT, OUT + RIGHT, OUT + RIGHT]
        for label, point, vect in zip(labels, dots.get_points(), vects):
            label.rotate(89 * DEGREES, RIGHT)
            label.next_to(point, vect, buff=SMALL_BUFF)

        frame.reorient(-33, 84, 0, (0.34, 0.8, 1.42), 7.12)
        frame.add_updater(lambda m: m.set_theta(-math.cos(7 * self.time * DEGREES) * 35 * DEGREES))

        self.play(LaggedStartMap(FadeIn, labels, shift=0.5 * OUT, lag_ratio=0.5, run_time=3))
        self.wait(30)
