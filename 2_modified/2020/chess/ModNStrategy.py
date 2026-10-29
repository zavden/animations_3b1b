# ==============================================================================
# Scene:      ModNStrategy
# Source:     videos/_2020/chess.py (lines 2169-2328)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl ModNStrategy.py ModNStrategy -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
# ==============================================================================

from manim_imports_ext import *

def string_to_bools(message):
    # For easter eggs on the board
    as_int = int.from_bytes(message.encode(), 'big')
    bits = "{0:b}".format(as_int)
    bits = (len(message) * 8 - len(bits)) * '0' + bits
    return [bool(int(b)) for b in bits]


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


class Coin(Group):
    CONFIG = {
        "disk_resolution": (4, 51),
        "height": 1,
        "depth": 0.1,
        "color": GOLD_D,
        "tails_color": RED,
        "include_labels": True,
        "numeric_labels": False,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        res = self.disk_resolution
        self.top = Disk3D(resolution=res, gloss=0.2)
        self.bottom = self.top.copy()
        self.top.shift(OUT)
        self.bottom.shift(IN)
        self.edge = Cylinder(height=2, resolution=(res[1], 2))
        self.add(self.top, self.bottom, self.edge)
        self.rotate(90 * DEGREES, OUT)
        self.set_color(self.color)
        self.bottom.set_color(RED)

        if self.include_labels:
            chars = "10" if self.numeric_labels else "HT"
            labels = VGroup(*[TexText(c) for c in chars])
            for label, vect in zip(labels, [OUT, IN]):
                label.shift(1.02 * vect)
                label.set_height(0.8)
            labels[1].rotate(PI, RIGHT)
            labels.apply_depth_test()
            labels.set_stroke(width=0)
            self.add(*labels)
            self.labels = labels

        self.set_height(self.height)
        self.set_depth(self.depth, stretch=True)

    def is_heads(self):
        return self.top.get_center()[2] > self.bottom.get_center()[2]

    def flip(self, axis=RIGHT):
        super().flip(axis)
        return self


class CoinsOnBoard(Group):
    CONFIG = {
        "proportion_of_square_height": 0.7,
        "coin_config": {},
    }

    def __init__(self, chessboard, **kwargs):
        super().__init__(**kwargs)
        prop = self.proportion_of_square_height
        for cube in chessboard:
            coin = Coin(**self.coin_config)
            coin.set_height(prop * cube.get_height())
            coin.next_to(cube, OUT, buff=0)
            self.add(coin)

    def flip_at_random(self, p=0.5):
        bools = np.random.random(len(self)) < p
        self.flip_by_bools(bools)
        return self

    def flip_by_message(self, message):
        self.flip_by_bools(string_to_bools(message))
        return self

    def flip_by_bools(self, bools):
        for coin, head in zip(self, bools):
            if coin.is_heads() ^ head:
                coin.flip()
        return self

    def get_bools(self):
        return [coin.is_heads() for coin in self]


class FlipCoin(Animation):
    CONFIG = {
        "axis": RIGHT,
        "run_time": 1,
        "shift_dir": OUT,
    }

    # CHANGE: Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
    def __init__(self, coin, axis=RIGHT, shift_dir=OUT, **kwargs):
        self.axis = axis
        self.shift_dir = shift_dir
        super().__init__(coin, **kwargs)
        self.shift_vect = coin.get_height() * self.shift_dir / 2

    def interpolate_mobject(self, alpha):
        coin = self.mobject
        for sm, start_sm in self.families:
            sm.match_points(start_sm)
        coin.rotate(alpha * PI, axis=self.axis)
        coin.shift(4 * alpha * (1 - alpha) * self.shift_vect)
        return coin


class ModNStrategy(ThreeDScene):
    def construct(self):
        # Board
        n_shown = 5
        board = Chessboard()
        coins = CoinsOnBoard(board, coin_config={"numeric_labels": True})
        coins.flip_by_message(r"75% odds")

        nums = VGroup()
        for n, square in enumerate(board):
            num = Integer(n)
            num.set_height(0.4 * square.get_height())
            num.next_to(square, OUT, buff=0)
            nums.add(num)
        nums.set_stroke(BLACK, 3, background=True)

        coins.generate_target()
        for coin in coins.target:
            coin.set_opacity(0.2)
            coin[-2:].set_opacity(0)

        self.add(board)
        self.add(coins)
        self.wait()
        self.play(
            MoveToTarget(coins),
            FadeIn(nums, lag_ratio=0.1)
        )
        self.wait()

        # # Compress
        # square_groups = Group(*[
        #     Group(square, coin, num)
        #     for square, coin, num in zip(board, coins, nums)
        # ])
        # segments = Group(
        #     square_groups[:n_shown],
        #     square_groups[n_shown:-n_shown],
        #     square_groups[-n_shown:],
        # )
        # segments.generate_target()
        # dots = OldTex("\\cdots")
        # dots.center()
        # segments.target[0].next_to(dots, LEFT)
        # segments.target[2].next_to(dots, RIGHT)
        # segments.target[1].scale(0)
        # segments.target[1].move_to(dots)

        # self.play(
        #     Write(dots),
        #     MoveToTarget(segments),
        # )
        # self.wait()
        # self.remove(segments[1])

        # # Raise coins
        # coins = Group(*coins[:n_shown], *coins[-n_shown:])
        # nums = VGroup(*nums[:n_shown], *nums[-n_shown:])
        # board = Group(*board[:n_shown], *board[-n_shown:])
        # self.play(
        #     coins.shift, UP,
        #     coins.set_opacity, 1,
        # )

        # Setup sum
        mid_coins = coins[n_shown:-n_shown]
        mid_nums = nums[n_shown:-n_shown]
        coins = Group(*coins[:n_shown], *coins[-n_shown:])
        nums = VGroup(*nums[:n_shown], *nums[-n_shown:])
        nums.generate_target()
        coins.generate_target()
        coins.target.set_opacity(1)

        full_sum = Group()
        to_fade_in = VGroup()
        for num, coin in zip(nums.target, coins.target):
            coin.set_height(0.7)
            num.set_height(0.5)
            summand = Group(
                coin,
                OldTex("\\cdot"),
                num,
                OldTex("+"),
            )
            to_fade_in.add(summand[1], summand[3])
            VGroup(*summand[1:]).set_stroke(BLACK, 3, background=True)
            summand.arrange(RIGHT, buff=MED_SMALL_BUFF)

            full_sum.add(summand)

        dots = OldTex("\\dots")
        full_sum = Group(*full_sum[:n_shown], dots, *full_sum[n_shown:])
        full_sum.arrange(RIGHT, buff=MED_SMALL_BUFF)
        full_sum.set_width(FRAME_WIDTH - 1)
        full_sum[-1][-1].scale(0, about_edge=LEFT)
        full_sum.move_to(UP)

        brace = Brace(full_sum, DOWN)
        s_label = VGroup(
            OldTexText("Sum (mod 64) = "),
            Integer(53),
        )
        s_label[1].set_color(BLUE)
        s_label[1].match_height(s_label[0][0][0])
        s_label.arrange(RIGHT)
        s_label[1].align_to(s_label[0][0][0], DOWN)
        s_label.next_to(brace, DOWN)

        words = OldTexText("Can't know if a flip will add or subtract")
        words.to_edge(UP)

        for mob in mid_coins, mid_nums:
            mob.generate_target()
            mob.target.move_to(dots)
            mob.target.scale(0)
            mob.target.set_opacity(0)

        self.play(
            FadeOut(board, IN),
            MoveToTarget(mid_coins, remover=True),
            MoveToTarget(mid_nums, remover=True),
            MoveToTarget(nums),
            MoveToTarget(coins),
            Write(dots),
            FadeIn(to_fade_in, lag_ratio=0.1),
            run_time=2
        )
        self.play(
            GrowFromCenter(brace),
            FadeIn(s_label, 0.25 * UP)
        )
        self.wait()

        self.play(Write(words, run_time=1))
        self.wait()

        # Do some flips
        s_label[1].add_updater(lambda m: m.set_value(m.get_value() % 64))
        for x in range(10):
            n = random.randint(-n_shown, n_shown - 1)
            coin = coins[n]
            n = n % 64
            diff_label = Integer(n, include_sign=True)
            if not coin.is_heads():
                diff_label.set_color(GREEN)
            else:
                diff_label.set_color(RED)
                diff_label.set_value(-diff_label.get_value())
            diff_label.next_to(coin, UP, aligned_edge=LEFT)
            self.play(
                ChangeDecimalToValue(
                    s_label[1],
                    s_label[1].get_value() + n,
                    rate_func=squish_rate_func(smooth, 0.5, 1)
                ),
                FlipCoin(coin),
                FadeIn(diff_label, 0.5 * DOWN)
            )
            self.play(FadeOut(diff_label))
            self.wait()
