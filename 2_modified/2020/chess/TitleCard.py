# ==============================================================================
# Scene:      TitleCard
# Source:     videos/_2020/chess.py (lines 999-1036)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl TitleCard.py TitleCard -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - get_color() of a Cube (Group) no longer returns the color of its faces: it is read from square[0]
# ==============================================================================

from manim_imports_ext import *

class Chessboard(Group):
    CONFIG = {
        "shape": (8, 8),
        "height": 7,
        "depth": 0.25,
        "colors": [GREY_B, GREY_E],
        "gloss": 0.2,
        "square_resolution": (3, 3),
        "top_square_resolution": (5, 5),
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        nr, nc = self.shape
        cube = Cube(square_resolution=self.square_resolution)
        # Replace top square with something slightly higher res
        top_square = Square3D(resolution=self.top_square_resolution)
        top_square.replace(cube[0])
        cube.replace_submobject(0, top_square)
        self.add(*[cube.copy() for x in range(nc * nr)])
        self.arrange_in_grid(nr, nc, buff=0)
        self.set_height(self.height)
        self.set_depth(self.depth, stretch=True)
        for i, j in it.product(range(nr), range(nc)):
            color = self.colors[(i + j) % 2]
            self[i * nc + j].set_color(color)
        self.center()
        self.set_gloss(self.gloss)


class TitleCard(Scene):
    def construct(self):
        n = 6
        board = Chessboard(shape=(n, n))
        for square in board:
            # CHANGE: get_color() of a Cube (Group) no longer returns the color of its faces: it is read from square[0]
            square.set_color(interpolate_color(square[0].get_color(), BLACK, 0.25))
        # board[0].set_opacity(0)

        grid = NumberPlane(
            x_range=(0, n),
            y_range=(0, n),
            faded_line_ratio=0
        )
        grid.match_height(board)
        grid.next_to(board, OUT, 1e-8)
        low_grid = grid.copy()
        low_grid.next_to(board, IN, 1e-8)
        grid.add(low_grid)
        grid.set_stroke(GREY, width=1)
        grid.set_gloss(0.5)
        grid.prepare_for_nonlinear_transform(0)
        grid.rotate(PI, RIGHT)

        frame = self.camera.frame
        frame.set_phi(45 * DEGREES)

        text = OldTexText("The impossible\\\\chessboard puzzle")
        # text.set_width(board.get_width() - 0.5)
        text.set_width(FRAME_WIDTH - 2)
        text.set_stroke(BLACK, 10, background=True)
        text.fix_in_frame()
        self.play(
            ApplyMethod(frame.set_phi, 0, run_time=5),
            ShowCreationThenDestruction(grid, lag_ratio=0.02, run_time=3),
            LaggedStartMap(FadeIn, board, run_time=3, lag_ratio=0),
            Write(text, lag_ratio=0.1, run_time=3, stroke_color=BLUE_A),
        )
        self.wait(2)
