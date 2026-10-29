# ==============================================================================
# Scene:      WantAdditionToBeSubtraction
# Source:     videos/_2020/chess.py (lines 4159-4230)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl WantAdditionToBeSubtraction.py WantAdditionToBeSubtraction -w -m --fps 15
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


# Animations for Matt
class WantAdditionToBeSubtraction(ThreeDScene):
    def construct(self):
        # Add sum
        coins = CoinsOnBoard(
            Chessboard(shape=(1, 4)),
            coin_config={"numeric_labels": True},
        )
        for coin in coins[0], coins[2]:
            coin.flip()

        coefs = VGroup(*[Tex(f"X_{i}") for i in range(len(coins))])
        full_sum = Group()
        to_fade = VGroup()
        for coin, coef in zip(coins, coefs):
            coin.set_height(0.7)
            coef.set_height(0.5)
            summand = Group(coin, OldTex("\\cdot"), coef, OldTex("+"))
            to_fade.add(*summand[1::2])
            summand.arrange(RIGHT, buff=0.2)
            full_sum.add(summand)
        full_sum.add(OldTex("\\dots"))
        full_sum.arrange(RIGHT, buff=0.2)
        to_fade.add(full_sum[-1])

        some_label = OldTexText("Some kind of ``numbers''")
        some_label.next_to(full_sum, DOWN, buff=2)
        arrows = VGroup(*[
            Arrow(some_label.get_top(), coef.get_bottom())
            for coef in coefs
        ])

        for coin in coins:
            coin.save_state()
            coin.rotate(90 * DEGREES, UP)
            coin.set_opacity(0)

        self.play(
            LaggedStartMap(Restore, coins, lag_ratio=0.3),
            run_time=1
        )
        self.play(
            FadeIn(to_fade),
            LaggedStartMap(FadeInFromPoint, coefs, lambda m: (m, some_label.get_top())),
            LaggedStartMap(GrowArrow, arrows),
            Write(some_label, run_time=1)
        )
        self.wait()
        self.play(FadeOut(some_label), FadeOut(arrows))

        # Show a flip
        add_label = OldTex("+X_2", color=GREEN)
        sub_label = OldTex("-X_2", color=RED)
        for label in add_label, sub_label:
            label.next_to(coins[2], UR)
            label.match_height(coefs[2])
            self.play(
                FlipCoin(coins[2]),
                FadeIn(label, 0.5 * DOWN)
            )
            self.play(FadeOut(label))

        # What we want
        want_label = OldTexText("Want: ", "$X_i = -X_i$")
        eq = OldTexText("$X_i + X_i = 0$")
        want_label.next_to(full_sum, DOWN, LARGE_BUFF)
        eq.next_to(want_label[1], DOWN, aligned_edge=LEFT)

        self.play(FadeIn(want_label))
        self.wait()
        self.play(FadeIn(eq, UP))
        self.wait()
