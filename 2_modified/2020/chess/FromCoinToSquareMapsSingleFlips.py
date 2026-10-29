# ==============================================================================
# Scene:      FromCoinToSquareMapsSingleFlips
# Source:     videos/_2020/chess.py (lines 486-496)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl FromCoinToSquareMapsSingleFlips.py FromCoinToSquareMapsSingleFlips -w -m --fps 15
#
# Changes from the original (look for '# CHANGE' in the code):
#   - Animation no longer digests CONFIG (axis, shift_dir): they become parameters of FlipCoin.__init__
#   - get_color() of a Cube (Group) no longer returns the color of its faces: it is read from cube[0]
#   - Arrow no longer has .tip (it is a single filled shape): removing the stroke from the tip is omitted
# ==============================================================================

from manim_imports_ext import *

def boolian_linear_combo(bools):
    return reduce(op.xor, [b * n for n, b in enumerate(bools)], 0)


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


class FromCoinToSquareMaps(ThreeDScene):
    CONFIG = {
        "messages": [
            "Please, ",
            "go watch",
            "Stand-up",
            "Maths on",
            "YouTube."
        ],
        "flip_lag_ratio": 0.05,
    }

    def construct(self):
        messages = self.messages

        board1 = Chessboard()
        board1.set_width(5.5)
        board1.to_corner(DL)

        board2 = board1.copy()
        board2.to_corner(DR)

        coins = CoinsOnBoard(board1)
        bools = string_to_bools(messages[0])
        for coin, head in zip(coins, bools):
            if not head:
                coin.flip(RIGHT)

        for cube in board2:
            # CHANGE: get_color() of a Cube (Group) no longer returns the color of its faces: it is read from cube[0]
            cube.original_color = cube[0].get_color()

        arrow = Arrow(board1.get_right(), board2.get_left())
        # CHANGE: Arrow no longer has .tip (it is a single filled shape): removing the stroke from the tip is omitted
        pass  # manimgl's arrow is a single filled shape, without .tip

        title1 = OldTexText("Pattern of coins")
        title2 = OldTexText("Individual square")

        for title, board in [(title1, board1), (title2, board2)]:
            title.scale(0.5 / title[0][0].get_height())
            title.next_to(board, UP, MED_LARGE_BUFF)

        title2.align_to(title1, UP)

        def get_special_square(coins=coins, board=board2):
            bools = [coin.is_heads() for coin in coins]
            return board[boolian_linear_combo(bools)]

        self.add(board1)
        self.add(title1)
        self.add(coins)

        self.play(
            GrowArrow(arrow),
            FadeIn(board2, 2 * LEFT)
        )
        square = get_special_square()
        rect = SurroundingRectangle(square, buff=0)
        rect.set_color(PINK)
        rect.next_to(square, OUT, buff=0.01)
        self.play(
            square.set_color, MAROON_C,
            ShowCreation(rect),
            FadeIn(title2)
        )

        for message in messages[1:]:
            new_bools = string_to_bools(message)
            coins_to_flip = Group()
            for coin, to_heads in zip(coins, new_bools):
                if coin.is_heads() ^ to_heads:
                    coins_to_flip.add(coin)
            coins_to_flip.shuffle()
            self.play(LaggedStartMap(
                FlipCoin, coins_to_flip,
                lag_ratio=self.flip_lag_ratio,
                run_time=1,
            ))

            new_square = get_special_square()
            self.play(
                square.set_color, square.original_color,
                new_square.set_color, MAROON_C,
                rect.move_to, new_square, OUT,
                rect.shift, 0.01 * OUT,
            )
            square = new_square
            self.wait()


class FromCoinToSquareMapsSingleFlips(FromCoinToSquareMaps):
    CONFIG = {
        "messages": [
            "FlipBits",
            "BlipBits",
            "ClipBits",
            "ChipBits",
            "ChipBats",
            "ChipRats",
        ]
    }
