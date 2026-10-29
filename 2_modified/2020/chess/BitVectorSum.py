# ==============================================================================
# Scene:      BitVectorSum
# Source:     videos/_2020/chess.py (lines 4233-4346)
# Category:   2 · Renders with modifications
#
# Run from this folder:
#     manimgl BitVectorSum.py BitVectorSum -w -m --fps 15
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


def bit_coords_to_int(bits):
    return sum([(2**n) * b for n, b in enumerate(reversed(bits))])


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


class BitVectorSum(ThreeDScene):
    def construct(self):
        # Setup
        board = Chessboard(shape=(1, 4))
        board.set_height(1)
        coins = CoinsOnBoard(board, coin_config={"numeric_labels": True})
        coins[2].flip()

        all_coords = [np.array([b0, b1]) for b0, b1 in it.product(range(2), range(2))]
        bit_vectors = VGroup(*[
            IntegerMatrix(coords.reshape((2, 1))).set_height(1)
            for coords in all_coords
        ])
        bit_vectors.arrange(RIGHT, buff=2)
        bit_vectors.to_edge(UP)
        bit_vectors.set_stroke(BLACK, 4, background=True)

        arrows = VGroup(
            Arrow(board[0].get_corner(UL), bit_vectors[0].get_corner(DR)),
            Arrow(board[1].get_corner(UP), bit_vectors[1].get_corner(DOWN)),
            Arrow(board[2].get_corner(UP), bit_vectors[2].get_corner(DOWN)),
            Arrow(board[3].get_corner(UR), bit_vectors[3].get_corner(DL)),
        )

        # Show vectors
        self.add(board)
        self.add(coins)
        for arrow, vector in zip(arrows, bit_vectors):
            self.play(
                GrowArrow(arrow),
                FadeInFromPoint(vector, arrow.get_start()),
            )
            self.wait()

        # Move coins
        coin_copies = coins.copy()
        cdots = VGroup()
        plusses = VGroup()
        for cc, vector in zip(coin_copies, bit_vectors):
            dot = OldTex("\\cdot")
            dot.next_to(vector, LEFT, MED_SMALL_BUFF)
            cdots.add(dot)
            plus = OldTex("+")
            plus.next_to(vector, RIGHT, MED_SMALL_BUFF)
            plusses.add(plus)
            cc.next_to(dot, LEFT, MED_SMALL_BUFF)
        plusses[-1].set_opacity(0)

        for coin, cc, dot, plus in zip(coins, coin_copies, cdots, plusses):
            self.play(
                TransformFromCopy(coin, cc),
                Write(dot),
            )
            self.play(Write(plus))
        self.wait()

        # Show sum
        eq = OldTex("=")
        eq.move_to(plusses[-1])

        def get_rhs(coins=coins, bit_vectors=bit_vectors, all_coords=all_coords, eq=eq):
            bit_coords = sum([
                (b * coords)
                for coords, b in zip(all_coords, coins.get_bools())
            ]) % 2
            n = bit_coords_to_int(bit_coords)
            result = bit_vectors[n].copy()
            result.next_to(eq, RIGHT)
            result.n = n
            return result

        def get_rhs_anim(rhs, bit_vectors=bit_vectors):
            bv_copies = bit_vectors.copy()
            bv_copies.generate_target()
            for bv in bv_copies.target:
                bv.move_to(rhs)
                bv.set_opacity(0)
            bv_copies.target[rhs.n].set_opacity(1)
            return AnimationGroup(
                MoveToTarget(bv_copies, remover=True),
                ShowIncreasingSubsets(Group(rhs), int_func=np.floor)
            )

        rhs = get_rhs()

        mod2_label = OldTexText("(Add mod 2)")
        mod2_label.next_to(rhs, DOWN, MED_LARGE_BUFF)
        mod2_label.to_edge(RIGHT)

        self.play(
            Write(eq),
            get_rhs_anim(rhs),
            FadeIn(mod2_label),
            FadeOut(board),
            FadeOut(coins),
            FadeOut(arrows),
        )
        self.wait(2)

        # Show some flips
        for x in range(8):
            i = random.randint(0, 3)
            rect = SurroundingRectangle(Group(coin_copies[i], bit_vectors[i]))
            old_rhs = rhs
            coins[i].flip()
            rhs = get_rhs()
            self.play(
                ShowCreation(rect),
                FlipCoin(coin_copies[i]),
                FadeOut(old_rhs, RIGHT),
                FadeIn(rhs, LEFT),
            )
            self.play(FadeOut(rect))
            self.wait(2)
