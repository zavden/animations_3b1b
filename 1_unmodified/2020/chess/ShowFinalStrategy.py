# ==============================================================================
# Scene:      ShowFinalStrategy
# Source:     videos/_2020/chess.py (lines 4672-4782)
# Category:   1 · Renders unmodified
#
# Run from this folder:
#     manimgl ShowFinalStrategy.py ShowFinalStrategy -w -m --fps 15
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


class ShowFinalStrategy(Scene):
    CONFIG = {
        "show_with_lines": False,
    }

    def construct(self):
        # Setup board and such
        board = Chessboard()
        board.to_edge(RIGHT)
        coins = CoinsOnBoard(board, coin_config={"numeric_labels": True})
        coins.flip_by_message("3b1b  :)")

        encoding_lines = VGroup(*[Line(ORIGIN, 0.5 * RIGHT) for x in range(6)])
        encoding_lines.arrange(LEFT, buff=SMALL_BUFF)
        encoding_lines.next_to(board, LEFT, LARGE_BUFF)
        encoding_lines.shift(UP)

        code_words = OldTexText("Encoding")
        code_words.next_to(encoding_lines, DOWN)

        add_words = OldTexText("Check the parity\\\\of these coins")
        add_words.next_to(board, LEFT, LARGE_BUFF, aligned_edge=UP)

        self.add(board, coins)
        self.add(encoding_lines)
        self.add(code_words)

        # Set up groups
        fade_groups = Group()
        line_groups = VGroup()
        mover_groups = VGroup()
        count_mobs = VGroup()
        one_groups = VGroup()
        bits = VGroup()
        for i in range(6):
            bit = Integer(0)
            bit.next_to(encoding_lines[i], UP, SMALL_BUFF)
            bits.add(bit)

            count_mob = Integer(0)
            count_mob.set_color(RED)
            count_mob.next_to(add_words, DOWN, MED_SMALL_BUFF)
            count_mobs.add(count_mob)

            line_group = VGroup()
            fade_group = Group()
            mover_group = VGroup()
            one_rect_group = VGroup()
            count = 0
            for n, coin in enumerate(coins):
                if bool(n & (1 << i)):
                    line_group.add(Line(
                        coin.get_center(),
                        bit.get_center(),
                    ))
                    mover_group.add(coin.labels[1 - int(coin.is_heads())].copy())
                    if coin.is_heads():
                        one_rect_group.add(SurroundingRectangle(coin))
                        count += 1
                else:
                    fade_group.add(coin)
            bit.set_value(count % 2)
            fade_group.save_state()
            line_group.set_stroke(BLUE, width=1, opacity=0.5)
            fade_groups.add(fade_group)
            line_groups.add(line_group)
            mover_groups.add(mover_group)
            one_groups.add(one_rect_group)

        # Animate
        for lines, fades, movers, og, cm, bit in zip(line_groups, fade_groups, mover_groups, one_groups, count_mobs, bits):
            self.play(
                FadeIn(add_words),
                fades.set_opacity, 0.1,
            )
            if self.show_with_lines:
                for mover in movers:
                    mover.generate_target()
                    mover.target.replace(bit)
                    mover.target.set_opacity(0)
                bit.save_state()
                bit.replace(movers[0])
                bit.set_opacity(0)
                self.play(
                    LaggedStartMap(ShowCreation, lines, run_time=2),
                    LaggedStartMap(MoveToTarget, movers, lag_ratio=0.01),
                    Restore(bit)
                )
                self.remove(movers)
                self.add(bit)
                self.play(
                    FadeOut(lines)
                )
            else:
                self.play(
                    ShowIncreasingSubsets(og),
                    UpdateFromFunc(cm, lambda m: m.set_value(len(og)))
                )
                self.play(FadeInFromPoint(bit, cm.get_center()))
                self.play(
                    FadeOut(og),
                    FadeOut(cm),
                )

            self.play(
                FadeOut(add_words),
                Restore(fades),
            )
            self.remove(fades)
            self.add(coins)
        self.wait()
