# ==============================================================================
# Scene:      RotateCubeThreeTimes
# Source:     videos/_2018/quaternions.py (lines 1021-1046)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotateCubeThreeTimes.py RotateCubeThreeTimes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

class RubiksCube(VGroup):
    CONFIG = {
        "colors": [
            "#FFD500",  # Yellow
            "#C41E3A",  # Orange
            "#009E60",  # Green
            "#FF5800",  # Red
            "#0051BA",  # Blue
            "#FFFFFF"   # White
        ],
    }

    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        vectors = [OUT, RIGHT, UP, LEFT, DOWN, IN]
        faces = [
            self.create_face(color, vector)
            for color, vector in zip(self.colors, vectors)
        ]
        VGroup.__init__(self, *it.chain(*faces), **kwargs)
        self.set_shade_in_3d(True)

    def create_face(self, color, vector):
        squares = VGroup(*[
            self.create_square(color)
            for x in range(9)
        ])
        squares.arrange_in_grid(
            3, 3,
            buff=0
        )
        squares.set_width(2)
        squares.move_to(OUT, OUT)
        squares.apply_matrix(z_to_vector(vector))
        return squares

    def create_square(self, color):
        square = Square(
            stroke_width=3,
            stroke_color=BLACK,
            fill_color=color,
            fill_opacity=1,
            side_length=1,
        )
        square.flip()
        return square
        # back = square.copy()
        # back.set_fill(BLACK, 0.85)
        # back.set_stroke(width=0)
        # back.shift(0.5 * IN)
        # return VGroup(square, back)

    def get_face(self, vect):
        self.sort(lambda p: np.dot(p, vect))
        return self[-(12 + 9):]


class RotateCubeThreeTimes(SpecialThreeDScene):
    def construct(self):
        cube = RubiksCube()
        cube.set_fill(opacity=0.8)
        cube.set_stroke(width=1)
        randy = Randolph(mode="pondering")
        randy.set_height(cube.get_height() - 2 * SMALL_BUFF)
        randy.move_to(cube.get_edge_center(OUT))
        randy.set_fill(opacity=0.8)
        # randy.set_shade_in_3d(True)
        cube.add(randy)
        axes = self.get_axes()

        self.add(axes, cube)
        self.move_camera(
            phi=70 * DEGREES,
            theta=-140 * DEGREES,
        )
        self.begin_ambient_camera_rotation(rate=0.02)
        self.wait(2)
        self.play(Rotate(cube, TAU / 4, RIGHT, run_time=3))
        self.wait(2)
        self.play(Rotate(cube, TAU / 4, UP, run_time=3))
        self.wait(2)
        self.play(Rotate(cube, -TAU / 3, np.ones(3), run_time=3))
        self.wait(7)
