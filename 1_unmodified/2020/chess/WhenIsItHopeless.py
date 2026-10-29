# ==============================================================================
# Scene:      WhenIsItHopeless
# Source:     videos/_2020/chess.py (lines 3856-3908)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl WhenIsItHopeless.py WhenIsItHopeless -w -m --fps 15
# ==============================================================================

from manim_imports_ext import *

def string_to_bools(message):
    # For easter eggs on the board
    as_int = int.from_bytes(message.encode(), 'big')
    bits = "{0:b}".format(as_int)
    bits = (len(message) * 8 - len(bits)) * '0' + bits
    return [bool(int(b)) for b in bits]


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


class WhenIsItHopeless(Scene):
    def construct(self):
        boards = Group(
            Chessboard(shape=(1, 3)),
            Chessboard(shape=(2, 2)),
            Chessboard(shape=(2, 3)),
            Chessboard(shape=(2, 3)),
            Chessboard(shape=(2, 4)),
            Chessboard(shape=(2, 4)),
            Chessboard(shape=(3, 3)),
            Chessboard(shape=(3, 4)),
            Chessboard(shape=(3, 4)),
            Chessboard(shape=(3, 4)),
        )
        last_board = None
        last_coins = None
        last_words = None
        for n, board in zip(it.count(3), boards):
            board.scale(1 / board[0].get_height())
            coins = CoinsOnBoard(board)
            coins.flip_at_random()
            diff = len(board) - n
            if diff > 0:
                board[-diff:].set_opacity(0)
                coins[-diff:].set_opacity(0)

            if sum(int_to_bit_coords(n)) == 1:
                words = OldTexText("Maybe possible")
                words.set_color(GREEN)
            else:
                words = OldTexText("Futile!")
                words.set_color(RED)
            words.scale(1.5)
            words.next_to(board, UP, MED_LARGE_BUFF)

            if n == 3:
                self.play(
                    FadeIn(board),
                    FadeIn(coins),
                    FadeIn(words, DOWN),
                )
            else:
                self.play(
                    ReplacementTransform(last_board, board),
                    ReplacementTransform(last_coins, coins),
                    FadeOut(last_words),
                    FadeIn(words, DOWN),
                )
            self.wait()

            last_board = board
            last_coins = coins
            last_words = words
