# ==============================================================================
# Scene:      SkipSkipYesYes
# Source:     videos/_2020/chess.py (lines 4425-4444)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl SkipSkipYesYes.py SkipSkipYesYes -w -m --fps 15
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


class SkipSkipYesYes(Scene):
    def construct(self):
        board = Chessboard()
        board.next_to(ORIGIN, DOWN)
        words = VGroup(
            OldTexText("Skip"),
            OldTexText("Skip"),
            OldTexText("Yes"),
            OldTexText("Yes"),
        )
        words.add(*words.copy())
        words.set_width(board[0].get_width() * 0.8)
        for word, square in zip(words, board):
            word.move_to(square)
            word.set_y(0, UP)

        for group in words[:4], words[4:]:
            self.play(ShowIncreasingSubsets(group, rate_func=double_smooth, run_time=2))
            self.play(FadeOut(group))
            self.wait()
