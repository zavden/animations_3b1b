# ==============================================================================
# Scene:      ThreeDSpaceExample
# Source:     videos/_2024/transformers/embedding.py (lines 778-903)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeDSpaceExample.py ThreeDSpaceExample -w -m --fps 15
# ==============================================================================

from __future__ import annotations
from manim_imports_ext import *

class ThreeDSpaceExample(InteractiveScene):
    def construct(self):
        # Set up axes
        frame = self.frame
        frame.reorient(-15, 78, 0, (1.07, 1.71, 1.41), 6.72)
        frame.add_ambient_rotation(1 * DEGREES)
        axes = ThreeDAxes((-5, 5), (-5, 5), (-4, 4))
        plane = NumberPlane((-5, 5), (-5, 5))
        plane.fade(0.5)

        self.add(plane)
        self.add(axes)

        # Show coordiantes creating directions
        x, y, z = coordinates = np.array([3, 1, 2])
        colors = [RED, GREEN, BLUE]

        coords = DecimalMatrix(np.zeros((3, 1)), num_decimal_places=1)
        coords.fix_in_frame()
        coords.to_corner(UR)
        coords.shift(1.5 * LEFT)
        coords.get_entries().set_submobject_colors_by_gradient(*colors)

        lines = VGroup(
            Line(axes.c2p(0, 0, 0), axes.c2p(x, 0, 0)),
            Line(axes.c2p(x, 0, 0), axes.c2p(x, y, 0)),
            Line(axes.c2p(x, y, 0), axes.c2p(x, y, z)),
        )
        lines.set_flat_stroke(False)
        lines.set_submobject_colors_by_gradient(*colors)
        labels = VGroup(*map(Tex, "xyz"))
        labels.rotate(89 * DEGREES, RIGHT)
        directions = [OUT, OUT + RIGHT, RIGHT]
        for label, line, direction in zip(labels, lines, directions):
            label.next_to(line, direction, buff=SMALL_BUFF)
            label.match_color(line)

        dot = GlowDot(color=WHITE)
        dot.move_to(axes.get_origin())

        vect = Arrow(axes.get_origin(), axes.c2p(x, y, z), buff=0)
        vect.set_flat_stroke(False)

        self.add(coords)
        for entry, line, label, value in zip(coords.get_entries(), lines, labels, coordinates):
            rect = SurroundingRectangle(entry)
            rect.set_fill(line.get_color(), 0.3)
            rect.set_stroke(line.get_color(), width=2)
            self.play(
                ShowCreation(line),
                FadeInFromPoint(label, line.get_start()),
                VFadeInThenOut(rect),
                ChangeDecimalToValue(entry, value),
                dot.animate.move_to(line.get_end()),
            )
            self.wait(0.5)
        self.play(ShowCreation(vect))

        # Wait for a bit
        self.wait(15)

        # Show many points
        points = GlowDots(np.random.uniform(-3, 3, size=(50, 3)), radius=0.1)
        frame.clear_updaters()
        self.play(
            FadeOut(coords),
            FadeOut(dot),
            FadeOut(plane),
            LaggedStartMap(FadeOut, VGroup(*lines, vect, *labels)),
            frame.animate.reorient(-81, 61, 0, (-0.82, 0.6, 0.36), 8.95),
            ShowCreation(points),
            run_time=2,
        )
        frame.add_ambient_rotation(5 * DEGREES)
        self.wait(2)

        # Take a 2d slice
        plane = Square3D()
        plane.set_height(10)
        plane.set_color([GREY_E, GREY_C])
        plane.set_opacity(0.25)
        grid = NumberPlane(
            (-5, 5), (-5, 5),
            background_line_style=dict(stroke_color=GREY_B, stroke_width=1),
            faded_line_ratio=0,
        )
        grid.axes.match_style(grid.background_lines)
        grid.match_height(plane)
        plane_group = Group(plane, grid)
        plane_group.rotate(60 * DEGREES, UR)

        bases = [
            normalize(point)
            for point in plane.get_points()[:2]
        ]

        def project(points):
            return np.array([
                sum(np.dot(point, b) * b for b in bases)
                for point in points
            ])

        projected_points = points.copy()
        projected_points.apply_points_function(project)

        projection_lines = VGroup(*(
            Line(p1, p2)
            for p1, p2 in zip(points.get_points(), projected_points.get_points())
        ))
        projection_lines.set_stroke()

        self.play(ShowCreation(plane), Write(grid, lag_ratio=0.01, stroke_width=1))
        self.wait(2)
        self.play(
            axes.animate.set_stroke(opacity=0.25),
            points.animate.set_opacity(0.5),
            TransformFromCopy(points, projected_points),
            ShowCreation(projection_lines, lag_ratio=0.05),
            run_time=3
        )
        self.play(
            FadeOut(points),
            FadeOut(projection_lines),
            FadeOut(axes)
        )
        self.wait(15)
