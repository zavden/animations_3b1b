# ==============================================================================
# Scene:      ExampleSquareAsBinaryNumber
# Source:     videos/_2020/chess.py (lines 4349-4422)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ExampleSquareAsBinaryNumber.py ExampleSquareAsBinaryNumber -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def int_to_bit_coords(n, min_dim=3):
    bits = "{0:b}".format(n)
    bits = (min_dim - len(bits)) * '0' + bits
    return np.array(list(map(int, bits)))


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


class ExampleSquareAsBinaryNumber(Scene):
    def construct(self):
        # Setup
        board = Chessboard()
        nums = VGroup()
        bin_nums = VGroup()
        for n, square in enumerate(board):
            bin_num = VGroup(*[
                Integer(int(b))
                for b in int_to_bit_coords(n, min_dim=6)
            ])
            bin_num.arrange(RIGHT, buff=SMALL_BUFF)
            bin_num.set_width((square.get_width() * 0.8))
            num = Integer(n)
            num.set_height(square.get_height() * 0.4)

            for mob in num, bin_num:
                mob.move_to(square, OUT)
                mob.set_stroke(BLACK, 4, background=True)

            num.generate_target()
            num.target.replace(bin_num, stretch=True)
            num.target.set_opacity(0)
            bin_num.save_state()
            bin_num.replace(num, stretch=True)
            bin_num.set_opacity(0)

            nums.add(num)
            bin_nums.add(bin_num)

        # Transform to binary
        self.add(board, nums)
        self.wait()
        original_nums = nums.copy()
        self.play(LaggedStart(*[
            AnimationGroup(MoveToTarget(num), Restore(bin_num))
            for num, bin_num in zip(nums, bin_nums)
        ]), lag_ratio=0.1)
        self.remove(nums)
        nums = original_nums
        self.wait(2)

        self.play(
            bin_nums.set_stroke, None, 0,
            bin_nums.set_opacity, 0.1,
        )
        self.wait()

        # Count
        n = 43
        self.play(
            board[n].set_color, MAROON_E,
            Animation(bin_nums[n]),
        )

        last = VMobject()
        shown_nums = VGroup()
        for k in [0, 8, 16, 24, 32, 40, 41, 42, 43]:
            nums[k].set_fill(YELLOW)
            self.add(nums[k])
            self.play(last.set_fill, WHITE, run_time=0.5)
            last = nums[k]
            shown_nums.add(last)
            if k == 40:
                self.wait()
        self.wait()
        self.play(LaggedStartMap(FadeOut, shown_nums[:-1]))
        self.wait()
        self.play(
            FadeOut(last),
            bin_nums[n].set_opacity, 1,
            bin_nums[n].set_fill, YELLOW
        )
        self.wait()
