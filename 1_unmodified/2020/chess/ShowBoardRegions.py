# ==============================================================================
# Scene:      ShowBoardRegions
# Source:     videos/_2020/chess.py (lines 4567-4669)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowBoardRegions.py ShowBoardRegions -w -m --fps 15
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


class ShowBoardRegions(ThreeDScene):
    def construct(self):
        # Setup
        board = Chessboard()
        nums = VGroup()
        pre_bin_nums = VGroup()
        bin_nums = VGroup()
        for n, square in enumerate(board):
            bin_num = VGroup(*[
                Integer(int(b), fill_color=GREY_A)
                for b in int_to_bit_coords(n, min_dim=6)
            ])
            bin_num.arrange(RIGHT, buff=SMALL_BUFF)
            bin_num.set_width((square.get_width() * 0.8))
            num = Integer(n)
            num.set_height(square.get_height() * 0.4)

            for mob in num, bin_num:
                mob.move_to(square, OUT)
                mob.set_stroke(BLACK, 4, background=True)

            bin_num.align_to(square, DOWN)
            bin_num.shift(SMALL_BUFF * UP)

            pre_bin_num = num.copy()
            pre_bin_num.generate_target()
            pre_bin_num.target.replace(bin_num, stretch=True)
            pre_bin_num.target.set_opacity(0)

            num.generate_target()
            num.target.scale(0.7)
            num.target.align_to(square, UP)
            num.target.shift(SMALL_BUFF * DOWN)

            bin_num.save_state()
            bin_num.replace(num, stretch=True)
            bin_num.set_opacity(0)

            nums.add(num)
            bin_nums.add(bin_num)
            pre_bin_nums.add(pre_bin_num)

        # Transform to binary
        self.add(board)
        self.play(
            ShowIncreasingSubsets(nums, run_time=4, rate_func=bezier([0, 0, 1, 1]))
        )
        self.wait()
        self.play(
            LaggedStart(*[
                AnimationGroup(
                    MoveToTarget(num),
                    MoveToTarget(pbn),
                    Restore(bin_num),
                )
                for num, pbn, bin_num in zip(nums, pre_bin_nums, bin_nums)
            ], lag_ratio=1.5 / 64),
        )
        self.remove(pre_bin_nums)
        self.wait(2)

        # Build groups to highlight
        one_groups = VGroup()
        highlights = VGroup()
        for i in reversed(range(6)):
            one_group = VGroup()
            highlight = VGroup()
            for bin_num, square in zip(bin_nums, board):
                boundary_square = Square()
                # boundary_square.set_stroke(YELLOW, 4)
                boundary_square.set_stroke(BLUE, 4)
                boundary_square.set_fill(BLUE, 0.5)
                boundary_square.replace(square)
                boundary_square.move_to(square, OUT)
                bit = bin_num[i]
                if bit.get_value() == 1:
                    one_group.add(bit)
                    highlight.add(boundary_square)
            one_group.save_state()
            one_groups.add(one_group)
            highlights.add(highlight)

        # Highlight hit_groups
        curr_highlight = None
        for one_group, highlight in zip(one_groups, highlights):
            one_group.generate_target()
            one_group.target.set_fill(YELLOW)
            one_group.target.set_stroke(YELLOW, 2)
            if curr_highlight is None:
                self.play(MoveToTarget(one_group))
                self.wait()
                self.play(LaggedStartMap(DrawBorderThenFill, highlight, lag_ratio=0.1, run_time=3))
                curr_highlight = highlight
            else:
                self.add(one_group, curr_highlight)
                self.play(
                    MoveToTarget(one_group),
                    Transform(curr_highlight, highlight)
                )
            self.wait()
            self.play(Restore(one_group))
        self.wait()
        self.play(FadeOut(curr_highlight))
