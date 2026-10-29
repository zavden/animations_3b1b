# ==============================================================================
# Scene:      DimensionsPointingToEachOther
# Source:     videos/_2024/puzzles/supplements.py (lines 688-738)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl DimensionsPointingToEachOther.py DimensionsPointingToEachOther -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class DimensionsPointingToEachOther(InteractiveScene):
    def construct(self):
        # Show shapes
        shapes = VGroup(
            VGroup(Line(LEFT, RIGHT)),
            VGroup(Square(side_length=2)),
            self.get_cube(),
            self.get_hypercube(),
        )
        shapes.arrange(RIGHT, buff=1.0)
        shapes.set_submobject_colors_by_gradient(TEAL, YELLOW)

        point = VectorizedPoint()

        self.add(shapes[0])
        for s1, s2 in zip(shapes, shapes[1:]):
            point.move_to(s1).align_to(shapes, UP)
            arrow = Arrow(s2.get_top(), point.get_center(), buff=0.1, path_arc=120 * DEGREES, thickness=4)
            self.play(
                FadeIn(arrow),
                TransformFromCopy(s1, s2, lag_ratio=0.5 / len(s2), run_time=1.5),
            )
            self.wait(0.25)

    def get_cube(self, side_length=2.0):
        cube = VCube(side_length=side_length)
        cube.set_stroke(WHITE, 2)
        cube.set_fill(opacity=0)
        cube.rotate(20 * DEGREES, OUT).rotate(80 * DEGREES, LEFT)
        return cube

    def get_hypercube(self, side_length=2.0, theta=20 * DEGREES, phi=80 * DEGREES):
        cubes = VGroup(
            VCube().set_height(side_length),
            VCube().set_height(side_length / 2),
        )
        for cube in cubes:
            cube.sort(lambda p: p[2])
        edges = VGroup()
        for i in [0, -1]:
            edges.add(*(
                Line(*pair)
                for pair in zip(cubes[0][i].get_vertices(), cubes[1][i].get_vertices())
            ))

        result = VGroup(*cubes, edges)
        result.set_stroke(WHITE, 2)
        result.set_fill(opacity=0)
        result.rotate(theta, OUT)
        result.rotate(phi, LEFT)
        return VGroup(*result.family_members_with_points())
