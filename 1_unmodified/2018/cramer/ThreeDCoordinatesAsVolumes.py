# ==============================================================================
# Scene:      ThreeDCoordinatesAsVolumes
# Source:     videos/_2018/cramer.py (lines 2061-2113)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ThreeDCoordinatesAsVolumes.py ThreeDCoordinatesAsVolumes -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

X_COLOR = GREEN


Y_COLOR = RED


Z_COLOR = BLUE


class ThreeDCoordinatesAsVolumes(Scene):
    def construct(self):
        colors = [X_COLOR, Y_COLOR, Z_COLOR]
        x, y, z = coords = VGroup(*list(map(Tex, "xyz")))
        coords.set_color_by_gradient(*colors)
        matrix = IntegerMatrix(np.identity(3))
        matrix.set_column_colors(*colors)
        det_text = get_det_text(matrix)
        equals = OldTex("=")
        equals.next_to(det_text[0], LEFT)
        equals.shift(SMALL_BUFF * DOWN)
        coords.next_to(equals, LEFT)

        columns = VGroup(*[
            VGroup(*matrix.mob_matrix[:, i])
            for i in range(3)
        ])

        coord_column = coords.copy()
        for coord, m_elem in zip(coord_column, columns[2]):
            coord.move_to(m_elem)
        coord_column.set_color(WHITE)
        coord_column[2].set_color(BLUE)
        coord_column.generate_target()

        self.play(LaggedStartMap(FadeIn, VGroup(
            z, equals, det_text, matrix.brackets,
            VGroup(*matrix.mob_matrix[:, :2].flatten()),
            coord_column
        )))
        self.wait(2)
        coord_column.target.move_to(columns[1])
        coord_column.target.set_color_by_gradient(WHITE, Y_COLOR, WHITE)
        self.play(
            MoveToTarget(coord_column, path_arc=np.pi),
            FadeOut(columns[1]),
            FadeIn(columns[2]),
            FadeInFromDown(y),
            z.shift, UP,
            z.fade, 1,
        )
        self.wait(2)
        coord_column.target.move_to(columns[0])
        coord_column.target.set_color_by_gradient(X_COLOR, WHITE, WHITE)
        self.play(
            MoveToTarget(coord_column, path_arc=np.pi),
            FadeOut(columns[0]),
            FadeIn(columns[1]),
            FadeInFromDown(x),
            y.shift, UP,
            y.fade, 1,
        )
        self.wait(2)
