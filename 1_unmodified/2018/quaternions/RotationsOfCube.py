# ==============================================================================
# Scene:      RotationsOfCube
# Source:     videos/_2018/quaternions.py (lines 5954-6000)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RotationsOfCube.py RotationsOfCube -w -m --fps 15
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


class RotationsOfCube(SpecialThreeDScene):
    def construct(self):
        self.set_camera_orientation(**self.get_default_camera_position())
        self.begin_ambient_camera_rotation(0.0001)
        cube = RubiksCube()
        cube2 = cube.copy()
        axes = self.get_axes()
        axes.scale(0.75)

        label1 = OldTexText(
            "z-axis\\\\",
            "then x-axis"
        )
        label2 = OldTexText(
            "x-axis\\\\",
            "then z-axis"
        )
        for label in [label1, label2]:
            for part in label:
                part.add_background_rectangle()
            label.rotate(90 * DEGREES, RIGHT)
            label.move_to(3 * OUT + 0.5 * IN)

        self.add(axes, cube)
        self.play(
            Rotate(cube, 90 * DEGREES, OUT, run_time=2),
            FadeIn(label1[0], IN),
        )
        self.play(
            Rotate(cube, 90 * DEGREES, RIGHT, run_time=2),
            FadeIn(label1[1], IN),
        )
        self.wait()
        self.play(
            cube.shift, 5 * RIGHT,
            label1.shift, 5 * RIGHT,
            Write(cube2, run_time=1)
        )
        self.play(
            Rotate(cube2, 90 * DEGREES, RIGHT, run_time=2),
            FadeIn(label2[0], IN),
        )
        self.play(
            Rotate(cube2, 90 * DEGREES, OUT, run_time=2),
            FadeIn(label2[1], IN),
        )
        self.wait(5)
