# ==============================================================================
# Scene:      RubuiksCubeOperations
# Source:     videos/_2018/quaternions.py (lines 5921-5951)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl RubuiksCubeOperations.py RubuiksCubeOperations -w -m --fps 15
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


class RubuiksCubeOperations(SpecialThreeDScene):
    def construct(self):
        self.set_camera_orientation(**self.get_default_camera_position())
        self.begin_ambient_camera_rotation()
        cube = RubiksCube()
        cube.shift(2.5 * RIGHT)
        cube2 = cube.copy()

        self.add(cube)
        self.play(
            Rotate(cube.get_face(RIGHT), 90 * DEGREES, RIGHT),
            run_time=2
        )
        self.play(
            Rotate(cube.get_face(DOWN), 90 * DEGREES, UP),
            run_time=2
        )
        self.wait()
        self.play(
            cube.shift, 5 * LEFT,
            FadeIn(cube2)
        )
        self.play(
            Rotate(cube2.get_face(DOWN), 90 * DEGREES, UP),
            run_time=2
        )
        self.play(
            Rotate(cube2.get_face(RIGHT), 90 * DEGREES, RIGHT),
            run_time=2
        )
        self.wait(6)
